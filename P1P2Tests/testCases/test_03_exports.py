import pytest

from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.home.home_page import HomePage
from P1P2Tests.userInputs.user_inputs import UserData

""""Contains test cases related to the Exports module"""

@pytest.mark.data
@pytest.mark.exportsFormData
@pytest.mark.p1p2EscapeDefect
def test_case_21_form_exports(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    name = export.add_form_exports()
    export.form_exports(name)

@pytest.mark.data
@pytest.mark.exportsCaseData
@pytest.mark.p1p2EscapeDefect
def test_case_21_case_exports(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    name = export.add_case_exports()
    export.case_exports(name)


@pytest.mark.data
@pytest.mark.exportsFormData
@pytest.mark.p1p2EscapeDefect
def test_case_88_repeat_form_exports(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    export.add_repeat_form_exports(UserData.basic_test_app[0], UserData.basic_test_app[1], UserData.basic_test_app[2], UserData.repeat_form_export_name)



@pytest.mark.data
@pytest.mark.deleteBulkExports
def test_exports_cleanup(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    export = ExportDataPage(driver)
    export.delete_all_bulk_exports()


