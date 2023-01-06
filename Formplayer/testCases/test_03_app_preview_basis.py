from Formplayer.testPages.app_preview.app_preview_basics import AppPreviewBasics
from Formplayer.testPages.app_preview.login_as_app_preview_page import LoginAsAppPreviewPage
from Formplayer.userInputs.user_inputs import UserData

def test_case_07_toggle_phone_tablet(driver, settings):
    toggle = AppPreviewBasics(driver)
    app_preview = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.test_application['tests_app'])
    toggle.verify_toggle_functionality()

def test_case_08_icons_in_app_preview(driver, settings):
    icons = AppPreviewBasics(driver)
    app_preview = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.test_application['tests_app'])
    icons.icons_are_present()


def test_case_09_back_button_functionality(driver, settings):
    back_button = AppPreviewBasics(driver)
    app_preview = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.test_application['tests_app'])
    back_button.back_button_functionality()


def test_case_10_refresh_button_functionality(driver, settings):
    refresh_button = AppPreviewBasics(driver)
    app_preview = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.test_application2['tests_app'])
    refresh_button.refresh_button_functionality_01()
    refresh_button.refresh_button_functionality_02()


def test_case_11_web_user_submission(driver, settings):
    submission = AppPreviewBasics(driver)
    app_preview = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.test_application2['tests_app'])
    submission.web_user_submission()


def test_case_12_one_question_per_screen(driver, settings):
    question = AppPreviewBasics(driver)
    app_preview = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.test_application2['tests_app'])
    question.one_question_per_screen_negative()
    question.one_question_per_screen_positive()


def test_case_13_clear_user_data(driver, settings):
    data = AppPreviewBasics(driver)
    app_preview = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.test_application['tests_app'])
    data.clear_user_data()


def test_case_14_change_language(driver, settings):
    language = AppPreviewBasics(driver)
    app_preview = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.test_application['tests_app'])
    language.change_language()


def test_case_15_add_empty_form(driver, settings):
    form = AppPreviewBasics(driver)
    app_preview = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.test_application2['tests_app'])
    form.add_empty_form()
