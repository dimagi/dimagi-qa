import pytest

from Formplayer.testPages.app_preview.login_as_app_preview_page import LoginAsAppPreviewPage
from Formplayer.testPages.basic_test_app.basic_test_app_preview import BasicTestAppPreview
from Formplayer.testPages.basic_test_app.basic_test_web_apps import BasicTestWebApps
from Formplayer.testPages.project_settings.project_settings_page import ProjectSettingsPage
from Formplayer.testPages.webapps.login_as_page import LoginAsPage
from Formplayer.userInputs.user_inputs import UserData

def test_case_16_incomplete_form_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    app_preview.login_as_user(UserData.app_preview_mobile_worker)
    basic.delete_all_incomplete_forms()
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_tests_app['form_name'])
    basic.save_incomplete_form(basic.name_input1)
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_tests_app['form_name'])
    basic.save_incomplete_form(basic.name_input2)
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_tests_app['form_name'])
    basic.save_incomplete_form(basic.name_input3)
    basic.verify_number_of_forms(3)
    basic.delete_first_form()
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    basic.verify_saved_form_and_submit_unchanged(basic.name_input2)
    basic.verify_submit_history(basic.name_input2, UserData.app_preview_mobile_worker)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    basic.verify_saved_form_and_submit_changed(basic.name_input1)
    basic.verify_submit_history(basic.changed_name_input, UserData.app_preview_mobile_worker)

def test_case_17_incomplete_form_web_apps(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    basic.delete_all_incomplete_forms()
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_tests_app['form_name'])
    basic.save_incomplete_form(basic.name_input1)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_tests_app['form_name'])
    basic.save_incomplete_form(basic.name_input2)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_tests_app['form_name'])
    basic.save_incomplete_form(basic.name_input3)
    basic.verify_number_of_forms(3)
    basic.delete_first_form()
    basic.verify_saved_form_and_submit_unchanged(basic.name_input2)
    basic.verify_submit_history(basic.name_input2, UserData.app_preview_mobile_worker)
    login.open_webapps_menu()
    basic.verify_saved_form_and_submit_changed(basic.name_input1)
    basic.verify_submit_history(basic.changed_name_input, UserData.app_preview_mobile_worker)

def test_case_18_data_preview_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    app_preview.login_as_user(UserData.app_preview_mobile_worker)
    expression = basic.random_expression()
    basic.verify_data_preview(expression)

def test_case_18_data_preview_web_apps(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    app_preview = BasicTestAppPreview(driver)
    expression = app_preview.random_expression()
    basic.verify_data_preview(expression)

def test_case_19_group_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    app_preview.login_as_user(UserData.app_preview_mobile_worker)
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_test_app_forms['group'])
    basic.group()

def test_case_19_group_web_apps(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    basic.delete_all_incomplete_forms()
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_test_app_forms['group'])
    basic.group()


def test_case_20_end_of_navigation_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    app_preview.login_as_user(UserData.app_preview_mobile_worker)
    basic.open_form(UserData.basic_test_app_forms['eofn'], UserData.basic_test_app_forms['home'])
    basic.end_of_navigation_module(UserData.basic_test_app_forms['eofn'])

def test_case_20_end_of_navigation_web_apps(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['eofn'], UserData.basic_test_app_forms['home'])
    basic.end_of_navigation_module(UserData.basic_test_app_forms['eofn'], settings)

def test_case_21_case_register_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    app_preview.login_as_user(UserData.app_preview_mobile_worker)
    basic.submit_basic_test_form()
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_case'])
    basic.register_negative_case()
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_case'])
    basic.register_positive_case()
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['caselist'])
    basic.case_detail_verification()
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['update_case'])
    new_data = basic.update_a_case()
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['caselist'])
    basic.updated_case_detail_verification(new_data)
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_subcase'])
    basic.create_and_verify_sub_case()
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['close_case'])
    basic.close_case()


def test_case_21_case_register_web_app(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.submit_basic_test_form()
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_case'])
    basic.register_negative_case()
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_case'])
    basic.register_positive_case()
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['caselist'])
    basic.case_detail_verification()
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['update_case'])
    new_data = basic.update_a_case()
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['caselist'])
    basic.updated_case_detail_verification(new_data)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_subcase'])
    basic.create_and_verify_sub_case(settings)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['close_case'])
    basic.close_case(settings)

def test_case_22_unicode_verification_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    app_preview.login_as_user(UserData.app_preview_mobile_worker)
    basic.submit_basic_test_form()
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_case'])
    basic.unicode_verification_case()
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['caselist'])
    basic.verify_updated_unicode()

def test_case_22_unicode_verification_web_app(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.submit_basic_test_form()
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_case'])
    basic.unicode_verification_case(settings)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['caselist'])
    basic.verify_updated_unicode()

def test_case_23_fixtures_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    app_preview.login_as_user(UserData.app_preview_mobile_worker)
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_test_app_forms['fixtures'])
    basic.fixtures_form()


def test_case_23_fixtures_web_app(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_test_app_forms['fixtures'])
    basic.fixtures_form()

def test_case_24_constraints_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    app_preview.login_as_user(UserData.app_preview_mobile_worker)
    basic.open_form(UserData.basic_test_app_forms['logic_test1'], UserData.basic_test_app_forms['constraints'])
    basic.constraint_form()

def test_case_24_constraints_web_apps(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['logic_test1'], UserData.basic_test_app_forms['constraints'])
    basic.constraint_form()

def test_case_25_functions_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    app_preview.login_as_user(UserData.app_preview_mobile_worker)
    basic.open_form(UserData.basic_test_app_forms['logic_test1'], UserData.basic_test_app_forms['functions'])
    basic.functions_form()

def test_case_25_functions_web_apps(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['logic_test1'], UserData.basic_test_app_forms['functions'])
    basic.functions_form()

def test_case_26_questions_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    app_preview.login_as_user(UserData.app_preview_mobile_worker)
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_test_app_forms['question'])
    basic.questions_form()

def test_case_26_questions_web_apps(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_test_app_forms['question'])
    basic.questions_form()

@pytest.mark.xfail("functionality not working via automation")
def test_case_27_webapps_forced_refresh(driver, settings):
    project = ProjectSettingsPage(driver, settings)
    project.clear_inactivity_timeout()
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_test_app_forms['question'])
    basic.fill_some_questions()
    project.get_new_tab()
    project.set_inactivity_timeout()
    app_preview = LoginAsAppPreviewPage(driver, settings)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    basic_app_preview = BasicTestAppPreview(driver)
    basic_app_preview.update_description(settings)
    basic.click_update_later()
    basic_app_preview.update_description(settings)
    basic.click_get_latest_app()
    project.clear_inactivity_timeout()


def test_case_28_pagination_web_apps(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    basic = BasicTestWebApps(driver)
    basic.verify_pagination()

def test_case_28_pagination_app_preview(driver, settings):
    app_preview = LoginAsAppPreviewPage(driver, settings)
    basic = BasicTestAppPreview(driver)
    app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
    basic.verify_pagination()

