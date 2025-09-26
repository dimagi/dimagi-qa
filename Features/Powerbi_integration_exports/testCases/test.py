import pytest

from Features.Powerbi_integration_exports.userInputs.user_inputs import UserData
from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from HQSmokeTests.testPages.home.home_page import HomePage
from Features.Powerbi_integration_exports.testPages.data.power_bi_page import PowerBiPage

""""Contains test cases related to the Data module"""

values = dict()

@pytest.mark.lookup
def test_01_Odata_Feed_1(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()

def test_02_Odata_Feed_2(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_feed_type()


def test_03_Odata_Feed_3(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_form()

def test_04_Odata_Feed_4(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_form()
    data.application_dropdown(UserData.reassign_cases_application)

def test_05_Odata_Feed_5(driver, settings):
    home = (HomePage(driver, settings))
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_form()
    data.application_dropdown(UserData.reassign_cases_application)
    data.menu_dropdown()

def test_06_Odata_Feed_6(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.cancel()

def test_07_Odata_Feed_07(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()
    data.save_odata_feed()
    data.delete1()

def test_08_Odata_Feed_08(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()

def test_09_Odata_Feed_09(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_form()
    data.form_feed(UserData.reassign_cases_application, UserData.reassign_menu, UserData.reassign_form)
    data.add_odata()
    data.show_advance_question()


def test_10_Odata_Feed_10(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_case()
    data.case_feed(UserData.case)
    data.add_odata()
    data.save_odata_feed()
    data.delete1()



def test_11_Odata_Feed_11(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()
    data.save_odata_feed()
    data.copy_edit_feed()


def test_12_Odata_Feed_12(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()
    data.odata_20()


def test_13_Odata_Feed_13(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.create_multiple_odatafeed(10)
    data.go_to_page()
    data.power_bi_tableau_integration_bulk_delete()

def test_14_Odata_Feed_14(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()
    data.delete_questions()

def test_15_Odata_Feed_15(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()
    data.de_identified()

def test_16_Odata_Feed_16(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    username = settings["login_username"]
    password = settings["login_password"]
    data.ui()
    data.select_form()
    data.form_feed(UserData.reassign_cases_application,UserData.reassign_menu,UserData.reassign_form)
    data.add_odata()
    data.odata_20()
    data.view_odata_feed(username, password)

def test_17_Odata_Feed_17(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_form()
    data.form_feed(UserData.Basic_tests_application,UserData.Basic_menu,UserData.Repeat_form)
    data.add_odata()
    data.repeat_checkbox2()
    data.save_odata_feed()
    data.edit_filters()


def test_18_Odata_Feed_18(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = PowerBiPage(driver)
    data.ui()
    data.select_case()
    data.case_feed(UserData.parent)
    data.add_odata()
    data.parent_checkbox1()
    data.save_odata_feed()