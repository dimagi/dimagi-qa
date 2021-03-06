from Pages.homePage import HomePage
from Pages.webappsPermissionPage import WebAppPermissionPage
from TestBase.environmentSetupPage import EnvironmentSetup


class WebAppPermissionsTests(EnvironmentSetup):

    def test_01_toggle_option_webapp_permission(self):
        driver = self.driver
        menu = HomePage(driver)
        web = WebAppPermissionPage(driver)
        menu.users_menu()
        web.webapp_permission_option_toggle()