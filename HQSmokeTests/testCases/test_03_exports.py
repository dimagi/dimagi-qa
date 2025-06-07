import pytest

from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.home.home_page import HomePage

""""Contains test cases related to the Exports module"""


@pytest.mark.data
@pytest.mark.exportsFormData
def test_case_21_form_exports(driver, settings):
    """
        1. Navigate to Data section
        2. Verify you are able to Export forms from "Export Form data".
        3. Leave the form or case export open to reference IDs in a future test case
    """
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    name = export.add_form_exports()
    export.form_exports(name)


@pytest.mark.data
@pytest.mark.exportsCaseData
def test_case_21_case_exports(driver, settings):
    """
        1. Navigate to Data section
        2. Verify you are able to Export cases from "Export Case Data".
        3. Leave the form or case export open to reference IDs in a future test case
    """
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    name = export.add_case_exports()
    export.case_exports(name)


@pytest.mark.data
@pytest.mark.deleteBulkExports
def test_exports_cleanup(driver, settings):
    """
        1. Go to Export Form Data and bulk delete all exports.
        2. Go to Export Case Data and bulk delete all exports.
        3. Go to Daily Saved reports and bulk delete all exports.
    """
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    export.delete_all_bulk_exports()
