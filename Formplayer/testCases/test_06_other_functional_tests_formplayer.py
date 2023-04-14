from Formplayer.testPages.basic_test_app.basic_test_web_apps import BasicTestWebApps
from Formplayer.testPages.reports.case_list_page import CaseListPage
from Formplayer.testPages.webapps.login_as_page import LoginAsPage
from Formplayer.userInputs.user_inputs import UserData

test_data = dict()

def test_case_29_minimize_duplicate(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.submit_basic_test_form()
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_case_list(UserData.basic_test_app_forms['min_dup'])
    test_data["parent case name"], test_data["sub_case_name"], test_data["number"] = basic.minimize_duplicate_create_case_subcase()
    print("Test Data:", test_data["parent case name"] +", "+ test_data["sub_case_name"] +", "+ test_data["number"])
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_case_list(UserData.basic_test_app_forms['min_dup'])
    test_data['text'], test_data['phone number'], test_data['singleselect'], test_data['multiselect'], test_data["intval"], test_data['place'], test_data['dateval'], test_data['data node'] = basic.minimize_duplicate_update_case(test_data["parent case name"], test_data["sub_case_name"])
    print("Updated Test Data:", test_data)
    return test_data


def test_case_30_case_detail(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.submit_basic_test_form()
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_case'])
    casename = basic.case_node_create_case()
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_subcase'])
    subcase = basic.case_node_create_subcase(casename, "1", "1")
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_subcase'])
    subcase.update(basic.case_node_create_subcase(casename, "2","1"))
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_subcase'])
    subcase.update(basic.case_node_create_subcase(casename, "3","2"))
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['create_subcase'])
    subcase.update(basic.case_node_create_subcase(casename, "4","3"))
    print(subcase)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['update_case'])
    basic.search_case_open(casename)
    basic.verify_case_details("3",subcase)
    basic.verify_case_details("4",subcase)

def test_case_31_model_repeats(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['fst'], UserData.basic_test_app_forms['fst_repeat'])
    basic.fst_repeat_form_validation()


def test_case_31_model_iteration(driver, settings):
    login = LoginAsPage(driver, settings)
    login.open_webapps_menu()
    login.login_as_user(UserData.app_preview_mobile_worker)
    basic = BasicTestWebApps(driver)
    login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
    basic.open_form(UserData.basic_test_app_forms['fst'], UserData.basic_test_app_forms['fst_cross_iter_repeat'])
    basic.fst_cross_iter_repeat_form_validation()

def test_case_29_minimize_duplicate_data_verification(driver, settings):
    case = CaseListPage(driver, settings)
    case.open_reports_menu()
    case.verify_form_data_case_list(test_data)