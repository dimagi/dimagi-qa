import pytest

from Features.Powerbi_integration_exports.userInputs.user_inputs import UserData
from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.home.home_page import HomePage
from Features.Powerbi_integration_exports.testPages.data.power_bi_page import PowerBiPage

""""Contains test cases related to the Data module"""

values = dict()

@pytest.mark.powerbi
def test_case_01_verify_odata_feed_ui(driver,settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')

@pytest.mark.powerbi
def test_case_02_verify_odata_feed_select_type(driver,settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_feed_type()

@pytest.mark.powerbi
def test_case_03_verify_odata_feed_select_form(driver,settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_form()

@pytest.mark.powerbi
def test_case_04_verify_odata_feed_select_application(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_form()
    data.application_dropdown(UserData.reassign_cases_application)

@pytest.mark.powerbi
def test_case_05_verify_odata_feed_select_menu(driver, settings):
    home = (HomePage(driver, settings))
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_form()
    data.application_dropdown(UserData.reassign_cases_application)
    data.menu_dropdown()

@pytest.mark.powerbi
def test_case_06_verify_odata_feed_cancel_selection(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.cancel_feed()

def test_case_07_verify_save_and_delete_odata_feed_form(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.adding_odata_feed()
    data.save_odata_feed()
    data.delete_feed()

@pytest.mark.powerbi
def test_case_08_verify_save_odata_feed_form(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.adding_odata_feed()

@pytest.mark.powerbi
def test_case_09_validate_odata_feed_show_advance_question(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_form()
    data.form_feed(UserData.reassign_cases_application, UserData.reassign_menu, UserData.reassign_form)
    data.adding_odata_feed()
    data.show_advance_question()

@pytest.mark.powerbi
def test_case_10_verify_save_and_delete_odata_feed_case(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_case()
    data.create_case_feed(UserData.case)
    data.adding_odata_feed()
    data.save_odata_feed()
    data.delete_feed()


@pytest.mark.powerbi
def test_case_11_verify_save_and_copy_odata_feed(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.adding_odata_feed()
    data.save_odata_feed()
    data.copy_edit_feed()

@pytest.mark.powerbi
def test_case_12_verify_add_description_to_odata_feed(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.adding_odata_feed()
    data.add_description()

@pytest.mark.powerbi
def test_case_13_verify_bulk_create_bulk_delete_odata_feed(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.create_multiple_odata_feed(10)
    data.validate_go_to_page()
    data.power_bi_tableau_integration_bulk_delete()

@pytest.mark.powerbi
def test_case_14_verify_delete_questions_on_odata_feed_page(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.adding_odata_feed()
    data.delete_questions()

@pytest.mark.powerbi
def test_case_15_verify_deidentified_odata_feed(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.adding_odata_feed()
    data.validate_de_identified()

@pytest.mark.powerbi
def test_case_16_verify_view_created_odata_feed(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    username = settings["login_username"]
    password = settings["login_password"]
    data.power_bi_page_ui('y')
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.adding_odata_feed()
    data.add_description()
    data.view_odata_feed(username, password)

@pytest.mark.powerbi
def test_case_17_verify_odata_feed_edit_filters(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_form()
    data.form_feed(UserData.Basic_tests_application,UserData.Basic_menu,UserData.Repeat_form)
    data.adding_odata_feed()
    data.verify_repeat_checkbox()
    data.save_odata_feed()
    data.edit_filters()

@pytest.mark.powerbi
def test_case_18_verify_odata_feed_include_parent(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_page_ui('y')
    data.select_case()
    data.create_case_feed(UserData.parent)
    data.adding_odata_feed()
    data.verify_parent_checkbox()
    data.save_odata_feed()