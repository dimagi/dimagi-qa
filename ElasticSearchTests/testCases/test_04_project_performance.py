import pytest

from ElasticSearchTests.testPages.project_performance.project_performance_page import ProjectPerformancePage
from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.users.org_structure_page import latest_download_file
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.case_activity.case_activity_page import CaseActivityPage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_project_performance_report_fields_filters_columns(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = ProjectPerformancePage(driver)
    activity.verify_proj_perf_page_fields()
    activity.hide_filters()
    activity.show_filters()
    activity.verify_tables_columns()


def test_case_02_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = ProjectPerformancePage(driver)
    activity.verify_proj_perf_page_fields()
    activity.proj_perf_pagination_list()
    activity.verify_pagination_dropdown()



@pytest.mark.login
@pytest.mark.reports
def test_case_03_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = ProjectPerformancePage(driver)
    activity.proj_perf_save_report()

@pytest.mark.login
@pytest.mark.reports
def test_case_04_multi_option_export_to_excel(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = ProjectPerformancePage(driver)
    activity.proj_perf_group_selection()
    list_low, list_inactive, list_high = activity.export_proj_perf_to_excel()
    activity.compare_pp_with_excel(list_low, list_inactive, list_high)

@pytest.mark.login
@pytest.mark.reports
def test_case_05_email_report(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = ProjectPerformancePage(driver)
    web_data, subject = activity.export_proj_perf_email()
    email = EmailVerification(settings)
    table_data = email.get_email_body_from_latest_email_proj_perf(subject, settings['url'])
    activity.compare_proj_perf_with_html_table(table_data, web_data)

