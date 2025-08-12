## CO BHA Regression Test Script

This script contains covers the happy paths/critical workflows of Colorado's BHA app. Here are the scripted [regression tests.](https://docs.google.com/spreadsheets/d/1OIcd1V8Vd73OSPEt4x2o8N9MihqBlviAIvPbJAm2L4o/edit#gid=1373088023)

## Executing Scripts

### <ins> On Local Machine </ins>

#### Setting up the test environment

```sh

# Create and activate a virtualenv using your preferred method. Example:
python -m venv venv
source venv/bin/activate


# install requirements
pip install -r requires.txt

```

[More on setting up virtual environments](https://confluence.dimagi.com/display/GTD/QA+and+Python+Virtual+Environments)


#### Running Tests


 -   Copy `settings-sample.cfg` to `settings.cfg` and populate `settings.cfg` for
the environment you want to test.
- Run tests using pytest command like:

```sh

# To execute all the test cases 
pytest -v --rootdir= USH_Apps/CO_BHA/test_cases

```
- You could also pass the following arguments
  - ` -n 3 --dist=loadfile` - This will run the tests parallelly in 3 instances. The number of reruns is configurable.
  - ` --reruns 1` - This will re-run the tests once in case of failures. The number of reruns is configurable too.

### <ins> Trigger Manually on Gitaction </ins>

To manually trigger the script,
  - Go to [CO BHA Tests action](https://github.com/dimagi/dimagi-qa/actions/workflows/bha-tests.yml)
  - Run workflow
  - Use workflow from ```master```
  - Use the environment as desired
  - Run!

## Script Results

 -  Failures would be triggered on the Slack channel **#qa-bha-automated-test-results**

<img align="center" width="900" src="https://github.com/dimagi/dimagi-qa/assets/67914792/e2b024f0-a584-468d-99b8-9adb7ec4b16b" alt="clone this repository" />


 -  You should be able to find the zipped results in the **Artifacts** section, of the corresponding run (after a run is complete).

<img align="center" width="500" src="https://user-images.githubusercontent.com/67914792/168756705-88e4b330-b05a-4df2-a60c-7d45e8a2d002.PNG" alt="clone this repository" />
