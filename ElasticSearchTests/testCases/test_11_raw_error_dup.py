import pytest

from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.raw_forms_errors_duplicates.raw_forms_errors_duplicates_page import RawFormsErrorsDuplicatesPage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_red_report_no_case_type_filters(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    case = RawFormsErrorsDuplicatesPage(driver)
    case.verify_page()
    case.hide_filters()
    case.show_filters()
    case.verify_red_page_no_filter()
    case.verify_red_page_fields_columns()


@pytest.mark.login
@pytest.mark.reports
def test_case_02_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    case = RawFormsErrorsDuplicatesPage(driver)
    case.red_pagination_list()
    case.verify_pagination_dropdown()
    case.verify_sorted_list("Username")
    case.verify_sorted_list("Submit Time")

@pytest.mark.login
@pytest.mark.reports
def test_case_03_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    case = RawFormsErrorsDuplicatesPage(driver)
    case.red_save_report()


@pytest.mark.login
@pytest.mark.reports
def test_case_04_different_submission_type(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = RawFormsErrorsDuplicatesPage(driver)
    activity.verify_submission_form_type(UserData.submit_form_type[0])
    activity.verify_submission_form_type(UserData.submit_form_type[1])
    activity.verify_submission_form_type(UserData.submit_form_type[2])
    activity.verify_submission_form_type(UserData.submit_form_type[3])
    activity.verify_submission_form_type(UserData.submit_form_type[4])
    activity.verify_submission_form_type(UserData.submit_form_type[5])
    activity.verify_submission_form_type_all()

@pytest.mark.login
@pytest.mark.reports
def test_case_05_view_form_update(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = RawFormsErrorsDuplicatesPage(driver)
    activity.view_form_update()
