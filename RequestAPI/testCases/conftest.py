import os
import pytest

from configparser import ConfigParser
from pathlib import Path


""""This file provides fixture functions for driver initialization"""


@pytest.fixture(scope="session", autouse=True)
def settings():
    if os.environ.get("CI") == "true":
        settings = {}
        for name in ["url", "password", "login_user", "login_pass", "prod_api_key","staging_api_key", "india_api_key"]:
            var = f"DIMAGIQA_{name.upper()}"
            if var in os.environ:
                settings[name] = os.environ[var]
        if "url" not in settings:
            env = os.environ.get("DIMAGIQA_ENV") or "staging"
            subdomain = "www" if env == "production" else ("india" if env == "india" else env)
            # updates the url with the project domain while testing in CI
            settings["url"] = f"https://{subdomain}.commcarehq.org/"
            settings['api_key'] = settings['prod_api_key'] if env == "production" else settings[subdomain+'_api_key']

        if any(x not in settings for x in ["url", "password","login_user", "login_pass", "prod_api_key", "staging_api_key", "india_api_key"]):
            lines = settings.__doc__.splitlines()
            vars_ = "\n  ".join(line.strip() for line in lines if "DIMAGIQA_" in line)
            raise RuntimeError(
                f"Environment variables not set:\n  {vars_}\n\n"
                "See https://docs.github.com/en/actions/reference/encrypted-secrets "
                "for instructions on how to set them."
            )

    else:
        path = Path(__file__).parent.parent / "settings.cfg"
        if not path.exists():
            raise RuntimeError(
                f"Not found: {path}\n\n"
                "Copy settings-sample.cfg to settings.cfg and populate "
                "it with values for the environment you want to test."
            )
        settings = ConfigParser()
        settings.read(path)
        settings["default"]["password"]=settings["default"].pop("json_password")
        if settings["default"]["url"] == "https://www.commcarehq.org/":
            settings["default"]["api_key"] = settings['default']['prod_api_key']
        elif settings["default"]["url"] == "https://india.commcarehq.org/":
            settings["default"]["api_key"] = settings['default']['india_api_key']
        else:
            settings["default"]["api_key"] = settings['default']['staging_api_key']
        settings = settings["default"]
    # updates the url with the project domain while testing in local
    yield settings


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == "call" or report.when == "teardown":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            print("reports skipped or failed")
        report.extra = extra

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # Collect test counts
    passed = terminalreporter.stats.get('passed', [])
    failed = terminalreporter.stats.get('failed', [])
    error = terminalreporter.stats.get('error', [])
    skipped = terminalreporter.stats.get('skipped', [])
    xfail = terminalreporter.stats.get('xfail', [])
    # Write the counts to a file
    # Determine the environment
    env = os.environ.get("DIMAGIQA_ENV", "default_env")

    # Define the filename based on the environment
    filename = f'test_counts_{env}.txt'
    with open(filename, 'w') as f:
        f.write(f'PASSED={len(passed)}\n')
        f.write(f'FAILED={len(failed)}\n')
        f.write(f'ERROR={len(error)}\n')
        f.write(f'SKIPPED={len(skipped)}\n')
        f.write(f'XFAIL={len(xfail)}\n')
