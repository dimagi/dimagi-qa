"""Builds a deterministic plan of household form submissions.

The same seed always produces the same households, case ids and form instance ids,
so a run that stops part-way can be restarted and already-submitted forms skipped.
A different seed produces a fresh set of households (used for refills).
"""
import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime, time, timedelta, timezone

from QA_Requests.DataPipelineTestData.userInputs.test_data import Distributions, Names, Notes, Places


@dataclass
class FormEvent:
    kind: str  # "register" | "followup" | "close"
    case_id: str
    instance_id: str
    owner: str
    time_start: datetime
    time_end: datetime
    case_name: str = ""
    answers: dict = field(default_factory=dict)


def _weighted(rng, weights):
    keys = list(weights)
    return rng.choices(keys, weights=[weights[k] for k in keys])[0]


def _uuid(rng):
    return str(uuid.UUID(int=rng.getrandbits(128), version=4))


def _visit_time(rng, day):
    """A plausible field-visit time on `day`: weekday daytime, 4-15 minutes long."""
    start = datetime.combine(day, time(6, 0), tzinfo=timezone.utc) + timedelta(minutes=rng.randint(0, 9 * 60))
    return start, start + timedelta(minutes=rng.randint(4, 15), seconds=rng.randint(0, 59))


def _working_day(rng, start_day, end_day):
    span = (end_day - start_day).days
    for _ in range(10):
        day = start_day + timedelta(days=rng.randint(0, span))
        if day.weekday() < 5 or rng.random() < 0.08:
            return day
    return day


def _gps(rng, centre):
    lat, lon = centre
    return f"{lat + rng.uniform(-0.015, 0.015):.6f} {lon + rng.uniform(-0.015, 0.015):.6f} " \
           f"{rng.uniform(1100, 1250):.1f} {rng.uniform(3, 15):.1f}"


def _worker_villages(workers):
    """Give each worker a 'home' patch of villages so ownership looks like real field work."""
    villages = list(Places.villages)
    return {w: villages[i::len(workers)] or [villages[i % len(villages)]] for i, w in enumerate(workers)}


def _registration(rng, owner, home_villages, day):
    village = rng.choice(home_villages) if rng.random() < 0.9 else rng.choice(list(Places.villages))
    profile = Places.villages[village]
    gender = _weighted(rng, Distributions.head_gender)
    first = rng.choice(Names.female if gender == "female" else Names.male)
    middle = f" {rng.choice(Names.middle_initials)}." if rng.random() < Names.middle_initial_share else ""
    name = f"{first}{middle} {rng.choice(Names.surnames)}"

    size = _weighted(rng, Distributions.household_size)
    children = min(_weighted(rng, Distributions.children_under_5), size - 1) if size > 1 else 0
    count = _weighted(rng, Distributions.livelihood_count)
    livelihoods = []
    while len(livelihoods) < count:
        choice = _weighted(rng, Distributions.livelihoods)
        if village == "riverbend" and rng.random() < 0.25:
            choice = "fishing"
        if choice not in livelihoods:
            livelihoods.append(choice)

    return name, {
        "hh_head_name": name,
        "hh_head_gender": gender,
        "village": village,
        "district": profile["district"],
        "household_size": size,
        "children_under_5": children,
        "water_source": _weighted(rng, profile["water"]),
        "has_electricity": "yes" if rng.random() < profile["electricity"] else "no",
        "livelihoods": " ".join(livelihoods),
        "registration_date": day.isoformat(),
        "gps_location": _gps(rng, profile["gps"]),
    }


def _followup(rng, previous_size, day):
    size = min(max(previous_size + _weighted(rng, Distributions.household_size_change), 1), 20)
    attended = "yes" if rng.random() < Distributions.attended_training else "no"
    answers = {
        "visit_date": day.isoformat(),
        "current_household_size": size,
        "members_present": rng.randint(max(1, size // 3), size),
        "attended_training": attended,
        "visit_notes": "" if rng.random() < Distributions.visit_notes_blank else rng.choice(Notes.followup),
    }
    if attended == "yes":
        answers["training_topic"] = _weighted(rng, Distributions.training_topic)
    return answers


def _close(rng, day):
    reason = _weighted(rng, Distributions.close_reason)
    answers = {"close_date": day.isoformat(), "close_reason": reason}
    if reason == "other":
        answers["close_reason_other"] = rng.choice(Notes.close_other)
    return answers


def build_plan(workers, count, seed, days, end_day=None):
    """Return all form events for `count` households, in chronological order."""
    rng = random.Random(seed)
    end_day = end_day or (datetime.now(timezone.utc).date() - timedelta(days=1))
    start_day = end_day - timedelta(days=days)
    weights = Distributions.worker_weights[:len(workers)]
    if len(weights) < len(workers):
        weights = [1] * len(workers)
    home = _worker_villages(workers)

    events = []
    for _ in range(count):
        owner = rng.choices(workers, weights=weights)[0]
        case_id = _uuid(rng)
        reg_day = _working_day(rng, start_day, end_day)
        start, end = _visit_time(rng, reg_day)
        name, answers = _registration(rng, owner, home[owner], reg_day)
        events.append(FormEvent("register", case_id, _uuid(rng), owner, start, end, name, answers))

        roll = rng.random()
        visits = 2 if roll < Distributions.two_followups else \
            1 if roll < Distributions.two_followups + Distributions.one_followup else 0
        last_day, size = reg_day, answers["household_size"]
        for _ in range(visits):
            day = last_day + timedelta(days=rng.randint(14, 60))
            if day > end_day:
                break
            start, end = _visit_time(rng, day)
            followup = _followup(rng, size, day)
            events.append(FormEvent("followup", case_id, _uuid(rng), owner, start, end, name, followup))
            last_day, size = day, followup["current_household_size"]

        if rng.random() < Distributions.closed:
            day = last_day + timedelta(days=rng.randint(7, 45))
            if day <= end_day:
                start, end = _visit_time(rng, day)
                events.append(FormEvent("close", case_id, _uuid(rng), owner, start, end, name, _close(rng, day)))

    events.sort(key=lambda e: e.time_end)
    return events
