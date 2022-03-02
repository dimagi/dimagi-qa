from HQSmokeTests.testPages.base.login_page import LoginPage
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.userInputs.user_inputs import UserData


def test_case_01_menu_visibility(driver):

    visible = HomePage(driver)
    visible.reports_menu()
    visible.dashboard_menu()
    visible.data_menu()
    visible.users_menu()
    visible.applications_menu()
    visible.messaging_menu()
    visible.web_apps_menu()


def test_case_53_rage_clicks(driver):

    visible = HomePage(driver)
    visible.rage_clicks()


def test_case_two_factor_auth(driver, settings):

    login = LoginPage(driver, settings["url"])
    login.two_factor_auth(UserData.two_fa_user, settings["login_password"], settings["auth_key"])
