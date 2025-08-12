import time

from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from common_utilities.selenium.webapps import WebApps
from Features.CaseSearch.constants import *

""""Contains all inline search related test cases"""


def test_case_01_check_search_input_on_caselist_casedetail_form(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.five_star,
                                       property_type=COMBOBOX)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.seven,
                                        expected_value=CaseSearchUserInput.five)
    case_name = webapps.select_first_case_on_list()
    casesearch.check_value_on_case_detail(tabname=CaseSearchUserInput.rating,
                                          search_property=CaseSearchUserInput.rating_input,
                                          expected_value=CaseSearchUserInput.five)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.update_song_form)
    casesearch.check_value_on_form(CaseSearchUserInput.five)
    webapps.submit_the_form()


def test_case_02_navigation_via_breadcrumbs(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.five_star,
                                       property_type=COMBOBOX)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.seven,
                                        expected_value=CaseSearchUserInput.five)
    case_name = webapps.select_first_case_on_list()
    casesearch.check_value_on_case_detail(tabname=CaseSearchUserInput.rating,
                                          search_property=CaseSearchUserInput.rating_input,
                                          expected_value=CaseSearchUserInput.five)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.update_song_form)
    webapps.navigate_to_breadcrumb(CaseSearchUserInput.inline_search_menu)


def test_case_03_search_property_settings(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.four_star,
                                       property_type=COMBOBOX)
    time.sleep(2)
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.five_star,
                                       property_type=COMBOBOX,
                                       include_blanks=YES)
    time.sleep(2)
    flag = casesearch.check_values_selected(search_property=CaseSearchUserInput.rating,
                                     value_list=[CaseSearchUserInput.four_star, CaseSearchUserInput.five_star],
                                     rating=YES)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=[CaseSearchUserInput.four,
                                                        CaseSearchUserInput.five,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES,
                                        flag=flag)
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.seven,
                                        expected_value=CaseSearchUserInput.rating_four_and_five,
                                        flag=flag)
    webapps.select_first_case_on_list()
    casesearch.check_value_on_case_detail(tabname=CaseSearchUserInput.rating,
                                          search_property=CaseSearchUserInput.rating_input,
                                          expected_value=CaseSearchUserInput.rating_four_and_five)


def test_case_04_load_from_external_domain(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.casesearch,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    case_name = webapps.omni_search(CaseSearchUserInput.song_case_on_casesearch_1)
    webapps.select_case_and_continue(case_name)
    domain_url = driver.current_url
    assert "casesearch" in domain_url, "casesearch not present in url"
    print("casesearch present in url")
    webapps.open_form(CaseSearchUserInput.add_show_form)
    webapps.submit_the_form()
    casesearch.check_eof_navigation(eof_nav=MENU,
                                    menu=CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    webapps.search_button_on_case_search_page()
    webapps.select_first_case_on_list_and_continue()
    webapps.open_form(CaseSearchUserInput.add_show_form)
    webapps.submit_the_form()


def test_case_05_old_case_search_instance(driver, settings):
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.old_inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    webapps.search_button_on_case_search_page()
    webapps.select_first_case_on_list_and_continue()
    webapps.submit_the_form()
