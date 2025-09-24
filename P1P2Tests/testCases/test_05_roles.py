import time

import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.users.mobile_workers_page import MobileWorkerPage
from HQSmokeTests.testPages.users.roles_permissions_page import RolesPermissionPage
from HQSmokeTests.testPages.users.web_user_page import WebUsersPage
from HQSmokeTests.testPages.users.webapps_permission_page import WebAppPermissionPage
from HQSmokeTests.userInputs.user_inputs import UserData
from common_utilities.generate_random_string import fetch_random_string
from common_utilities.hq_login.login_page import LoginPage

""""Contains test cases related to the User's Roles and Permissions module"""

group_id = dict()
group_id['rolename'] = None

@pytest.mark.user
@pytest.mark.groups
@pytest.mark.rolesPermission
@pytest.mark.p1p2EscapeDefect
@pytest.mark.bulkUpload
@pytest.mark.bulkDelete
def test_case_73_non_admin_role_permission(driver, settings):
    login = LoginPage(driver, settings["url"])
    login.logout()
    time.sleep(2)
    login.login(settings["login_username"], settings["login_password"])
    menu = HomePage(driver, settings)
    menu.users_menu()
    role = RolesPermissionPage(driver, settings)
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    group_id['rolename'] = role.add_non_admin_role()
    webuser = WebUsersPage(driver)
    menu.users_menu()
    webuser.edit_user_permission(group_id['rolename'])
    login.logout()
    time.sleep(2)
    login.login(UserData.p1p2_user, settings["login_password"])
    load = ReportPage(driver)
    load.verify_only_permitted_report(UserData.report_for_p1p2)
    mobile = MobileWorkerPage(driver)
    mobile.bulk_upload_mobile_worker()
    mobile.delete_bulk_users()
    login.logout()
    time.sleep(2)
    login.login(settings["login_username"], settings["login_password"])
    menu.users_menu()
    webuser.edit_user_permission("Admin")

@pytest.mark.user
@pytest.mark.mobileWorker
@pytest.mark.groups
@pytest.mark.userImport
@pytest.mark.userExport
@pytest.mark.p1p2EscapeDefect
def test_case_74_delete_role_column(driver, settings, rerun_count):
    role = RolesPermissionPage(driver, settings)
    login = LoginPage(driver, settings["url"])
    login.logout()
    time.sleep(2)
    login.login(settings["login_username"], settings["login_password"])
    username = f"username_p1p2_{fetch_random_string()}{rerun_count}"
    user = MobileWorkerPage(driver)
    home = HomePage(driver, settings)
    home.users_menu()
    user.mobile_worker_menu()
    user.create_mobile_worker()
    user.mobile_worker_enter_username(username)
    user.mobile_worker_enter_password(fetch_random_string())
    user.click_create(username)
    user.mobile_worker_menu()
    user.select_mobile_worker_created(username)
    user.update_role_for_mobile_worker(group_id['rolename'])
    newest_file = user.download_mobile_worker()
    user.remove_role_in_downloaded_file(newest_file, username, group_id['rolename'])
    home.users_menu()
    user.upload_mobile_worker(newest_file)
    time.sleep(2)
    home.users_menu()
    user.mobile_worker_menu()
    user.select_mobile_worker_created(username)
    user.verify_role_for_mobile_worker(group_id['rolename'])
    user.mobile_worker_menu()
    user.select_mobile_worker_created(username)
    user.update_role_for_mobile_worker(UserData.default_mw_role)
    home.users_menu()
    user.delete_bulk_users()
    time.sleep(2)
    home.users_menu()
    role.roles_menu_click()
    role.delete_test_roles()


@pytest.mark.user
@pytest.mark.role
def test_cleanup_items_in_role_menu(driver, settings):
    menu = HomePage(driver, settings)
    menu.users_menu()
    webuser = WebUsersPage(driver)
    clean3 = RolesPermissionPage(driver, settings)
    clean3.roles_menu_click()
    webuser.edit_user_permission("Admin")
    menu.users_menu()
    clean3.roles_menu_click()
    clean3.delete_test_roles()
    print("Deleted the role")
