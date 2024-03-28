import pytest

from ElasticSearchTests.testPages.device_logs_details.device_logs_details_page import DeviceLogsDetailsPage
from ElasticSearchTests.testPages.data.reassign_cases_page import ReassignCasesPage
from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.device_logs_details.device_logs_details_page import DeviceLogsDetailsPage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_device_logs_details_report_fields_filters_columns(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = DeviceLogsDetailsPage(driver)
    activity.verify_page()
    activity.hide_filters()
    activity.show_filters()
    activity.verify_device_logs_details_page_fields_columns()


def test_case_02_date_range(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = DeviceLogsDetailsPage(driver)
    activity.device_logs_details_search(UserData.date_range[0])
    report.reports_menu()
    activity.device_logs_details_search(UserData.date_range[1])
    report.reports_menu()
    activity.device_logs_details_search(UserData.date_range[2])
    report.reports_menu()
    activity.device_logs_details_search_custom_date()


@pytest.mark.login
@pytest.mark.reports
def test_case_03_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = DeviceLogsDetailsPage(driver)
    activity.device_logs_details_pagination_list()
    # activity.verify_pagination_dropdown()
    activity.verify_sorted_list(UserData.device_logs_column_names[0])
    activity.verify_sorted_list(UserData.device_logs_column_names[1])
    activity.verify_sorted_list(UserData.device_logs_column_names[2])
    activity.verify_sorted_list(UserData.device_logs_column_names[3])
    activity.verify_sorted_list(UserData.device_logs_column_names[4])
    # activity.verify_sorted_list(UserData.device_logs_column_names[5])
    # activity.verify_sorted_list(UserData.device_logs_column_names[6])
    activity.verify_sorted_list(UserData.device_logs_column_names[7])

@pytest.mark.login
@pytest.mark.reports
def test_case_04_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = DeviceLogsDetailsPage(driver)
    activity.device_logs_details_save_report()

@pytest.mark.login
@pytest.mark.reports
def test_case_05_email_report(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = DeviceLogsDetailsPage(driver)
    web_data, subject = activity.export_device_logs_details_email()
    email = EmailVerification(settings)
    table_data = email.get_email_body_from_latest_email(subject, settings['url'])
    activity.compare_dld_with_html_table(table_data, web_data)




