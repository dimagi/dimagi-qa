import pytest
from HQSmokeTests.testPages.home.home_page import HomePage
from Features.Lookuptable.testPages.data.lookup_table_page import LookUpTablePage
from Features.Lookuptable.userInputs.user_inputs import UserData

""""Contains test cases related to the Data module"""

values = dict()

@pytest.mark.lookup
def test_01_upload(driver,settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.upload_1(UserData.data_upload_path,'1')

@pytest.mark.lookup
def test_02_error_upload1(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id']=data.create_download_lookuptable()
    download_path = data.latest_download_file()
    data.update_excel_user_value(values['table_id'],download_path)
    data.err_upload(download_path)
    data.invalid_data_assert()

@pytest.mark.lookup
def test_03_error_upload2(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id']=data.create_download_lookuptable()
    download_path = data.latest_download_file()
    data.update_excel_group_value(values['table_id'],download_path)
    data.err_upload(download_path)
    data.invalid_data_assert()

@pytest.mark.lookup
def test_04_Error_upload3(driver,settings):
    data = LookUpTablePage(driver)
    data.err_upload(UserData.malformed_document_upload_path)
    data.missing_data_assert()










