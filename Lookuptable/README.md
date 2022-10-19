## Commcare HQ Smoke Test Script

Smoke tests ensure that the important features are working and there are no showstoppers in the build deployed to environments.\
The automated tests comprises of [these smoke tests.](https://docs.google.com/spreadsheets/d/1mfnqPQoi4l5_kXL26bQRhiWxZnxVfG4roEXjX82GNqc/edit#gid=1948263112)

## Executing Scripts

### <ins> On Local Machine </ins>

#### Setting up test environment

```sh

# create and activate a virtualenv using your preferred method. Example:
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
pytest -v --rootdir= HQSmokeTests/testCases

```
- You could also pass the following arguments
  - ` -n 3 --dist=loadfile` - This will run the tests parallelly in 3 instances. The number of reruns is configurable.
  - ` --reruns 1` - This will re-run the tests once in case of failures.The number of reruns is configurable too.

### <ins> Trigger Manually on Gitaction </ins>

<img align="right" width="400" src="https://user-images.githubusercontent.com/67914792/168757107-3ce9bb6a-57b5-4c15-b20d-e7883bf9ed65.PNG" alt="clone this repository" />

To manually trigger the script,
  - Go to [HQ Smoke Tests action](https://github.com/dimagi/dimagi-qa/actions/workflows/python-app.yml)
  - Run workflow
  - Use workflow from ```master```
  - Run!

If you are a part of the QA team, you'll receive emails for the result of the run after it's complete. 

<img align="right" width="400" src="https://user-images.githubusercontent.com/67914792/168756705-88e4b330-b05a-4df2-a60c-7d45e8a2d002.PNG" alt="clone this repository" />

Besides, you should be able to find the zipped results in the **Artifacts** section, of the corresponding run (after it's complete).
