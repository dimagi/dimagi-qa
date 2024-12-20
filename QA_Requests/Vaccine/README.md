## Data creation for Dimagi Vaccine Solution Dashboard

QA Ticket: [QA-3939](https://dimagi-dev.atlassian.net/browse/QA-3352)

### Setting up and Running tests

- Setup Environment

```sh
# create and activate a virtualenv using your preferred method. Example:
python -m venv venv
source venv/bin/activate

# install requirements
pip install -r requires.txt

```

- Copy `settings-sample.cfg` to `settings.cfg` and populate `settings.cfg` for the environment you want to test.

- Run tests

```sh
python test_new_apk.py
```
