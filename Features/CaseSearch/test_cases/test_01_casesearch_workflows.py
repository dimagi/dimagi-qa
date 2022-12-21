import pytest

from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from common_utilities.selenium.webapps import WebApps

""""Contains all case search workflow related test cases"""


@pytest.mark.casesearch
def test_case_01_normal_workflow(driver):
    webapps = WebApps(driver)
    casesearch = CaseSearchWorkflows(driver)
    """Checks if user can submit a form for normal search"""
    webapps.login_as(CaseSearchUserInput.user_1)
    webapps.open_app(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.search_all_cases()
    webapps.clear_and_search_all_cases_on_case_search_page()
    case_name = webapps.omni_search(CaseSearchUserInput.song_case_bugs)
    webapps.select_case_and_continue(case_name)
    webapps.open_form(CaseSearchUserInput.play_song_form)
    webapps.submit_the_form()
    """Checks if claim successful"""
    webapps.navigate_to_breadcrumb(CaseSearchUserInput.case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    casesearch.check_element_claimed(case_name)
