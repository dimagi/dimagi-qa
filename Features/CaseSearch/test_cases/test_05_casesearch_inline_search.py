import time

import pytest

from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from common_utilities.selenium.webapps import WebApps
from Features.CaseSearch.constants import *

""""Contains all inline search related test cases"""


def test_case_01_check_search_input_on_caselist_casedetail_form(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.inline_search_menu)
    webapps.clear_selections_on_case_search_page()
    casesearch.search_against_property(search_property=CaseSearchUserInput.rating,
                                       input_value=CaseSearchUserInput.five_star,
                                       property_type=COMBOBOX)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.seven,
                                        expected_value=CaseSearchUserInput.five)
    case_name = webapps.select_first_case_on_list()
    casesearch.check_value_on_case_detail(tabname=CaseSearchUserInput.rating,
                                          search_property=CaseSearchUserInput.rating_input,
                                          expected_value=CaseSearchUserInput.five)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.update_song_form)
    casesearch.check_value_on_form(CaseSearchUserInput.five)
    webapps.submit_the_form()
