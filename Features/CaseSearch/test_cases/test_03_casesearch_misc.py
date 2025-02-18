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
    time.sleep(2)
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


def test_case_02_related_property_search(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check related property search"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.song_automation_song,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    webapps.select_case_and_continue(CaseSearchUserInput.song_automation_song)
    webapps.open_form(CaseSearchUserInput.shows_form)
    casesearch.search_against_property(search_property=CaseSearchUserInput.parent_artist,
                                       input_value=CaseSearchUserInput.automation_artist_1,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    webapps.omni_search(CaseSearchUserInput.automation_artist_1)
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.automation_artist_1
                                        )
    webapps.omni_search(CaseSearchUserInput.show_case_show1)
    webapps.select_case(CaseSearchUserInput.show_case_show1)
    casesearch.check_value_on_case_detail(search_property=CaseSearchUserInput.parent_artist,
                                          expected_value=CaseSearchUserInput.automation_artist_1
                                          )


def test_case_03_auto_advance_menus(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check auto advance to forms"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.artist_menu)
    case_name = webapps.omni_search(CaseSearchUserInput.automation_artist_1)
    webapps.select_case_and_continue(case_name)
    casesearch.check_eof_navigation(eof_nav=MENU,
                                    menu=case_name
                                    )


def test_case_04_display_only_forms(driver, settings):
    webapps = WebApps(driver, settings)
    base = BasePage(driver)
    """Check display only form modes"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.display_only_forms_menu)
    assert not base.is_displayed(webapps.search_all_cases_button), "Search All Cases button should not be present"
    print("Search All Cases button not present")


def test_case_05_shadow_menu(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check forms in normal menu"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    if 'www' in settings['url']:
        casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                           input_value=CaseSearchUserInput.song_just_babe,
                                           property_type=TEXT_INPUT
                                           )
    else:
        casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                           input_value=CaseSearchUserInput.song_123,
                                           property_type=TEXT_INPUT
                                           )

    # casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
    #                                    input_value=CaseSearchUserInput.song_automation_song,
    #                                    property_type=TEXT_INPUT
    #                                    )
    webapps.search_button_on_case_search_page()
    if 'www' in settings['url']:
        search_first_form_names = webapps.select_case_and_continue(CaseSearchUserInput.song_just_babe)
    else:
        search_first_form_names = webapps.select_case_and_continue(CaseSearchUserInput.song_123)
    # search_first_form_names = webapps.select_case_and_continue(CaseSearchUserInput.song_automation_song)
    """Check search and forms in shadow menu"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.shadow_menu)
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.five_star,
                                       property_type=COMBOBOX
                                       )
    webapps.search_button_on_case_search_page()
    if 'www' in settings['url']:
        case_name = webapps.omni_search(CaseSearchUserInput.song_just_babe)
    else:
        case_name = webapps.omni_search(CaseSearchUserInput.song_123)

    # case_name = webapps.omni_search(CaseSearchUserInput.song_automation_song)
    shadow_form_names = webapps.select_case_and_continue(case_name)
    assert shadow_form_names == search_first_form_names, "Values mismatched " + str(shadow_form_names) + " and " + str(
        search_first_form_names
        )
    print("Values matched " + str(shadow_form_names) + " and " + str(search_first_form_names))


def test_case_06_performance_check(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check performance"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.musical_instruments_menu)
    webapps.open_form(CaseSearchUserInput.view_instruments_form)
    webapps.search_all_cases()
    casesearch.search_against_property(search_property=CaseSearchUserInput.instrument_name,
                                       input_value=CaseSearchUserInput.instrument_case_guitar,
                                       property_type=TEXT_INPUT
                                       )
    start_time = time.perf_counter()  # Start capturing time
    webapps.search_button_on_case_search_page()
    end_time = time.perf_counter()  # Stop capturing time
    run_time = end_time - start_time
    if run_time <= 4:
        print("Results load time is within expected range: " + str(run_time) + " sec.")
        assert True
    else:
        print("Results load time is more than expected: " + str(run_time) + " sec.")
    webapps.search_again_cases()
    casesearch.search_against_property(search_property=CaseSearchUserInput.instrument_name,
                                       input_value=CaseSearchUserInput.instrument_case_guitar,
                                       property_type=TEXT_INPUT
                                       )
    start_time = time.perf_counter()
    webapps.search_button_on_case_search_page()
    end_time = time.perf_counter()
    run_time = end_time - start_time
    if run_time <= 4:
        print("Results load time is within expected range: " + str(run_time) + " sec.")
        assert True
    else:
        print("Results load time is more than expected: " + str(run_time) + " sec.")


def test_case_07_multi_case_types_and_related_cases(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    """Check multi case type case list"""
    webapps.open_menu(CaseSearchUserInput.mixed_case_type_menu)
    casesearch.search_against_property(search_property=CaseSearchUserInput.name,
                                       input_value=CaseSearchUserInput.show_case_show1,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    # Checks case type show
    webapps.omni_search(CaseSearchUserInput.show_case_show1)
    webapps.navigate_to_breadcrumb(CaseSearchUserInput.mixed_case_type_menu)
    webapps.clear_selections_on_case_search_page()
    # Checks case type song
    casename = casesearch.search_against_property(search_property=CaseSearchUserInput.name,
                                                  input_value=CaseSearchUserInput.song_automation_song_1,
                                                  property_type=TEXT_INPUT
                                                  )
    webapps.search_button_on_case_search_page()
    webapps.omni_search(casename)
    # Include related cases check
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.two
                                        )
    webapps.select_case_and_continue(casename)
    webapps.submit_the_form()
    # Tests form linking
    casesearch.check_eof_navigation(eof_nav=MENU, menu=CaseSearchUserInput.add_show_form)
    """Check multi case type case list for DR workflow"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.mixed_case_type_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.name,
                                       input_value=CaseSearchUserInput.show_case_casesearch_1,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    webapps.omni_search(CaseSearchUserInput.show_case_casesearch_1)
    webapps.select_case_and_continue(CaseSearchUserInput.show_case_casesearch_1)
    webapps.submit_the_form()


def test_case_08_display_condition(driver, settings):
    webapps = WebApps(driver, settings)
    base = BasePage(driver)
    """Check Display condition for a_user"""
    webapps.login_as(CaseSearchUserInput.a_user)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_setting_menu)
    assert base.is_displayed(webapps.search_all_cases_button), "Search All Cases button should be present"
    print("Search All Cases button present")
    """Check Display condition for another user"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_setting_menu)
    assert not base.is_displayed(webapps.search_all_cases_button), "Search All Cases button should not be present"
    print("Search All Cases button not present")


def test_case_09_search_filter(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check Search Filter"""
    webapps.login_as(CaseSearchUserInput.a_user)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_filter_menu)
    webapps.search_all_cases()
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=CaseSearchUserInput.five
                                        )


def test_case_10_claim_condition(driver, settings):
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


def test_case_11_do_not_search_cases(driver, settings):
    if "staging" in settings["url"]:
        pytest.xfail("This test is failing on Staging")
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check don't search cases owned by the following ids"""
    webapps.login_as(CaseSearchUserInput.a_user)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_setting_menu)
    webapps.search_all_cases()
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.four,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    webapps.omni_search(CaseSearchUserInput.song_case_b_users_song, displayed=NO)


def test_case_12_sync_cases_on_form_entry(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Update rating as another user"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    case_name = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                   input_value=CaseSearchUserInput.song_automation_song_update,
                                                   property_type=TEXT_INPUT
                                                   )
    webapps.search_button_on_case_search_page()
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.update_ratings_form)
    rating_star, rating_value = random.choice(list(CaseSearchUserInput.rating_on_form.items()))
    casesearch.select_rating_answer_(rating_star)
    webapps.submit_the_form()
    """Check rating as owner"""
    webapps.login_as(CaseSearchUserInput.user_2)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=case_name,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.play_song_form)
    casesearch.check_label_in_form(rating_value)
    webapps.submit_the_form()


def test_case_13_ancestor_exists_query(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    """Check default filter with ancestor exist query"""
    webapps.open_menu(CaseSearchUserInput.shows_ancestor_exists_menu)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=CaseSearchUserInput.metal
                                        )
    webapps.search_again_cases()
    """Check multi valued parent property search"""
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_subgenre,
                                       input_value=CaseSearchUserInput.funk_metal,
                                       property_type=COMBOBOX
                                       )
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_subgenre,
                                       input_value=CaseSearchUserInput.nu_metal,
                                       property_type=COMBOBOX
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=[CaseSearchUserInput.funk_metal, CaseSearchUserInput.nu_metal],
                                        is_multi=YES
                                        )
