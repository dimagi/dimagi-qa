## Bulk Form Submission Appium Test Script

This test script is used to validate that the test the above "over total limit" labels in CCC without having to submit 60 Infant Immunization Record forms in the app.

## Executing Scripts

### <ins> On Local Machine </ins>

#### Setting up test environment

```sh

# create and activate a virtualenv using your preferred method. Example:
python -m venv venv
source venv/bin/activate


# install requirements
pip install -r .\MobileTest\ccc_bulk_submission\requires.txt

```

[More on setting up the machine and the scripts](https://docs.google.com/document/d/12C-BJzdDCu0tl3WfwnP90jdzT4SGEMz--p10FrYSJ8Y/edit)


#### Running Tests

- Run tests using pytest command like:

```sh

# To execute all the test cases 
python .\MobileTest\ccc_bulk_submission\main.py

```


### <ins> Trigger Manually on Gitaction </ins>

<img align="right" width="400" src="https://github.com/dimagi/dimagi-qa/assets/67914792/002fbfd3-2512-4e12-a8ea-e57f93f5a615" alt="clone this repository" />

To manually trigger the script,
  - Go to [Gitactions](https://github.com/dimagi/dimagi-qa/actions/)
  - Select the desired workflow, here [HQ Smoke Tests action](https://github.com/dimagi/dimagi-qa/actions/workflows/hq-smoke-tests.yml)
  - Run workflow
  - Select workflow as ```master```
  - Select the environment as desired
  - Run!

If you are a part of the QA team, you'll receive emails for the result of the run after it's complete. 

<img align="right" width="400" src="https://user-images.githubusercontent.com/67914792/168756705-88e4b330-b05a-4df2-a60c-7d45e8a2d002.PNG" alt="clone this repository" />

Besides, you should be able to find the zipped results in the **Artifacts** section, of the corresponding run (after it's complete).
