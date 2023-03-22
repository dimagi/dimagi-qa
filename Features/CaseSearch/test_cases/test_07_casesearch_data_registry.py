import pytest

from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from common_utilities.selenium.webapps import WebApps
from Features.CaseSearch.constants import *

""""Contains all data registry related test cases"""


def test_case_01_no_access_dr_caselist(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    case_name = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                   input_value=CaseSearchUserInput.song_case_on_casesearch2,
                                                   property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(case_name, displayed=NO)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.load_external_search_first_menu)
    webapps.clear_selections_on_case_search_page()
    case_name = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                   input_value=CaseSearchUserInput.song_case_on_casesearch2,
                                                   property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(case_name, displayed=NO)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.smart_link_skip_default_menu)
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    case_name = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                   input_value=CaseSearchUserInput.song_case_on_casesearch2,
                                                   property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(case_name, displayed=NO)


def test_case_02_access_to_non_dr_caselist(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    case_name = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                   input_value=CaseSearchUserInput.song_case_on_casesearch_1,
                                                   property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(case_name, displayed=NO)


def test_case_03_load_external_case_into_caselist_skip_default(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.load_external_skip_default_menu)
    casename = webapps.omni_search(CaseSearchUserInput.song_case_cs4_song_300, displayed=NO)
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=casename,
                                       property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_id,
                                       input_value="3300",
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(casename)
    webapps.select_case_and_continue(casename)
    domain_url = driver.current_url
    assert "casesearch" in domain_url
    webapps.submit_the_form()


def test_case_04_load_external_case_into_caselist_search_first(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_2)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.load_external_search_first_menu)
    webapps.clear_and_search_all_cases_on_case_search_page()
    casename = webapps.omni_search(CaseSearchUserInput.song_case_cs4_song_300, displayed=NO)
    webapps.search_again_cases()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=casename,
                                       property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_id,
                                       input_value="3300",
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(casename)
    webapps.select_case_and_continue(casename)
    domain_url = driver.current_url
    assert "casesearch" in domain_url
    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()


@pytest.mark.skip(reason="Failing")
def test_case_05_smart_link_skip_default(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_domain(domain_name=CaseSearchUserInput.casesearch, current_url=driver.current_url)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.smart_link_skip_default_menu)
    casename = webapps.omni_search(CaseSearchUserInput.song_case_cs4_song_300, displayed=NO)
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=casename,
                                       property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_id,
                                       input_value="3300",
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(casename)
    webapps.select_case_and_continue(casename)
    webapps.select_user(CaseSearchUserInput.kiran)  # Failing 404! Raise a ticket
    domain_url = driver.current_url
    assert "casesearch-1" in domain_url
    webapps.submit_the_form()


@pytest.mark.skip(reason="Failing")
def test_case_06_smart_link_search_first(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_domain(domain_name=CaseSearchUserInput.casesearch, current_url=driver.current_url)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.smart_link_search_first_menu)
    webapps.clear_and_search_all_cases_on_case_search_page()
    casename = webapps.omni_search(CaseSearchUserInput.song_case_cs4_song_300, displayed=NO)
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=casename,
                                       property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_id,
                                       input_value="3300",
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(casename)
    webapps.select_case_and_continue(casename)
    webapps.select_user(CaseSearchUserInput.kiran)  # Failing 404! Raise a ticket
    domain_url = driver.current_url
    assert "casesearch-1" in domain_url
    webapps.submit_the_form()


@pytest.mark.skip(reason="Failing on prod")
def test_case_08_unrelated_case_property(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_domain(domain_name=CaseSearchUserInput.casesearch, current_url=driver.current_url)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.unrelated_case_load_external_menu)
    webapps.clear_selections_on_case_search_page()
    casename = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                  input_value=CaseSearchUserInput.song_automation_song_1,
                                                  property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(casename)
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=CaseSearchUserInput.case_with_unrelated_id.get("case_id"))
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=CaseSearchUserInput.case_with_unrelated_id.get("song_name"))
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.case_with_unrelated_id.get("rating"))
    webapps.select_case_and_continue(casename)
    webapps.submit_the_form()
