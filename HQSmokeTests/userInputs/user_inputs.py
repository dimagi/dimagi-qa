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
    web_user = "[Web Users]"
    all_data = "[All Data]"
    mobile_testuser = "mobile_testuser"
    copied_to_user = "mobile_testuser \"DO NOT DELETE! DO NOT DELETE!\""
    searched_user = "appiumtest \"DO NOT DELETE! DO NOT DELETE!\""

    appiumtest_owner_id = "appiumtest@qa-automation.commcarehq.org"
    appiumtest_owner_id_prod = "appiumtest@qa-automation-prod.commcarehq.org"
    default_mw_role = "Mobile Worker Default"
    user_group = "automation_user"
    web_user = "[Web Users]"

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
    p1p2_form_export_name = "Smoke Form Export P1P2"
    p1p2_case_export_name = "Smoke Case Export P1P2"
    form_export_name_dse = "Smoke Form Export DSE"
    case_export_name_dse = "Smoke Case Export DSE"
    dashboard_feed_form = "Smoke Dashboard Form feed"
    dashboard_feed_case = "Smoke Dashboard Case feed"
    odata_feed_form = "Smoke Odata Form feed"
    odata_feed_case = "Smoke Odata Case feed"
    case_updated_export_name = "Smoke Updated Case Export"

    # Date Filter
    date_having_submissions = "2022-01-18 to 2022-02-18"
    india_date_having_submission = "2024-05-10 to 2024-05-30"

    # Excel column names
    case_id = 'caseid'
    text_value = 'name'
    random_value = 'enter_a_random_value'

    """New web user invitation"""
    yahoo_url = "https://login.yahoo.com/"
    yahoo_user_name = 'automation_webuser_test@yahoo.com'

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
    from_email_india = "commcarehq-noreply-india@dimagi.com"

    """Report email subjects"""
    daily_form_activity = "Daily Form Activity: Requested export excel data"
    app_status = "Application Status: Requested export excel data"
    location_list = ['Delhi', 'Boston', 'Cape Town']

    """Data Forwarding"""
    http_req_methods = ['DELETE','POST','PUT']
    payload_format = ['XML','JSON']

    """Parent Child Import Case"""
    parent_1_id = "d1c8f20e-c54d-4207-a4b1-0000bfd5b040"
    parent_2_id = "0463bcfc80234bfe8d2072eaf2be881b"
    child_case_id = "ba0ff57e-cbb5-4887-bca6-c43b29e82dde"
    parent_type = "pregnancy"
    child_type = "village"
    child_name = "Saharanpur"
