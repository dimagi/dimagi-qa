from Formplayer.testPages.webapps.webapps_basics import WebAppsBasics


def test_case_01_verify_app_is_present(driver):

    app = WebAppsBasics(driver)
    app.application_is_present()


def test_case_02_run_through_the_app(driver):

    app = WebAppsBasics(driver)
    app.submit_form()


def test_case_03_locate_forms_and_cases(driver):

    forms = WebAppsBasics(driver)
    forms.verify_form_data_submit_history()
    forms.verify_form_data_case_list(case_name = forms.name_input)


def test_case_04_verify_web_apps_settings(driver):

    settings = WebAppsBasics(driver)
    settings.verify_web_apps_settings()


def test_case_05_verify_language(driver):

    language = WebAppsBasics(driver)
    language.verify_language()
