import os
from pathlib import Path

""""Contains test data that are used as user inputs across various areasn in CCHQ"""


class UserData:
    """Path Settings"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    if os.environ.get("CI") == "true":
        DOWNLOAD_PATH = Path("/home/runner/work/dimagi-qa/dimagi-qa")
    else:
        DOWNLOAD_PATH = Path('~/Downloads').expanduser()

    """User Test Data"""

    # Pre-setup application and case names
    basic_tests = {"tests_app": "Formplayer Tests",
                   "case_list": "Basic Form Tests",
                   "form_name": "Basic Form"}

    app_preview_mobile_worker = "appiumtest"

    # Mobile Worker name
    mw_username = "appiumtest@qa-automation.commcarehq.org"
    mw_password = "Pass@123"
    language = 'es'
    web_user = "automation.user.commcarehq@gmail.com"

    # Submit History
    test_application = {
        "tests_app": "Test Application -Formplayer Automation",
        "case_list": "Case List",
        "form_name": "Registration Form"}
    case_type = 'case'
    test_app = 'Test Application - One question per screen'
    test_application2 = {
        "tests_app": "Test Application - One question per screen",
        "case_list": "Case List",
        "form_name": "Registration Form"}

    basic_tests_app = {
        "tests_app": "Basic Tests",
        "case_list": "Basic Form Tests",
        "form_name": "Basic Form"}

    basic_test_app_forms = {
        "basic": "Basic Form",
        "group": "Groups",
        "fst": "Formplayer Specific Tests",


    }