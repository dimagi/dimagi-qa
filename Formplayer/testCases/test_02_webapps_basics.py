from Formplayer.testPages.webapps.webapps_basics import WebAppsBasics
from Formplayer.userInputs.user_inputs import UserData

def test_case_02_verify_breadcrumbs_and_app_home(driver):

    app = WebAppsBasics(driver)
    app.application_is_present()
    app.verify_app_home_screen()
    app.verify_breadcrumbs(UserData.test_application)
    app.verify_ribbon()



def test_case_03_run_through_the_app(driver):

    app = WebAppsBasics(driver)
    app.submit_form()
    app.sync_forms()


def test_case_04_locate_forms_and_cases(driver):

    forms = WebAppsBasics(driver)
    forms.verify_form_data_case_list(forms.name_input, UserData.app_preview_mobile_worker)
    forms.verify_form_data_submit_history(forms.name_input, UserData.test_application)



def test_case_05_verify_web_apps_settings(driver):

    settings = WebAppsBasics(driver)
    settings.verify_web_apps_settings()


def test_case_06_verify_language(driver):

    language = WebAppsBasics(driver)
    language.verify_language()
