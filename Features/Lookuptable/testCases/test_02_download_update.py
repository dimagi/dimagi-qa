import pytest
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.users.org_structure_page import latest_download_file
from common_utilities.Excel.excel_manage import ExcelManager
from Features.Lookuptable.testPages.data.lookup_table_page import LookUpTablePage
from Features.Lookuptable.userInputs.user_inputs import UserData

""""Contains test cases related to the lookup table download and updates"""



@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_05_download1(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    value = data.create_download_lookuptable()
    home.data_menu()
    data.delete_lookup_table(value)


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_06_download_upload2(driver, settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_2(UserData.hypertension_upload_path, "1")
    data.download1_specific_table()


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_07_download_update_3(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    value = data.create_download_lookuptable()
    download_path = latest_download_file()
    data.upload_1_update_excel(download_path)
    home.data_menu()
    data.delete_lookup_table(value)


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_08_download_update_4(driver, settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    value = data.create_download_lookuptable()
    download_path = latest_download_file()
    data.delete_excel_sheet(download_path)
    home.data_menu()
    data.verify_missing_data_alert(download_path)
    home.data_menu()
    data.delete_lookup_table(value)


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_09_download_update_5(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    value = data.create_download_lookuptable()
    download_path = latest_download_file()
    home.data_menu()
    data.update_delete_field(download_path, value)
    home.data_menu()
    data.delete_lookup_table(value)


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_11_download_update_7(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    value = data.create_download_lookuptable()
    download_path = latest_download_file()
    home.data_menu()
    d1, d2 = data.download_update_7(value, download_path)
    data.compare_excel(d1, d2, 0)
    home.data_menu()
    data.delete_lookup_table(value)


# user1 is displayed twice
@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_12_download_update_8(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    value = data.create_download_lookuptable()
    download_path = latest_download_file()
    home.data_menu()
    d1, d2 = data.download_update_8(download_path, value)
    data.compare_excel(d1, d2, 1)
    home.data_menu()
    data.delete_lookup_table(value)

@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_13_download_update_9(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    value = data.create_download_lookuptable()
    download_path = latest_download_file()
    home.data_menu()
    data.test_13(download_path, value)
    home.data_menu()
    data.delete_lookup_table(value)


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_14_download_update_10(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    value = data.create_download_lookuptable()
    download_path = latest_download_file()
    home.data_menu()
    data.delete_row_from_table(download_path, value)
    home.data_menu()
    data.delete_lookup_table(value)


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_15_download_update_11(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    value = data.create_download_lookuptable()
    download_path = latest_download_file()
    home.data_menu()
    data.test_15(download_path, value)
    home.data_menu()
    data.delete_lookup_table(value)


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_16_Attributes_1(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    value = data.create_download_lookup_table_without_field()
    download_path = latest_download_file()
    print("path is ", download_path)
    home.data_menu()
    data.attribute_2(download_path, value)
    data.restore_attribute_default(settings["url"]+UserData.url+settings['login_username'])
    home.data_menu()
    data.delete_lookup_table(value)


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_17_Attributes_2(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    value = data.create_download_lookup_table_without_field()
    download_path = latest_download_file()
    print("path is ", download_path)
    home.data_menu()
    data.attribute_2(download_path, value)
    home.data_menu()
    data.delete_lookup_table(value)


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_case_18_Attributes_3(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    value = data.create_download_lookup_table_without_field()
    download_path = latest_download_file()
    print("path is ", download_path)
    home.data_menu()
    data.attribute_2(download_path, value)
    home.data_menu()
    data.delete_field_columns(download_path, value)
    home.data_menu()
    data.delete_lookup_table(value)


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.excel
def test_24_bulkupload_1(driver, settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    tableid1 = data.create_lookup_table()
    tableid2 = data.create_new_lookuptable()
    tablenames = tableid1 + ":" + tableid2
    print("tables", tablenames)
    data.select_multiple_tables_download(tablenames, 2)
    download_path = latest_download_file()
    home.data_menu()
    data.bulkupload_1(tablenames, 2, download_path)
    home.data_menu()
    data.delete_lookup_table(tableid1)
    home.data_menu()
    data.delete_lookup_table(tableid2)


@pytest.mark.lookup
@pytest.mark.bulkUpload
def test_25_bulkupload_2(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    value = data.create_download_lookuptable()
    download_path = latest_download_file()
    home.data_menu()
    data.bulk_upload_verification(download_path, value)
