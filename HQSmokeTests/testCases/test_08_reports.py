import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage

""""Contains test cases related to the Data module"""


@pytest.mark.report
@pytest.mark.reportMonitorWorkers
@pytest.mark.reportInspectData
@pytest.mark.reportManageDeployments
@pytest.mark.reportMessaging
def test_case_14_report_loading(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    load = ReportPage(driver)
    load.worker_activity_report()
    load.daily_form_activity_report()
    load.submissions_by_form_report()
    load.form_completion_report()
    load.case_activity_report()
    load.completion_vs_submission_report()
    # load.worker_activity_times_report()
    load.project_performance_report()
    load.submit_history_report()
    load.case_list_report()
    load.sms_usage_report()
    load.messaging_history_report()
    load.message_log_report()
    load.sms_opt_out_report()
    load.scheduled_messaging_report()


@pytest.mark.webApps
@pytest.mark.report
@pytest.mark.reportSubmitHistory
@pytest.mark.reportFormData
@pytest.mark.reportCaseList
@pytest.mark.reportCaseData
def test_case_15_16_submit_form_verify_formdata_casedata(driver, settings):
    home = HomePage(driver, settings)
    driver.refresh()
    home.web_apps_menu()
    webapps = WebAppsPage(driver)
    webapps.verify_apps_presence()
    case_name = webapps.submit_case_form()
    home.reports_menu()
    load = ReportPage(driver)
    load.verify_form_data_submit_history(case_name, settings['login_username'])
    load.verify_form_data_case_list(case_name)


@pytest.mark.report
@pytest.mark.reportBuilder
def test_case_18_create_case_report(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    load = ReportPage(driver)
    load.create_report_builder_case_report()
    load.delete_report()



@pytest.mark.report
@pytest.mark.savedReport
def test_case_19_saved_report(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    load = ReportPage(driver)
    load.delete_scheduled_and_saved_reports()
    report.reports_menu()
    load.saved_report()



@pytest.mark.report
@pytest.mark.scheduledReport
def test_case_20_scheduled_report(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    load = ReportPage(driver)
    load.delete_scheduled_and_saved_reports()
    time, user = load.scheduled_report()
    load.verify_scheduled_report(time, user)
    load.delete_scheduled_and_saved_reports()

@pytest.mark.report
@pytest.mark.deleteReport
def test_case_delete_saved_reports(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    load = ReportPage(driver)
    load.delete_saved_reports()
    load.delete_report_case_links()
    load.delete_report_form_links()
