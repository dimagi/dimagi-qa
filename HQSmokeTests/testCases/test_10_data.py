import pytest

from HQSmokeTests.testPages.dataPage import DataPage
from HQSmokeTests.testPages.exportDataPage import ExportDataPage


@pytest.mark.order(1)
def test_TC_31_auto_case_update(driver):

    export = ExportDataPage(driver)
    data = DataPage(driver)
    export.data_tab()
    data.open_auto_case_update_page()
    data.add_new_rule()
    data.remove_rule()


@pytest.mark.order(2)
def test_TC_32_create_lookup_table(driver):

    data = DataPage(driver)
    export = ExportDataPage(driver)
    export.data_tab()
    data.create_lookup_table()


@pytest.mark.order(3)
def test_TC_33_view_lookup_table(driver):

    data = DataPage(driver)
    export = ExportDataPage(driver)
    export.data_tab()
    data.view_lookup_table()
    data.delete_lookup_table()
