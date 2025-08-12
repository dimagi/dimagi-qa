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

    app_preview_mobile_worker = "formplayer_user"
    automation_user = "automation_user"
    automation_user_group = "automation_user [group]"

    # Mobile Worker name
    mw_username = "formplayer_user@qa-automation.commcarehq.org"
    mw_password = "Pass@123"
    language = 'es'
    web_user = "automation.user.commcarehq@gmail.com"

    # Submit History
    test_application = {
        "tests_app": "Test Application -Formplayer Automation",
        "case_list": "Case List",
        "form_name": "Registration Form"}
    case_type = 'case'
    case_type_formplayer = 'sub_case_one'
    test_app = 'Test Application - One question per screen'
    test_application2 = {
        "tests_app": "Test Application - One question per screen",
        "case_list": "Case List",
        "form_name": "Registration Form"}

    basic_tests_app = {
        "tests_app": "Basic Tests [Linked]",
        "case_list": "Basic Form Tests",
        "form_name": "Basic Form"}

    basic_test_app_forms = {
        "basic": "Basic Form",
        "group": "Groups",
        "fst": "Formplayer Specific Tests",
        "question": "Question Types",
        "eofn": "End of Form Navigation",
        "home": "Home Screen",
        "module": "Module Screen",
        "prev": "Previous Screen",
        "current": "Current Module",
        "close": "Close Case",
        "another": "Another Menu",
        "case_test" : "Case Tests",
        "create_case": "Create a Case",
        "update_case": "Update a Case",
        "close_case": "Close a Case",
        "create_subcase": "Create a Sub Case",
        "create_multi_subcase": "Create Multiple Sub Case",
        "caselist": "Case list",
        "subcaseone": "Sub Case One",
        "close_subcase": "Close Case",
        "logic_test1": "Logic Tests 1",
        "constraints": "Constraints",
        "fixtures": "Fixtures",
        "functions": "Functions",
        "min_dup": "Minimize Duplicates",
        "view_case_subcase": "View Case\'s Sub Case",
        "fst_repeat": "[Formplayer] Repeats",
        "fst_cross_iter_repeat": "[Formplayer] Cross Iteration Repeats",
        "form_linking": "Form Linking Parent",
        "fl_add_case": "Add Case",
        "cond_expression": "Conditional expression",
        "no_cond_expression": "No conditional expression",
        "hin_basic_form": "HIN: Basic Form Update",
        "form_linking_child": "Form Linking Child",
        "linking_data": "Linking Data"
    }

    form_specific_tests_app = {
        "tests_app": "Basic Tests",
        "case_list": "Formplayer Specific Tests",
        "form_name": "[Formplayer] Appearance Attributes and Formatting"}

    expressions = ['true()', 'false()', 'boolean-from-string(1)',
                   'boolean-from-string(0)', 'boolean(1)', 'boolean(0)']
    unicode = "☕️☕️☕️"
    unicode_new = "☕️☕️☕️☕️☕️☕️"
    page_list = ["10","25","50","100"]

    text_now_number = "16174655292"
    staging_number = "16173804069"
    keyword_list = ["REGISTER", "UPDATE", "CLOSE"]
    sms_survey_list = ["SMS Tests > Case List > Registration Form",
                       "SMS Tests > Case List > Followup Form",
                       "SMS Tests > Case List > Close"]

    domain_staging = "qa-automation"
    multimedia_app = {
        "tests_app": "Multimedia"}
    map_input = "New Delhi"