import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.form_completion_vs_submission_trends.form_completion_vs_submission_trends_page import FormCompletionVsSubmissionTrends

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_form_comp_sub_trends_report_fields_filters_columns(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = FormCompletionVsSubmissionTrends(driver)
    activity.verify_form_comp_sub_trends_page_fields()
    activity.hide_filters()
    activity.show_filters()
    activity.verify_table_columns()
    activity.form_comp_sub_trends_users_active()


@pytest.mark.login
@pytest.mark.reports
def test_case_02_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = FormCompletionVsSubmissionTrends(driver)
    activity.form_comp_sub_trends_pagination_list()
    activity.verify_pagination_dropdown()
    activity.verify_sorted_list("User")
    activity.verify_sorted_list("Completion Time")
    activity.verify_sorted_list("Submission Time")
    activity.verify_sorted_list("Form Name")
    activity.verify_sorted_list("Difference")


@pytest.mark.login
@pytest.mark.reports
def test_case_03_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = FormCompletionVsSubmissionTrends(driver)
    activity.form_comp_sub_trends_save_report()
    activity.save_report_error()

@pytest.mark.login
@pytest.mark.reports
def test_case_04_export_to_excel(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = FormCompletionVsSubmissionTrends(driver)
    web_data = activity.export_form_comp_sub_trends_to_excel()
    activity.compare_fct_with_email(web_data)


def test_case_06_advanced_options(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = FormCompletionVsSubmissionTrends(driver)
    activity.advanced_options()
    activity.form_column_verification(UserData.reassign_cases_application,
                                      list(UserData.reasign_modules_forms.keys())[1],
                                      UserData.reasign_modules_forms[
                                          list(UserData.reasign_modules_forms.keys())[1]][0])
    activity.form_column_verification(UserData.reassign_cases_application)
    activity.form_column_verification(UserData.reassign_cases_application,
                                      list(UserData.reasign_modules_forms.keys())[1])
    activity.form_column_verification(UserData.reassign_cases_application,
                                      list(UserData.reasign_modules_forms.keys())[0])
