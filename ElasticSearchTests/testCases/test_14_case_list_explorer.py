import pytest

from HQSmokeTests.testPages.email.email_verification import EmailVerification
from HQSmokeTests.testPages.home.home_page import HomePage
from ElasticSearchTests.userInputs.user_inputs import UserData
from ElasticSearchTests.testPages.case_list_explorer.case_list_explorer_page import CaseListExplorerPage

""""Contains all test cases that aren't specifically related any menu modules"""


@pytest.mark.login
@pytest.mark.reports
def test_case_01_case_list_explorer_report_no_case_type_filters(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    case = CaseListExplorerPage(driver)
    case.verify_page()
    case.hide_filters()
    case.show_filters()
    case.verify_case_list_explorer_page_fields_columns()


@pytest.mark.login
@pytest.mark.reports
def test_case_02_pagination(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    case = CaseListExplorerPage(driver)
    case.case_list_explorer_pagination_list()
    case.verify_pagination_dropdown()
    case.verify_sorted_list("case_type")
    # case.verify_sorted_list("case_name")
    case.verify_sorted_list("last_modified")


@pytest.mark.login
@pytest.mark.reports
def test_case_03_save_report_and_favorite(driver, settings):
    report = HomePage(driver, settings)
    report.reports_menu()
    case = CaseListExplorerPage(driver)
    case.case_list_explorer_save_report()


@pytest.mark.login
@pytest.mark.reports
def test_case_04_report_filter_selections(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    case = CaseListExplorerPage(driver)
    case.report_filter_search_section()
    case.verify_open_form_options(UserData.open_close_options[0])
    case.verify_open_form_options(UserData.open_close_options[1])
    case.verify_open_form_options(UserData.open_close_options[2])

@pytest.mark.login
@pytest.mark.reports
def test_case_05_export_to_excel(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = CaseListExplorerPage(driver)
    web_data = activity.export_case_list_explorer_to_excel()
    email = EmailVerification(settings)
    link = email.get_hyperlink_from_latest_email(UserData.case_list_explorer_report, settings['url'])
    activity.compare_status_with_email(link, web_data)

@pytest.mark.login
@pytest.mark.reports
def test_case_06_email_report(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    activity = CaseListExplorerPage(driver)
    web_data, subject = activity.export_case_list_explorer_email()
    email = EmailVerification(settings)
    table_data = email.get_email_body_from_latest_email(UserData.email_case_list_explorer_report, settings['url'])
    activity.compare_status_with_html_table(table_data, web_data)

@pytest.mark.login
@pytest.mark.reports
def test_case_07_case_list_explorer_users_groups_selection(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    case = CaseListExplorerPage(driver)
    case.verify_users_selections()
    case.verify_group_selections()

@pytest.mark.login
@pytest.mark.reports
def test_case_08_case_list_explorer_queries_verification(driver, settings):
    home = HomePage(driver, settings)
    home.reports_menu()
    case = CaseListExplorerPage(driver)
    case.verify_query_1_case_data()
    case.verify_query_2_case_data()
    # case.verify_timezone_change() # not working using automation users


