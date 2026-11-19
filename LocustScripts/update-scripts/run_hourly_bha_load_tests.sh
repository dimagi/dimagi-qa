#!/usr/bin/env bash
# Run the three hourly BHA load tests in parallel on one runner.
#
# Each scenario runs from its own directory, reports/<scenario>/, which
# gets its hourly HTML report and its log, so their output stays separate.
# The logs are printed one scenario at a time once all three have finished.
#
# Each scenario's result (success or failure) is written to the step's
# outputs, keyed by scenario name. Exits non-zero if any scenario failed.
set -uo pipefail

# The locustfiles import modules from the repository root (common_utilities),
# which is importable only from the root unless it's on PYTHONPATH.
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
SCRIPTS="$PWD/LocustScripts/update-scripts"
CONFIG="$SCRIPTS/project-config/co-carecoordination-perf"
SCENARIOS=()
PIDS=()

function start {
    local scenario="$1"
    shift
    mkdir -p "reports/$scenario"
    (
        cd "reports/$scenario" &&
        python "$SCRIPTS/run_24hr_locust_schedule.py" --domain co-carecoordination-perf "$@"
    ) > "reports/$scenario/locust.log" 2>&1 &
    SCENARIOS+=("$scenario")
    PIDS+=($!)
}

start admit-client \
    --locust-file "$SCRIPTS/commcarehq-hourly-search-and-admit-mw-login.py" \
    --user-details "$CONFIG/mobile_worker_credentials_search_admit_hourly.json" \
    --app-config "$CONFIG/app_config_automated_cr_admit_client.json" \
    --host https://www.commcarehq.org \
    --app-id 77bbaaa1d7e5404781bbe680ce9a90d2 \
    --build-id 2ae6dcfc44834e40a703155ebedd3bec

start send-referrals \
    --locust-file "$SCRIPTS/commcarehq-hourly-send_refferals-mw-login.py" \
    --user-details "$CONFIG/mobile_worker_credentials_send_refferals_hourly.json" \
    --app-config "$CONFIG/app_config_send_referrals.json" \
    --host https://www.commcarehq.org \
    --app-id 5abfe7d62fd54e7cb7e6038f8a68e0ea \
    --build-id b9a1ef9ff5ba4b61957f1e0524f0dd03

start update-bed-avail \
    --locust-file "$SCRIPTS/commcarehq-hourly-update-bed-availability-mw-login.py" \
    --user-details "$CONFIG/mobile_worker_credentials_update_bed_avail_hourly.json" \
    --app-config "$CONFIG/app_config_update_bed_avail.json" \
    --host https://www.commcarehq.org/ \
    --app-id 5abfe7d62fd54e7cb7e6038f8a68e0ea \
    --build-id b9a1ef9ff5ba4b61957f1e0524f0dd03

failed=0
for i in "${!SCENARIOS[@]}"; do
    scenario="${SCENARIOS[$i]}"
    wait "${PIDS[$i]}"
    status=$?
    echo "::group::$scenario (exit status $status)"
    cat "reports/$scenario/locust.log"
    echo "::endgroup::"
    if (( status == 0 )); then
        echo "$scenario=success" >> "${GITHUB_OUTPUT:-/dev/null}"
    else
        echo "$scenario=failure" >> "${GITHUB_OUTPUT:-/dev/null}"
        failed=1
    fi
done
exit $failed
