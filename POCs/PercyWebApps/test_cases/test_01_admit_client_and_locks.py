from POCs.PercyWebApps.test_pages.visual_test_page import VisualTestPage
from POCs.PercyWebApps.user_inputs.bha_user_inputs import BhaUserInput
from common_utilities.selenium.webapps import WebApps



def test_case_take_screenshots(driver, settings):
    """use case: Admit the client - case doesn't exist"""
    webapps = WebApps(driver, settings)
    vc = VisualTestPage(driver)
    vc.take_screenshots(BhaUserInput.screens['home_screen'])
    webapps.open_app(BhaUserInput.bha_app_name)
    vc.take_screenshots(BhaUserInput.screens['central_registry_app'])
    webapps.open_form(BhaUserInput.search_and_admit_client)
    vc.take_screenshots(BhaUserInput.screens['search_and_admit'])

# def test_case_compare_screenshots(driver, settings):
#     """use case: Admit the client - case doesn't exist"""
#     webapps = WebApps(driver, settings)
#     vc = VisualTestPage(driver)
#     vc.compare_screeshot(BhaUserInput.screens['home_screen'])
#     webapps.open_app(BhaUserInput.bha_app_name)
#     vc.compare_screeshot(BhaUserInput.screens['central_registry_app'])
#     webapps.open_form(BhaUserInput.search_and_admit_client)
#     vc.compare_screeshot(BhaUserInput.screens['search_and_admit'])

