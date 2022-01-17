from HQSmokeTests.testPages.data.data_page import DataPage
from HQSmokeTests.testPages.data.export_data_page import ExportDataPage


def test_TC_21_form_exports(driver):
    export = ExportDataPage(driver)
    export.data_tab()
    export.add_form_exports()
    export.form_exports()
    export.validate_downloaded_form_exports()


def test_TC_21_case_exports(driver):
    export = ExportDataPage(driver)
    export.add_case_exports()
    export.case_exports()
    export.validate_downloaded_case_exports()


def test_TC_22_sms_exports(driver):
    export = ExportDataPage(driver)
    export.sms_exports()


def test_TC_24_daily_saved_exports(driver):
    export = ExportDataPage(driver)
    export.daily_saved_exports_form()
    export.deletion()
    export.delete_bulk_exports()
    export.daily_saved_exports_case()
    export.deletion()


def test_TC_25_excel_dashboard_integration_form(driver):
    export = ExportDataPage(driver)
    export.excel_dashboard_integration_form()


def test_TC_26_excel_dashboard_integration_case(driver):
    export = ExportDataPage(driver)
    export.excel_dashboard_integration_case()


def test_TC_28_powerBI_tableau_integration_case(driver, settings):
    username = settings["login_username"]
    password = settings["login_password"]
    export = ExportDataPage(driver)
    export.power_bi_tableau_integration_case(username, password)


def test_TC_29_powerBI_tableau_integration_form(driver, settings):
    username = settings["login_username"]
    password = settings["login_password"]
    export = ExportDataPage(driver)
    export.power_bi_tableau_integration_form(username, password)
    export.delete_all_bulk_exports()


def test_TC_31_manage_forms(driver):
    export = ExportDataPage(driver)
    driver.refresh()
    export.manage_forms()


def test_TC_32_auto_case_update(driver):

    data = DataPage(driver)
    data.open_auto_case_update_page()
    data.add_new_rule()
    data.remove_rule()


def test_TC_33_create_lookup_table(driver):

    data = DataPage(driver)
    data.create_lookup_table()


def test_TC_34_view_lookup_table(driver):

    data = DataPage(driver)
    data.view_lookup_table()
    data.delete_lookup_table()
