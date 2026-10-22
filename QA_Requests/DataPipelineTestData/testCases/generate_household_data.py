"""QA-8710: generate realistic household data in the marketing-advanced-plan project space.

Registers households (one case each) through real form submissions, adds follow-up
visits for some of them and closes a few, spread over the past months and across the
mobile workers listed in settings.cfg.

    python generate_household_data.py --dry-run          # build the plan + sample XML, no submissions
    python generate_household_data.py --limit 20         # submit the first 20 forms only (smoke check)
    python generate_household_data.py                    # full run (resumes where it stopped)
    python generate_household_data.py --seed 2           # a fresh batch of households (refill)
"""
import argparse
import os
import re
import sys
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from QA_Requests.DataPipelineTestData.testPages.household_data.data_generator import build_plan  # noqa: E402
from QA_Requests.DataPipelineTestData.testPages.household_data.form_builder import build_form_xml  # noqa: E402
from QA_Requests.DataPipelineTestData.testPages.household_data.submitter import (  # noqa: E402
    ProgressLog, Submitter, full_username, lookup_user_ids)

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "OutputFiles"
MAX_CONSECUTIVE_FAILURES = 20


def load_settings():
    path = BASE_DIR.parent / "settings.cfg"
    if not path.exists():
        raise RuntimeError(
            f"Not found: {path}\n\n"
            "Copy settings-sample.cfg to settings.cfg and populate "
            "it with values for the environment you want to use."
        )
    settings = ConfigParser()
    settings.read(path)
    settings = settings["default"]
    match = re.search(r"/a/([^/]+)", settings["url"])
    if not match:
        raise RuntimeError("settings.cfg url must look like https://<server>/a/<project-space>/")
    settings["domain"] = match.group(1)
    # in CI the shared mobile worker password comes from the DIMAGI_MOBILE_PASSWORD secret
    settings["mobile_password"] = os.environ.get("DIMAGI_MOBILE_PASSWORD") or settings.get("mobile_password", "")
    return settings


def plan_end_day(seed, end_date=None):
    """Pin the plan's last day per seed, so a resumed run on a later day rebuilds the same plan."""
    anchor = OUTPUT_DIR / f"plan_end_day_seed_{seed}.txt"
    if end_date:
        end_day = date.fromisoformat(end_date)
    elif anchor.exists():
        return date.fromisoformat(anchor.read_text().strip())
    else:
        end_day = date.today() - timedelta(days=1)
    OUTPUT_DIR.mkdir(exist_ok=True)
    anchor.write_text(end_day.isoformat())
    return end_day


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--count", type=int, default=10000, help="number of households (cases) to register")
    parser.add_argument("--seed", type=int, default=1, help="data seed; use a new seed for a fresh batch")
    parser.add_argument("--days", type=int, default=180, help="spread registrations over this many past days")
    parser.add_argument("--end-date", help="last day of the plan (YYYY-MM-DD); pass the date printed by "
                                           "an earlier run to resume it on a machine without its OutputFiles")
    parser.add_argument("--limit", type=int, help="submit at most this many forms in this run")
    parser.add_argument("--delay", type=float, default=0.0, help="seconds to wait after each submission")
    parser.add_argument("--dry-run", action="store_true", help="build the plan and sample XML without submitting")
    return parser.parse_args()


def summarise(events, workers):
    kinds = Counter(e.kind for e in events)
    per_worker = Counter(e.owner for e in events if e.kind == "register")
    print(f"Plan: {kinds['register']} registrations, {kinds['followup']} follow-up visits, "
          f"{kinds['close']} closures = {len(events)} forms")
    print(f"Dates: {events[0].time_end:%Y-%m-%d} to {events[-1].time_end:%Y-%m-%d}")
    for w in workers:
        print(f"  {w}: {per_worker[w]} households")


def write_samples(events, settings, workers):
    sample_dir = OUTPUT_DIR / "samples"
    sample_dir.mkdir(parents=True, exist_ok=True)
    for kind in ("register", "followup", "close"):
        event = next((e for e in events if e.kind == kind), None)
        if event:
            xml = build_form_xml(event, full_username(event.owner, settings["domain"]), "DRY-RUN-USER-ID",
                                 settings["app_version"])
            (sample_dir / f"{kind}.xml").write_text(xml, encoding="utf-8")
    print(f"Sample XML written to {sample_dir}")


def run():
    args = parse_args()
    settings = load_settings()
    workers = [w.strip() for w in settings["mobile_workers"].split(",") if w.strip()]
    end_day = plan_end_day(args.seed, args.end_date)
    events = build_plan(workers, args.count, args.seed, args.days, end_day)
    summarise(events, workers)
    print(f"Seed {args.seed}, end date {end_day}: "
          f"re-run with --seed {args.seed} --end-date <that date> to resume this exact plan")

    if args.dry_run:
        write_samples(events, settings, workers)
        return

    if not settings["mobile_password"]:
        raise RuntimeError("No mobile worker password: set DIMAGI_MOBILE_PASSWORD or mobile_password in settings.cfg")
    base_url = settings["url"].rstrip("/") + "/"
    user_ids = lookup_user_ids(base_url, settings["domain"], workers, settings["mobile_password"],
                               OUTPUT_DIR / "user_ids.json")
    progress = ProgressLog(OUTPUT_DIR / f"submitted_seed_{args.seed}.log")
    pending = [e for e in events if e.instance_id not in progress.done]
    if args.limit:
        pending = pending[:args.limit]
    print(f"Already submitted: {len(progress.done)}. Submitting now: {len(pending)}")

    # one thread per worker, each in chronological order, so a case's forms never race each other
    by_worker = defaultdict(list)
    for event in pending:
        by_worker[event.owner].append(event)

    submitter = Submitter(base_url, settings["app_id"], settings["domain"], settings["mobile_password"],
                          delay=args.delay)
    stats = Counter()
    lock = threading.Lock()
    stop = threading.Event()
    failed_log = OUTPUT_DIR / f"failed_seed_{args.seed}.log"

    def submit_all(worker, worker_events):
        consecutive = 0
        username = full_username(worker, settings["domain"])
        for event in worker_events:
            if stop.is_set():
                return
            xml = build_form_xml(event, username, user_ids[worker], settings["app_version"])
            ok, detail = submitter.submit(worker, xml)
            with lock:
                stats["ok" if ok else "failed"] += 1
                if not ok:
                    with failed_log.open("a") as f:
                        f.write(f"{event.instance_id}\t{event.kind}\t{worker}\t{detail}\n")
                done = stats["ok"] + stats["failed"]
                if done % 250 == 0 or done == len(pending):
                    print(f"  {done}/{len(pending)} submitted ({stats['failed']} failed)")
            if ok:
                progress.add(event.instance_id)
                consecutive = 0
            else:
                consecutive += 1
                if consecutive >= MAX_CONSECUTIVE_FAILURES:
                    print(f"Stopping: {worker} had {consecutive} failures in a row. Last error: {detail}")
                    stop.set()
                    return

    with ThreadPoolExecutor(max_workers=len(by_worker) or 1) as pool:
        futures = [pool.submit(submit_all, w, worker_events) for w, worker_events in by_worker.items()]
    for future in futures:
        future.result()  # re-raise anything a worker thread hit

    print(f"Done: {stats['ok']} submitted, {stats['failed']} failed.")
    if stats["failed"]:
        print(f"Failures are listed in {failed_log}; re-run the same command to retry them.")


if __name__ == "__main__":
    run()
