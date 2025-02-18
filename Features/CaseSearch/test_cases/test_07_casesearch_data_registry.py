import pytest
from selenium.common import NoSuchElementException

from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from common_utilities.selenium.webapps import WebApps
from Features.CaseSearch.constants import *

""""Contains all data registry related test cases"""


def test_case_01_no_access_dr_caselist(driver, settings):
    webapps = WebApps(driver, settings)
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


def test_case_02_access_to_non_dr_caselist(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    case_name = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                   input_value=CaseSearchUserInput.song_case_on_casesearch_1,
                                                   property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(case_name, displayed=NO)

@pytest.mark.skip
def test_case_03_load_external_case_into_caselist_skip_default(driver, settings):
    webapps = WebApps(driver, settings)
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
    assert "casesearch" in domain_url, "casesearch not present in url"
    print("casesearch present in url")
    webapps.submit_the_form()

@pytest.mark.skip
def test_case_04_load_external_linked_domain_case_into_caselist_search_first(driver, settings):
    webapps = WebApps(driver, settings)
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
    assert "casesearch" in domain_url, "casesearch not present in url"
    print("casesearch present in url")
    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()


def test_case_05_load_external_same_domain_into_caselist_search_first(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_2)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.load_external_search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casename = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                  input_value=CaseSearchUserInput.song_automation_song_1,
                                                  property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(casename)
    webapps.select_case_and_continue(casename)
    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()

@pytest.mark.skip
def test_case_06_smart_link_skip_default(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_domain(domain_name=CaseSearchUserInput.casesearch, current_url=driver.current_url)
    webapps.login_as(CaseSearchUserInput.user_1)
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
    assert "casesearch-1" in domain_url, "casesearch-1 not present in url"
    print("casesearch-1 present in url")
    webapps.submit_the_form()

@pytest.mark.skip
def test_case_07_smart_link_search_first_linked_domain_case(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_domain(domain_name=CaseSearchUserInput.casesearch, current_url=driver.current_url)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    """Search case in another domain"""
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
    try:
        webapps.select_user(CaseSearchUserInput.kiran)
    except NoSuchElementException:
        print("Already logged in")
        pass
    domain_url = driver.current_url
    assert "casesearch-1" in domain_url, "casesearch-1 not present in url"
    print("casesearch-1 present in url")
    webapps.submit_the_form()

@pytest.mark.skip
def test_case_08_smart_link_search_first_shadow(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_domain(domain_name=CaseSearchUserInput.casesearch, current_url=driver.current_url)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    """Search case in another domain"""
    webapps.open_menu(CaseSearchUserInput.shadow_smart_link_search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casename = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                  input_value=CaseSearchUserInput.casesearch_1,
                                                  property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(casename)
    webapps.select_case_and_continue(casename)
    try:
        webapps.select_user(CaseSearchUserInput.kiran)
    except NoSuchElementException:
        print("Already logged in")
        pass
    domain_url = driver.current_url
    assert "casesearch-1" in domain_url, "casesearch-1 not present in url"
    print("casesearch-1 present in url")
    webapps.submit_the_form()


def test_case_09_smart_link_skip_default_shadow(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_domain(domain_name=CaseSearchUserInput.casesearch, current_url=driver.current_url)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.shadow_smart_link_skip_default_menu)
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    casename = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                  input_value=CaseSearchUserInput.casesearch_1,
                                                  property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(casename)
    webapps.select_case_and_continue(casename)
    try:
        webapps.select_user(CaseSearchUserInput.kiran)
    except NoSuchElementException:
        print("Already logged in")
        pass
    domain_url = driver.current_url
    assert "casesearch-1" in domain_url, "casesearch-1 not present in url"
    print("casesearch-1 present in url")
    webapps.submit_the_form()


def test_case_10_smart_link_search_first_same_domain_case(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_domain(domain_name=CaseSearchUserInput.casesearch, current_url=driver.current_url)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    """Search case in present in same domain"""
    webapps.open_menu(CaseSearchUserInput.smart_link_search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casename = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                  input_value=CaseSearchUserInput.song_automation_song_1,
                                                  property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(casename)
    webapps.select_case_and_continue(casename)
    webapps.submit_the_form()


@pytest.mark.skip(reason="Failing on prod and in USH backlog: https://dimagi-dev.atlassian.net/browse/USH-2263")
def test_case_11_unrelated_case_property(driver, settings):
    webapps = WebApps(driver, settings)
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
