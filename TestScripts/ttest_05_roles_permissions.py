from Pages.homePage import HomePage
from Pages.rolesPermissionsPage import RolesPermissionPage
from TestBase.environmentSetupPage import EnvironmentSetup


class RolesPermissionsTests(EnvironmentSetup):

    def test_01_open_roles_permissions_page(self):
        driver = self.driver
        menu = HomePage(driver)
        visible = RolesPermissionPage(driver)
        menu.users_menu()
        visible.roles_menu_click()
        print("Opened Roles and Permissions Page")

    def test_02_add_role(self):
        driver = self.driver
        role = RolesPermissionPage(driver)
        role.add_role()
        print("New Role Added")

    def test_03_edit_role(self):
        driver = self.driver
        role = RolesPermissionPage(driver)
        role.edit_role()
        print("Role Edited Successfully")

    def test_04_cleanup_role(self):
        driver = self.driver
        clean = RolesPermissionPage(driver)
        clean.roles_menu_click()
        clean.cleanup_role()
        print("Deleted the role")
