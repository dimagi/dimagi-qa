import time

import pytest

from Features.CaseSearch.constants import *
from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from common_utilities.selenium.webapps import WebApps
from common_utilities.selenium.base_page import BasePage


""""Contains all case search configurations related test cases"""


def test_case_01_default_value_expression(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check default values are displayed"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.song_name,
                                              default_value=CaseSearchUserInput.default,
                                              search_format=text
                                              )
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.mood,
                                              default_value=CaseSearchUserInput.three,
                                              search_format=text
                                              )
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.date_opened,
                                              default_value=casesearch.parse_date_range(
                                                  no_of_days=60,
                                                  default=True
                                                  ),
                                              search_format=text
                                              )
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.rating,
                                              default_value=CaseSearchUserInput.four_star,
                                              search_format=combobox
                                              )
    """Check values can be cleared and desired value can be searched"""
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.song_automation_song_1,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.one,
                                        expected_value=CaseSearchUserInput.song_automation_song_1
                                        )


def test_case_02_help_text(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check help text shows up"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    casesearch.check_help_text(search_property=CaseSearchUserInput.mood,
                               help_text_value=CaseSearchUserInput.mood_help_text
                               )


def test_case_03_text_format(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check text format search property"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.song_automation_song_1,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.one,
                                        expected_value=CaseSearchUserInput.song_automation_song_1
                                        )


def test_case_04_barcode_format(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check barcode format search property"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.three,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=CaseSearchUserInput.three
                                        )


def test_case_05_date_range_format(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    base = BasePage(driver)
    """Check date range format search property"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    # MM/DD/YYYY
    webapps.clear_selections_on_case_search_page()
    date = casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                              input_value=CaseSearchUserInput.date_08_16_2023_slash,
                                              property_type=TEXT_INPUT
                                              )
    casesearch.check_date_range(search_property=CaseSearchUserInput.date_opened,
                                date_range=casesearch.parse_date_range(input_date=date,
                                                                       input_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YYYY"
                                                                           ),
                                                                       output_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YYYY"
                                                                           )
                                                                       )
                                )
    # MM-DD-YYYY
    webapps.clear_selections_on_case_search_page()
    date = casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                              input_value=CaseSearchUserInput.date_08_16_2023_hyphen,
                                              property_type=TEXT_INPUT
                                              )
    casesearch.check_date_range(search_property=CaseSearchUserInput.date_opened,
                                date_range=casesearch.parse_date_range(input_date=date,
                                                                       input_format=CaseSearchUserInput.dates.get(
                                                                           "MM-DD-YYYY"
                                                                           ),
                                                                       output_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YYYY"
                                                                           )
                                                                       )
                                )
    # MM/DD/YY
    webapps.clear_selections_on_case_search_page()
    date = casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                              input_value=CaseSearchUserInput.date_08_16_23_slash,
                                              property_type=TEXT_INPUT
                                              )
    casesearch.check_date_range(search_property=CaseSearchUserInput.date_opened,
                                date_range=casesearch.parse_date_range(input_date=date,
                                                                       input_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YY"
                                                                           ),
                                                                       output_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YYYY"
                                                                           )
                                                                       )
                                )
    # MM-DD-YY
    webapps.clear_selections_on_case_search_page()
    date = casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                              input_value=CaseSearchUserInput.date_08_16_23_hyphen,
                                              property_type=TEXT_INPUT
                                              )
    casesearch.check_date_range(search_property=CaseSearchUserInput.date_opened,
                                date_range=casesearch.parse_date_range(input_date=date,
                                                                       input_format=CaseSearchUserInput.dates.get(
                                                                           "MM-DD-YY"
                                                                           ),
                                                                       output_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YYYY"
                                                                           )
                                                                       )
                                )
    # YYYY-MM-DD - DOM doesn't load value , so searching instead of a check
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                       input_value=CaseSearchUserInput.date_2023_08_16,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.six,
                                        expected_value=CaseSearchUserInput.date_16_08_2023
                                        )
    base.back()
    casesearch.reload_page()
    # Date Range Search Again with Enter on keyboard
    webapps.clear_selections_on_case_search_page()
    date = casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                              input_value=CaseSearchUserInput.date_08_16_2023_slash,
                                              property_type=TEXT_INPUT
                                              )
    casesearch.check_date_range(search_property=CaseSearchUserInput.date_opened,
                                date_range=casesearch.parse_date_range(input_date=date,
                                                                       input_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YYYY"
                                                                           ),
                                                                       output_format=CaseSearchUserInput.dates.get(
                                                                           "MM/DD/YYYY"
                                                                           )
                                                                       )
                                )
    if 'staging' in settings['url']:
        webapps.search_button_on_case_search_page()
    else:
        webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.six,
                                        expected_value=casesearch.parse_date(
                                            input_date=date,
                                            input_format=CaseSearchUserInput.dates.get("MM/DD/YYYY"),
                                            output_format=CaseSearchUserInput.dates.get("DD/MM/YYYY")
                                            )
                                        )


def test_case_06_lookup_table_format(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check lookup table format search property"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.two_star,
                                       property_type=COMBOBOX
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.ratings.get(CaseSearchUserInput.two_star)
                                        )


def test_case_07_address_geocoder_format(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    base = BasePage(driver)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    """Check receivers in form get autopoulated after bradcast value is provided"""
    webapps.open_menu(CaseSearchUserInput.artist_menu)
    webapps.select_first_case_on_list_and_continue()
    webapps.open_form(CaseSearchUserInput.add_address_form)
    casesearch.add_address(address=CaseSearchUserInput.full_home_address,
                           search_property=CaseSearchUserInput.search_home_address
                           )
    webapps.open_data_preview()
    webapps.present_in_data_preview(CaseSearchUserInput.home_street_value)
    webapps.present_in_data_preview(CaseSearchUserInput.home_city_value)
    webapps.present_in_data_preview(CaseSearchUserInput.home_country_value)
    webapps.present_in_data_preview(CaseSearchUserInput.home_zipcode_value)
    """Check geocoder format search property"""
    base.back()
    time.sleep(4)
    base.back()
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.assert_address_is_hidden(CaseSearchUserInput.home_street)
    casesearch.add_address(address=CaseSearchUserInput.full_home_address,
                           search_property=CaseSearchUserInput.search_home_address
                           )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=CaseSearchUserInput.home_street_value
                                        )
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=CaseSearchUserInput.home_city_value
                                        )
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.five,
                                        expected_value=CaseSearchUserInput.home_country_value
                                        )
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.six,
                                        expected_value=CaseSearchUserInput.home_zipcode_value
                                        )


def test_case_08_mobile_ucr_format(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check mobile ucr format search property"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.artist,
                                       input_value=CaseSearchUserInput.artist_case_arijit,
                                       property_type=COMBOBOX
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=CaseSearchUserInput.artist_case_arijit
                                        )


def test_case_09_single_date_format(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check single date format search property"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    song = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                              input_value=CaseSearchUserInput.song_automation_song,
                                              property_type=TEXT_INPUT)
    date = casesearch.search_against_property(search_property=CaseSearchUserInput.song_release_date,
                                              input_value=CaseSearchUserInput.date_2022_12_30,
                                              property_type=TEXT_INPUT
                                              )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.eight,
                                        expected_value=casesearch.parse_date(
                                            input_date=date,
                                            input_format=CaseSearchUserInput.dates.get("YYYY-MM-DD"),
                                            output_format=CaseSearchUserInput.dates.get("DD-MM-YYYY")))


def test_case_10_is_multiselect_format(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    """Check multiselect format search property"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.three_star,
                                       property_type=COMBOBOX
                                       )
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.two_star,
                                       property_type=COMBOBOX
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=["2", "3"],
                                        is_multi=YES
                                        )
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.artist,
                                       input_value=CaseSearchUserInput.artist_case_arijit,
                                       property_type=COMBOBOX
                                       )
    casesearch.search_against_property(search_property=CaseSearchUserInput.artist,
                                       input_value=CaseSearchUserInput.artist_case_beach_boys,
                                       property_type=COMBOBOX
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=[CaseSearchUserInput.artist_case_arijit,
                                                        CaseSearchUserInput.artist_case_beach_boys],
                                        is_multi=YES
                                        )


def test_case_11_allow_blank_values_normal(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check allow blanks normal"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.two_star,
                                       property_type=COMBOBOX,
                                       include_blanks=YES
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=[CaseSearchUserInput.two,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES
                                        )
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.five_star,
                                       property_type=COMBOBOX,
                                       include_blanks=YES
                                       )
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.five,
                                       property_type=TEXT_INPUT,
                                       include_blanks=YES
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=[CaseSearchUserInput.five,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES
                                        )
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=[CaseSearchUserInput.five,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES
                                        )


def test_case_12_allow_blank_values_geocoder(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check allow blanks geocoder"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.artist_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.home_country,
                                       input_value=CaseSearchUserInput.home_country_belgium,
                                       property_type=TEXT_INPUT,
                                       include_blanks=YES
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.five,
                                        expected_value=[CaseSearchUserInput.home_country_belgium,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES
                                        )


def test_case_13_allow_blank_values_others(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    """Check allow blanks all formats"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                       input_value=CaseSearchUserInput.date_2023_08_16,
                                       property_type=TEXT_INPUT,
                                       include_blanks=YES
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.six,
                                        expected_value=[CaseSearchUserInput.date_16_08_2023,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES
                                        )
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.artist,
                                       input_value=CaseSearchUserInput.artist_case_arijit,
                                       property_type=COMBOBOX,
                                       include_blanks=YES
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=[CaseSearchUserInput.artist_case_arijit,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES
                                        )


def test_case_14_exclude_property_from_case_search(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check exclude property from case search"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.exclude_property_from_case_search_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.one,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=CaseSearchUserInput.four,
                                        is_multi=YES
                                        )
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.four,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=[CaseSearchUserInput.one,
                                                        CaseSearchUserInput.two,
                                                        CaseSearchUserInput.three,
                                                        CaseSearchUserInput.four,
                                                        CaseSearchUserInput.five],
                                        is_multi=YES
                                        )


def test_case_15_sticky_search_without_default_value(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    base = BasePage(driver)
    """Check sticky search without default value"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.four,
                                       property_type=TEXT_INPUT
                                       )
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.three_star,
                                       property_type=COMBOBOX
                                       )
    webapps.search_button_on_case_search_page()
    base.back()
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.mood,
                                              default_value=CaseSearchUserInput.four,
                                              search_format=text
                                              )
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.rating,
                                              default_value=CaseSearchUserInput.three_star,
                                              search_format=combobox
                                              )
    # This is failing
    # driver.refresh()
    # casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.mood, default_value=CaseSearchUserInput.four, search_format=text)
    # casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.rating, default_value=CaseSearchUserInput.three_star, search_format=combobox)


def test_case_16_sticky_search_with_default_value(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check sticky search with default value"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.search_button_on_case_search_page()
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.mood,
                                              default_value=CaseSearchUserInput.three,
                                              search_format=text
                                              )
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.four,
                                       property_type=TEXT_INPUT
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=CaseSearchUserInput.four
                                        )
    webapps.navigate_to_breadcrumb(CaseSearchUserInput.search_first_menu)
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.mood,
                                              default_value=CaseSearchUserInput.three,
                                              search_format=text
                                              )


def test_case_17_required_property(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check required property"""
    webapps.login_as(CaseSearchUserInput.a_user)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_setting_menu)
    webapps.search_all_cases()
    webapps.search_button_on_case_search_page()
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.mood,
                                             message=CaseSearchUserInput.required_msg,
                                             required_or_validated=YES,
                                             property_type=TEXT_INPUT
                                             )
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.four,
                                       property_type=TEXT_INPUT
                                       )
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.mood,
                                             required_or_validated=NO,
                                             property_type=TEXT_INPUT
                                             )


def test_case_18_conditionally_required_condition_property(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check conditionally required condition property"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    """Check enabled"""
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.two_star,
                                       property_type=COMBOBOX
                                       )
    webapps.search_button_on_case_search_page()
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.subgenre,
                                             message=CaseSearchUserInput.required_msg_if_rating_two,
                                             required_or_validated=YES,
                                             property_type=COMBOBOX
                                             )
    """Check disabled"""
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.three_star,
                                       property_type=COMBOBOX
                                       )
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.subgenre,
                                             message=CaseSearchUserInput.required_msg_if_rating_two,
                                             required_or_validated=NO,
                                             property_type=COMBOBOX
                                             )
    """Check form submission"""
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.two_star,
                                       property_type=COMBOBOX
                                       )
    casesearch.search_against_property(search_property=CaseSearchUserInput.genre,
                                       input_value=CaseSearchUserInput.latin_music,
                                       property_type=COMBOBOX
                                       )
    casesearch.search_against_property(search_property=CaseSearchUserInput.subgenre,
                                       input_value=CaseSearchUserInput.latin_jazz,
                                       property_type=COMBOBOX
                                       )
    webapps.search_button_on_case_search_page()
    webapps.select_case_and_continue(CaseSearchUserInput.song_automation_song_24)
    webapps.open_form(CaseSearchUserInput.update_song_form)
    webapps.submit_the_form()


def test_case_19_json_property_function(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check json property funtion"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.artist_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    case_name = casesearch.search_against_property(search_property=CaseSearchUserInput.artist,
                                                   input_value=CaseSearchUserInput.automation_artist_1,
                                                   property_type=TEXT_INPUT
                                                   )
    webapps.search_button_on_case_search_page()
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.add_address_form)
    casesearch.add_address(address=CaseSearchUserInput.full_home_address,
                           search_property=CaseSearchUserInput.search_home_address
                           )
    casesearch.add_address(address=CaseSearchUserInput.full_work_address,
                           search_property=CaseSearchUserInput.search_work_address
                           )
    casesearch.check_value_on_form(city_address=CaseSearchUserInput.home_city_value,
                                   type=HOME
                                   )
    casesearch.check_value_on_form(city_address=CaseSearchUserInput.work_city_value,
                                   type=WORK
                                   )


def test_case_20_case_search_title(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check Case Search Title"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    casesearch.check_search_screen_title_sscs(CaseSearchUserInput.search_title)
    casesearch.check_search_screen_subtitle(CaseSearchUserInput.search_subtitle)
    webapps.navigate_to_breadcrumb(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.skip_default_menu)
    casesearch.check_search_screen_title(title=None)
    # webapps.open_app(CaseSearchUserInput.french_app)
    # webapps.open_menu(CaseSearchUserInput.search_first_menu)
    # casesearch.check_search_screen_title(CaseSearchUserInput.french_search_title)
    # casesearch.check_search_screen_subtitle(CaseSearchUserInput.french_search_subtitle)


def test_case_21_dependent_dropdowns_multiselect_combobox(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check Dependent Dropdowns"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    casesearch.search_against_property(search_property=CaseSearchUserInput.genre,
                                       input_value=CaseSearchUserInput.latin_music,
                                       property_type=COMBOBOX
                                       )
    casesearch.search_against_property(search_property=CaseSearchUserInput.subgenre,
                                       input_value=CaseSearchUserInput.latin_jazz,
                                       property_type=COMBOBOX
                                       )
    """Check other values do not appear in dropdown"""
    casesearch.check_dropdown_value(search_property=CaseSearchUserInput.subgenre,
                                    value=CaseSearchUserInput.funk_metal,
                                    present=NO
                                    )


def test_case_22_dependent_dropdowns_single_select_combobox(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check Dependent Dropdowns Inline Case Search"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.genre,
                                       input_value=CaseSearchUserInput.latin_music,
                                       property_type=COMBOBOX
                                       )
    """Check values that should appear in dropdown"""
    casesearch.search_against_property(search_property=CaseSearchUserInput.subgenre,
                                       input_value=CaseSearchUserInput.latin_jazz,
                                       property_type=COMBOBOX
                                       )
    """Check other values do not appear in dropdown"""
    casesearch.check_dropdown_value(search_property=CaseSearchUserInput.subgenre,
                                    value=CaseSearchUserInput.funk_metal,
                                    present=NO
                                    )
    """Search case and check if corresponding case is displayed"""
    webapps.search_button_on_case_search_page()
    webapps.omni_search(CaseSearchUserInput.song_automation_song_24)


@pytest.mark.skip(
    reason="https://dimagi-dev.atlassian.net/browse/USH-2348 and https://dimagi-dev.atlassian.net/browse/USH-2289"
    )
def test_case_23_dependent_dropdowns_value_clear(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    """Select genre and subgenre"""
    casesearch.search_against_property(search_property=CaseSearchUserInput.genre,
                                       input_value=CaseSearchUserInput.latin_music,
                                       property_type=COMBOBOX
                                       )
    casesearch.search_against_property(search_property=CaseSearchUserInput.subgenre,
                                       input_value=CaseSearchUserInput.latin_jazz,
                                       property_type=COMBOBOX
                                       )
    """Change genre and check if subgenre dropdown is reset"""
    casesearch.search_against_property(search_property=CaseSearchUserInput.genre,
                                       input_value=CaseSearchUserInput.hiphop,
                                       property_type=COMBOBOX
                                       )
    casesearch.check_clear_button_in_singleselect_combobox(expected=NO,
                                                           search_property=CaseSearchUserInput.subgenre
                                                           )
    """Clear search page selections and check if subgenre dropdown is reset"""
    webapps.clear_selections_on_case_search_page()
    casesearch.check_dropdown_value(search_property=CaseSearchUserInput.subgenre,
                                    value=CaseSearchUserInput.bounce,
                                    present=NO
                                    )


def test_case_24_case_search_validations(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Case Search Validations"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.energy,
                                       input_value=CaseSearchUserInput.three,
                                       property_type=TEXT_INPUT
                                       )
    
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.value_with_space,
                                       property_type=TEXT_INPUT
                                       )
    """Check validations imposed"""
    webapps.search_button_on_case_search_page()
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.song_name,
                                             message=CaseSearchUserInput.validation_msg_no_spaces,
                                             required_or_validated=YES,
                                             property_type=TEXT_INPUT
                                             )
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.energy,
                                             message=CaseSearchUserInput.validation_msg_invalid_respons,
                                             required_or_validated=YES,
                                             property_type=TEXT_INPUT
                                             )
    """Check validations removed"""
    webapps.clear_selections_on_case_search_page()
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.song_name,
                                             message=CaseSearchUserInput.validation_msg_no_spaces,
                                             required_or_validated=NO,
                                             property_type=TEXT_INPUT
                                             )
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.energy,
                                             message=CaseSearchUserInput.validation_msg_invalid_respons,
                                             required_or_validated=NO,
                                             property_type=TEXT_INPUT
                                             )
    """Check song seacrch w/o spaces and ensure case is displayed"""
    webapps.clear_selections_on_case_search_page()
    casename = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                  input_value=CaseSearchUserInput.song_automation_song_no_space,
                                                  property_type=TEXT_INPUT
                                                  )
    webapps.search_button_on_case_search_page()
    webapps.omni_search(casename)
    """Check including blanks"""
    webapps.clear_selections_on_case_search_page()
    casesearch.select_include_blanks(CaseSearchUserInput.rating)
    if 'staging' not in settings['url']:
        webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.blank
                                        )


def test_case_25_checkbox_selection(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.checkbox_selection_menu)
    """Check default selections"""
    input_values = casesearch.check_if_checkbox_selected(CaseSearchUserInput.mood, [3, 4])
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=input_values,
                                        is_multi=YES
                                        )
    """Check desired selections"""
    casesearch.check_if_checkbox_selected(CaseSearchUserInput.mood, [3, 4])
    webapps.clear_selections_on_case_search_page()
    input_values = casesearch.select_checkbox(CaseSearchUserInput.mood, [4, 5], select_by_value=index)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=input_values,
                                        is_multi=YES
                                        )
    """Check default filter is applied"""
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.five
                                        )


def test_case_26_checkbox_selection_sticky_search(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    base = BasePage(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.checkbox_selection_menu)
    driver.refresh()
    casesearch.check_if_checkbox_selected(CaseSearchUserInput.mood, [3, 4])
    webapps.search_button_on_case_search_page()
    base.back()
    casesearch.check_if_checkbox_selected(CaseSearchUserInput.mood, [3, 4])


def test_case_27_checkbox_single_selection_dependent_dropdown(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.checkbox_selection_menu)
    webapps.clear_selections_on_case_search_page()
    """Single Checkbox"""
    casesearch.select_checkbox(CaseSearchUserInput.genre, CaseSearchUserInput.latin_music, select_by_value=text)
    """Check related values appear in dropdown"""
    casesearch.search_against_property(search_property=CaseSearchUserInput.subgenre,
                                       input_value=CaseSearchUserInput.latin_jazz,
                                       property_type=COMBOBOX
                                       )
    """Check other values do not appear in dropdown"""
    casesearch.check_dropdown_value(search_property=CaseSearchUserInput.subgenre,
                                    value=CaseSearchUserInput.funk_metal,
                                    present=NO
                                    )
    webapps.search_button_on_case_search_page()
    webapps.select_first_case_on_list_and_continue()
    webapps.submit_the_form()


@pytest.mark.skip(reason="Failing: https://dimagi-dev.atlassian.net/browse/USH-2614")
def test_case_28_checkbox_multiple_selection_dependent_dropdown(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.checkbox_selection_menu)
    webapps.clear_selections_on_case_search_page()
    """Multiple Checkbox"""
    casesearch.select_checkbox(CaseSearchUserInput.genre, CaseSearchUserInput.hiphop, select_by_value=text)
    casesearch.select_checkbox(CaseSearchUserInput.genre, CaseSearchUserInput.latin_music, select_by_value=text)
    casesearch.check_dropdown_value(search_property=CaseSearchUserInput.subgenre,
                                    value=CaseSearchUserInput.latin_jazz,
                                    present=YES
                                    )
    casesearch.check_dropdown_value(search_property=CaseSearchUserInput.subgenre,
                                    value=CaseSearchUserInput.bounce,
                                    present=YES
                                    )
    casesearch.search_against_property(search_property=CaseSearchUserInput.subgenre,
                                       input_value=CaseSearchUserInput.latin_jazz,
                                       property_type=COMBOBOX
                                       )
    webapps.search_button_on_case_search_page()
    webapps.select_first_case_on_list_and_continue()
    webapps.submit_the_form()
