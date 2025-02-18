## Case Search Test Script

This feature flag adds a sidebar to the case search screen so the user does not need to navigate away to refine the case search results.

This script contains conatins [these regression tests.](https://docs.google.com/spreadsheets/d/13vUbmbMqtFWwjvmvuST66p3X5u6sLNnBrLWQICx_iaQ/edit#gid=1894003725)

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
pytest -v --rootdir= Features/SplitScreenCaseSearch/test_cases

```
- You could also pass the following arguments
  - ` -n 3 --dist=loadfile` - This will run the tests parallelly in 3 instances. The number of reruns is configurable.
  - ` --reruns 1` - This will re-run the tests once in case of failures.The number of reruns is configurable too.

### <ins> Trigger Manually on Gitaction </ins>

To manually trigger the script,
  - Go to [Case Search Split Screen Tests action](https://github.com/dimagi/dimagi-qa/actions/workflows/case-search-split-screen-tests.yml)
  - Run workflow
  - Use workflow from ```master```
  - Use the environment as desired
  - Run!
