from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from common_utilities.generate_random_string import fetch_random_string
from common_utilities.selenium.webapps import WebApps
from Features.CaseSearch.constants import *

""""Contains all multi-select related test cases"""


def test_case_01_multiple_selected_cases_accessible_on_form(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.multi_select_menu)
    webapps.clear_selections_on_case_search_page()
    webapps.search_button_on_case_search_page()
    casesearch.select_all_cases_and_check_selected_cases_present_on_form()
    webapps.answer_repeated_questions(question_label=CaseSearchUserInput.add_show_question, input_type=textarea, input_value=fetch_random_string())
    webapps.submit_the_form()
    casesearch.check_eof_navigation(eof_nav=MENU,
                                    menu=CaseSearchUserInput.multi_select_menu)
