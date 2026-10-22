## Data Pipeline / Bulk Actions API Test Data

QA Ticket: [QA-8710](https://dimagi.atlassian.net/browse/QA-8710)

Generates realistic, disposable household data in the `marketing-advanced-plan` project space on
staging, for trying out the CommCare Data Pipeline and the Bulk Actions API (which permanently
deletes forms).

The data is created through real form submissions to the **Household Registration** app
(case type `household`), as the project's mobile workers:

- **Register Household**: 10,000 households by default, one case each
- **Household Follow-up Visit**: about 40% of households get one visit and 15% get two
- **Close Household**: about 4% of households are closed afterwards

Names, villages and districts are made up, and no health information is collected. Each mobile
worker mostly covers its "own" villages, and the forms are spread over the last 180 days,
mainly on weekdays during working hours. Every submission has the device ID
`qa-8710-data-generator`, so the generated forms are easy to find.

### Setting up

```sh
# create and activate a virtualenv using your preferred method. Example:
python -m venv venv
source venv/bin/activate

# install requirements
pip install -r requires.txt
```

- Copy `settings-sample.cfg` to `settings.cfg`.
- Provide the password shared by all the mobile workers listed in `mobile_workers`, either as the
  `DIMAGI_MOBILE_PASSWORD` environment variable (the repository secret of the same name in CI)
  or as `mobile_password` in `settings.cfg`. The environment variable takes precedence.
- If the app is rebuilt, update `app_version` to the latest build number.

### Running

Run these commands from `QA_Requests/DataPipelineTestData/testCases`:

```sh
# 1. Build the plan and write one sample XML per form to OutputFiles/samples (nothing is submitted)
python generate_household_data.py --dry-run

# 2. Smoke check: submit the first 20 forms, then check the Case List report on HQ
python generate_household_data.py --limit 20

# 3. Full run. Re-running the same command resumes and skips forms that were already submitted
python generate_household_data.py
```

Options: `--count` (households, default 10000), `--days` (date spread, default 180),
`--delay` (seconds between submissions per worker) and `--seed` (see below).

### Running on GitHub Actions

The [QA-8710 Data Pipeline Test Data](../../.github/workflows/qa-8710-data-pipeline-test-data.yml)
workflow runs the same script. It is **manual only**: it never runs on a push, pull request or schedule.

- Go to Actions → **QA-8710 Data Pipeline Test Data** → Run workflow.
- Inputs: `count`, `seed`, `end_date`, `limit` (e.g. `20` for a smoke check) and `dry_run`.
- The mobile worker password comes from the `DIMAGI_MOBILE_PASSWORD` repository secret.
- The log prints the plan's end date. To resume a run that stopped, run again with the same `seed`
  and that `end_date`: the same forms are rebuilt, and HQ
  treats the ones it already received as duplicates without applying them again.
- The run's `OutputFiles` (progress and failure logs) are uploaded as an artifact.

### Refilling after Bulk Actions deletes

The data comes from a seed (`--seed`, default `1`), so the same seed always produces the same
households and form IDs. To add a **new** batch after data has been deleted, use a new seed:

```sh
python generate_household_data.py --seed 2 --count 2000
```

Progress is recorded per seed in `OutputFiles/submitted_seed_<n>.log`, and any failures go to
`OutputFiles/failed_seed_<n>.log`.
