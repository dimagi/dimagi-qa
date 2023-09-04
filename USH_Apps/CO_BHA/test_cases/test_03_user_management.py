from Features.CaseSearch.constants import TEXT_INPUT
from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from USH_Apps.CO_BHA.test_pages.bha_app_pages import BhaWorkflows
from USH_Apps.CO_BHA.user_inputs.bha_user_inputs import BhaUserInput
from common_utilities.selenium.webapps import WebApps
from Features.CaseSearch.constants import *


def test_case_access_to_module_state(driver):
    """use case: A state level user access the list of users and can enter the form to view their credential."""
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    app = BhaWorkflows(driver)

    webapps.login_as(BhaUserInput.state_level_user)
    webapps.open_app(BhaUserInput.bha_app_name)
    """Add Clinic"""
    webapps.open_menu(BhaUserInput.user_management)
    app.check_headers_on_case_list([BhaUserInput.name, BhaUserInput.username, BhaUserInput.creation_date])
    case_name = casesearch.search_against_property(search_property=BhaUserInput.first_name,
                                                   input_value=BhaUserInput.provider,
                                                   property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.select_case(case_name)
    app.select_clinic(BhaUserInput.arts_parkside_clinic)
    webapps.submit_the_form()
    """Remove Clinic"""
    webapps.open_menu(BhaUserInput.user_management)
    casesearch.search_against_property(search_property=BhaUserInput.first_name,
                                       input_value=BhaUserInput.provider,
                                       property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    webapps.select_case(case_name)
    app.remove_clinic(BhaUserInput.arts_parkside_clinic)
    webapps.submit_the_form()

