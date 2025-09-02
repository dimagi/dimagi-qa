import time

import pytest

from Features.DataDictionary.userInputs.user_inputs import UserData
from HQSmokeTests.testPages.data.import_cases_page import ImportCasesPage
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.applications.application_page import ApplicationPage
from Features.DataDictionary.testPages.data.data_dictionary_page import DataDictionaryPage
from HQSmokeTests.testPages.messaging.messaging_page import MessagingPage
from HQSmokeTests.testPages.users.org_structure_page import latest_download_file
from HQSmokeTests.testPages.users.roles_permissions_page import RolesPermissionPage
from common_utilities.hq_login.login_page import LoginPage
from HQSmokeTests.testPages.users.web_user_page import WebUsersPage


""""Contains test cases related to the Data module"""

values = dict()

@pytest.mark.lookup
def test_ui(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.dropdown()

def test_edit(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.edit_case_property_description()

def test_case_property_adding(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.add_new_case_property()
    data.delete_case_property1()

def test_add_case_group(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.add_a_new_group()

def test_deprecate(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.deprecate_property()

def test_add_group_description(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.group_description()

def test_download(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.download()

def test_upload(driver, settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    download_path = data.latest_download_file()
    data.upload_dd(download_path)

def test_case_type_deprecate(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.deprecate_case_type1()
    data.restore_case_type1()

def test_make_new_version(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.deprecate_case_type1()
    home.applications_menu(UserData.application)
    data.application()
    data.case_data_page()
    home.data_menu()
    data.data_page()
    data.restore_case_type1()

def test_deprecate_case_types_reports(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.deprecate_case_type1()
    home.reports_menu()
    data.reports()
    home.data_menu()
    data.restore_case_type1()

def test_deprecate_case_types_exports(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.deprecate_case_type1()
    home.data_menu()
    data.exports()
    home.data_menu()
    data.restore_case_type1()
    home.data_menu()
    data.exports()

def test_deprecate_case_types_exports_1(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.create_case_export()
    home.data_menu()
    data.ui()
    data.deprecate_case_type1()
    data.validate_exports()
    data.restore_case_type1()
    home.data_menu()
    data.validate_exports()

def test_edit_data_deprecate_cases(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.deprecate_case_type1()
    data.exports_edit_data_section(UserData.data_upload_path)
    home.data_menu()
    data.restore_case_type1()
    data.exports_edit_data_section(UserData.data_upload_path)

def test_messaging(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.deprecate_case_type1()
    menu = HomePage(driver, settings)
    msg = MessagingPage(driver)
    menu.messaging_menu()
    data.messaging()
    home.data_menu()
    data.restore_case_type1()
    menu.messaging_menu()
    data.messaging()


def test_vv2(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.dropdown()
    data.valid_values_2()

def test_vv3(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.dropdown()
    data.valid_values_3()

def test_vv5(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.download()
    download_path = latest_download_file()
    data.excel_verification(download_path)

def test_vv6(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.download()
    download_path = latest_download_file()
    data.update_excel(download_path)
    data.upload_dd(download_path)

def test_vv7(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.download()
    download_path = latest_download_file()
    data.update_excel_invalid(download_path)
    data.upload_dd(download_path)


def test_case_management(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.add_property_description()
    home.applications_menu(UserData.application)
    data.case_management()
    data.app_summary()

def test_restore_case_property(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    data.deprecate_case_property()
    home.applications_menu(UserData.application)
    data.case_management()
    data.warning_message()
    home.data_menu()
    data.ui()
    data.restore_case_property()

def test_cle(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    data = DataDictionaryPage(driver)
    data.ui()
    property_value = data.add_new_case_property()
    home.reports_menu()
    data.case_list_explorer1(property_value,'yes')
    home.data_menu()
    data.ui()
    data.delete_case_property1()
    home.reports_menu()
    data.case_list_explorer1(property_value,'no')

def test_roles_permission(driver,settings):
    login = LoginPage(driver, settings["url"])
    login.logout()
    login.login(settings["login_username"], settings["login_password"])
    menu = HomePage(driver, settings)
    menu.users_menu()
    role = RolesPermissionPage(driver, settings)
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    role_name1 = role.add_non_admin_role_dd(1)
    print (role_name1)
    web_user1 = WebUsersPage(driver)
    menu.users_menu()
    web_user1.edit_user_permission(role_name1)
    login.logout()
    login.login(UserData.p1p2_user, settings["login_password"])
    data = DataDictionaryPage(driver)
    data.data_dictionary_access_page()
    login.logout()
    login.login(settings["login_username"], settings["login_password"])
    menu = HomePage(driver, settings)
    menu.users_menu()
    role = RolesPermissionPage(driver, settings)
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    role_name1 = role.add_non_admin_role_dd(2)
    print(role_name1)
    web_user1 = WebUsersPage(driver)
    time.sleep(2)
    menu.users_menu()
    web_user1.edit_user_permission(role_name1)
    login.logout()
    login.login(UserData.p1p2_user, settings["login_password"])
    data = DataDictionaryPage(driver)
    data.data_dictionary_access_page()
    login = LoginPage(driver, settings["url"])
    login.logout()
    login.login(settings["login_username"], settings["login_password"])
    menu = HomePage(driver, settings)
    menu.users_menu()
    role = RolesPermissionPage(driver, settings)
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    role_name1 = role.add_non_admin_role_dd(3)
    print(role_name1)
    web_user1 = WebUsersPage(driver)
    menu.users_menu()
    web_user1.edit_user_permission(role_name1)
    login.logout()
    login.login(UserData.p1p2_user, settings["login_password"])
    data = DataDictionaryPage(driver)
    data.data_dictionary_revoke_access()
    login.logout()
    time.sleep(2)
    login.login(settings["login_username"], settings["login_password"])
    menu.users_menu()
    web_user1.edit_user_permission("Admin")
    role.roles_menu_click()
    role.delete_test_roles()

def test_case_importer(driver,settings):
    home = HomePage(driver, settings)
    home.data_menu()
    imp = ImportCasesPage(driver)
    imp.replace_property_and_upload(UserData.case_type, UserData.file, "YES", ['Hindi', 'Telugu','YYYY-MM-DD'],
                                    ['select_dd_language', 'opened_date'])













