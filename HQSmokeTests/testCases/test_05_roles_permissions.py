import pytest

from HQSmokeTests.testPages.homePage import HomePage
from HQSmokeTests.testPages.rolesPermissionsPage import RolesPermissionPage


@pytest.mark.order(1)
def test_TC_05_add_role(driver):

    menu = HomePage(driver)
    menu.users_menu()
    role = RolesPermissionPage(driver)
    role.roles_menu_click()
    print("Opened Roles and Permissions Page")
    role = RolesPermissionPage(driver)
    role.add_role()
    print("New Role Added")


@pytest.mark.order(2)
def test_TC_05_edit_role(driver):

    role = RolesPermissionPage(driver)
    role.edit_role()
    print("Role Edited Successfully")


@pytest.mark.order(3)
def test_cleanup_role(driver):

    clean = RolesPermissionPage(driver)
    clean.roles_menu_click()
    clean.cleanup_role()
    print("Deleted the role")
