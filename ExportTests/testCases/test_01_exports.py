import pytest

from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.home.home_page import HomePage

""""Contains test cases related to the Exports module"""


@pytest.mark.data
@pytest.mark.exportsFormData
def test_case_21_form_exports(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    name = export.add_form_exports()
    export.form_exports(name)


@pytest.mark.data
@pytest.mark.exportsCaseData
def test_case_21_case_exports(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    name = export.add_case_exports()
    export.case_exports(name)


@pytest.mark.data
@pytest.mark.exportsSMSMessages
def test_case_22_sms_exports(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    export.sms_exports()


@pytest.mark.data
@pytest.mark.exportsCaseData
@pytest.mark.exportsFormData
@pytest.mark.dailySavedExports
def test_case_24_daily_saved_exports(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    export.cleanup_existing_dse()
    export.daily_saved_exports_form()
    export.daily_saved_exports_case()


@pytest.mark.data
@pytest.mark.deleteBulkExports
def test_exports_cleanup(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    export.delete_all_bulk_exports()
