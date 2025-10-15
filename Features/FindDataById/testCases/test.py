import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from Features.FindDataById.testPages.data.find_data_page import FindIdPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage
from HQSmokeTests.testPages.reports.report_page import ReportPage

""""Contains test cases related to the Data module"""

values = dict()

@pytest.mark.lookup
def test_case_01_ui(driver,settings):
    home = HomePage(driver, settings)
    page = FindIdPage(driver)
    home.data_menu()
    page.page_ui()

def test_case_02_find_group_id(driver,settings):
    home = HomePage(driver, settings)
    page = FindIdPage(driver)
    home.data_menu()
    page.page_ui()
    page.group_id("case")
    page.group_id("form")

def test_case_03_invalid_ids(driver,settings):
    home = HomePage(driver, settings)
    page = FindIdPage(driver)
    home.data_menu()
    page.page_ui()
    page.search_invalid_id("case")
    page.search_invalid_id("form")

def test_case_04_find_location_id(driver,settings):
    home = HomePage(driver, settings)
    page = FindIdPage(driver)
    home.data_menu()
    page.page_ui()
    page.location_id("case")
    home.data_menu()
    page.page_ui()
    page.location_id("form")

def test_case_05_export_page(driver,settings):
    home = HomePage(driver, settings)
    page = FindIdPage(driver)
    home.data_menu()
    page.page_ui()
    page.data_exports_link("case")
    page.page_ui()
    page.data_exports_link("form")


def test_case_06_find_web_user_id(driver,settings):
    home = HomePage(driver, settings)
    page = FindIdPage(driver)
    home.data_menu()
    page.page_ui()
    page.web_user_id("case")
    page.web_user_id("form")

def test_case_07_find_id(driver,settings):
    home = HomePage(driver, settings)
    webapps = WebAppsPage(driver)
    load = ReportPage(driver)
    page = FindIdPage(driver)
    driver.refresh()
    home.web_apps_menu()
    case_name = webapps.submit_case_form()
    webapps.verify_apps_presence()
    home.reports_menu()
    case_id_value= load.verify_form_data_submit_history(case_name, settings['login_username'], "case")
    user_id_value= load.verify_form_data_submit_history(case_name, settings['login_username'], "user")
    form_id_value= load.verify_form_data_submit_history(case_name, settings['login_username'], "form")
    home.data_menu()
    page.page_ui()
    page.input_id("case",case_id_value)
    page.page_ui()
    page.input_id("case",user_id_value)
    page.page_ui()
    page.input_id("form",form_id_value)