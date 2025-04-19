import pytest

from Features.CaseSearch.constants import *
from Features.CaseSearch.test_pages.casesearch_page import CaseSearchWorkflows
from POCs.VisualComparison.test_pages.visual_test_page import VisualTestPage
from USH_Apps.CO_BHA.test_pages.bha_app_pages import BhaWorkflows
from POCs.VisualComparison.user_inputs.bha_user_inputs import BhaUserInput
from common_utilities.hq_login.login_page import LoginPage
from common_utilities.selenium.webapps import WebApps
import names


def test_case_take_screenshots(driver, settings):
    """use case: Admit the client - case doesn't exist"""
    webapps = WebApps(driver, settings)
    vc = VisualTestPage(driver)

    vc.take_screenshots(BhaUserInput.screens['home_screen'])
    webapps.open_app(BhaUserInput.bha_app_name)
    vc.take_screenshots(BhaUserInput.screens['central_registry_app'])
    webapps.open_form(BhaUserInput.search_and_admit_client)
    vc.take_screenshots(BhaUserInput.screens['search_and_admit'])

def test_case_compare_screenshots(driver, settings):
    """use case: Admit the client - case doesn't exist"""
    webapps = WebApps(driver, settings)
    vc = VisualTestPage(driver)
    vc.compare_screeshot(BhaUserInput.screens['home_screen'])
    webapps.open_app(BhaUserInput.bha_app_name)
    vc.compare_screeshot(BhaUserInput.screens['central_registry_app'])
    webapps.open_form(BhaUserInput.search_and_admit_client)
    vc.compare_screeshot(BhaUserInput.screens['search_and_admit'])

