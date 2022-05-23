import os
import names
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
    village_application = "Village Health"
    reassign_cases_application = 'Reassign Cases'
    case_pregnancy = "pregnancy"
    case_reassign = "reassign"
    model_type_case = "case"
    model_type_form = "form"
    new_form_name = "Android Test Form"
    app_login = "AppiumTest"
    app_password = "pass123"
    two_fa_user = "2fa.commcare.user@gmail.com"
    yahoo_email_username = "automation_user_commcare"

    # Phone Number
    area_code = "91"
    # invite_web_user user email
    web_user_mail = 'automation.user.commcarehq+test@gmail.com'

    #  web app
    app_type = "Applications"
    case_list_name = 'Case List'
    form_name = 'Registration Form'
    login_as = 'henry'
    update_case_change_link = "Case Change"
    case_register_form = "Case Register"
    case_update_form = "Update Case"
    case_update_name = "reassign_change"
    # Export report names
    form_export_name = "Smoke Form Export"
    case_export_name = "Smoke Case Export"
    form_export_name_dse = "Smoke Form Export DSE"
    case_export_name_dse = "Smoke Case Export DSE"
    dashboard_feed_form = "Smoke Dashboard Form feed"
    dashboard_feed_case = "Smoke Dashboard Case feed"
    odata_feed_form = "Smoke Odata Form feed"
    odata_feed_case = "Smoke Odata Case feed"
    case_updated_export_name = "Smoke Updated Case Export"

    # Date Filter
    date_having_submissions = "2022-01-18 to 2022-02-18"

    # Excel column names
    case_id = 'caseid'
    text_value = 'name'
    random_value = 'enter_a_random_value'

    #Accept Invite
    web_user_name = names.get_full_name()
    web_user_password = "AutomationUser@1234"

