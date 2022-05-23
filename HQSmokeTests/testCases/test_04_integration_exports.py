from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.webapps.web_apps_page import WebAppsPage

import pytest

""""Contains test cases related to the Integrated Exports"""

test_case_update_case = dict()

@pytest.mark.run(order=0)
def test_case_55_update_case(driver):

    case = HomePage(driver)
    case.web_apps_menu()
    webapps = WebAppsPage(driver)
    case_name = webapps.submit_case_change_register_form()
    value = webapps.submit_case_update_form(case_name)
    webapps.click_case_link()
    load = ReportPage(driver)
    case_id = load.verify_updated_data_in_case_list(case_name,value)
    test_case_update_case["case_id"] = case_id
    test_case_update_case["case_name"] = case_name
    test_case_update_case["value"] = value
    return test_case_update_case


def test_case_25_excel_dashboard_integration_form(driver):
    export = ExportDataPage(driver)
    export.data_tab()
    export.excel_dashboard_integration_form()


def test_case_26_excel_dashboard_integration_case(driver):
    export = ExportDataPage(driver)
    export.data_tab()
    export.excel_dashboard_integration_case()


def test_case_27_powerbi_tableau_integration_case(driver, settings):
    username = settings["login_username"]
    password = settings["login_password"]
    export = ExportDataPage(driver)
    export.data_tab()
    export.power_bi_tableau_integration_case(username, password)


def test_case_28_powerbi_tableau_integration_form(driver, settings):
    username = settings["login_username"]
    password = settings["login_password"]
    export = ExportDataPage(driver)
    export.data_tab()
    export.power_bi_tableau_integration_form(username, password)


def test_exports_cleanup(driver):
    export = ExportDataPage(driver)
    export.data_tab()
    export.delete_all_bulk_integration_exports()


@pytest.mark.run(order=-1)
def test_case_55_verify_change_in_export_data(driver):

    export = ExportDataPage(driver)
    export.data_tab()
    export.add_updated_case_exports()
    export.verify_export_has_updated_case_data(test_case_update_case["case_id"],
                                               test_case_update_case["case_name"],
                                               test_case_update_case["value"])
    export.data_tab()
    export.clean_up_case_data()