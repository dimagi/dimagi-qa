import pytest

from ElasticSearchTests.testPages.daily_form_activity.daily_form_activity_page import DailyFormActivityPage
from ElasticSearchTests.testPages.data.reassign_cases_page import ReassignCasesPage
from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.daily_form_activity.daily_form_activity_page import DailyFormActivityPage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_daily_form_activity_report_fields_filters_columns(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = DailyFormActivityPage(driver)
    activity.verify_daily_activity_page_fields()
    activity.hide_filters()
    activity.show_filters()
    activity.verify_table_columns()
    activity.verify_users_in_the_group()

def test_case_02_date_range(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = DailyFormActivityPage(driver)
    activity.daily_form_activity_search(UserData.date_range[0])
    report.reports_menu()
    activity.daily_form_activity_search(UserData.date_range[1])
    report.reports_menu()
    activity.daily_form_activity_search(UserData.date_range[2])
    report.reports_menu()
    activity.daily_form_activity_search_custom_date()


@pytest.mark.login
@pytest.mark.reports
def test_case_03_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = DailyFormActivityPage(driver)
    activity.daily_form_activity_pagination_list()
    activity.verify_pagination_dropdown()
    activity.verify_sorted_list()

@pytest.mark.login
@pytest.mark.reports
def test_case_04_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = DailyFormActivityPage(driver)
    activity.daily_form_activity_save_report()

@pytest.mark.login
@pytest.mark.reports
def test_case_05_export_to_excel(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = DailyFormActivityPage(driver)
    web_data = activity.export_daily_form_activity_to_excel()
    email = EmailVerification(settings)
    link = email.get_hyperlink_from_latest_email(UserData.daily_form_report, settings['url'])
    activity.compare_dfa_with_email(link, web_data)

@pytest.mark.login
@pytest.mark.reports
def test_case_06_email_report(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = DailyFormActivityPage(driver)
    web_data, subject = activity.export_daily_form_activity_email()
    email = EmailVerification(settings)
    table_data = email.get_email_body_from_latest_email(subject, settings['url'])
    activity.compare_dfa_with_html_table(table_data, web_data)



@pytest.mark.login
@pytest.mark.reports
def test_case_07_user_type_filter_by(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = DailyFormActivityPage(driver)
    activity.daily_form_activity_users_active()
    activity.daily_form_activity_users_deactivated()
    activity.filter_dates_and_verify(UserData.filter_dates_by[0])
    activity.filter_dates_and_verify(UserData.filter_dates_by[1])

