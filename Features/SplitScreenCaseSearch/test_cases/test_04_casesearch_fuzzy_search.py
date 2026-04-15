import time

from Features.CaseSearch.constants import *
from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from Features.CaseSearch.user_inputs.casesearch_user_inputs import CaseSearchUserInput
from HQSmokeTests.testPages.reports.report_page import ReportPage
from HQSmokeTests.testPages.home.home_page import HomePage
from common_utilities.selenium.base_page import BasePage
from common_utilities.selenium.webapps import WebApps

""""Contains all fuzzy search related test cases"""


def test_case_01_fuzzy_search_and_case_claim(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)

    """Check fuzzy search"""
    webapps.open_domain(domain_name=CaseSearchUserInput.casesearch_split_screen, current_url=driver.current_url)
    webapps.login_as(CaseSearchUserInput.user_2)
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.search_all_cases()
    webapps.clear_selections_on_case_search_page()
    "Fuzzy search"
    song_automation_song_1 = casesearch.search_against_property(search_property=CaseSearchUserInput.song_name,
                                                                input_value=CaseSearchUserInput.song_automation_song_1,
                                                                property_type=TEXT_INPUT)
    webapps.search_button_on_case_search_page()
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.one,
                                        expected_value=song_automation_song_1)
    "Select case to cliam"
    webapps.select_case_and_continue(song_automation_song_1)
    "Check case claimed on user caselist"
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.normal_menu)
    webapps.omni_search(song_automation_song_1)




def test_case_02_default_search_properties(driver, settings):
    webapps = WebApps(driver, settings)
    casesearch = CaseSearchWorkflows(driver)
    """Check Default Search Properties"""
    webapps.open_app(CaseSearchUserInput.linked_case_search_app_name)
    webapps.open_menu(CaseSearchUserInput.skip_default_menu)
    casesearch.check_values_on_caselist(row_num=CaseSearchUserInput.four,
                                        expected_value=CaseSearchUserInput.five)


