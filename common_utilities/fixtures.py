import pytest
from py.xml import html

from selenium import webdriver
from common_utilities.path_settings import PathSettings
from common_utilities.hq_login.login_page import LoginPage


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
            chrome_options.add_argument('disable-extensions')
            chrome_options.add_argument('--safebrowsing-disable-download-protection')
            chrome_options.add_argument('--safebrowsing-disable-extension-blacklist')
            chrome_options.add_argument('window-size=1920,1080')
            chrome_options.add_argument("--disable-setuid-sandbox")
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument("--disable-notifications")
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
    login = LoginPage(web_driver, settings["url"])
    login.login(settings["login_username"], settings["login_password"])
    yield web_driver
    web_driver.quit()


def pytest_addoption(parser):
    """CLI args which can be used to run the tests with specified values."""
    parser.addoption("--browser", action="store", default='chrome', choices=['chrome', 'firefox'],
                     help='Your choice of browser to run tests.')
    parser.addoption("--appsite", action="store", choices=['CO', 'NY'],
                     help='Your choice of app site.')


@pytest.fixture(scope="module")
def browser(request):
    """Pytest fixture for browser"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def appsite(pytestconfig):
    """Pytest fixture for app site"""
    return pytestconfig.getoption("--appsite")


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_header(cells):
    # <th class="sortable result initial-sort asc inactive" col="result"><div class="sort-icon">vvv</div>Result</th>
    cells.insert(1, html.th('Tags', class_="sortable", col="tags"))
    cells.pop()


@pytest.hookimpl(optionalhook=True)
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(getattr(report, 'tags', '')))
    cells.pop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    tags = ", ".join([m.name for m in item.iter_markers() if m.name != 'run'])
    extra = getattr(report, 'extra', [])
    if report.when == "call" or report.when == "teardown":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            print("reports skipped or failed")
            file_name = report.nodeid.replace("::", "_") + ".png"
            screen_img = _capture_screenshot(item.funcargs["driver"])
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
        report.tags = tags
def _capture_screenshot(web_driver):
    return web_driver.get_screenshot_as_base64()
