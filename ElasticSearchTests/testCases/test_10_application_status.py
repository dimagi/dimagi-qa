import pytest

from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.application_status.application_status_page import ApplicationStatusPage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_application_status_report_no_case_type_filters(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    case = ApplicationStatusPage(driver)
    case.verify_page()
    case.hide_filters()
    case.show_filters()
    case.verify_application_status_page_fields_columns()


@pytest.mark.login
@pytest.mark.reports
def test_case_02_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    case = ApplicationStatusPage(driver)
    case.application_status_pagination_list()
    case.verify_pagination_dropdown()
    case.verify_sorted_list("Username")
    case.verify_sorted_list("Last Submission")
    case.verify_sorted_list("Last Sync")
    case.verify_sorted_list("Application Version")
    # case.verify_sorted_list("CommCare Version")

@pytest.mark.login
@pytest.mark.reports
def test_case_03_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    case = ApplicationStatusPage(driver)
    case.application_status_save_report()


@pytest.mark.login
@pytest.mark.reports
def test_case_04_export_to_excel(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = ApplicationStatusPage(driver)
    web_data = activity.export_app_status_to_excel()
    email = EmailVerification(settings)
    link = email.get_hyperlink_from_latest_email(UserData.app_status_report, settings['url'])
    activity.compare_status_with_email(link, web_data)

@pytest.mark.login
@pytest.mark.reports
def test_case_05_email_report(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = ApplicationStatusPage(driver)
    web_data, subject = activity.export_app_status_email()
    email = EmailVerification(settings)
    table_data = email.get_email_body_from_latest_email(UserData.email_app_status_report, settings['url'])
    activity.compare_status_with_html_table(table_data, web_data)
