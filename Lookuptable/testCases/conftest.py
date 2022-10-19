import os

from configparser import ConfigParser
from pathlib import Path
from common_utilities.fixtures import *

""""This file provides fixture functions for driver initialization"""

global driver


@pytest.fixture(scope="session")
def environment_settings_hq():
    """Load settings from os.environ

            Names of environment variables:
                DIMAGIQA_URL
                DIMAGIQA_LOGIN_USERNAME
                DIMAGIQA_LOGIN_PASSWORD
                DIMAGIQA_MAIL_USERNAME
                DIMAGIQA_MAIL_PASSWORD

            See https://docs.github.com/en/actions/reference/encrypted-secrets
            for instructions on how to set them.
            """
    settings = {}
    for name in ["url", "login_username", "login_password", "mail_username",
                 "mail_password", "bs_user", "bs_key", "staging_auth_key", "prod_auth_key", "invited_webuser_password"]:

        var = f"DIMAGIQA_{name.upper()}"
        if var in os.environ:
            settings[name] = os.environ[var]
    if "url" not in settings:
        env = os.environ.get("DIMAGIQA_ENV") or "staging"
        subdomain = "www" if env == "production" else env
        # updates the url with the project domain while testing in CI
        project = "a/qa-automation-prod" if env == "production" else "a/qa-automation"
        settings["url"] = f"https://{subdomain}.commcarehq.org/{project}"
    return settings


@pytest.fixture(scope="session", autouse=True)
def settings(environment_settings_hq):
    if os.environ.get("CI") == "true":
        settings = environment_settings_hq
        settings["CI"] = "true"
        if any(x not in settings for x in ["url", "login_username", "login_password",
                                           "mail_username", "mail_password", "bs_user", "bs_key", "staging_auth_key",
                                           "prod_auth_key", "invited_webuser_password"]):
            lines = environment_settings_hq.__doc__.splitlines()
            vars_ = "\n  ".join(line.strip() for line in lines if "DIMAGIQA_" in line)
            raise RuntimeError(
                f"Environment variables not set:\n  {vars_}\n\n"
                "See https://docs.github.com/en/actions/reference/encrypted-secrets "
                "for instructions on how to set them."
            )
        return settings
    path = Path(__file__).parent.parent / "settings.cfg"
    if not path.exists():
        raise RuntimeError(
            f"Not found: {path}\n\n"
            "Copy settings-sample.cfg to settings.cfg and populate "
            "it with values for the environment you want to test."
        )
    settings = ConfigParser()
    settings.read(path)
    # updates the url with the project domain while testing in local
    if settings["default"]["url"] == "https://www.commcarehq.org/":
        settings["default"]["url"] = f"{settings['default']['url']}a/qa-automation-prod"
    else:
        settings["default"]["url"] = f"{settings['default']['url']}a/qa-automation"
    return settings["default"]
