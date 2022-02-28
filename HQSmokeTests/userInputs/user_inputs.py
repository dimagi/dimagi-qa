import os
from pathlib import Path


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

    # invite_web_user user email
    web_user_mail = 'automation.user.commcarehq+test@gmail.com'

    #  web app
    app_type = "Applications"
    case_list_name = 'Case List'
    form_name = 'Registration Form'
    login_as = 'henry'


    # Export report names
    form_export_name = "Smoke Form Export"
    case_export_name = "Smoke Case Export"
    form_export_name_dse = "Smoke Form Export DSE"
    case_export_name_dse = "Smoke Case Export DSE"
    dashboard_feed_form = "Smoke Dashboard Form feed"
    dashboard_feed_case = "Smoke Dashboard Case feed"
    odata_feed_form = "Smoke Odata Form feed"
    odata_feed_case = "Smoke Odata Case feed"

    # Date Filter
    date_having_submissions = "2022-01-18 to 2022-02-18"
