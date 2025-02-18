import pytest

from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.case_activity.case_activity_page import CaseActivityPage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_case_activity_report_fields_filters_columns(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = CaseActivityPage(driver)
    activity.verify_case_activity_page_fields()
    activity.hide_filters()
    activity.show_filters()
    activity.verify_table_columns()
    activity.verify_users_in_the_group()

@pytest.mark.login
@pytest.mark.reports
@pytest.mark.xfail
def test_case_02_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = CaseActivityPage(driver)
    activity.case_activity_pagination_list()
    activity.verify_pagination_dropdown()
    activity.verify_sorted_list()


@pytest.mark.login
@pytest.mark.reports
def test_case_03_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = CaseActivityPage(driver)
    activity.case_activity_save_report()

@pytest.mark.login
@pytest.mark.reports
def test_case_04_export_to_excel(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = CaseActivityPage(driver)
    web_data = activity.export_case_activity_to_excel()
    email = EmailVerification(settings)
    link = email.get_hyperlink_from_latest_email(UserData.case_report, settings['url'])
    activity.compare_ca_with_email(link, web_data)

@pytest.mark.login
@pytest.mark.reports
def test_case_05_email_report(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = CaseActivityPage(driver)
    web_data, subject = activity.export_case_activity_email()
    email = EmailVerification(settings)
    table_data = email.get_email_body_from_latest_email(subject, settings['url'])
    activity.compare_ca_with_html_table(table_data, web_data)



@pytest.mark.login
@pytest.mark.reports
def test_case_06_user_type_date_verification(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = CaseActivityPage(driver)
    activity.case_activity_users_active()
    activity.case_activity_users_deactivated()
    activity.user_data_verify()


