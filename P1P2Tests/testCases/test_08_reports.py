import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage

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

