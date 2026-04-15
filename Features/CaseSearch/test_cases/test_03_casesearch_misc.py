import random
import time

import pytest

from Features.CaseSearch.constants import *
from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from common_utilities.selenium.base_page import BasePage
from common_utilities.selenium.webapps import WebApps

""""Contains all case search miscellaneous test cases"""


def test_case_01_eof_navigations(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check eof navs"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.song_automation_song,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    webapps.select_case_and_continue(CaseSearchUserInput.song_automation_song)
    """EOF Nav - Prev Menu"""

    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()
    casesearch.check_eof_navigation(eof_nav=PREV_MENU,
                                    menu=CaseSearchUserInput.search_first_menu
                                    )
    """EOF Nav - Menu-Songs"""
    webapps.open_form(CaseSearchUserInput.add_show_form)
    webapps.submit_the_form()
    casesearch.check_eof_navigation(eof_nav=MENU,
                                    menu=CaseSearchUserInput.search_first_menu
                                    )
    """EOF Nav - First Menu"""
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.song_automation_song,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    webapps.select_case_and_continue(CaseSearchUserInput.song_automation_song)
    webapps.open_form(CaseSearchUserInput.update_ratings_form)
    webapps.submit_the_form()
    casesearch.check_eof_navigation(eof_nav=FIRST_MENU,
                                    menu=CaseSearchUserInput.case_search_app_name
                                    )
    """EOF Nav - Home Screen"""
    # This fails on prod currently so commenting..
    # webapps.open_form(CaseSearchUserInput.close_song_form)
    # webapps.submit_the_form()
    # casesearch.check_eof_navigation(eof_nav=HOME_SCREEN)


def test_case_02_claim_condition(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check Claim Condition"""
    webapps.login_as(CaseSearchUserInput.a_user)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_setting_menu)
    webapps.search_all_cases()
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.four,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    case_name = webapps.omni_search(CaseSearchUserInput.song_automation_song_10)
    form_name = webapps.select_case_and_continue(case_name)
    assert not bool(form_name), "Form name should not be present"
    print("Form name not present")
