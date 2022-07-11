from Formplayer.testPages.webapps.login_as_page import LoginAsPage
from Formplayer.testPages.app_preview.login_as_app_preview_page import LoginAsAppPreviewPage

def test_case_01_login_as_web_apps(driver):

    webapps = LoginAsPage(driver)
    webapps.login_as_presence()
    webapps.login_as_content()
    #webapps.login_as_form_submssion()


def test_case_01_login_as_app_preview(driver):

    app_preview = LoginAsAppPreviewPage(driver)
    app_preview.open_view_app_preview()
    app_preview.login_as_app_preview_presence()
    app_preview.login_as_app_preview_content()
    #app_preview.login_as_form_submssion()  //commenting the last step as there is some issue with the Basic Tests App