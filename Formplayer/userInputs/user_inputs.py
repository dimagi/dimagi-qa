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
    basic_tests_app = "Formplayer Tests"
    basic_tests_case_list = "Basic Form Tests"
    basic_tests_form_name= "Basic Form"
    app_preview_mobile_worker = "appiumtest"


    #Mobile Worker name
    mw_username = "appiumtest@qa-automation.commcarehq.org"
    mw_password = "Pass@123"
    language = 'es'

    #Submit History
    test_application = "Test Application -Formplayer Automation"
    case_list_name = "Case List"
    form_name = "Registration Form"

    test_app = 'Test App'