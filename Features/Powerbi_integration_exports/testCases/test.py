import pytest

from Features.Powerbi_integration_exports.userInputs.user_inputs import UserData
from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.home.home_page import HomePage
from Features.Powerbi_integration_exports.testPages.data.power_bi_page import PowerBiPage

""""Contains test cases related to the Data module"""

values = dict()

@pytest.mark.lookup
def test_case_01_odata_feed_ui(driver,settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)

def test_case_02_odata_feed_select_type(driver,settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_feed_type()


def test_case_03_odata_feed_select_form(driver,settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_form()

def test_case_04_odata_feed_select_application(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_form()
    data.application_dropdown(UserData.reassign_cases_application)

def test_case_05_odata_feed_select_menu(driver, settings):
    home = (HomePage(driver, settings))
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_form()
    data.application_dropdown(UserData.reassign_cases_application)
    data.menu_dropdown()

def test_case_06_odata_feed_6_cancel_selection(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.cancel()

def test_case_07_save_and_delete_odata_feed_form(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()
    data.save_odata_feed()
    data.delete1()

def test_case_08_save_odata_feed_form(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()

def test_case_09__odata_feed_show_advance_question(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_form()
    data.form_feed(UserData.reassign_cases_application, UserData.reassign_menu, UserData.reassign_form)
    data.add_odata()
    data.show_advance_question()


def test_case_10_save_and_delete_odata_feed_case(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_case()
    data.case_feed(UserData.case)
    data.add_odata()
    data.save_odata_feed()
    data.delete1()



def test_case_11_save_and_copy_odata_feed(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()
    data.save_odata_feed()
    data.copy_edit_feed()


def test_case_12_add_description_to_odata_feed(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()
    data.add_description()


def test_case_13_bulk_create_bulk_delete_odata_feed(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.create_multiple_odata_feed(10)
    data.go_to_page()
    data.power_bi_tableau_integration_bulk_delete()

def test_case_14_delete_questions_on_odata_feed_page(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()
    data.delete_questions()

def test_case_15_deidentified_odata_feed(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()
    data.de_identified()

def test_case_16_view_created_odata_feed(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    username = settings["login_username"]
    password = settings["login_password"]
    data.power_bi_ui(1)
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()
    data.add_description()
    data.view_odata_feed(username, password)

def test_case_17_odata_feed_edit_filters(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_form()
    data.form_feed(UserData.Basic_tests_application,UserData.Basic_menu,UserData.Repeat_form)
    data.add_odata()
    data.repeat_checkbox2()
    data.save_odata_feed()
    data.edit_filters()


def test_case_18_odata_feed_include_parent(driver, settings):
    home = HomePage(driver, settings)
    data = PowerBiPage(driver)
    home.data_menu()
    data.power_bi_ui(1)
    data.select_case()
    data.case_feed(UserData.parent)
    data.add_odata()
    data.parent_checkbox1()
    data.save_odata_feed()