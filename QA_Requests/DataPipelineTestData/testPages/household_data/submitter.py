"""Submits form XML to the CommCare HQ receiver as the owning mobile worker."""
import json
import random
import re
import threading
import time
from pathlib import Path

import requests

# 423: HQ is still processing an earlier attempt of the same form (e.g. after a timeout);
# resending is safe because a form that already went through comes back as a duplicate.
RETRY_STATUSES = {423, 429, 500, 502, 503, 504}
MAX_BACKOFF = 120


def full_username(username, domain):
    return username if "@" in username else f"{username}@{domain}.commcarehq.org"


def lookup_user_ids(base_url, domain, workers, password, cache_file):
    """Map each mobile worker to its user id, via a (small) OTA restore. Cached after the first run."""
    cache_file = Path(cache_file)
    cached = json.loads(cache_file.read_text()) if cache_file.exists() else {}
    for worker in workers:
        if worker in cached:
            continue
        auth = (full_username(worker, domain), password)
        for _ in range(10):
            response = requests.get(f"{base_url}phone/restore/", params={"version": "2.0", "items": "true"},
                                    auth=auth, timeout=120)
            if response.status_code == 202:  # restore is being generated asynchronously
                time.sleep(int(response.headers.get("Retry-After", 5)))
                continue
            break
        if response.status_code != 200:
            raise RuntimeError(f"Could not log in as {worker} (HTTP {response.status_code}). "
                               "Check mobile_workers and mobile_password in settings.cfg.")
        match = re.search(r"<uuid>([^<]+)</uuid>", response.text)
        if not match:
            raise RuntimeError(f"No user id found in the restore for {worker}.")
        cached[worker] = match.group(1)
        cache_file.write_text(json.dumps(cached, indent=2))
    return {w: cached[w] for w in workers}


class ProgressLog:
    """Append-only record of submitted instance ids, so an interrupted run can resume."""

    def __init__(self, path):
        self.path = Path(path)
        self.done = set(self.path.read_text().split()) if self.path.exists() else set()
        self._lock = threading.Lock()

    def add(self, instance_id):
        with self._lock:
            self.done.add(instance_id)
            with self.path.open("a") as f:
                f.write(instance_id + "\n")


class Submitter:
    def __init__(self, base_url, app_id, domain, password, max_retries=8, delay=0.0):
        self.url = f"{base_url}receiver/{app_id}/"
        self.domain = domain
        self.password = password
        self.max_retries = max_retries
        self.delay = delay
        self._local = threading.local()

    def _session(self, username):
        sessions = getattr(self._local, "sessions", None)
        if sessions is None:
            sessions = self._local.sessions = {}
        if username not in sessions:
            session = requests.Session()
            session.auth = (full_username(username, self.domain), self.password)
            session.headers["Content-Type"] = "text/xml"
            sessions[username] = session
        return sessions[username]

    def submit(self, username, xml):
        """Post one form. Returns (ok, detail); retries transient errors with backoff."""
        session = self._session(username)
        detail = ""
        for attempt in range(1, self.max_retries + 1):
            try:
                response = session.post(self.url, data=xml.encode("utf-8"), timeout=60)
            except requests.RequestException as e:
                detail = f"{type(e).__name__}: {e}"
            else:
                if response.status_code in (200, 201):
                    if self.delay:
                        time.sleep(self.delay)
                    return True, ""
                detail = f"HTTP {response.status_code}: {response.text[:300]}"
                if response.status_code not in RETRY_STATUSES:
                    return False, detail
                retry_after = _retry_after(response)
                if retry_after is not None:
                    time.sleep(retry_after + random.uniform(0, 2))
                    continue
            # jitter keeps the worker threads from retrying in lockstep
            time.sleep(min(2 ** attempt * random.uniform(0.5, 1.5), MAX_BACKOFF))
        return False, detail


def _retry_after(response):
    """Seconds the server asked us to wait (429/503 Retry-After), if it said."""
    value = response.headers.get("Retry-After", "")
    return min(int(value), MAX_BACKOFF) if value.isdigit() else None
