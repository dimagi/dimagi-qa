## Case Search Test Script

Case Search allows mobile workers to search for cases across locations / owners as well as claim those cases. Specific search fields can be configured per application. 

This script contains conatins [it's regression tests.](https://docs.google.com/spreadsheets/d/13vUbmbMqtFWwjvmvuST66p3X5u6sLNnBrLWQICx_iaQ/edit#gid=2133071371)

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
pytest -v --rootdir= Features/CaseSearch/test_cases

```
- You could also pass the following arguments
  - ` -n 3 --dist=loadfile` - This will run the tests parallelly in 3 instances. The number of reruns is configurable.
  - ` --reruns 1` - This will re-run the tests once in case of failures.The number of reruns is configurable too.

### <ins> Trigger Manually on Gitaction </ins>

To manually trigger the script,
  - Go to [Gitactions](https://github.com/dimagi/dimagi-qa/actions/)
  - Select the desired workflow, here [Case Search Tests](https://github.com/dimagi/dimagi-qa/actions/workflows/case-search-tests.yml)
  - Run workflow
  - Use workflow from ```master```
  - Use the environment as desired
  - Run!
