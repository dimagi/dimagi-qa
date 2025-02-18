import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from common_utilities.hq_login.login_page import LoginPage
from HQSmokeTests.userInputs.user_inputs import UserData

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.dashboard
@pytest.mark.reports
@pytest.mark.data
@pytest.mark.users
@pytest.mark.applications
@pytest.mark.webApps
@pytest.mark.messaging
def test_case_01_menu_visibility(driver, settings):
    visible = HomePage(driver, settings)
    visible.reports_menu()
    visible.dashboard_menu()
    visible.data_menu()
    visible.users_menu()
    visible.applications_menu(UserData.reassign_cases_application)
    visible.messaging_menu()
    visible.web_apps_menu()


@pytest.mark.misc
def test_case_53_rage_clicks(driver, settings):
    visible = HomePage(driver, settings)
    visible.rage_clicks()


@pytest.mark.twoFactorAuth
def test_case_two_factor_auth(driver, settings):
    login = LoginPage(driver, settings["url"])
    login.logout()
    if "staging" in settings["url"]:
        login.login(UserData.two_fa_user, settings["login_password"], settings["staging_auth_key"])
    elif "india" in settings["url"]:
        login.login(UserData.two_fa_user, settings["login_password"], settings["india_auth_key"])
    else:
        login.login(UserData.two_fa_user, settings["login_password"], settings["prod_auth_key"])
