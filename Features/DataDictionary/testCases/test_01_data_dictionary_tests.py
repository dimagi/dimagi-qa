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

# values = dict()
@pytest.mark.datadictionary
def test_case_01_verify_data_dictionary_ui(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("Y")
    data.verify_dropdown_values()

@pytest.mark.datadictionary
def test_case_02_add_update_delete_case_property(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("N")
    data.add_new_case_property()
    data.update_case_property_description()
    data.delete_added_case_property()

@pytest.mark.datadictionary
def test_case_03_verify_deprecate_property(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("Y")
    data.verify_deprecate_restore_case_property("Y")

@pytest.mark.datadictionary
def test_case_04_verify_adding_group_description(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("N")
    data.updating_group_description()

@pytest.mark.datadictionary
def test_case_05_verify_downloading_dd_file(driver, settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("N")
    data.verify_file_getting_downloaded()

@pytest.mark.datadictionary
def test_case_06_verify_uploading_dd_file(driver, settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("N")
    download_path =latest_download_file()
    data.verify_uploading_dd(download_path)

@pytest.mark.datadictionary
def test_case_07_validate_deprecate_case_type(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("N")
    data.case_type_deprecate()
    data.case_type_restore()

@pytest.mark.datadictionary
def test_case_08_validate_deprecate_case_types_reports(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("N")
    data.case_type_deprecate()
    home.reports_menu()
    data.verify_reports()
    home.data_menu()
    data.case_type_restore()

@pytest.mark.datadictionary
def test_case_09_validate_deprecate_restore_data_exports(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("N")
    data.case_type_deprecate()
    home.data_menu()
    data.verify_exports()
    home.data_menu()
    data.case_type_restore()
    home.data_menu()
    data.verify_exports()

@pytest.mark.datadictionary
def test_case_10_validate_deprecate_restore_case_exports(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.create_case_export()
    home.data_menu()
    data.verify_data_page("N")
    data.case_type_deprecate()
    data.validate_exports()
    data.case_type_restore()
    home.data_menu()
    data.validate_exports()

@pytest.mark.datadictionary
def test_case_11_validate_case_type_deprecate_restore_on_data_exports(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("N")
    data.case_type_deprecate()
    data.validate_exports_edit_data_section(UserData.data_upload_path)
    data.case_type_restore()
    data.validate_exports_edit_data_section(UserData.data_upload_path)

@pytest.mark.datadictionary
def test_case_12_verify_deprecate_cases_under_messaging_menu(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    menu = HomePage(driver, settings)
    home.data_menu()
    data.verify_data_page("N")
    data.case_type_deprecate()
    menu.messaging_menu()
    data.verify_conditional_alert_under_messaging()
    home.data_menu()
    data.case_type_restore()
    menu.messaging_menu()
    data.verify_conditional_alert_under_messaging()

@pytest.mark.datadictionary
def test_case_13_validate_date_type_valid_values(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("Y")
    data.verify_valid_values_date_type()

@pytest.mark.datadictionary
def test_case_14_validate_multiple_choice_type_valid_values(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("Y")
    data.verify_valid_values_multiple_choice_type()

@pytest.mark.datadictionary
def test_case_15_validate_downloaded_valid_values(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("N")
    data.verify_file_getting_downloaded()
    download_path = latest_download_file()
    data.verify_excel_verification(download_path)

@pytest.mark.datadictionary
def test_case_16_verify_uploading_updated_file(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("N")
    data.verify_file_getting_downloaded()
    download_path = latest_download_file()
    data.verify_update_excel(download_path)
    data.verify_uploading_dd(download_path)

@pytest.mark.datadictionary
def test_case_17_validate_invalid_valid_values(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("Y")
    data.verify_file_getting_downloaded()
    download_path = latest_download_file()
    data.verify_updating_excel_invalid_values(download_path)
    data.verify_uploading_dd(download_path)
    data.verify_data_page("Y")
    data.verify_updating_excel_valid_values(download_path)
    data.verify_uploading_dd(download_path)

@pytest.mark.datadictionary
def test_case_18_verify_added_property_under_case_management_tab(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("Y")
    data.verify_add_property_description()
    home.applications_menu(UserData.application)
    data.verify_case_management()
    data.validating_app_summary()

@pytest.mark.datadictionary
def test_case_19_verify_restore_case_property(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("Y")
    data.verify_deprecate_restore_case_property("N")
    home.applications_menu(UserData.application)
    data.verify_case_management()
    data.verify_warning_message()
    home.data_menu()
    data.verify_data_page("N")
    data.verify_restore_case_property()

@pytest.mark.datadictionary
def test_case_20_verify_case_list_explorer_report(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("Y")
    property_value = data.add_new_case_property()
    home.reports_menu()
    data.view_case_list_explorer_report(property_value,'yes')
    home.data_menu()
    data.verify_data_page("Y")
    data.delete_added_case_property()
    home.reports_menu()
    data.view_case_list_explorer_report(property_value,'no')

@pytest.mark.datadictionary
def test_case_21_verify_roles_permission_with_dd_access(driver,settings):
    login = LoginPage(driver, settings["url"])
    menu = HomePage(driver, settings)
    role = RolesPermissionPage(driver, settings)
    web_user = WebUsersPage(driver)
    data = DataDictionaryPage(driver)
    login.logout()
    login.login(settings["login_username"], settings["login_password"])
    menu.users_menu()
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    role_name = role.add_non_admin_role_dd(1)
    print (role_name)
    menu.users_menu()
    web_user.edit_user_permission(role_name)
    login.logout()
    login.login(UserData.p1p2_user, settings["login_password"])
    data.verify_data_dictionary_access_page()
    login.logout()
    login.login(settings["login_username"], settings["login_password"])
    menu.users_menu()
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    role_name = role.add_non_admin_role_dd(2)
    print(role_name)
    time.sleep(2)
    menu.users_menu()
    web_user.edit_user_permission(role_name)
    login.logout()
    login.login(UserData.p1p2_user, settings["login_password"])
    data.verify_data_dictionary_access_page()
    login.logout()
    login.login(settings["login_username"], settings["login_password"])
    menu.users_menu()
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    role_name = role.add_non_admin_role_dd(3)
    print(role_name)
    menu.users_menu()
    web_user.edit_user_permission(role_name)
    login.logout()
    login.login(UserData.p1p2_user, settings["login_password"])
    data.verify_data_dictionary_revoke_access()
    login.logout()
    time.sleep(2)
    login.login(settings["login_username"], settings["login_password"])
    menu.users_menu()
    web_user.edit_user_permission("Admin")
    role.roles_menu_click()
    role.delete_test_roles()

@pytest.mark.datadictionary
def test_case_22_validate_case_importer_valid_values(driver,settings):
    home = HomePage(driver, settings)
    imp = ImportCasesPage(driver)
    home.data_menu()
    imp.replace_property_and_upload(UserData.case_type, UserData.file, "Yes", ['Hindi', 'Telugu','YYYY-MM-DD'],
                                    ['select_dd_language', 'opened_date'])

@pytest.mark.datadictionary
def test_case_23_verify_making_a_new_version_for_deprecated_case_type(driver,settings):
    home = HomePage(driver, settings)
    data = DataDictionaryPage(driver)
    home.data_menu()
    data.verify_data_page("Y")
    data.case_type_deprecate()
    home.applications_menu(UserData.application)
    data.validating_application()
    data.verify_case_data_page()












