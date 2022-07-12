from Formplayer.testPages.webapps.login_as_page import LoginAsPage


def test_case_01_login_as_web_apps(driver):

    webapps = LoginAsPage(driver)
    webapps.login_as_presence()
    webapps.login_as_content()
    webapps.login_as_form_submssion()

