import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from Features.FindDataById.testPages.data.find_data_page import FindDataPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from Features.FindDataById.userInputs.user_inputs import UserData

""""Contains test cases related to the Data module"""

values = dict()


def test_case_01_verify_page_ui(driver,settings):
    home = HomePage(driver, settings)
    page = FindDataPage(driver)
    home.data_menu()
    page.find_data_by_id_page_ui()

def test_case_02_verify_invalid_ids(driver,settings):
    home = HomePage(driver, settings)
    page = FindDataPage(driver)
    home.data_menu()
    page.find_data_by_id_page_ui()
    page.search_invalid_ids("case")
    page.search_invalid_ids("form")

def test_case_03_validating_export_page(driver,settings):
    home = HomePage(driver, settings)
    page = FindDataPage(driver)
    home.data_menu()
    page.find_data_by_id_page_ui()
    page.verify_data_exports_link("case")
    page.find_data_by_id_page_ui()
    page.verify_data_exports_link("form")


def test_case_04_finding_case_form_ids(driver,settings):
    home = HomePage(driver, settings)
    webapps = WebAppsPage(driver)
    load = ReportPage(driver)
    page = FindDataPage(driver)
    driver.refresh()
    home.web_apps_menu()
    case_name = webapps.submit_case_form()
    webapps.verify_apps_presence()
    home.reports_menu()
    case_id_value= load.verify_form_data_submit_history(case_name, settings['login_username'], "case", UserData.reassign_cases_app_data)
    form_id_value = load.verify_form_data_submit_history(case_name, settings['login_username'], "form", UserData.reassign_cases_app_data )
    #user_id_value= load.verify_form_data_submit_history(case_name, settings['login_username'], "user", UserData.reassign_cases_app_data)
    home.data_menu()
    page.find_data_by_id_page_ui()
    page.validate_web_user_location_group_data_pages("case","location",case_id_value)
    page.find_data_by_id_page_ui()
    page.validate_web_user_location_group_data_pages("case","location",form_id_value)
    #page.find_data_by_id_page_ui()
    #page.validate_web_user_location_group_data_pages("case","location",user_id_value)


def test_case_05_validating_correct_data_pages(driver,settings):
    home = HomePage(driver, settings)
    page = FindDataPage(driver)
    home.data_menu()
    page.find_data_by_id_page_ui()
    page.validate_web_user_location_group_data_pages("case","location")
    page.find_data_by_id_page_ui()
    page.validate_web_user_location_group_data_pages("case","group")
    page.find_data_by_id_page_ui()
    page.validate_web_user_location_group_data_pages("form","location")
    page.find_data_by_id_page_ui()
    page.validate_web_user_location_group_data_pages("form","group")
    #page.find_data_by_id_page_ui()
    #page.validate_web_user_location_group_data_pages("case","web_user")
    #page.find_data_by_id_page_ui()
    #page.validate_web_user_location_group_data_pages("form", "web_user")

