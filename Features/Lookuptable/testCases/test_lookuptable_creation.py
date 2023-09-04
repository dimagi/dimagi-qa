import pytest

from HQSmokeTests.testPages.applications.app_preview import AppPreviewPage
from HQSmokeTests.testPages.home.home_page import HomePage
from Features.Lookuptable.userInputs.user_inputs import UserData
from Features.Lookuptable.testPages.data.lookup_table_page import LookUpTablePage

""""Contains test cases related to the Data module"""

values = dict()

@pytest.mark.data
@pytest.mark.managetables
def test_19_create_lookup_table(driver,settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.create_lookup_table()

@pytest.mark.data
@pytest.mark.viewtables
def test_28_view_lookup_table(driver,settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    values['table_id'] = data.create_lookup_table()
    data.view_lookup_table(values['table_id'])
    data.delete_lookup_table()


@pytest.mark.data
@pytest.mark.managetables
def test_36_select_deselect(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    data.selects_deselects()

@pytest.mark.data
@pytest.mark.managetables
def test_37_edit_table(driver,settings):
    data = LookUpTablePage(driver)
    home = HomePage(driver, settings)
    home.data_menu()
    data.edit_table()

@pytest.mark.data
@pytest.mark.managetables
def test_38_create_dummy_id(driver,settings):
        data = LookUpTablePage(driver)
        home = HomePage(driver, settings)
        home.data_menu()
        data.create_dummyid()

@pytest.mark.data
@pytest.mark.managetables
def test_39_edit_dummy_data(driver,settings):
        data = LookUpTablePage(driver)
        home = HomePage(driver, settings)
        home.data_menu()
        data.edit_dummy_data()

@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.lookupexcel
def test_21_Error_upload3(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    download_path = data.latest_download_file()
    data.write_data_excel(values['table_id'], download_path)
    data.upload_1(download_path, '1')


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.lookupexcel
def test_20_creation2(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    download_path = data.latest_download_file()
    data.download_update_8(download_path,values['table_id'])
    data.replace_existing_table(download_path)
    data.create_new_form()
    data.Navigation_to_a_caselist( values['table_id'])
    data.formbuilder_5()
    AppPreview = AppPreviewPage(driver)
    AppPreview.check_access_to_app_preview()
    data.submit_form_on_registration("en","kiran")
    driver.switch_to.default_content()
    data.delete_caselist()



@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.lookupexcel
def test_40_Multiple_groups(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    download_path = data.latest_download_file()
    data.multiple_groups(download_path,values['table_id'])
    data.view_lookup_table(values['table_id'])


@pytest.mark.data
@pytest.mark.managetables
@pytest.mark.lookupexcel
def test_41_User_restore(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.create_download_lookuptable()
    download_path = data.latest_download_file()
    data.multiple_groups(download_path,values['table_id'])
    driver.get(UserData.restore_url)
    data.restore_attribute_1()


@pytest.mark.data
@pytest.mark.managetables
def test_42_delete_test_tables(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = LookUpTablePage(driver)
    values['table_id'] = data.download_bulk_tables()
    download_path = data.latest_download_file()
    data.compare_and_delete(download_path)


