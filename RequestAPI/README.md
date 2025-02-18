# Automated API Requests
Automated test suite for [CommCare HQ APIs](https://dimagi.atlassian.net/wiki/spaces/commcarepublic/pages/2143958022/CommCare+HQ+APIs)

## Executing Scripts

### <ins> On Local Machine </ins>

#### Setting up test environment

```sh

# create and activate a virtualenv using your preferred method. Example:
python -m venv venv
source venv/bin/activate


# install requirements
pip install -r requirements.txt

```

[More on setting up virtual environments](https://confluence.dimagi.com/display/GTD/QA+and+Python+Virtual+Environments)

#### Running Tests

- Copy `settings-sample.cfg` to `settings.cfg` and populate `settings.cfg` for
the environment you want to test.
- Run tests

```sh
## command to execute the scripts 
pytest -v 

## command to execute the scripts with 2 reruns and in parallel with limited traceback
pytest -v -n auto --dist=loadfile --reruns 2 --capture=tee-sys  --tb=short

## command to execute individual test module or test case
# Example: pytest -v -k <complete or partial test module name/complete or partial test case name> 
pytest -v -k test_01/test_case_1 

```
- Similarly, you could pass the following arguments:
  - `-n auto --dist=loadfile` - This will run the tests parallelly; it'll automatically choose the number of instances. The number of reruns is configurable.
  - `--reruns 1` - This will re-run the tests once in case of failures. The number of reruns is configurable too.
  - `--capture=tee-sys` - This disables all capturing and replaces sys. stdout/stderr with in-mem files
  - `--tb=short` - This enables a shorter traceback format

### <ins> Trigger Manually on Gitaction </ins>

<img align="right" width="400" src="https://github.com/dimagi/dimagi-qa/assets/67914792/002fbfd3-2512-4e12-a8ea-e57f93f5a615" alt="clone this repository" />

To manually trigger the script,
  - Go to [Gitactions](https://github.com/dimagi/dimagi-qa/actions/)
  - Select the desired workflow, here [Python Request API action](https://github.com/dimagi/dimagi-qa/actions/workflows/request_api.yml)
  - Run workflow
  - Select workflow as ```master```
  - Select the environment as desired
  - Run!

If you are a part of the QA team, you'll receive emails for the result of the run after it's complete. 

<img align="right" width="400" src="https://user-images.githubusercontent.com/67914792/168756705-88e4b330-b05a-4df2-a60c-7d45e8a2d002.PNG" alt="clone this repository" />

Besides, you should be able to find the zipped results in the **Artifacts** section, of the corresponding run (after it's complete).
