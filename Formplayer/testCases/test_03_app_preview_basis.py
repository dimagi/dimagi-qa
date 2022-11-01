from Formplayer.testPages.app_preview.app_preview_basics import AppPreviewBasics


def test_case_06_icons_in_app_preview(driver):

    icons = AppPreviewBasics(driver)
    icons.icons_are_present()


def test_case_07_back_button_functionality(driver):

    back_button = AppPreviewBasics(driver)
    back_button.back_button_functionality()


def test_case_08_refresh_button_functionality(driver):

    refresh_button = AppPreviewBasics(driver)
    refresh_button.refresh_button_functionality_01()
    refresh_button.refresh_button_functionality_02()


def test_case_09_web_user_submission(driver):

    submission = AppPreviewBasics(driver)
    submission.web_user_submission()


def test_case_10_one_question_per_screen(driver):

    question = AppPreviewBasics(driver)
    question.one_question_per_screen_negative()
    question.one_question_per_screen_positive()


def test_case_11_clear_user_data(driver):

    data = AppPreviewBasics(driver)
    data.clear_user_data()


def test_case_12_change_language(driver):

    language = AppPreviewBasics(driver)
    language.change_language()


def test_case_13_add_empty_form(driver):

    form = AppPreviewBasics(driver)
    form.add_empty_form()