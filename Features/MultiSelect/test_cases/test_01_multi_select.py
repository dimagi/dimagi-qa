import time

import pytest

from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from Features.MultiSelect.test_pages.multiselect_page import MultiSelectWorkflows
from Features.MultiSelect.user_inputs.multiselect_user_inputs import MultiSelectUserInput
from HQSmokeTests.testPages.home.home_page import HomePage
from common_utilities.generate_random_string import fetch_random_string
from common_utilities.selenium.webapps import WebApps
from Features.CaseSearch.constants import *

""""Contains all multi-select related test cases"""


def test_case_01_multiple_selected_cases_accessible_on_form(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.songs_MS_SF_IS)
    webapps.search_button_on_case_search_page()
    cases_selected = multiselect.multi_select_cases(case_count=3)
    multiselect.continue_to_proceed_multiselect()
    webapps.open_form(MultiSelectUserInput.update_song_back_to_menu_form)
    multiselect.check_selected_cases_present_on_form(cases_selected, case_type=SONG)
    webapps.answer_repeated_questions(question_label=CaseSearchUserInput.add_show_question,
                                      input_type=textarea,
                                      input_value=fetch_random_string())
    webapps.submit_the_form()
    """Check EOF to menu"""
    casesearch.check_eof_navigation(eof_nav=MENU,
                                    menu=MultiSelectUserInput.songs_MS_SF_IS)


@pytest.mark.skip(reason="Failing, Kiran to check and raise a support ticket")
def test_case_02_multiselect_with_omnisearch(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.songs_MS_N_NIS)
    case_name = webapps.omni_search(CaseSearchUserInput.song_automation_song_1)
    webapps.select_case(case_name)
    multiselect.select_case_on_case_detail()
    webapps.omni_search(CaseSearchUserInput.song_automation_song_1)
    multiselect.check_if_checkbox_is_selected(case_name)


def test_case_03_multiselect_with_pagination(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.songs_MS_N_NIS)
    webapps.search_all_cases()
    webapps.clear_and_search_all_cases_on_case_search_page()
    cases_selected = multiselect.multi_select_cases(case_count=3)
    webapps.change_page_number("25")
    webapps.change_page_number("10")
    multiselect.check_if_checkbox_are_selected(cases_selected)
    webapps.switch_bw_pages()
    multiselect.check_if_checkbox_are_selected(cases_selected)
    webapps.go_to_page("2")
    webapps.go_to_page("1")
    multiselect.check_if_checkbox_are_selected(cases_selected)


def test_case_04_multiselect_with_select_parent_first_as_parent(driver, settings):
    webapps = WebApps(driver, settings)
    multiselect = MultiSelectWorkflows(driver)
    casesearch = CaseSearchWorkflows(driver)

    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.shows_MS_SPFP)
    casename = webapps.omni_search(CaseSearchUserInput.song_auto_parent)
    webapps.select_case(casename)
    casesearch.search_against_property(search_property=CaseSearchUserInput.artist_city,
                                       input_value=CaseSearchUserInput.show_auto,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    multiselect.multi_select_cases(case_count=1)
    multiselect.continue_to_proceed_multiselect()
    webapps.open_form(MultiSelectUserInput.does_nothing_form)
    webapps.submit_the_form()


@pytest.mark.skip(reason="Failing on prod: https://dimagi-dev.atlassian.net/browse/SUPPORT-16271")
def test_case_05_multiselect_disabled_select_parent_first(driver, settings):
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.yet_another_show_NMS)
    webapps.search_button_on_case_search_page()
    webapps.select_first_case_on_list_and_continue()
    webapps.open_form(MultiSelectUserInput.update_shows_multi_form)
    webapps.submit_the_form()


def test_case_06_parent_multi_child_nonmulti(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    """"Parent multi, child non-multi"""
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.shows_MS_SPFO)
    multiselect.multi_select_cases(case_count=3)
    multiselect.continue_to_proceed_multiselect()
    webapps.search_button_on_case_search_page()
    multiselect.multi_select_cases(case_count=3)
    multiselect.continue_to_proceed_multiselect()
    webapps.open_form(MultiSelectUserInput.another_shows_non)
    webapps.select_first_case_on_list_and_continue()
    webapps.open_form(MultiSelectUserInput.update_show_normal_form)
    webapps.submit_the_form()


def test_case_07_parent_multi_child_multi(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    """ Parent multi, child multi"""
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.shows_MS_SPFO)
    multiselect.multi_select_cases(case_count=2)
    multiselect.continue_to_proceed_multiselect()
    webapps.search_button_on_case_search_page()
    cases_selected = multiselect.multi_select_cases(case_count=2)
    multiselect.continue_to_proceed_multiselect()
    webapps.open_form(MultiSelectUserInput.child_shows_SF_MS)
    webapps.search_button_on_case_search_page()
    multiselect.multi_select_cases(case_count=1)
    multiselect.continue_to_proceed_multiselect()
    multiselect.check_selected_cases_present_on_form(cases_selected, case_type=SHOW)
    webapps.submit_the_form()


def test_case_08_parent_nonmulti_child_multi(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    """Parent non-multi, child multi"""
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.yet_another_show_NMS)
    multiselect.multi_select_cases(case_count=3)
    multiselect.continue_to_proceed_multiselect()
    webapps.search_button_on_case_search_page()
    webapps.select_first_case_on_list_and_continue()
    webapps.open_form(MultiSelectUserInput.another_shows_MS)
    webapps.search_button_on_case_search_page()
    cases_selected = multiselect.multi_select_cases(case_count=3)
    multiselect.continue_to_proceed_multiselect()
    multiselect.check_selected_cases_present_on_form(cases_selected, case_type=SHOW)
    webapps.submit_the_form()


def test_case_09_parent_nonmulti_child_nonmulti(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    """Parent non-multi, child non-multi"""
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.yet_another_show_NMS)
    multiselect.multi_select_cases(case_count=3)
    multiselect.continue_to_proceed_multiselect()
    webapps.search_button_on_case_search_page()
    webapps.select_first_case_on_list_and_continue()
    webapps.open_form(MultiSelectUserInput.another_shows_not_MS)
    webapps.submit_the_form()


def test_case_10_multiselect_with_shadow_menus(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    """source menu that has multiselect enabled"""
    webapps.open_menu(MultiSelectUserInput.shadow_menu_multi)
    cases_selected = multiselect.multi_select_cases(case_count=3)
    multiselect.continue_to_proceed_multiselect()
    webapps.open_form(MultiSelectUserInput.update_song_normal_form)
    multiselect.check_selected_cases_present_on_form(cases_selected, case_type=SONG)
    webapps.answer_repeated_questions(question_label=CaseSearchUserInput.add_show_question,
                                      input_type=textarea,
                                      input_value=fetch_random_string())
    webapps.submit_the_form()
    """Check EOF: To other menu (Form Linking)"""
    casesearch.check_eof_navigation(eof_nav=MENU,
                                    menu=MultiSelectUserInput.shadow_menu_multi)
    """source menu that has multiselect disabled"""
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.songs_Non_Multi)
    webapps.select_first_case_on_list_and_continue()
    webapps.submit_the_form()


def test_case_11_multiselect_form_linking(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_2)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.songs_MS_SF_IS)
    webapps.search_button_on_case_search_page()
    multiselect.multi_select_cases(case_count=2)
    multiselect.continue_to_proceed_multiselect()
    webapps.open_form(MultiSelectUserInput.update_song_back_to_other_form)
    webapps.answer_repeated_questions(question_label=CaseSearchUserInput.add_show_question,
                                      input_type=textarea,
                                      input_value=fetch_random_string())
    webapps.submit_the_form()
    """Check EOF to menu"""
    casesearch.check_eof_navigation(eof_nav=MENU,
                                    menu=MultiSelectUserInput.does_nothing_form)


def test_case_12_multiselect_with_case_search_workflows(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    """Normal"""
    webapps.open_menu(MultiSelectUserInput.songs_multi_normal)
    multiselect.multi_select_cases(case_count=1)
    multiselect.continue_to_proceed_multiselect()
    webapps.open_form(MultiSelectUserInput.update_song_normal_form)
    webapps.answer_repeated_questions(question_label=CaseSearchUserInput.add_show_question,
                                      input_type=textarea,
                                      input_value=fetch_random_string())
    webapps.submit_the_form()
    """Search First"""
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.songs_multi_search_first)
    webapps.search_button_on_case_search_page()
    multiselect.multi_select_cases(case_count=1)
    multiselect.continue_to_proceed_multiselect()
    webapps.open_form(MultiSelectUserInput.update_song_back_to_menu_form)
    webapps.answer_repeated_questions(question_label=CaseSearchUserInput.add_show_question,
                                      input_type=textarea,
                                      input_value=fetch_random_string())
    webapps.submit_the_form()
    """Skip ES"""
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.songs_multi_skip_es)
    multiselect.multi_select_cases(case_count=1)
    multiselect.continue_to_proceed_multiselect()
    webapps.open_form(MultiSelectUserInput.update_song_normal_form)
    webapps.answer_repeated_questions(question_label=CaseSearchUserInput.add_show_question,
                                      input_type=textarea,
                                      input_value=fetch_random_string())
    webapps.submit_the_form()
    """See More"""
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.songs_multi_see_more)
    multiselect.multi_select_cases(case_count=1)
    multiselect.continue_to_proceed_multiselect()
    webapps.open_form(MultiSelectUserInput.update_song_normal_form)
    webapps.answer_repeated_questions(question_label=CaseSearchUserInput.add_show_question,
                                      input_type=textarea,
                                      input_value=fetch_random_string())
    webapps.submit_the_form()


def test_case_13_multiselect_with_display_only_forms(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.display_only_forms)
    multiselect.click_select_all_checkbox()
    multiselect.continue_to_proceed_multiselect()
    multiselect.multi_select_cases(case_count=1)
    multiselect.continue_to_proceed_multiselect()
    webapps.submit_the_form()


def test_case_14_eof_nav_to_single_select_menu(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.shows_MS_SPFP)
    casename = webapps.omni_search(CaseSearchUserInput.song_auto_parent)
    webapps.select_case(casename)
    casesearch.search_against_property(search_property=CaseSearchUserInput.artist_city,
                                       input_value=CaseSearchUserInput.show_auto,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    multiselect.multi_select_cases(case_count=1)
    multiselect.continue_to_proceed_multiselect()
    webapps.open_form(MultiSelectUserInput.update_show_to_single_select)
    webapps.submit_the_form()
    """Eof Navigation"""
    casesearch.check_eof_navigation(eof_nav=MENU,
                                    menu=MultiSelectUserInput.single_select_no_parent)
    webapps.select_first_case_on_list_and_continue()
    webapps.submit_the_form()


def test_case_15_eof_nav_to_form_on_single_select_menu(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.shows_MS_SPFP)
    casename = webapps.omni_search(CaseSearchUserInput.song_auto_parent)
    webapps.select_case(casename)
    casesearch.search_against_property(search_property=CaseSearchUserInput.artist_city,
                                       input_value=CaseSearchUserInput.show_auto,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    multiselect.multi_select_cases(case_count=1)
    multiselect.continue_to_proceed_multiselect()
    webapps.open_form(MultiSelectUserInput.update_show_to_form_on_single_select)
    webapps.submit_the_form()
    """Eof Navigation"""
    casesearch.check_eof_navigation(eof_nav=FORM,
                                    menu=MultiSelectUserInput.does_nothing_form)
    webapps.submit_the_form()


def test_case_16_multiselect_with_case_tiles(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.multi_select_with_case_tiles)
    webapps.search_all_cases()
    webapps.clear_and_search_all_cases_on_case_search_page()
    cases_selected = multiselect.multi_select_case_tiles(case_count=1)
    multiselect.continue_to_proceed_multiselect()
    multiselect.check_selected_cases_present_on_form(cases_selected, case_type=SONG)
    webapps.answer_repeated_questions(question_label=CaseSearchUserInput.add_show_question,
                                      input_type=textarea,
                                      input_value=fetch_random_string())
    webapps.submit_the_form()


def test_case_17_multiselect_enabled_select_parent_first(driver, settings):
    if 'www' in settings['url']:
        pytest.skip("Production has a linked app")
    multiselect = MultiSelectWorkflows(driver)
    menu = HomePage(driver, settings)
    menu.applications_menu(MultiSelectUserInput.multiselect_app_name)
    multiselect.open_menu_settings(MultiSelectUserInput.shows_MS_SPFP)
    multiselect.check_if_value_present_in_drop_down(MultiSelectUserInput.shows_MS_SPFO, match=NO)
    multiselect.open_menu_settings(MultiSelectUserInput.shows_MS_SPFO)
    multiselect.check_if_value_present_in_drop_down(MultiSelectUserInput.shows_MS_SPFP, match=YES)

