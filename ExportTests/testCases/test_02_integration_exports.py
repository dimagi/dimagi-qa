from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage

import pytest

""""Contains test cases related to the Integrated Exports"""

test_case_update_case = dict()
test_case_update_case["case_id"] = None
test_case_update_case["case_name"] = None
test_case_update_case["value"] = None

@pytest.mark.webApps
@pytest.mark.reports
@pytest.mark.data
@pytest.mark.exportCaseData
@pytest.mark.caseList
@pytest.mark.run(order=0)
def test_case_55_update_case(driver, settings):
    case = HomePage(driver, settings)
    case.web_apps_menu()
    webapps = WebAppsPage(driver)
    case_name = webapps.submit_case_change_register_form()
    value = webapps.submit_case_update_form(case_name)
    webapps.click_case_link()
    load = ReportPage(driver)
    case_id = load.verify_updated_data_in_case_list(case_name, value)
    test_case_update_case["case_id"] = case_id
    test_case_update_case["case_name"] = case_name
    test_case_update_case["value"] = value
    # return test_case_update_case


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
def test_case_27_powerbi_tableau_integration_case(driver, settings):
    username = settings["login_username"]
    password = settings["login_password"]
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    export.power_bi_tableau_integration_case(username, password)



@pytest.mark.data
@pytest.mark.powerBiTableauIntegrationForm
def test_case_28_powerbi_tableau_integration_form(driver, settings):
    username = settings["login_username"]
    password = settings["login_password"]
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    export.power_bi_tableau_integration_form(username, password)


@pytest.mark.data
@pytest.mark.deleteBulkExports
def test_exports_cleanup(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    export.delete_all_bulk_integration_exports()


@pytest.mark.webApps
@pytest.mark.reports
@pytest.mark.data
@pytest.mark.exportCaseData
@pytest.mark.caseList
@pytest.mark.run(order=-1)
def test_case_55_verify_change_in_export_data(driver, settings):
    if test_case_update_case["case_id"]==None:
        pytest.skip("Skipping this as the test case creation failed")
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    export_name = export.add_updated_case_exports()
    export.verify_export_has_updated_case_data(test_case_update_case["case_id"],
                                               test_case_update_case["case_name"],
                                               test_case_update_case["value"], export_name)
    home.data_menu()
    export.clean_up_case_data()
