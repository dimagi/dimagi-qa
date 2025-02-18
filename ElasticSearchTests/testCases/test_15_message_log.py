import pytest

from ElasticSearchTests.testPages.message_log.message_log_page import MessageLogPage
from ElasticSearchTests.testPages.data.reassign_cases_page import ReassignCasesPage
from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.message_log.message_log_page import MessageLogPage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_message_log_report_fields_filters_columns(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = MessageLogPage(driver)
    activity.verify_page()
    activity.hide_filters()
    activity.show_filters()
    activity.verify_message_log_page_fields_columns()


def test_case_02_date_range(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = MessageLogPage(driver)
    activity.message_log_search(UserData.date_range[0])
    report.reports_menu()
    activity.message_log_search(UserData.date_range[1])
    report.reports_menu()
    activity.message_log_search(UserData.date_range[2])
    report.reports_menu()
    activity.message_log_search_custom_date()


@pytest.mark.login
@pytest.mark.reports
def test_case_03_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = MessageLogPage(driver)
    activity.message_log_pagination_list()
    activity.verify_pagination_dropdown()
    activity.verify_sorted_list(UserData.ml_column_names[1])
    activity.verify_sorted_list(UserData.ml_column_names[2])
    activity.verify_sorted_list(UserData.ml_column_names[3])
    activity.verify_sorted_list(UserData.ml_column_names[4])
    activity.verify_sorted_list(UserData.ml_column_names[5])
    activity.verify_sorted_list(UserData.ml_column_names[0])

@pytest.mark.login
@pytest.mark.reports
def test_case_04_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = MessageLogPage(driver)
    activity.message_log_save_report()


def test_case_05_report_filter_selections(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    case = MessageLogPage(driver)
    case.report_filter_message_type()
    case.report_filter_location_filter(UserData.location_filter[0])
    case.report_filter_location_filter(UserData.location_filter[1])


@pytest.mark.login
@pytest.mark.reports
def test_case_06_export_to_excel(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = MessageLogPage(driver)
    web_data = activity.export_message_log_to_excel()
    activity.compare_message_log_with_webdata(web_data)

