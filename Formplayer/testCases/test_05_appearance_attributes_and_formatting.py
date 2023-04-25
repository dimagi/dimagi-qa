from Formplayer.testPages.app_preview.login_as_app_preview_page import LoginAsAppPreviewPage
from Formplayer.testPages.basic_test_app.basic_test_app_preview import BasicTestAppPreview
from Formplayer.testPages.basic_test_app.basic_test_web_apps import BasicTestWebApps
from Formplayer.testPages.webapps.login_as_page import LoginAsPage
from Formplayer.userInputs.user_inputs import UserData


def test_case_20_maps_web_apps(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.form_specific_tests_app['case_list'], UserData.form_specific_tests_app['form_name'])
    basic.maps_record_location()


def test_case_21_maps_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    login = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic.turn_off_one_question_per_screen()
    basic.open_form(UserData.form_specific_tests_app['case_list'], UserData.form_specific_tests_app['form_name'])
    basic.maps_record_location()


def test_case_26_sub_menu_web_apps(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.sub_menus()


def test_case_27_sub_menu_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    login = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic.turn_off_one_question_per_screen()
    basic.sub_menus()


def test_case_28_multimedia_app_logo_and_menu_and_form_multimedia_web_apps(driver, settings):
    login = LoginAsPage(driver,settings)
    login.open_webapps_menu()
    basic = BasicTestWebApps(driver)
    basic.multimedia_logo()
    basic.multimedia_forms_menus()


def test_case_29_menu_and_form_multimedia_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.multimedia_app['tests_app'])
    basic.multimedia_forms_menus()


def test_case_30_multimedia_form_nav_web_apps(driver, settings):
    login = LoginAsPage(driver,settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.multimedia_app['tests_app'])
    basic.multimedia_form_navigation()


def test_case_31_multimedia_form_nav_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    login = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.multimedia_app['tests_app'])
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic.turn_off_one_question_per_screen()
    basic.multimedia_form_navigation()


def test_case_32_custom_badge_web_apps(driver, settings):
    login = LoginAsPage(driver,settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.custom_badge()


def test_case_33_custom_badge_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    basic.custom_badge()