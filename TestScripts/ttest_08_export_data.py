from Pages.exportDataPage import ExportDataPage
from TestBase.environmentSetupPage import EnvironmentSetup


class ExportTests(EnvironmentSetup):

    def test_01_form_exports(self):
        driver = self.driver
        export = ExportDataPage(driver)
        export.data_tab()
        export.add_form_exports()
        export.form_exports()
        export.validate_downloaded_form_exports()

    def test_02_case_exports(self):
        driver = self.driver
        export = ExportDataPage(driver)
        export.data_tab()
        export.add_case_exports()
        export.case_exports()
        export.validate_downloaded_case_exports()

    def test_03_sms_exports(self):
        driver = self.driver
        export = ExportDataPage(driver)
        export.data_tab()
        export.sms_exports()

    def test_04_daily_saved_exports(self):
        driver = self.driver
        export = ExportDataPage(driver)
        export.data_tab()
        export.daily_saved_exports_form()
        export.deletion()
        export.daily_saved_exports_case()
        export.deletion()

    def test_05_excel_dashboard_integration(self):
        driver = self.driver
        export = ExportDataPage(driver)
        export.data_tab()
        export.excel_dashboard_integration_form()
        export.deletion()
        export.excel_dashboard_integration_case()
        export.deletion()

    def test_06_powerBI_tableau_integration(self):
        driver = self.driver
        export = ExportDataPage(driver)
        export.data_tab()
        export.power_bi_tableau_integration_form()
        export.bi_tab_deletion()
        export.power_bi_tableau_integration_case()
        export.bi_tab_deletion()

    def test_07_manage_forms(self):
        driver = self.driver
        export = ExportDataPage(driver)
        self.driver.refresh()
        export.data_tab()
        export.manage_forms()
