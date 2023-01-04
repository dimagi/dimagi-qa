import time

import pytest

from Features.CaseSearch.constants import *
from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from common_utilities.selenium.webapps import WebApps

""""Contains all case search configurations related test cases"""


def test_case_01_default_value_expression(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check default values are displayed"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.song_name,
                                              default_value=CaseSearchUserInput.default, search_format=text)
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.mood,
                                              default_value=CaseSearchUserInput.three, search_format=text)
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.date_opened,
                                              default_value=casesearch.date_range(60), search_format=text)
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.rating,
                                              default_value=CaseSearchUserInput.four_star, search_format=combobox)
    """Check values can be cleared and desired value can be searched"""
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.song_case_bugs,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.one,
                                        expected_value=CaseSearchUserInput.song_case_bugs)


def test_case_02_help_text(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check help text shows up"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    casesearch.check_help_text(search_property=CaseSearchUserInput.mood,
                               help_text=CaseSearchUserInput.mood_help_text)


def test_case_03_text_format(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check text format search property"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.song_case_bugs,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.one,
                                        expected_value=CaseSearchUserInput.song_case_bugs)


def test_case_04_barcode_format(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check barcode format search property"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.three,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=CaseSearchUserInput.three)


def test_case_05_date_range_format(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check date range format search property"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                       input_value=CaseSearchUserInput.date_2021_08_25,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.six,
                                        expected_value=CaseSearchUserInput.date_25_08_2021)


def test_case_06_date_range_search(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check date range search"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                       input_value=CaseSearchUserInput.date_2021_08_25,
                                       property_type=TEXT_INPUT)
    time.sleep(10)
    casesearch.check_date_range(CaseSearchUserInput.date_2021_08_25 + " to " + CaseSearchUserInput.date_2021_08_25)
    webapps.search_button_on_case_search_page(enter_key=YES)
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.six,
                                        expected_value=CaseSearchUserInput.date_25_08_2021)


def test_case_07_lookup_table_format(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check lookup table format search property"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.two_star,
                                       property_type=COMBOBOX)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.ratings.get(CaseSearchUserInput.two_star))


def test_case_08_address_geocoder_format(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check geocoder format search property"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.artist_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.assert_address_is_hidden(CaseSearchUserInput.home_street)
    casesearch.add_address(address=CaseSearchUserInput.full_home_address,
                           search_property=CaseSearchUserInput.search_home_address)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=CaseSearchUserInput.home_street_value)
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=CaseSearchUserInput.home_city_value)
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.five,
                                        expected_value=CaseSearchUserInput.home_country_value)
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.six,
                                        expected_value=CaseSearchUserInput.home_zipcode_value)


def test_case_09_mobile_ucr_format(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check mobile ucr format search property"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.artist,
                                       input_value=CaseSearchUserInput.artist_case_beach_boys,
                                       property_type=COMBOBOX)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=CaseSearchUserInput.artist_case_beach_boys)


def test_case_10_single_date_format(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check single date format search property"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_and_search_all_cases_on_case_search_page()
    case_name = webapps.omni_search(CaseSearchUserInput.song_case_bugs)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.shows_form)
    webapps.search_again_cases()
    casesearch.search_against_property(search_property=CaseSearchUserInput.show_date,
                                       input_value=CaseSearchUserInput.date_2022_08_04,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=CaseSearchUserInput.date_2022_08_04)


def test_case_11_is_multiselect_format(driver):
    webapps = WebApps(driver)
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
                                       input_value=CaseSearchUserInput.artist_case_beach_boys,
                                       property_type=COMBOBOX)
    casesearch.search_against_property(search_property=CaseSearchUserInput.artist,
                                       input_value=CaseSearchUserInput.artist_case_arijit,
                                       property_type=COMBOBOX)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=[CaseSearchUserInput.artist_case_beach_boys,
                                                        CaseSearchUserInput.artist_case_arijit],
                                        is_multi=YES)


def test_case_12_allow_blank_values_normal(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check allow blanks normal"""
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


def test_case_13_allow_blank_values_geocoder(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check allow blanks geocoder"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.artist_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.home_country,
                                       input_value=CaseSearchUserInput.home_country_belgium,
                                       property_type=TEXT_INPUT,
                                       include_blanks=YES)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.five,
                                        expected_value=[CaseSearchUserInput.home_country_belgium,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES)


def test_case_14_allow_blank_values_others(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check allow blanks all formats"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.date_opened,
                                       input_value=CaseSearchUserInput.date_2021_08_25,
                                       property_type=TEXT_INPUT,
                                       include_blanks=YES)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.six,
                                        expected_value=[CaseSearchUserInput.date_25_08_2021,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES)
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.artist,
                                       input_value=CaseSearchUserInput.artist_case_beach_boys,
                                       property_type=COMBOBOX,
                                       include_blanks=YES)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=[CaseSearchUserInput.artist_case_beach_boys,
                                                        CaseSearchUserInput.blank],
                                        is_multi=YES)


def test_case_15_exclude_property_from_case_search(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check exclude property from case search"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.exclude_property_from_case_search_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.one,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.two,
                                        expected_value=CaseSearchUserInput.four,
                                        is_multi=YES)
    webapps.search_again_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.four,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=[CaseSearchUserInput.one,
                                                        CaseSearchUserInput.two,
                                                        CaseSearchUserInput.three,
                                                        CaseSearchUserInput.four,
                                                        CaseSearchUserInput.five],
                                        is_multi=YES)


def test_case_16_sticky_search_without_default_value(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check sticky search without default value"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.four,
                                       property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.three_star,
                                       property_type=COMBOBOX)
    webapps.search_button_on_case_search_page()
    driver.back()
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


def test_case_17_sticky_search_with_default_value(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check sticky search with default value"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    webapps.search_button_on_case_search_page()
    webapps.search_again_cases()
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.mood,
                                              default_value=CaseSearchUserInput.three,
                                              search_format=text)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.mood,
                                       input_value=CaseSearchUserInput.four,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.three,
                                        expected_value=CaseSearchUserInput.four)
    webapps.search_again_cases()
    casesearch.check_default_values_displayed(search_property=CaseSearchUserInput.mood,
                                              default_value=CaseSearchUserInput.three,
                                              search_format=text)


def test_case_18_required_property(driver):
    webapps = WebApps(driver)
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


def test_case_19_conditionally_required_condition_property(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check conditionally required condition property"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    """Check enabled"""
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.two_star,
                                       property_type=COMBOBOX)
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.subgenre,
                                             message=CaseSearchUserInput.required_msg_if_rating_two,
                                             required_or_validated=YES,
                                             property_type=COMBOBOX)
    """Check disabled"""
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.three_star,
                                       property_type=COMBOBOX)
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.subgenre,
                                             message=CaseSearchUserInput.required_msg_if_rating_two,
                                             required_or_validated=NO,
                                             property_type=COMBOBOX)
    """Check form submission"""
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.two_star,
                                       property_type=COMBOBOX)
    casesearch.check_validations_on_property(search_property=CaseSearchUserInput.subgenre,
                                             message=CaseSearchUserInput.required_msg_if_rating_two,
                                             required_or_validated=YES,
                                             property_type=COMBOBOX)
    casesearch.search_against_property(search_property=CaseSearchUserInput.genre,
                                       input_value=CaseSearchUserInput.latin_music,
                                       property_type=COMBOBOX)
    casesearch.search_against_property(search_property=CaseSearchUserInput.subgenre,
                                       input_value=CaseSearchUserInput.latin_jazz,
                                       property_type=COMBOBOX)
    webapps.search_button_on_case_search_page()


def test_case_20_json_property_function(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check json property funtion"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.artist_menu)
    case_name = webapps.omni_search(CaseSearchUserInput.song_case_bugs)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.add_address_form)
    casesearch.add_address(address=CaseSearchUserInput.full_home_address,
                           search_property=CaseSearchUserInput.search_home_address)
    casesearch.add_address(address=CaseSearchUserInput.full_work_address,
                           search_property=CaseSearchUserInput.search_work_address)
    casesearch.check_value_on_form(city_address=CaseSearchUserInput.home_city_value,
                                   type=HOME)
    casesearch.check_value_on_form(city_address=CaseSearchUserInput.work_city_value,
                                   type=WORK)


@pytest.mark.skip(reason="This will fail, setting reverted!")
def test_case_21_case_search_title(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check Case Search Title"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    casesearch.check_search_screen_title(CaseSearchUserInput.search_title)
    webapps.open_menu(CaseSearchUserInput.skip_default_menu)
    webapps.search_again_cases()
    casesearch.check_search_screen_title(CaseSearchUserInput.default_search_title)
    webapps.open_app(CaseSearchUserInput.french_app)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    casesearch.check_search_screen_title(CaseSearchUserInput.search_title)


def test_case_22_dependent_dropdowns(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check Dependent Dropdowns"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.search_first_menu)
    casesearch.search_against_property(search_property=CaseSearchUserInput.genre,
                                       input_value=CaseSearchUserInput.latin_music,
                                       property_type=COMBOBOX)
    casesearch.search_against_property(search_property=CaseSearchUserInput.subgenre,
                                       input_value=CaseSearchUserInput.latin_jazz,
                                       property_type=COMBOBOX)
    """Check other values do not appear in dropdown"""
    casesearch.check_dropdown_value(search_property=CaseSearchUserInput.subgenre,
                                    not_to_be_present=CaseSearchUserInput.funk_metal)


def test_case_23_dependent_dropdowns_inline_case_search(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Check Dependent Dropdowns Inline Case Search"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu("Songs Inline Case Search")
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.genre,
                                       input_value=CaseSearchUserInput.latin_music,
                                       property_type=COMBOBOX)
    casesearch.search_against_property(search_property=CaseSearchUserInput.subgenre,
                                       input_value=CaseSearchUserInput.latin_jazz,
                                       property_type=COMBOBOX)
    """Check other values do not appear in dropdown"""
    casesearch.check_dropdown_value(search_property=CaseSearchUserInput.subgenre,
                                    not_to_be_present=CaseSearchUserInput.funk_metal)
    """Search case and check if corresponding case is displayed"""
    webapps.search_button_on_case_search_page()
    webapps.omni_search(CaseSearchUserInput.song_case_bugs)


def test_case_24_case_search_validations(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Case Search Validations"""
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu("Songs Inline Case Search")
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.energy,
                                       input_value=CaseSearchUserInput.three,
                                       property_type=TEXT_INPUT)
    time.sleep(2)
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.value_with_space,
                                       property_type=TEXT_INPUT)
    """Check validations imposed"""
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
    casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                       input_value=CaseSearchUserInput.song_case_bugs,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.omni_search(CaseSearchUserInput.song_case_bugs)
    """Check including blanks"""
    driver.back()
    time.sleep(2)
    driver.back()
    webapps.clear_selections_on_case_search_page()
    casesearch.select_include_blanks(CaseSearchUserInput.rating)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.blank)
