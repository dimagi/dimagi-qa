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
@pytest.mark.deleteBulkExports
def test_exports_cleanup(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    export.delete_all_bulk_exports()
