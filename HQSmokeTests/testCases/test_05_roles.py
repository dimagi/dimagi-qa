import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.users.roles_permissions_page import RolesPermissionPage
from HQSmokeTests.testPages.users.webapps_permission_page import WebAppPermissionPage

""""Contains test cases related to the User's Roles and Permissions module"""


@pytest.mark.user
@pytest.mark.groups
@pytest.mark.rolesPermission
def test_case_06_add_role(driver, settings):
    menu = HomePage(driver, settings)
    menu.users_menu()
    role = RolesPermissionPage(driver)
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    role = RolesPermissionPage(driver)
    role.add_role()
    print("New Role Added")


@pytest.mark.user
@pytest.mark.groups
@pytest.mark.rolesPermission
def test_case_06_edit_role(driver, settings):
    menu = HomePage(driver, settings)
    menu.users_menu()
    role = RolesPermissionPage(driver)
    role.roles_menu_click()
    role = RolesPermissionPage(driver)
    role.edit_role()
    print("Role Edited Successfully")


@pytest.mark.user
@pytest.mark.webUsers
@pytest.mark.rolesPermission
def test_case_12_toggle_option_webapp_permission(driver, settings):
    menu = HomePage(driver, settings)
    menu.users_menu()
    role = RolesPermissionPage(driver)
    role.roles_menu_click()
    web = WebAppPermissionPage(driver)
    web.webapp_permission_option_toggle()


@pytest.mark.user
@pytest.mark.role
def test_cleanup_items_in_role_menu(driver, settings):
    menu = HomePage(driver, settings)
    menu.users_menu()
    clean3 = RolesPermissionPage(driver)
    clean3.roles_menu_click()
    clean3.delete_test_roles()
    print("Deleted the role")
