import pytest

from Formplayer.testPages.app_preview.login_as_app_preview_page import LoginAsAppPreviewPage
from Formplayer.testPages.basic_test_app.basic_test_app_preview import BasicTestAppPreview
from Formplayer.testPages.basic_test_app.basic_test_web_apps import BasicTestWebApps
from Formplayer.testPages.project_settings.project_settings_page import ProjectSettingsPage
from Formplayer.testPages.webapps.login_as_page import LoginAsPage
from Formplayer.userInputs.user_inputs import UserData

#
# def test_case_23_fixtures_app_preview(driver, settings):
#     app_preview = LoginAsAppPreviewPage(driver, settings)
#     basic = BasicTestAppPreview(driver)
#     app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
#     app_preview.login_as_user(UserData.app_preview_mobile_worker)
#     basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_test_app_forms['fixtures'])
#     basic.fixtures_form()
#
#
# def test_case_23_fixtures_web_app(driver, settings):
#     login = LoginAsPage(driver, settings)
#     login.open_webapps_menu()
#     login.login_as_user(UserData.app_preview_mobile_worker)
#     basic = BasicTestWebApps(driver)
#     login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
#     basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_test_app_forms['fixtures'])
#     basic.fixtures_form()
#
#
# def test_case_24_constraints_app_preview(driver, settings):
#     app_preview = LoginAsAppPreviewPage(driver, settings)
#     basic = BasicTestAppPreview(driver)
#     app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
#     app_preview.login_as_user(UserData.app_preview_mobile_worker)
#     basic.open_form(UserData.basic_test_app_forms['logic_test1'], UserData.basic_test_app_forms['constraints'])
#     basic.constraint_form()
#
#
# def test_case_24_constraints_web_apps(driver, settings):
#     login = LoginAsPage(driver, settings)
#     login.open_webapps_menu()
#     login.login_as_user(UserData.app_preview_mobile_worker)
#     basic = BasicTestWebApps(driver)
#     login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
#     basic.open_form(UserData.basic_test_app_forms['logic_test1'], UserData.basic_test_app_forms['constraints'])
#     basic.constraint_form()
#
#
# def test_case_25_functions_app_preview(driver, settings):
#     app_preview = LoginAsAppPreviewPage(driver, settings)
#     basic = BasicTestAppPreview(driver)
#     app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
#     app_preview.login_as_user(UserData.app_preview_mobile_worker)
#     basic.open_form(UserData.basic_test_app_forms['logic_test1'], UserData.basic_test_app_forms['functions'])
#     basic.functions_form()
#
#
# def test_case_25_functions_web_apps(driver, settings):
#     login = LoginAsPage(driver, settings)
#     login.open_webapps_menu()
#     login.login_as_user(UserData.app_preview_mobile_worker)
#     basic = BasicTestWebApps(driver)
#     login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
#     basic.open_form(UserData.basic_test_app_forms['logic_test1'], UserData.basic_test_app_forms['functions'])
#     basic.functions_form()
#
#
# def test_case_26_questions_app_preview(driver, settings):
#     app_preview = LoginAsAppPreviewPage(driver, settings)
#     basic = BasicTestAppPreview(driver)
#     app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
#     app_preview.login_as_user(UserData.app_preview_mobile_worker)
#     basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_test_app_forms['question'])
#     basic.questions_form()
#
#
# def test_case_26_questions_web_apps(driver, settings):
#     login = LoginAsPage(driver, settings)
#     login.open_webapps_menu()
#     login.login_as_user(UserData.app_preview_mobile_worker)
#     basic = BasicTestWebApps(driver)
#     login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
#     basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_test_app_forms['question'])
#     basic.questions_form()
#
#
# def test_case_27_webapps_forced_refresh(driver, settings):
#     pytest.xfail("functionality not working via automation")
#     project = ProjectSettingsPage(driver, settings)
#     project.clear_inactivity_timeout()
#     login = LoginAsPage(driver, settings)
#     login.open_webapps_menu()
#     login.login_as_user(UserData.app_preview_mobile_worker)
#     basic = BasicTestWebApps(driver)
#     login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
#     basic.open_form(UserData.basic_tests_app['case_list'], UserData.basic_test_app_forms['question'])
#     basic.fill_some_questions()
#     project.get_new_tab()
#     project.set_inactivity_timeout()
#     app_preview = LoginAsAppPreviewPage(driver, settings)
#     app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
#     basic_app_preview = BasicTestAppPreview(driver)
#     basic_app_preview.update_description(settings)
#     basic.click_update_later()
#     basic_app_preview.update_description(settings)
#     basic.click_get_latest_app()
#     project.clear_inactivity_timeout()
#
#
# def test_case_28_pagination_web_apps(driver, settings):
#     login = LoginAsPage(driver, settings)
#     login.open_webapps_menu()
#     basic = BasicTestWebApps(driver)
#     basic.verify_pagination()
#
#
# def test_case_28_pagination_app_preview(driver, settings):
#     app_preview = LoginAsAppPreviewPage(driver, settings)
#     basic = BasicTestAppPreview(driver)
#     app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
#     basic.verify_pagination()
#
#
# def test_case_34_form_linking_app_preview(driver, settings):
#     app_preview = LoginAsAppPreviewPage(driver, settings)
#     basic = BasicTestAppPreview(driver)
#     app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
#     app_preview.login_as_user(UserData.app_preview_mobile_worker)
#     basic.open_form(UserData.basic_test_app_forms['form_linking'], UserData.basic_test_app_forms['fl_add_case'])
#     case, cond, child = basic.form_linking_parent_form()
#     # app_preview.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
#     basic.open_form(UserData.basic_test_app_forms['form_linking'], UserData.basic_test_app_forms['cond_expression'])
#     basic.conditional_expression_form(case, cond)
#     # app_preview.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
#     basic.open_form(UserData.basic_test_app_forms['form_linking'], UserData.basic_test_app_forms['no_cond_expression'])
#     basic.no_conditional_expression_form(case, cond)
#     # app_preview.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
#     basic.open_form(UserData.basic_test_app_forms['form_linking'], UserData.basic_test_app_forms['form_linking_child'])
#     basic.form_linking_child(case, child)
