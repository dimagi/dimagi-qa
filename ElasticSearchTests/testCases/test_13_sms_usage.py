import pytest

from ElasticSearchTests.testPages.sms_usage.sms_usage_page import SMSUsagePage
from ElasticSearchTests.testPages.data.reassign_cases_page import ReassignCasesPage
from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.sms_usage.sms_usage_page import SMSUsagePage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_sms_usage_report_fields_filters_columns(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = SMSUsagePage(driver)
    activity.verify_page()
    activity.hide_filters()
    activity.show_filters()
    activity.verify_sms_usage_page_fields_columns()


def test_case_02_date_range(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = SMSUsagePage(driver)
    activity.sms_usage_search(UserData.date_range[0])
    report.reports_menu()
    activity.sms_usage_search(UserData.date_range[1])
    report.reports_menu()
    activity.sms_usage_search(UserData.date_range[2])
    report.reports_menu()
    activity.sms_usage_search_custom_date()


@pytest.mark.login
@pytest.mark.reports
def test_case_03_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = SMSUsagePage(driver)
    activity.sms_usage_pagination_list()
    activity.verify_sorted_list(UserData.sms_usage_column_names[1])
    activity.verify_sorted_list(UserData.sms_usage_column_names[2])
    activity.verify_sorted_list(UserData.sms_usage_column_names[3])
    activity.verify_sorted_list(UserData.sms_usage_column_names[0])

@pytest.mark.login
@pytest.mark.reports
def test_case_04_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = SMSUsagePage(driver)
    activity.sms_usage_save_report()


@pytest.mark.login
@pytest.mark.reports
def test_case_05_group_and_user_verification(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = SMSUsagePage(driver)
    activity.verify_deleted_group()
    activity.verify_valid_group_with_user()
