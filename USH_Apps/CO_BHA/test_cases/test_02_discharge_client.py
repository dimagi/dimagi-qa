import pytest

from Features.CaseSearch.constants import *
from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from USH_Apps.CO_BHA.test_pages.bha_app_pages import BhaWorkflows
from USH_Apps.CO_BHA.user_inputs.bha_user_inputs import BhaUserInput
from common_utilities.selenium.webapps import WebApps
import names


def test_case_discharge_client_1(driver, settings):
    """use case: state level user"""
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    app = BhaWorkflows(driver)

    # webapps.login_as(BhaUserInput.state_level_user)
    webapps.bha_login_as(BhaUserInput.state_level_user, settings['bha_password'], settings['url'], settings['db'])
    webapps.open_app(BhaUserInput.bha_app_name)
    webapps.open_menu(BhaUserInput.search_and_admit_client)
    first_name = casesearch.search_against_property(search_property=BhaUserInput.first_name_required,
                                                    input_value=names.get_first_name(),
                                                    property_type=TEXT_INPUT)
    last_name = casesearch.search_against_property(search_property=BhaUserInput.last_name_required,
                                                   input_value=names.get_last_name(),
                                                   property_type=TEXT_INPUT)
    dob = casesearch.search_against_property(search_property=BhaUserInput.dob_required,
                                             input_value=BhaUserInput.date_1950_05_01,
                                             property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=BhaUserInput.reason_for_no_ssn,
                                       input_value=BhaUserInput.does_not_have_ssn,
                                       property_type=COMBOBOX2)
    casesearch.select_checkbox(BhaUserInput.consent, BhaUserInput.yes_small, select_by_value=text)
    webapps.search_button_on_case_search_page()
    app.click_on_admit_new_client()
    app.select_radio(BhaUserInput.yes)
    app.check_client_info_on_form(search_property=BhaUserInput.first_name_on_form,
                                  search_value=first_name)
    app.check_client_info_on_form(search_property=BhaUserInput.last_name_on_form,
                                  search_value=last_name)
    app.check_client_info_on_form(search_property=BhaUserInput.dob_on_form,
                                  search_value=dob)
    app.select_clinic(BhaUserInput.aurora_therapy_center)
    webapps.submit_the_form()
    """Search Central Registry"""
    webapps.open_menu(BhaUserInput.search_central_registry)
    casesearch.search_against_property(search_property=BhaUserInput.first_name,
                                       input_value=first_name,
                                       property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=BhaUserInput.last_name,
                                       input_value=last_name,
                                       property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=BhaUserInput.dob,
                                       input_value=dob,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=BhaUserInput.two,
                                        expected_value=first_name)
    """Search My Clients as clinic user"""
    # sync
    webapps.sync_app()
    # webapps.login_as(BhaUserInput.clinic_level_user)
    # webapps.bha_login_as(BhaUserInput.clinic_level_user, settings['bha_password'], settings['url'], settings['db'])
    # webapps.open_app(BhaUserInput.bha_app_name)
    # webapps.open_menu(BhaUserInput.search_my_clients)
    # casesearch.search_against_property(search_property=BhaUserInput.first_name,
    #                                    input_value=first_name,
    #                                    property_type=TEXT_INPUT)
    # casesearch.search_against_property(search_property=BhaUserInput.last_name,
    #                                    input_value=last_name,
    #                                    property_type=TEXT_INPUT)
    # casesearch.search_against_property(search_property=BhaUserInput.date_of_birth,
    #                                    input_value=dob,
    #                                    property_type=TEXT_INPUT)
    # full_name = first_name + " " + last_name
    # webapps.search_button_on_case_search_page()
    # # might fail on prod due to sync delays
    # app.check_values_on_caselist(row_num=BhaUserInput.one,
    #                                     expected_value=full_name)
    webapps.sync_app()
    """Search Central Registry as state user"""
    # webapps.login_as(BhaUserInput.state_level_user)
    webapps.bha_login_as(BhaUserInput.state_level_user, settings['bha_password'], settings['url'], settings['db'])
    webapps.open_app(BhaUserInput.bha_app_name)
    webapps.open_menu(BhaUserInput.search_central_registry)
    casesearch.search_against_property(search_property=BhaUserInput.first_name,
                                       input_value=first_name,
                                       property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=BhaUserInput.last_name,
                                       input_value=last_name,
                                       property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=BhaUserInput.dob,
                                       input_value=dob,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.select_case(first_name)
    webapps.open_form(BhaUserInput.discharge_client)
    app.select_radio(BhaUserInput.suboxone)
    app.select_radio(BhaUserInput.completed_treatment)
    # check future discharge date
    webapps.submit_the_form()
    """Check the admission status on case list"""
    webapps.navigate_to_breadcrumb(BhaUserInput.bha_app_name)
    webapps.open_menu(BhaUserInput.search_central_registry)
    casesearch.search_against_property(search_property=BhaUserInput.first_name,
                                       input_value=first_name,
                                       property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=BhaUserInput.last_name,
                                       input_value=last_name,
                                       property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=BhaUserInput.dob,
                                       input_value=dob,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=BhaUserInput.six,
                                        expected_value=BhaUserInput.discharged)
