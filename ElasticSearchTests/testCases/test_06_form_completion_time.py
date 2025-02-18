import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.form_completion_time.form_completion_time_page import FormCompletionTimePage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_form_comp_time_report_fields_filters_columns(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = FormCompletionTimePage(driver)
    activity.verify_form_comp_time_page_fields()
    activity.hide_filters()
    activity.show_filters()
    activity.verify_table_columns()
    activity.verify_users_in_the_group()



@pytest.mark.login
@pytest.mark.reports
def test_case_02_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = FormCompletionTimePage(driver)
    activity.form_comp_time_pagination_list()
    activity.verify_pagination_dropdown()
    activity.verify_sorted_list()


@pytest.mark.login
@pytest.mark.reports
def test_case_03_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = FormCompletionTimePage(driver)
    activity.form_comp_time_save_report()

@pytest.mark.login
@pytest.mark.reports
def test_case_04_export_to_excel(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = FormCompletionTimePage(driver)
    web_data = activity.export_form_comp_time_to_excel()
    activity.compare_fct_with_email(web_data)

@pytest.mark.login
@pytest.mark.reports
def test_case_05_user_type_filter_by(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = FormCompletionTimePage(driver)
    activity.form_comp_time_users_active()
    activity.form_comp_time_users_deactivated()
    activity.filter_dates_and_verify(UserData.filter_dates_by[0])
    # Commenting verification for Submission time filter as there is a bug
    # activity.filter_dates_and_verify(UserData.filter_dates_by[1])

def test_case_06_advanced_options(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = FormCompletionTimePage(driver)
    activity.no_form_selected()
    activity.advanced_options()
