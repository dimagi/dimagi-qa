from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from Features.MultiSelect.test_pages.multiselect_page import MultiSelectWorkflows
from Features.MultiSelect.user_inputs.multiselect_user_inputs import MultiSelectUserInput
from common_utilities.generate_random_string import fetch_random_string
from common_utilities.selenium.webapps import WebApps
from Features.CaseSearch.constants import *

""""Contains all auto-select plus multi-select related test cases"""


def test_case_01_max_selected_values_for_auto_selection(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.songs_auto)
    webapps.open_form(MultiSelectUserInput.update_song_normal_form)
    multiselect.check_no_of_cases_on_form(100,  str(SONG).lower())
    driver.back()
    webapps.open_form(MultiSelectUserInput.does_nothing_form)
    webapps.submit_the_form()
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.songs_auto_max_limit, 'No')
    multiselect.check_error_message_shown_for_max_limit_exceed()


def test_case_02_max_selected_values_for_manual_selection(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.songs_manual)
    multiselect.multi_select_cases(case_count=6)
    multiselect.continue_to_proceed_multiselect()
    multiselect.check_error_message_shown_for_max_limit_exceed()
    # Deselect selections
    multiselect.click_select_all_checkbox()
    multiselect.click_select_all_checkbox()
    multiselect.close_all_alerts()
    cases_selected = multiselect.multi_select_cases(case_count=2)
    multiselect.continue_to_proceed_multiselect()
    multiselect.check_selected_cases_present_on_form(cases_selected, case_type=SONG)
    webapps.answer_repeated_questions(question_label=CaseSearchUserInput.add_show_question,
                                      input_type=textarea,
                                      input_value=fetch_random_string())
    webapps.submit_the_form()


def test_case_03_auto_select_display_only_forms(driver, settings):
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.display_only_forms_auto)
    webapps.submit_the_form()


def test_case_04_auto_select_shadow_menus(driver, settings):
    multiselect = MultiSelectWorkflows(driver)
    webapps = WebApps(driver, settings)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(MultiSelectUserInput.multiselect_app_name)
    webapps.open_menu(MultiSelectUserInput.shadow_auto)
    webapps.open_form(MultiSelectUserInput.update_song_normal_form)
    multiselect.check_no_of_cases_on_form(100, SONG)
    driver.back()
    webapps.open_form(MultiSelectUserInput.does_nothing_form)
    webapps.submit_the_form()

