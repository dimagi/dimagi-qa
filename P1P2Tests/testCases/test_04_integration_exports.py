from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage

import pytest

""""Contains test cases related to the Integrated Exports"""


@pytest.mark.data
@pytest.mark.excelDashboardIntegrationForm
@pytest.mark.p1p2EscapeDefect
def test_case_25_excel_dashboard_integration_form(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    form = export.excel_dashboard_integration_form()
    link = export.check_feed_link(form)
    export.verify_duplicate_data_in_dashboard(link, settings['login_username'], settings['login_password'])


@pytest.mark.data
@pytest.mark.excelDashboardIntegrationCase
@pytest.mark.p1p2EscapeDefect
def test_case_26_excel_dashboard_integration_case(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    case = export.excel_dashboard_integration_case()
    link = export.check_feed_link(case)
    export.verify_duplicate_data_in_dashboard(link, settings['login_username'], settings['login_password'])

@pytest.mark.data
@pytest.mark.powerBiTableauIntegrationCase
@pytest.mark.p1p2EscapeDefect
#SAAS-13243, SAAS-14468
def test_case_27_powerbi_tableau_integration_case(driver, settings):
    username = settings["login_username"]
    password = settings["login_password"]
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    export.power_bi_tableau_integration_case(username, password)