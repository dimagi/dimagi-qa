from datetime import datetime

import pytest
from py.xml import html

from selenium import webdriver
from common_utilities.path_settings import PathSettings
from common_utilities.hq_login.login_page import LoginPage
import base64
import json
from pathlib import Path
import ast
import os


""""This file provides fixture functions for driver initialization"""

global driver
from collections import OrderedDict

failed_items = OrderedDict()

@pytest.fixture(scope="module", autouse=True)
def driver(settings, browser):
    web_driver = None
    chrome_options = webdriver.ChromeOptions()
    firefox_options = webdriver.FirefoxOptions()
    if settings.get("CI") == "true":
        if browser == "chrome":
            # chrome_options.add_argument('--no-sandbox')
            # chrome_options.add_argument('disable-extensions')
            # chrome_options.add_argument('--safebrowsing-disable-download-protection')
            # chrome_options.add_argument('--safebrowsing-disable-extension-blacklist')
            # chrome_options.add_argument('window-size=1920,1080')
            # chrome_options.add_argument("--disable-setuid-sandbox")
            # chrome_options.add_argument('--start-maximized')
            # chrome_options.add_argument('--disable-dev-shm-usage')
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--headless=new')  # or '--headless=chrome' for newer versions
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--safebrowsing-disable-download-protection')
            chrome_options.add_argument('--safebrowsing-disable-extension-blacklist')
            chrome_options.add_argument('--window-size=1920,1080')  # sets consistent resolution
            chrome_options.add_argument('--force-device-scale-factor=1')  # fixes zoom/dpi issues

            chrome_options.add_experimental_option("prefs", {
                "download.default_directory": str(PathSettings.DOWNLOAD_PATH),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
                "safebrowsing.disable_download_protection": True})
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
            firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                           "application/vnd.ms-excel,application/octet-stream,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                           )
            firefox_options.set_preference("pdfjs.disabled", True)
            firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
            firefox_options.set_preference("browser.download.panel.shown", False)
            firefox_options.set_preference("security.mixed_content.block_active_content", False)  # allow mixed content if needed
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


def _capture_screenshot(driver):
    return base64.b64encode(driver.get_screenshot_as_png()).decode('utf-8')

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
                html = (
                    '<div><img src="data:image/png;base64,%s" alt="screenshot" '
                    'style="width:600px;height:300px;" onclick="window.open(this.src)" align="right"/></div>'
                    % screen_img
                )
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
        report.tags = tags



# def pytest_sessionfinish(session, exitstatus):
#     if not failed_items:
#         return
#
#     seen = set()
#     lines = []
#     for nodeid, item in failed_items.items():
#         if nodeid in seen:
#             continue
#         seen.add(nodeid)
#
#         try:
#             doc = item.function.__doc__ or "No reproduction steps provided."
#         except AttributeError:
#             doc = "No docstring available (non-function test case)"
#         lines.append(f"Test: {nodeid}\nRepro Steps:\n{doc.strip()}\n\n---")
#
#     with open("jira_ticket_body.txt", "w", encoding="utf-8") as f:
#         f.write(f"🔥 Automated Failure Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
#         f.write("\n".join(lines) if lines else "✅ All tests passed.")
#
def check_if_any_test_failed(json_path="final_failures.json") -> bool:
    """
    Returns True if any test has outcome 'failed' in the JSON report.
    """
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        return any(t.get("outcome") == "failed" for t in data.get("tests", []))
    except Exception as e:
        print(f"Error checking failures: {e}")
        return False

def generate_jira_summary_from_json_report(json_path="final_failures.json", output_path="jira_ticket_body.html"):
    """
    Extracts failed test cases from JSON report and gathers their docstrings for Jira summary in HTML format.
    """
    json_file = Path(json_path)
    if not json_file.exists():
        print(f"JSON report {json_path} not found.")
        return

    with open(json_file, "r") as f:
        report_data = json.load(f)

    failures = [
        test for test in report_data.get("tests", [])
        if test.get("outcome") == "failed"
    ]

    seen = set()
    unique_failures = []
    for test in failures:
        if test["nodeid"] not in seen:
            unique_failures.append(test)
            seen.add(test["nodeid"])

    def extract_docstring_from_file(nodeid):
        parts = nodeid.split("::")
        if not parts:
            return "Could not parse nodeid"

        filepath = parts[0]
        test_func = parts[-1]

        try:
            full_path = Path(filepath).resolve()
            with open(full_path, "r") as f:
                parsed = ast.parse(f.read())
                for node in ast.walk(parsed):
                    if isinstance(node, ast.FunctionDef) and node.name == test_func:
                        return ast.get_docstring(node) or "Not documented."
        except Exception as e:
            return f"Error reading docstring: {e}"

        return "Docstring not found."

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("<html><body style='font-family:Arial,sans-serif;'>\n")
        if not unique_failures:
            f.write("<p>✅ All testcases passed.</p>\n")
        else:
            f.write(f"<h2 style='color:red;'>🚨 Failed Test Cases with Reproducible Steps ({datetime.now().strftime('%Y-%m-%d %H:%M')})</h2>\n")
            for test in unique_failures:
                doc = extract_docstring_from_file(test["nodeid"])
                f.write(f"<b>Test:</b> {test['nodeid']}<br>\n")
                f.write(f"<b>Repro Steps:</b><br>\n")
                f.write(f"{doc.strip().replace('\n', '<br>')}<br><hr>\n")
        f.write("</body></html>\n")

    print(f"Jira summary written to {output_path}")