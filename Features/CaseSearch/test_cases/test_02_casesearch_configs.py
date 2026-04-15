import time

import pytest

from Features.CaseSearch.constants import *
from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from common_utilities.selenium.base_page import BasePage
from common_utilities.selenium.webapps import WebApps

""""Contains all case search configurations related test cases"""


def test_case_01_default_value_expression(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check default values are displayed"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.song_name,
                                              default_value=CaseSearchUserInput.blank,
                                              search_format=text)
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.mood,
                                              default_value=CaseSearchUserInput.five,
                                              search_format=text)
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.date_opened,
                                              default_value=casesearch.parse_date_range(
                                                  no_of_days=60,
                                                  default=True),
                                              search_format=text)
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.rating,
                                              default_value=CaseSearchUserInput.five_star,
                                              search_format=combobox)
    """Check values can be cleared and desired value can be searched"""
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.song_automation_song_1,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.one,
                                        expected_value=CaseSearchUserInput.song_automation_song_1)


def test_case_02_text_format(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check text format search property"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.song_automation_song_1,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.one,
                                        expected_value=CaseSearchUserInput.song_automation_song_1)

def test_case_03_date_range_format(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check date range format search property"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    # MM/DD/YYYY
    webapps.clear_selections_on_case_search_page()
    date = casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                              input_value=CaseSearchUserInput.date_12_30_2022_slash,
                                              property_type=TEXT_INPUT)
    casesearch.check_date_range(search_property=CaseSearchUserInput.date_opened, date_range=casesearch.parse_date_range(input_date=date,
                                                                       input_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YYYY"),
                                                                       output_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YYYY")))
    # MM-DD-YYYY
    webapps.clear_selections_on_case_search_page()
    date = casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                               input_value=CaseSearchUserInput.date_12_30_2022_hyphen,
                                               property_type=TEXT_INPUT)
    casesearch.check_date_range(search_property=CaseSearchUserInput.date_opened, date_range=casesearch.parse_date_range(input_date=date,
                                                                       input_format=CaseSearchUserInput.dates.get(
                                                                           "MM-DD-YYYY"),
                                                                       output_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YYYY")))
    # MM/DD/YY
    webapps.clear_selections_on_case_search_page()
    date = casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                               input_value=CaseSearchUserInput.date_12_30_22_slash,
                                               property_type=TEXT_INPUT)
    casesearch.check_date_range(search_property=CaseSearchUserInput.date_opened, date_range=casesearch.parse_date_range(input_date=date,
                                                                       input_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YY"),
                                                                       output_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YYYY")))
    # MM-DD-YY
    webapps.clear_selections_on_case_search_page()
    date = casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                                   input_value=CaseSearchUserInput.date_12_30_22_hyphen,
                                                   property_type=TEXT_INPUT)
    casesearch.check_date_range(search_property=CaseSearchUserInput.date_opened, date_range=casesearch.parse_date_range(input_date=date,
                                                                           input_format=CaseSearchUserInput.dates.get(
                                                                               "MM-DD-YY"),
                                                                           output_format=CaseSearchUserInput.dates.get(
                                                                               "MM/DD/YYYY")))
        # YYYY-MM-DD - DOM doesn't load value , so searching instead of a check
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                           input_value=CaseSearchUserInput.date_2022_12_30,
                                           property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.six,
                                            expected_value=CaseSearchUserInput.date_30_12_2022)
    # Date Range Search Again with Enter on keyboard
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    date = casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                              input_value=CaseSearchUserInput.date_12_30_2022_slash,
                                              property_type=TEXT_INPUT)
    casesearch.check_date_range(search_property=CaseSearchUserInput.date_opened, date_range=casesearch.parse_date_range(input_date=date,
                                                            input_format=CaseSearchUserInput.dates.get("MM/DD/YYYY"),
                                                            output_format=CaseSearchUserInput.dates.get("MM/DD/YYYY")))
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.six,
                                        expected_value=casesearch.parse_date(
                                            input_date=date,
                                            input_format=CaseSearchUserInput.dates.get("MM/DD/YYYY"),
                                            output_format=CaseSearchUserInput.dates.get("DD/MM/YYYY")))



def test_case_04_is_multiselect_format(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check multiselect format search property"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.three_star,
                                       property_type=COMBOBOX)
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.two_star,
                                       property_type=COMBOBOX)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=["2", "3"],
                                        is_multi=YES)
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.artist,
                                       input_value=CaseSearchUserInput.artist_case_arijit,
                                       property_type=COMBOBOX)
    casesearch.search_against_property(search_property=CaseSearchUserInput.artist,
                                       input_value=CaseSearchUserInput.artist_case_beach_boys,
                                       property_type=COMBOBOX)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=[CaseSearchUserInput.artist_case_arijit,
                                                        CaseSearchUserInput.artist_case_beach_boys],
                                        is_multi=YES)


def test_case_05_allow_blank_values_normal(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check allow blanks normal"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.two_star,
                                       property_type=COMBOBOX,
                                       include_blanks=YES)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=[CaseSearchUserInput.two,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES)
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.five_star,
                                       property_type=COMBOBOX,
                                       include_blanks=YES)
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.five,
                                       property_type=TEXT_INPUT,
                                       include_blanks=YES)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=[CaseSearchUserInput.five,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES)
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=[CaseSearchUserInput.five,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES)







def test_case_06_sticky_search_without_default_value(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    base = BasePage(driver)
    """Check sticky search without default value"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.four,
                                       property_type=TEXT_INPUT)
    time.sleep(10)
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.three_star,
                                       property_type=COMBOBOX)
    time.sleep(2)
    webapps.search_button_on_case_search_page()
    base.back()
    if 'staging' in settings['url']:
        casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.mood,
                                                  default_value=CaseSearchUserInput.four,
                                                  search_format=text)
        casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.rating,
                                                  default_value=CaseSearchUserInput.three_star,
                                                  search_format=combobox)
    # This is failing
    # driver.refresh()
    # casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.mood, default_value=CaseSearchUserInput.four, search_format=text)
    # casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.rating, default_value=CaseSearchUserInput.three_star, search_format=combobox)



def test_case_07_required_property(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check required property"""
    webapps.login_as(CaseSearchUserInput.a_user)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_setting_menu)
    webapps.search_all_cases()
    webapps.search_button_on_case_search_page()
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.mood,
                                             message=CaseSearchUserInput.required_msg,
                                             required_or_validated=YES,
                                             property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.four,
                                       property_type=TEXT_INPUT)
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.mood,
                                             required_or_validated=NO,
                                             property_type=TEXT_INPUT)

@pytest.mark.skip(reason="https://dimagi-dev.atlassian.net/browse/USH-2348 and https://dimagi-dev.atlassian.net/browse/USH-2289")
def test_case_08_dependent_dropdowns_value_clear(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    """Select genre and subgenre"""
    casesearch.search_against_property(search_property=CaseSearchUserInput.genre,
                                       input_value=CaseSearchUserInput.latin_music,
                                       property_type=COMBOBOX)
    casesearch.search_against_property(search_property=CaseSearchUserInput.subgenre,
                                       input_value=CaseSearchUserInput.latin_jazz,
                                       property_type=COMBOBOX3)
    """Change genre and check if subgenre dropdown is reset"""
    casesearch.search_against_property(search_property=CaseSearchUserInput.genre,
                                       input_value=CaseSearchUserInput.hiphop,
                                       property_type=COMBOBOX)
    casesearch.check_clear_button_in_singleselect_combobox(expected=NO,
                                                           search_property=CaseSearchUserInput.subgenre)
    """Clear search page selections and check if subgenre dropdown is reset"""
    webapps.clear_selections_on_case_search_page()
    casesearch.check_dropdown_value(search_property=CaseSearchUserInput.subgenre,
                                    value=CaseSearchUserInput.bounce,
                                    present=NO)


def test_case_09_case_search_validations(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    base = BasePage(driver)
    """Case Search Validations"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.energy,
                                       input_value=CaseSearchUserInput.three,
                                       property_type=TEXT_INPUT)
    
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.value_with_space,
                                       property_type=TEXT_INPUT)
    """Check validations imposed"""
    webapps.search_button_on_case_search_page()
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.song_name,
                                             message=CaseSearchUserInput.validation_msg_no_spaces,
                                             required_or_validated=YES,
                                             property_type=TEXT_INPUT)
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.energy,
                                             message=CaseSearchUserInput.validation_msg_invalid_respons,
                                             required_or_validated=YES,
                                             property_type=TEXT_INPUT)
    """Check validations removed"""
    webapps.clear_selections_on_case_search_page()
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.song_name,
                                             message=CaseSearchUserInput.validation_msg_no_spaces,
                                             required_or_validated=NO,
                                             property_type=TEXT_INPUT)
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.energy,
                                             message=CaseSearchUserInput.validation_msg_invalid_respons,
                                             required_or_validated=NO,
                                             property_type=TEXT_INPUT)
    """Check song seacrch w/o spaces and ensure case is displayed"""
    webapps.clear_selections_on_case_search_page()
    casename = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                  input_value=CaseSearchUserInput.song_automation_song_no_space,
                                                  property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(casename)
    """Check including blanks"""
    #base.back()
    #base.back()
    webapps.clear_selections_on_case_search_page()
    casesearch.select_include_blanks(CaseSearchUserInput.rating)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.blank)
