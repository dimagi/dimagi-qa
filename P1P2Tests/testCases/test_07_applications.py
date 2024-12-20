import pytest

from HQSmokeTests.testPages.applications.app_preview import AppPreviewPage
from HQSmokeTests.testPages.applications.application_page import ApplicationPage
from HQSmokeTests.testPages.android.android_screen import AndroidScreen
from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.reports.report_page import ReportPage
from P1P2Tests.userInputs.user_inputs import UserData

""""Contains test cases related to the Application module"""

@pytest.mark.application
@pytest.mark.appSettings
@pytest.mark.p1p2EscapeDefect
def test_case_84_verify_form_settings(driver, settings):
    menu = HomePage(driver, settings)
    menu.applications_menu(UserData.reassign_cases_application)
    load = ApplicationPage(driver)
    load.verify_form_settings_page(UserData.form_name)
    load.verify_form_settings_page(UserData.followup_form_name)

@pytest.mark.application
@pytest.mark.appSettings
@pytest.mark.p1p2EscapeDefect
def test_case_85_verify_app_version_page(driver, settings):
    menu = HomePage(driver, settings)
    menu.applications_menu(UserData.reassign_cases_application)
    load = ApplicationPage(driver)
    load.verify_app_version_page()

@pytest.mark.application
@pytest.mark.appSettings
@pytest.mark.p1p2EscapeDefect
def test_case_90_verify_app_installation(driver, settings):
    menu = HomePage(driver, settings)
    menu.applications_menu(UserData.village_application)
    load = ApplicationPage(driver)
    code = load.get_app_code(UserData.village_application)
    mobile = AndroidScreen(settings)
    mobile.verify_app_install(code)
    mobile.close_android_driver()




