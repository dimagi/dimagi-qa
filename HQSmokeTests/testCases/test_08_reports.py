import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage
from HQSmokeTests.userInputs.user_inputs import UserData

""""Contains test cases related to the Data module"""


@pytest.mark.report
@pytest.mark.reportMonitorWorkers
@pytest.mark.reportInspectData
@pytest.mark.reportManageDeployments
@pytest.mark.reportMessaging
def test_case_14_report_loading(driver, settings):
    """
        1. Navigate to HQ.
        2. Go to Reports>View all.
        3. Verify following types of Reports section are displayed.
            -Monitor Workers
            -Inspect Data
            -Manage Deployments
            -Messaging
        4. Access and run each report from the sections above
        5. Verify user is able run every report from each section and respective data should be reflected.
    """
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
    """
        1. Access the webapps
        2. Login as a mobile worker
        3. Verify user is able to view few of the applications that has web apps access enabled.
        4. Verify user can access any forms/modules of the application from Web Apps.
        5. Submit few forms.
        6. Navigate to Reports>Submit History.
        7. Apply filters.
        8. Verify user is able to search for the forms just submitted under Submit History & Case List
        9. Run the Submit History report and select a form
        10. Verify you're able to access the Form Data page
        11. Run the Case List report and select a case
        12. Verify you're able to access the Case Data page
    """
    home = HomePage(driver, settings)
    driver.refresh()
    home.web_apps_menu()
    webapps = WebAppsPage(driver)
    webapps.verify_apps_presence()
    case_name = webapps.submit_case_form()
    home.reports_menu()
    load = ReportPage(driver)
    load.verify_form_data_submit_history(case_name, settings['login_username'], app_config=UserData.reassign_cases)
    load.verify_form_data_case_list(case_name, settings['login_username'])


@pytest.mark.report
@pytest.mark.reportBuilder
def test_case_18_create_case_report(driver, settings):
    """
        1. Navigate to HQ.
        2. Go to Reports>View all.
        3. Click on Create new report under 'Report Builder' section.
        4. Enter report name.
        5. Select a case report
        5. Select remaining fields as you desire.
        6. Create and save and view report
        7. Verify you are able to create a custom report.
    """
    report = HomePage(driver, settings)
    report.reports_menu()
    load = ReportPage(driver)
    load.create_report_builder_case_report()
    load.delete_report()



@pytest.mark.report
@pytest.mark.savedReport
def test_case_19_saved_report(driver, settings):
    """
        1. Access any report that can be saved and emailed (The Case Activity report, for example)
        2. Save the report
        3. Verify the report can now be found under My Saved Reports
    """
    report = HomePage(driver, settings)
    report.reports_menu()
    load = ReportPage(driver)
    load.delete_scheduled_and_saved_reports()
    report.reports_menu()
    load.saved_report()

@pytest.mark.report
@pytest.mark.scheduledReport
def test_case_20_scheduled_report(driver, settings):
    """
        1. Remaining on My Saved Reports, go to the Scheduled Reports tab
        2. Create a new Scheduled Report
        3. Please delete the scheduled reports once you have tested what you need.
    """
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
    """
        1. Go to Reports
        2. Delete saved reports, report case and form links
    """
    report = HomePage(driver, settings)
    report.reports_menu()
    load = ReportPage(driver)
    load.delete_saved_reports()
    load.delete_report_case_links()
    load.delete_report_form_links()
