""""Contains test data that are used as user inputs across various areasn in CCHQ"""
import os


class UserData:
    """User Test Data"""
    USER_INPUT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Pre-setup application and case names
    village_application = "Village Health"
    reassign_cases_application = 'Reassign Cases'
    case_pregnancy = "pregnancy"
    case_reassign = "reassign"
    model_type_case = "case"
    model_type_form = "form"
    new_form_name = "Android Test Form"
    app_login = "appiumtest"
    app_password = "Pass@123"
    two_fa_user = "2fa.commcare.user@gmail.com"
    appiumtest_owner_id = "appiumtest@qa-automation.commcarehq.org"
    appiumtest_owner_id_prod = "appiumtest@qa-automation-prod.commcarehq.org"
    # Phone Number
    area_code = "91"

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

    """New web user invitation"""
    yahoo_url = "https://login.yahoo.com/"
    yahoo_user_name = 'automation_webuser@yahoo.com'

    """Deduplicate Case Module """
    case_property = 'village_name'

    """Messaging History"""
    communication_type = "Conditional Alert"

    """Conditional Alert"""
    alert_case_property = "name"
    alert_case_property_value = "conditional alert"

    """Saved report"""
    report_for_p1p2 = "Report For P1P2"

    """Web user for p1p2"""
    p1p2_user = "p1p2.web.user@gmail.com"
    p1p2_profile = "p1p2_testprofile"
    from_email_prod = "commcarehq-noreply-production@dimagi.com"
    from_email = "commcarehq-noreply-staging@dimagi.com"

    """Report email subjects"""
    daily_form_activity = "Daily Form Activity: Requested export excel data"
    app_status = "Application Status: Requested export excel data"
    location_list = ['Delhi', 'Boston', 'Cape Town']