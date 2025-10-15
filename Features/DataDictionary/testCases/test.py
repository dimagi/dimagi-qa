import time

import pytest

from Features.DataDictionary.userInputs.user_inputs import UserData
from HQSmokeTests.testPages.data.import_cases_page import ImportCasesPage
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.applications.application_page import ApplicationPage
from Features.DataDictionary.testPages.data.data_dictionary_page import DataDictionaryPage
from HQSmokeTests.testPages.messaging.messaging_page import MessagingPage
from HQSmokeTests.testPages.users.roles_permissions_page import RolesPermissionPage
from common_utilities.hq_login.login_page import LoginPage
from HQSmokeTests.testPages.users.web_user_page import WebUsersPage
from HQSmokeTests.testPages.users.org_structure_page import latest_download_file


""""Contains test cases related to the Data module"""

values = dict()

@pytest.mark.lookup
def test_case_01_data_dictionary_ui(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("Y")
    data.dropdown()

def test_case_02_edit(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.edit_case_property_description()

def test_case_03_case_property_addition(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.add_new_case_property()
    data.case_property_deletion()

def test_case_04_add_case_group(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.add_a_new_group()

def test_case_05_deprecate(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.deprecate_property()

def test_case_06_add_group_description(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.group_description()

def test_case_07_download_dd_file(driver, settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.download()

def test_case_08_upload_dd_file(driver, settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    download_path =latest_download_file()
    data.upload_dd(download_path)

def test_case_09_case_type_deprecate(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.case_type_deprecate()
    data.case_type_restore()

def test_case_10_deprecate_case_types_reports(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.case_type_deprecate()
    home.reports_menu()
    data.reports()
    home.data_menu()
    data.case_type_restore()

def test_case_11_deprecate_case_types_exports(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.case_type_deprecate()
    home.data_menu()
    data.exports()
    home.data_menu()
    data.case_type_restore()
    home.data_menu()
    data.exports()

def test_case_12_deprecate_case_types_exports_1(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.create_case_export()
    home.data_menu()
    data.data_page("N")
    data.case_type_deprecate()
    data.validate_exports()
    data.case_type_restore()
    home.data_menu()
    data.validate_exports()

def test_case_13_edit_data_deprecate_cases(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.case_type_deprecate()
    data.exports_edit_data_section(UserData.data_upload_path)
    data.case_type_restore()
    data.exports_edit_data_section(UserData.data_upload_path)

def test_case_14_messaging(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    menu = HomePage(driver, settings)
    home.data_menu()
    data.data_page("N")
    data.case_type_deprecate()
    menu.messaging_menu()
    data.messaging()
    home.data_menu()
    data.case_type_restore()
    menu.messaging_menu()
    data.messaging()


def test_case_15_date_valid_values(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("Y")
    data.valid_values_date()

def test_case_16_multiple_choice_valid_values(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("Y")
    data.valid_values_multiple_choice()

def test_case_17_download_valid_values(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.download()
    download_path = latest_download_file()
    data.excel_verification(download_path)

def test_case_18_download_upload_updated_file(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.download()
    download_path = latest_download_file()
    data.update_excel(download_path)
    data.upload_dd(download_path)

def test_case_19_invalid_valid_values(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("N")
    data.download()
    download_path = latest_download_file()
    data.update_excel_invalid(download_path)
    data.upload_dd(download_path)


def test_case_20_case_management(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("Y")
    data.add_property_description()
    home.applications_menu(UserData.application)
    data.case_management()
    data.app_summary()

def test_case_21_restore_case_property(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("Y")
    data.deprecate_case_property()
    home.applications_menu(UserData.application)
    data.case_management()
    data.warning_message()
    home.data_menu()
    data.data_page("N")
    data.restore_case_property()

def test_case_22_cle(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("Y")
    property_value = data.add_new_case_property()
    home.reports_menu()
    data.case_list_explorer(property_value,'yes')
    home.data_menu()
    data.data_page("Y")
    data.case_property_deletion()
    home.reports_menu()
    data.case_list_explorer(property_value,'no')

def test_case_23_roles_permission(driver,settings):
    login = LoginPage(driver, settings["url"])
    menu = HomePage(driver, settings)
    role = RolesPermissionPage(driver, settings)
    web_user1 = WebUsersPage(driver)
    data = DataDictionaryPage(driver)
    login.logout()
    login.login(settings["login_username"], settings["login_password"])
    menu.users_menu()
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    role_name1 = role.add_non_admin_role_dd(1)
    print (role_name1)
    menu.users_menu()
    web_user1.edit_user_permission(role_name1)
    login.logout()
    login.login(UserData.p1p2_user, settings["login_password"])
    data.data_dictionary_access_page()
    login.logout()
    login.login(settings["login_username"], settings["login_password"])
    menu.users_menu()
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    role_name1 = role.add_non_admin_role_dd(2)
    print(role_name1)
    time.sleep(2)
    menu.users_menu()
    web_user1.edit_user_permission(role_name1)
    login.logout()
    login.login(UserData.p1p2_user, settings["login_password"])
    data.data_dictionary_access_page()
    login.logout()
    login.login(settings["login_username"], settings["login_password"])
    menu.users_menu()
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    role_name1 = role.add_non_admin_role_dd(3)
    print(role_name1)
    menu.users_menu()
    web_user1.edit_user_permission(role_name1)
    login.logout()
    login.login(UserData.p1p2_user, settings["login_password"])
    data.data_dictionary_revoke_access()
    login.logout()
    time.sleep(2)
    login.login(settings["login_username"], settings["login_password"])
    menu.users_menu()
    web_user1.edit_user_permission("Admin")
    role.roles_menu_click()
    role.delete_test_roles()

def test_case_24_case_importer(driver,settings):
    home = HomePage(driver, settings)
    imp = ImportCasesPage(driver)
    home.data_menu()
    imp.replace_property_and_upload(UserData.case_type, UserData.file, "Yes", ['Hindi', 'Telugu','YYYY-MM-DD'],
                                    ['select_dd_language', 'opened_date'])


def test_case_25_make_new_version(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.data_page("Y")
    data.case_type_deprecate()
    home.applications_menu(UserData.application)
    data.application()
    data.case_data_page()
    home.data_menu()
    data.data_page("N")
    data.case_type_restore()











