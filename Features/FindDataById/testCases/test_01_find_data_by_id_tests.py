import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from Features.FindDataById.testPages.data.find_data_page import FindIdPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from Features.FindDataById.userInputs.user_inputs import UserData

""""Contains test cases related to the Data module"""

values = dict()

@pytest.mark.lookup
def test_case_01_verify_page_ui(driver,settings):
    home = HomePage(driver, settings)
    page = FindIdPage(driver)
    home.data_menu()
    page.find_data_by_id_page_ui()

def test_case_02_finding_group_id(driver,settings):
    home = HomePage(driver, settings)
    page = FindIdPage(driver)
    home.data_menu()
    page.find_data_by_id_page_ui()
    page.validate_group_ids("case")
    page.validate_group_ids("form")

def test_case_03_verify_invalid_ids(driver,settings):
    home = HomePage(driver, settings)
    page = FindIdPage(driver)
    home.data_menu()
    page.find_data_by_id_page_ui()
    page.search_invalid_ids("case")
    page.search_invalid_ids("form")

def test_case_04_finding_location_id(driver,settings):
    home = HomePage(driver, settings)
    page = FindIdPage(driver)
    home.data_menu()
    page.find_data_by_id_page_ui()
    page.validate_location_ids("case")
    home.data_menu()
    page.find_data_by_id_page_ui()
    page.validate_location_ids("form")

def test_case_05_validating_export_page(driver,settings):
    home = HomePage(driver, settings)
    page = FindIdPage(driver)
    home.data_menu()
    page.find_data_by_id_page_ui()
    page.verify_data_exports_link("case")
    page.find_data_by_id_page_ui()
    page.verify_data_exports_link("form")


def test_case_06_finding_web_user_id(driver,settings):
    home = HomePage(driver, settings)
    page = FindIdPage(driver)
    home.data_menu()
    page.find_data_by_id_page_ui()
    page.validate_web_user_ids("case")
    page.validate_web_user_ids("form")

def test_case_07_finding_case_form_ids(driver,settings):
    home = HomePage(driver, settings)
    webapps = WebAppsPage(driver)
    load = ReportPage(driver)
    page = FindIdPage(driver)
    driver.refresh()
    home.web_apps_menu()
    case_name = webapps.submit_case_form()
    webapps.verify_apps_presence()
    home.reports_menu()
    case_id_value= load.verify_form_data_submit_history(case_name,settings['login_username'], "case")
    form_id_value= load.verify_form_data_submit_history(case_name,settings['login_username'], "form" )
    user_id_value= load.verify_form_data_submit_history(case_name,settings['login_username'], "user")
    home.data_menu()
    page.find_data_by_id_page_ui()
    page.validate_case_form_input_id("case",case_id_value)
    page.find_data_by_id_page_ui()
    page.validate_case_form_input_id("form", form_id_value)
    page.find_data_by_id_page_ui()
    page.validate_case_form_input_id("case",user_id_value)