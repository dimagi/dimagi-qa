from Features.CaseSearch.constants import TEXT_INPUT
from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from common_utilities.selenium.webapps import WebApps

""""Contains all case search workflow related test cases"""


def test_case_01_normal_workflow(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Checks if user can submit a form for normal search"""
    webapps.login_as(CaseSearchUserInput.user_2)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    case_name = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                   input_value=CaseSearchUserInput.song_automation_song_1,
                                                   property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(case_name)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()
    """Checks if claim successful"""
    webapps.navigate_to_breadcrumb(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.omni_search(case_name)


def test_case_02_normal_workflow_search_again(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Checks if user can submit a form for normal search when re-searched"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.search_all_cases()
    webapps.clear_and_search_all_cases_on_case_search_page()
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    case_name = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                   input_value=CaseSearchUserInput.song_automation_song_1,
                                                   property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(case_name)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()
    """Checks if claim successful"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.omni_search(case_name)


def test_case_03_search_first(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Checks if user can submit a form for search first"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    case_name = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                   input_value=CaseSearchUserInput.song_automation_song_1,
                                                   property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(case_name)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()


def test_case_04_search_first_search_again(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Checks if user can submit a form for search first when re-searched"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_and_search_all_cases_on_case_search_page()
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    case_name = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                   input_value=CaseSearchUserInput.song_automation_song_1,
                                                   property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(case_name)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()

def test_case_05_see_more(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Checks if user can submit a form for see more"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.see_more_menu)
    webapps.search_all_cases()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.ratings.get(CaseSearchUserInput.five_star))
    if 'www' in settings['url']:
        case_name = webapps.omni_search(CaseSearchUserInput.song_just_babe)
    else:
        case_name = webapps.omni_search(CaseSearchUserInput.song_123)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()


def test_case_06_see_more_search_again(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Checks if user can submit a form for see more when re-searched"""
    webapps.login_as(CaseSearchUserInput.user_2)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.see_more_menu)
    webapps.search_all_cases()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.ratings.get(CaseSearchUserInput.five_star))
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.song_automation_song_1,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    case_name = webapps.omni_search(CaseSearchUserInput.song_automation_song_1)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()


def test_case_07_skip_to_default_search(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Checks if user can submit a form for skip to default search"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.skip_default_menu)
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.ratings.get(CaseSearchUserInput.five_star))
    if 'www' in settings['url']:
        case_name = webapps.omni_search(CaseSearchUserInput.song_just_babe)
    else:
        case_name = webapps.omni_search(CaseSearchUserInput.song_123)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()


def test_case_08_skip_to_default_search_seach_again(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Checks if user can submit a form for skip to default search when re-searched """
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.skip_default_menu)
    webapps.search_again_cases()
    webapps.clear_and_search_all_cases_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.ratings.get(CaseSearchUserInput.five_star))
    if 'www' in settings['url']:
        case_name = webapps.omni_search(CaseSearchUserInput.song_just_babe)
    else:
        case_name = webapps.omni_search(CaseSearchUserInput.song_123)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()
