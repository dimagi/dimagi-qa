import argparse
import json
import os
import subprocess
from datetime import datetime, timedelta
import pytz

mt = pytz.timezone("America/Denver")

def get_remaining_minutes_in_hour():
    now = datetime.now(mt)
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    return int((next_hour - now).total_seconds() // 60)

def run_locust_for_current_hour(args):
    current_hour = datetime.now(mt).strftime("%H")
    print(f"Running for hour: {current_hour}")

    with open(args.user_details, 'r') as f:
        users_data = json.load(f)

    users_by_hour = users_data.get("users_by_hour", {})
    if current_hour not in users_by_hour:
        print(f"No user data for hour {current_hour}. Skipping...")
        return

    users = users_by_hour[current_hour]
    user_count = len(users)
    remaining_minutes = get_remaining_minutes_in_hour()
    os.environ["REMAINING_SECONDS"] = str(remaining_minutes * 60)

    # Use dynamic run-time and spawn-rate
    run_time = f"{remaining_minutes}m"
    spawn_rate = max(1, user_count // max(1, remaining_minutes))

    print(f"Users: {user_count}, Run-time: {run_time}, Spawn rate: {spawn_rate}")

    cmd = [
        "locust",
        "--headless",
        "-f", args.locust_file,
        "-u", str(user_count),
        "-r", str(spawn_rate),
        "--run-time", run_time,
        "--host", args.host,
        "--domain", args.domain,
        "--app-id", args.app_id,
        "--build-id", args.build_id,
        "--app-config", args.app_config,
        "--user-details", args.user_details,
        "--html", f"hour_{current_hour}_report.html"
    ]

    subprocess.run(cmd, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--locust-file", required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--build-id", required=True)
    parser.add_argument("--app-config", required=True)
    parser.add_argument("--user-details", required=True)
    args = parser.parse_args()

    run_locust_for_current_hour(args)


if __name__ == "__main__":
    main()
