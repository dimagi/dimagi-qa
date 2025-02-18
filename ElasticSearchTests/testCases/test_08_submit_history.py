import pytest

from ElasticSearchTests.testPages.data.reassign_cases_page import ReassignCasesPage
from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.submit_history.submit_history_page import SubmitHistoryPage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_submit_history_report_no_case_type_filters(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    history = SubmitHistoryPage(driver)
    history.verify_page()
    history.hide_filters()
    history.show_filters()
    history.verify_submit_history_page_fields_columns()


@pytest.mark.login
@pytest.mark.reports
def test_case_02_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    history = SubmitHistoryPage(driver)
    history.submit_history_pagination_list()
    history.verify_pagination_dropdown()
    history.verify_sorted_list("User")
    history.verify_sorted_list("Completion Time")
    history.verify_sorted_list("Form")


@pytest.mark.login
@pytest.mark.reports
def test_case_03_date_range(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    history = SubmitHistoryPage(driver)
    history.submit_history_date_range()

@pytest.mark.login
@pytest.mark.reports
def test_case_04_advanced_options_filter_by(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    history = SubmitHistoryPage(driver)
    history.advanced_options()
    history.filter_dates_and_verify(UserData.filter_dates_by[0])
    history.filter_dates_and_verify(UserData.filter_dates_by[1])

@pytest.mark.login
@pytest.mark.reports
def test_case_05_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    history = SubmitHistoryPage(driver)
    history.submit_history_save_report()


@pytest.mark.login
@pytest.mark.reports
def test_case_08_users_groups_forms(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    history = SubmitHistoryPage(driver)
    history.verify_single_user(UserData.app_login)
    history.verify_single_user(UserData.web_user)
    history.verify_multiple_users()
    history.verify_form_links()
