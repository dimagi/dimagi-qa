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


@pytest.mark.user
@pytest.mark.groups
@pytest.mark.rolesPermission
def test_case_06_add_role(driver, settings):
    menu = HomePage(driver, settings)
    menu.users_menu()
    role = RolesPermissionPage(driver, settings)
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    role.add_role()
    print("New Role Added")


@pytest.mark.user
@pytest.mark.groups
@pytest.mark.rolesPermission
def test_case_06_edit_role(driver, settings):
    menu = HomePage(driver, settings)
    menu.users_menu()
    role = RolesPermissionPage(driver, settings)
    role.roles_menu_click()
    role.edit_role()
    print("Role Edited Successfully")

# commenting this out as the functionality changed
# @pytest.mark.user
# @pytest.mark.webUsers
# @pytest.mark.rolesPermission
# def test_case_12_toggle_option_webapp_permission(driver, settings):
#     menu = HomePage(driver, settings)
#     menu.users_menu()
#     role = RolesPermissionPage(driver, settings)
#     role.roles_menu_click()
#     web = WebAppPermissionPage(driver)
#     web.webapp_permission_option_toggle()


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
