import json
import subprocess
import time
from datetime import datetime
import argparse
import os

def run_locust_for_hour(hour, args, is_ci):
    with open(args.users_json) as f:
        data = json.load(f)
    users = data["users_by_hour"].get(str(hour).zfill(2), [])
    user_count = len(users)

    if user_count == 0:
        print(f"[{hour:02d}:00] No users to run.")
        return

    print(f"[{hour:02d}:00] Running {user_count} users.")

    report_file = f"hour_{hour:02d}_report.html"
    cmd = [
        "locust",
        "-f", args.locust_file,
        "-u", str(user_count),
        "-r", str(max(1, user_count // 30)),
        "--run-time", "1h",
        f"--host={args.host}",
        f"--domain={args.domain}",
        f"--app-id={args.app_id}",
        f"--build-id={args.build_id}",
        f"--app-config={args.app_config}",
        f"--user-details={args.users_json}",
        f"--html={report_file}"
    ]

    if is_ci:
        cmd.insert(3, "--headless")

    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser(description="Run 24-hour Locust load test hourly.")
    parser.add_argument("--locust-file", required=True)
    parser.add_argument("--users-json", required=True)
    parser.add_argument("--app-config", required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--build-id", required=True)
    parser.add_argument("-u", required=False)
    parser.add_argument("-r", required=False)

    args = parser.parse_args()
    is_ci = os.environ.get("CI") == "true"

    for hour in range(24):
        run_locust_for_hour(hour, args, is_ci)
        if hour < 23:
            time.sleep(3600)

if __name__ == "__main__":
    main()
