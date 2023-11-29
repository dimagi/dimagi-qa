from Formplayer.testPages.app_preview.login_as_app_preview_page import LoginAsAppPreviewPage
from Formplayer.testPages.webapps.login_as_page import LoginAsPage
from Formplayer.testPages.webapps.webapps_basics import WebAppsBasics
from Formplayer.userInputs.user_inputs import UserData


def test_case_01_login_as_web_apps(driver, settings):
    loginPage = LoginAsPage(driver, settings)
    app_preview = LoginAsAppPreviewPage(driver, settings)
    loginPage.open_webapps_menu()
    loginPage.login_as_form_submssion(loginPage.form_input_no_login)
    app_preview.submit_history_verification("no login", UserData.web_user)
    loginPage.login_as_presence()
    loginPage.login_as_content()
    loginPage.login_as_form_submssion(loginPage.form_input)
    app_preview.submit_history_verification("login", UserData.app_preview_mobile_worker)

def test_case_01_login_as_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview()
    app_preview.login_as_app_preview_form_submission(app_preview.form_input_no_login)
    app_preview.submit_history_verification("no login", UserData.web_user)
    app_preview.open_view_app_preview()
    app_preview.login_as_app_preview_presence()
    app_preview.login_as_app_preview_content()
    app_preview.login_as_app_preview_form_submission(app_preview.form_input_login)
    app_preview.submit_history_verification("login", UserData.app_preview_mobile_worker)
