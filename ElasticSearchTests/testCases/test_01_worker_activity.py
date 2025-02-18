import pytest

from ElasticSearchTests.testPages.data.reassign_cases_page import ReassignCasesPage
from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.worker_activity.worker_activity_page import WorkerActivityPage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_worker_activity_report_no_case_type_filters(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = WorkerActivityPage(driver)
    activity.hide_filters()
    activity.show_filters()
    activity.worker_activity_report_no_case_type()
    activity.verify_users_in_the_group()


@pytest.mark.login
@pytest.mark.reports
def test_case_02_view_by_group_with_case_type(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = WorkerActivityPage(driver)
    activity.worker_activity_report_group_case_type()

@pytest.mark.login
@pytest.mark.reports
def test_case_03_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = WorkerActivityPage(driver)
    activity.worker_activity_pagination_list()
    activity.verify_pagination_dropdown()
    activity.verify_sorted_list()

@pytest.mark.login
@pytest.mark.reports
def test_case_04_date_range(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = WorkerActivityPage(driver)
    activity.worker_activity_search(UserData.date_range[0])
    report.reports_menu()
    activity.worker_activity_search(UserData.date_range[1])
    report.reports_menu()
    activity.worker_activity_search(UserData.date_range[2])
    report.reports_menu()
    activity.worker_activity_search_custom_date()
    activity.verify_users_in_the_group()

@pytest.mark.login
@pytest.mark.reports
def test_case_05_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    activity = WorkerActivityPage(driver)
    activity.worker_activity_save_report()

@pytest.mark.login
@pytest.mark.reports
def test_case_06_export_to_excel(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = WorkerActivityPage(driver)
    web_data = activity.export_worker_activity_to_excel()
    email = EmailVerification(settings)
    link = email.get_hyperlink_from_latest_email(UserData.worker_report, settings['url'])
    activity.compare_wa_with_email(link, web_data)

@pytest.mark.login
@pytest.mark.reports
def test_case_07_email_report(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = WorkerActivityPage(driver)
    web_data, subject = activity.export_worker_activity_email()
    email = EmailVerification(settings)
    table_data = email.get_email_body_from_latest_email(subject, settings['url'])
    activity.compare_wa_with_html_table(table_data, web_data)



@pytest.mark.login
@pytest.mark.reports
@pytest.mark.xfail
def test_case_08_case_assign(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = WorkerActivityPage(driver)
    actives, totals, text = activity.worker_activity_case_assign_data()
    home.data_menu()
    reassign = ReassignCasesPage(driver, settings)
    reassign.reassign_case(text)
    home.reports_menu()
    activity.verify_assigned_cases_count(actives, totals)
