from selenium.common import TimeoutException

from Features.CaseSearch.constants import *
from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from USH_Apps.CO_BHA.test_pages.bha_app_pages import BhaWorkflows
from USH_Apps.CO_BHA.user_inputs.bha_user_inputs import BhaUserInput
from common_utilities.selenium.webapps import WebApps
import names


def test_case_01_admit_case_1(driver):
    """use case: Admit the client - case doesn't exist"""
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    app = BhaWorkflows(driver)

    webapps.login_as(BhaUserInput.clinic_level_user)
    webapps.open_app(BhaUserInput.bha_app_name)
    webapps.open_menu(BhaUserInput.search_and_admit_client)
    app.check_search_properties_present([BhaUserInput.client_id, BhaUserInput.ssn, BhaUserInput.medicaid_id])
    global first_name, last_name
    first_name = casesearch.search_against_property(search_property=BhaUserInput.first_name_required,
                                                    input_value=names.get_first_name(),
                                                    property_type=TEXT_INPUT)
    last_name = casesearch.search_against_property(search_property=BhaUserInput.last_name_required,
                                                   input_value=names.get_last_name(),
                                                   property_type=TEXT_INPUT)
    dob = casesearch.search_against_property(search_property=BhaUserInput.dob_required,
                                             input_value=BhaUserInput.date_1950_05_01,
                                             property_type=TEXT_INPUT)  # generate a randon date
    casesearch.search_against_property(search_property=BhaUserInput.reason_for_no_ssn,
                                       input_value=BhaUserInput.does_not_have_ssn,
                                       property_type=COMBOBOX)
    casesearch.select_checkbox(BhaUserInput.consent, BhaUserInput.yes_small, select_by_value=text)
    webapps.search_button_on_case_search_page()
    webapps.check_case_list_is_empty(BhaUserInput.no_potential_match_found)
    app.expected_count_on_continue_button(BhaUserInput.zero)
    app.click_on_admit_new_client()
    casesearch.check_eof_navigation(eof_nav=MENU, menu=BhaUserInput.admit_client_form)
    app.select_radio(BhaUserInput.yes)
    app.check_client_info_on_form(search_property=BhaUserInput.first_name_on_form,
                                  search_value=first_name)
    app.check_client_info_on_form(search_property=BhaUserInput.last_name_on_form,
                                  search_value=last_name)
    app.check_client_info_on_form(search_property=BhaUserInput.dob_on_form,
                                  search_value=dob)
    app.select_clinic(BhaUserInput.aurora_therapy_center)
    webapps.submit_the_form()


def test_case_02_admit_case_2(driver):
    """use case: Admit a client - case does exist -> Request pending admission"""
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    app = BhaWorkflows(driver)

    webapps.login_as(BhaUserInput.clinic_level_user)
    webapps.open_app(BhaUserInput.bha_app_name)
    webapps.open_menu(BhaUserInput.search_and_admit_client)
    typo_first_name = casesearch.search_against_property(search_property=BhaUserInput.first_name_required,
                                                         input_value=app.replace_one_char(first_name),
                                                         property_type=TEXT_INPUT)
    typo_last_name = casesearch.search_against_property(search_property=BhaUserInput.last_name_required,
                                                        input_value=app.replace_one_char(last_name),
                                                        property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=BhaUserInput.dob_required,
                                       input_value=BhaUserInput.date_1950_05_01,
                                       property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=BhaUserInput.reason_for_no_ssn,
                                       input_value=BhaUserInput.does_not_have_ssn,
                                       property_type=COMBOBOX)
    casesearch.select_checkbox(BhaUserInput.consent, BhaUserInput.yes_small, select_by_value=text)
    webapps.search_button_on_case_search_page()
    # CHECK QUESTION TEXT
    try:
        app.select_radio(BhaUserInput.yes)
    except TimeoutException:
        app.click_on_admit_new_client()
        app.select_radio(BhaUserInput.yes)
    # CHECK TABLE CONTENT
    app.check_answer_options(label=BhaUserInput.admit_client_form, displayed=NO)
    """Admission question is hidden upon selecting cancel"""
    app.select_radio(BhaUserInput.cancel)
    app.check_question_label(label=BhaUserInput.where_admit, displayed=NO)
    """Selection of center"""
    app.select_radio(BhaUserInput.request_admission_review)
    app.select_clinic(BhaUserInput.aurora_therapy_center)
    webapps.submit_the_form()
    """Check if case present in pending requests menu"""
    webapps.open_menu(BhaUserInput.pending_requests)
    casesearch.search_against_property(search_property=BhaUserInput.name,
                                       input_value=typo_first_name + " " + typo_last_name,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=BhaUserInput.one,
                                        expected_value=BhaUserInput.pending)
    casesearch.check_values_on_caselist(row_num=BhaUserInput.two,
                                        expected_value=typo_first_name + " " + typo_last_name)


def test_case_03_lock_in_1_1(driver):
    """use case: no existing lock status for clinic user"""
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    app = BhaWorkflows(driver)

    webapps.login_as(BhaUserInput.clinic_level_user)
    webapps.open_app(BhaUserInput.bha_app_name)
    webapps.open_menu(BhaUserInput.search_my_clients)
    casesearch.search_against_property(search_property=BhaUserInput.first_name,
                                                    input_value=first_name,
                                                    property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=BhaUserInput.last_name,
                                                   input_value=last_name,
                                                   property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=BhaUserInput.date_of_birth,
                                             input_value=BhaUserInput.date_1950_05_01,
                                             property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.select_case(first_name)
    webapps.open_form(BhaUserInput.update_lock_status_request)
    app.select_radio(BhaUserInput.lock_in)
    app.select_clinic(BhaUserInput.aurora_therapy_center)
    app.select_radio(BhaUserInput.yes)
    app.check_question_label(label=BhaUserInput.bha_approval_needed, displayed=YES)
    webapps.submit_the_form()
    casesearch.check_eof_navigation(eof_nav=MENU, menu=BhaUserInput.search_my_clients)


def test_case_04_lock_in_1_2(driver):
    """use case: no existing lock status for state user"""
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    app = BhaWorkflows(driver)

    webapps.login_as(BhaUserInput.state_level_user)
    webapps.open_app(BhaUserInput.bha_app_name)
    webapps.open_menu(BhaUserInput.pending_requests)
    full_name = first_name + " " + last_name
    casesearch.search_against_property(search_property=BhaUserInput.case_name,
                                                   input_value=full_name,
                                                   property_type=TEXT_INPUT)
    webapps.select_case(full_name)
    app.select_radio(BhaUserInput.approve)
    app.check_answer_options(label=BhaUserInput.lock_out_confirmation, displayed=YES)
    webapps.submit_the_form()
    casesearch.check_eof_navigation(eof_nav=MENU, menu=BhaUserInput.pending_requests)
    """Check default results appear aftrt EOF navigation"""
    casesearch.check_values_on_caselist(row_num=BhaUserInput.five,
                                        expected_value=BhaUserInput.pending_status)


def test_case_05_admit_case_7(driver):
    """use case: match on inactive client"""
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    app = BhaWorkflows(driver)

    webapps.login_as(BhaUserInput.clinic_level_user)
    webapps.open_app(BhaUserInput.bha_app_name)
    webapps.open_menu(BhaUserInput.search_and_admit_client)
    domain_url = driver.current_url
    if "staging" in domain_url:
        casesearch.search_against_property(search_property=BhaUserInput.first_name_required,
                                           input_value=BhaUserInput.staging_inactive_first_name,
                                           property_type=TEXT_INPUT)
        casesearch.search_against_property(search_property=BhaUserInput.last_name_required,
                                           input_value=BhaUserInput.staging_inactive_last_name_with_typo,
                                           property_type=TEXT_INPUT)
        casesearch.search_against_property(search_property=BhaUserInput.dob_required,
                                           input_value=BhaUserInput.staging_inactive_dob,
                                           property_type=TEXT_INPUT)
    elif "www" in domain_url:
        casesearch.search_against_property(search_property=BhaUserInput.first_name_required,
                                           input_value=BhaUserInput.prod_inactive_first_name,
                                           property_type=TEXT_INPUT)
        casesearch.search_against_property(search_property=BhaUserInput.last_name_required,
                                           input_value=BhaUserInput.prod_inactive_last_name_with_typo,
                                           property_type=TEXT_INPUT)
        casesearch.search_against_property(search_property=BhaUserInput.dob_required,
                                           input_value=BhaUserInput.prod_inactive_dob,
                                           property_type=TEXT_INPUT)
    casesearch.search_against_property(search_property=BhaUserInput.reason_for_no_ssn,
                                       input_value=BhaUserInput.refused_to_provide,
                                       property_type=COMBOBOX)
    casesearch.select_checkbox(BhaUserInput.consent, BhaUserInput.yes_small, select_by_value=text)
    webapps.search_button_on_case_search_page()
    webapps.submit_the_form()
    """Case List Report Check"""
    if "staging" in domain_url:
        app.check_property_on_case_list_report(case_link=BhaUserInput.staging_case_link,
                                               case_property=BhaUserInput.potential_duplicate,
                                               case_property_value=BhaUserInput.staging_potential_duplicate_case_id)
        app.check_property_on_case_list_report(case_link=BhaUserInput.staging_duplicate_case_link,
                                               case_property=BhaUserInput.potential_duplicate_index,
                                               case_property_value=BhaUserInput.staging_potential_duplicate_index_case_id)
    elif "www" in domain_url:
        app.check_property_on_case_list_report(case_link=BhaUserInput.prod_case_link,
                                               case_property=BhaUserInput.potential_duplicate,
                                               case_property_value=BhaUserInput.prod_potential_duplicate_case_id)
        app.check_property_on_case_list_report(case_link=BhaUserInput.prod_duplicate_case_link,
                                               case_property=BhaUserInput.potential_duplicate_index,
                                               case_property_value=BhaUserInput.prod_potential_duplicate_index_case_id)
