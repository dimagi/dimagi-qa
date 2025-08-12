import os

from configparser import ConfigParser
from pathlib import Path
from common_utilities.fixtures import *
from POCs.PercyWebApps.test_pages.vc_login_page import VCLoginPage


""""This file provides fixture functions for driver initialization"""

global driver


@pytest.fixture(scope="module", autouse=True)
def driver(settings, browser):
    web_driver = None
    chrome_options = webdriver.ChromeOptions()
    firefox_options = webdriver.FirefoxOptions()
    if settings.get("CI") == "true":
        if browser == "chrome":
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--headless=new')  # or '--headless=chrome' for newer versions
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--safebrowsing-disable-download-protection')
            chrome_options.add_argument('--safebrowsing-disable-extension-blacklist')
            chrome_options.add_argument('--window-size=1920,1080')  # sets consistent resolution
            chrome_options.add_argument('--force-device-scale-factor=1')
            chrome_options.add_experimental_option("prefs", {
                "download.default_directory": str(PathSettings.DOWNLOAD_PATH),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True})
        elif browser == "firefox":
            firefox_options.add_argument('--headless')
            firefox_options.add_argument('--no-sandbox')
            firefox_options.add_argument('disable-extensions')
            firefox_options.add_argument('--safebrowsing-disable-download-protection')
            firefox_options.add_argument('--safebrowsing-disable-extension-blacklist')
            firefox_options.add_argument('window-size=1920,1080')
            firefox_options.add_argument("--disable-setuid-sandbox")
            firefox_options.add_argument('--start-maximized')
            firefox_options.add_argument('--disable-dev-shm-usage')
            firefox_options.add_argument('--headless')
            firefox_options.add_argument("--disable-notifications")
            firefox_options.set_preference("browser.download.dir", str(PathSettings.DOWNLOAD_PATH))
    if browser == "chrome":
        web_driver = webdriver.Chrome(options=chrome_options)
        print("Chrome version:", web_driver.capabilities['browserVersion'])
    elif browser == "firefox":
        web_driver = webdriver.Firefox(options=firefox_options)
    else:
        print("Provide valid browser")
    login = VCLoginPage(web_driver, settings["url"])
    login.vc_login(settings["bha_username"], settings["bha_password"], settings["ush_user_prod_auth_key"])
    yield web_driver
    web_driver.quit()


@pytest.fixture(scope="session")
def environment_settings_bha():
    """Load settings from os.environ

            Names of environment variables:
                DIMAGIQA_URL
                DIMAGIQA_bha_username
                DIMAGIQA_bha_password
                DIMAGIQA_USH_USER_PROD_AUTH_KEY
                DIMAGIQA_BHA_PASSWORD

            See https://docs.github.com/en/actions/reference/encrypted-secrets
            for instructions on how to set them.
            """
    settings = {}

    for name in ["url", "bha_username", "bha_password", "ush_user_prod_auth_key", "login_username", "login_password", "db", "user_b_pwd"]:

        var = f"DIMAGIQA_{name.upper()}"
        if var in os.environ:
            settings[name] = os.environ[var]
    if "url" not in settings:
        env = os.environ.get("DIMAGIQA_ENV") or "staging"
        subdomain = "www" if env == "production" else env
        # updates the url with the project domain while testing in CI
        settings["url"] = f"https://{subdomain}.commcarehq.org/a/co-carecoordination-test/cloudcare/apps/v2/#apps"
        settings["db"] = f"https://{subdomain}.commcarehq.org/a/co-carecoordination-test/dashboard/"
    if "db" not in settings:
        env = os.environ.get("DIMAGIQA_ENV") or "staging"
        subdomain = "www" if env == "production" else env
        # updates the url with the project domain while testing in CI
        settings["db"] = f"https://{subdomain}.commcarehq.org/a/co-carecoordination-test/dashboard/"
    return settings


@pytest.fixture(scope="session", autouse=True)
def settings(environment_settings_bha):
    if os.environ.get("CI") == "true":
        settings = environment_settings_bha
        settings["CI"] = "true"

        if any(x not in settings for x in ["url", "bha_username", "bha_password", "ush_user_prod_auth_key", "login_username", "login_password", "db", "user_b_pwd"]):

            lines = environment_settings_bha.__doc__.splitlines()
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
    return settings["default"]

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
    filename = f'percy_test_counts_{env}.txt'
    with open(filename, 'w') as f:
        f.write(f'PASSED={len(passed)}\n')
        f.write(f'FAILED={len(failed)}\n')
        f.write(f'ERROR={len(error)}\n')
        f.write(f'SKIPPED={len(skipped)}\n')
        f.write(f'XFAIL={len(xfail)}\n')