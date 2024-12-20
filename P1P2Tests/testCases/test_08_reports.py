import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage
from P1P2Tests.userInputs.user_inputs import UserData

""""Contains test cases related to the Data module"""


@pytest.mark.report
@pytest.mark.reportBuilderForm
@pytest.mark.reportBuilderCase
@pytest.mark.editReport
@pytest.mark.p1p2EscapeDefect
def test_case_17_create_form_report(driver, settings):
    report = HomePage(driver, settings)
    driver.refresh()
    report.reports_menu()
    load = ReportPage(driver)
    load.create_report_builder_form_report()
    report.reports_menu()
    load.configure_add_report()
    load.delete_report()

@pytest.mark.reportBuilderForm
@pytest.mark.reportBuilderCase
@pytest.mark.editReport
@pytest.mark.p1p2EscapeDefect
def test_case_17_create_case_report(driver, settings):
    report = HomePage(driver, settings)
    driver.refresh()
    report.reports_menu()
    load = ReportPage(driver)
    load.create_report_builder_case_report()
    load.delete_report()

@pytest.mark.report
@pytest.mark.caseListPage
@pytest.mark.p1p2EscapeDefect
def test_case_82_check_case_list(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    report = ReportPage(driver)
    report.verify_case_list_page()

@pytest.mark.report
@pytest.mark.caseListPage
@pytest.mark.p1p2EscapeDefect
def test_case_86_export_to_excel_config_report(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    report = ReportPage(driver)
    report.export_to_excel_config_report(UserData.report_for_p1p2)

@pytest.mark.report
@pytest.mark.applicationStatusPage
@pytest.mark.p1p2EscapeDefect
def test_case_87_application_status_report(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    report = ReportPage(driver)
    report.application_status_report_search()
    report.verify_sorted_list()


@pytest.mark.report
@pytest.mark.caseListExplorer
@pytest.mark.p1p2EscapeDefect
def test_case_92_verify_case_list_explorer_properties(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    report = ReportPage(driver)
    name = report.verify_case_list_explorer_properties()
    report.add_new_property(name)



