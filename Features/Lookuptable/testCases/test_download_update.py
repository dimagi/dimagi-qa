import time

import pytest
from HQSmokeTests.testPages.home.home_page import HomePage
from common_utilities.Excel.excel_manage import ExcelManager
from Features.Lookuptable.testPages.data.lookup_table_page import LookUpTablePage
from Features.Lookuptable.userInputs.user_inputs import UserData


""""Contains test cases related to the Data module"""

values = dict()

@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel

def test_05_download1(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    return values['table_id']


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_06_download_upload2(driver,settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_1(UserData.hypertension_upload_path, "1")
    data.download1_specificTable()

@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_07_download_update_3(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    download_path = data.latest_download_file()
    excel = ExcelManager(download_path)
    excel.write_data('types',UserData.type_data_list)
    excel.create_sheet(UserData.field_val)
    excel.write_data(UserData.field_val, UserData.type_sheet_headers)
    data.upload_1(download_path, str(excel.row_size('types')-1))

@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_08_download_update_4(driver,settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    values['table_id'] = data.create_download_lookuptable()
    excel = ExcelManager(driver)
    download_path = data.latest_download_file()
    excel = ExcelManager(download_path)
    excel.delete_sheet("types")
    data.err_upload(download_path)
    data.missing_data_assert()


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_09_download_update_5(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    download_path = data.latest_download_file()
    data.update_delete_field(download_path, values['table_id'])


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_11_download_update_7(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    download_path = data.latest_download_file()
    d1, d2 = data.download_update_7(values['table_id'], download_path)
    data.compare_excel(d1, d2, 0)


# user1 is displayed twice
@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_12_download_update_8(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    download_path = data.latest_download_file()
    d1, d2 = data.download_update_8(download_path, values['table_id'])
    data.compare_excel(d1, d2, 1)


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_13_download_update_9(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    download_path = data.latest_download_file()
    data.test_13(download_path,values['table_id'])


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_14_download_update_10(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    download_path = data.latest_download_file()
    excel = ExcelManager(download_path)
    data.delete_row_from_table(download_path, values['table_id'])


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_15_download_update_11(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    download_path = data.latest_download_file()
    data.test_15(download_path,values['table_id'])


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_16_Attributes_1(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    download_path = data.latest_download_file()
    print("path is ", download_path)
    values['table_id'] = data.create_download_lookup_table_without_field()
    excel = ExcelManager(download_path)
    data.attribute_2(download_path, values['table_id'])
    driver.get(UserData.url)
    data.restore_attribute_1()
@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_17_Attributes_2(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    download_path = data.latest_download_file()
    values['table_id'] = data.create_download_lookup_table_without_field()
    excel = ExcelManager(download_path)
    data.attribute_2(download_path, values['table_id'])


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_18_Attributes_3(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    download_path = data.latest_download_file()
    print("path is ", download_path)
    values['table_id'] = data.create_download_lookup_table_without_field()
    excel = ExcelManager(download_path)
    data.attribute_2(download_path, values['table_id'])
    data.delete_field_columns(download_path, values['table_id'])


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_24_bulkupload_1(driver,settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    tableid1 = data.create_lookup_table()
    tableid2 = data.create_new_lookuptable()
    tablenames = tableid1+":"+tableid2
    print("tables",tablenames)
    data.select_multipletables_download(tablenames, 2)
    download_path = data.latest_download_file()
    excel = ExcelManager(download_path)
    excel.write_data(tableid1, UserData.data_list1)
    excel.write_data(tableid2, UserData.data_list1)
    data.bulkupload_1(tablenames,2,download_path)

def test_25_bulkupload_2(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    download_path = data.latest_download_file()
    excel = ExcelManager(download_path)
    excel.write_data(values['table_id'], UserData.duplicate_values)
    data.err_upload(download_path)
    data.download1()
    data.view_lookup_table(values['table_id'])
    data.rowCount_table(values['table_id'])
    row_value = data.rowCount_table(values['table_id'])
    assert row_value == str((excel.row_size(values['table_id'])-1))



