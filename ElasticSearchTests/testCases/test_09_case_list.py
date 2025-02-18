import pytest

from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.case_list.case_list_page import CaseListPage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_case_list_report_no_case_type_filters(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    case = CaseListPage(driver)
    case.verify_page()
    case.hide_filters()
    case.show_filters()
    case.verify_case_list_page_fields_columns()


@pytest.mark.login
@pytest.mark.reports
def test_case_02_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    case = CaseListPage(driver)
    case.case_list_pagination_list()
    case.verify_pagination_dropdown()
    case.verify_sorted_list("Case Type")
    case.verify_sorted_list("Name")
    case.verify_sorted_list("Created Date")
    case.verify_sorted_list("Modified Date")

@pytest.mark.login
@pytest.mark.reports
def test_case_03_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    case = CaseListPage(driver)
    case.case_list_save_report()


@pytest.mark.login
@pytest.mark.reports
def test_case_04_report_filter_selections(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    case = CaseListPage(driver)
    case.report_filter_search_section()
    case.verify_open_form_options(UserData.open_close_options[0])
    case.verify_open_form_options(UserData.open_close_options[1])
    case.verify_open_form_options(UserData.open_close_options[2])

@pytest.mark.login
@pytest.mark.reports
def test_case_05_case_list_users_groups_selection(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    case = CaseListPage(driver)
    case.verify_users_selections()
    case.verify_group_selections()

@pytest.mark.login
@pytest.mark.reports
def test_case_06_case_list_case_data_verification(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    case = CaseListPage(driver)
    data_dict = case.case_list_get_case_data()
    case.compare_case_date_with_download(data_dict)
    case.verify_case_close(data_dict)