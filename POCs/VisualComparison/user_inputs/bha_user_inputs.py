""""Contains test data that are used as user inputs across various areass used in the project"""


class BhaUserInput:
    """Test Data"""

    """App Name"""
    bha_app_name = "Central Registry (Linked)" #"BHA Provider Services"  # check for both staging & prod

    """Users"""
    state_level_user = "bha_test_users+30@dimagi.com"#"state.level.user1"
    clinic_level_user = "bha_test_users+43@dimagi.com"#"clinic.level.user1"
    user_B = "bha_test_users+Central_Registry_Facility_User_B@dimagi.com"

    """Menus"""
    search_central_registry = "Search Central Registry"
    search_and_admit_client = "Search and Admit Client"
    search_my_clients = "Search My Clients"
    pending_requests = "Pending Requests"
    user_management = "User Management"

    """Forms"""
    admit_client_form = "Admit Client"
    request_admission_review = "Request admission review"
    discharge_client = "Discharge Client"
    update_lock_status_request = "Update Lock Status Request"

    """Clinics"""

    arts_parkside_clinic = "ARTS Parkside Clinic"
    aurora_therapy_center = "Aurora Therapy Center"
    baymark_baart_brighton = "BAYMARK (BAART) - Brighton"
    baymark_baart_brighton_clinic_type = "Opioid Treatment Programs, Substance Use Services"
    baymark_baart_brighton_address = "5 South 1st Avenue, Brighton, CO 80601"
    baymark_baart_brighton_phone_number = "(720) 909-6008"
    staging_baymark_baart_brighton_case_id = "2ab5d27d377b4fb4ba5acb85a86a5335"
    prod_baymark_baart_brighton_case_id = "29f0b47367e04fe0b722e33bf490b696"

    """Labels On Form"""
    first_name_on_form = "First Name"
    last_name_on_form = "Last Name"
    dob_on_form = "Date of Birth"
    cancel = "Cancel"
    completed_treatment = "Completed treatment"
    suboxone = "Suboxone"
    lock_in = "Lock In"
    clinic_id = "Clinic ID"
    type = "Type"
    address = "Address"
    phone_number = "Phone Number"


    "Questions"
    where_admit = "(Required) Where would you like to admit this client?"
    bha_approval_needed = "BHA approval is required before the client can be locked in. Please submit this form to send the lock status request to BHA for review."
    lock_out_confirmation = "Upon submission, the client will be locked in to care at " + aurora_therapy_center + " and the requesting clinic will be notified."

    """Search Fields"""
    first_name_required = "(Required) First Name"
    last_name_required = "(Required) Last Name"
    dob_required = "(Required) DOB"
    first_name = "First Name"
    last_name = "Last Name"
    name = "Name"
    dob = "DOB"
    date_of_birth = "Date of Birth"
    reason_for_no_ssn = "Reason for no SSN"
    consent = "(Required) Consent obtained by provider for the purposes of searching the Central Registry to confirm admission"
    ssn = "Social Security Number"
    medicaid_id = "Medicaid ID"
    client_id = "Client ID"
    case_name = "Case Name"
    admission_status = "(Required) Admission Status"

    """User Inputs"""
    inactive = "Inactive"
    date_1950_05_01 = "05/01/1950"
    refused_to_provide = "Refused to provide"
    does_not_have_ssn = "Does not have SSN"
    staging_inactive_first_name = "CLIENT1 FIRST NAME"
    staging_inactive_last_name_with_typo = "CLIENT1 LAST NAAA"
    staging_inactive_dob = "01/01/2010"
    prod_inactive_first_name = "PROD CLIENT1 FIRST NAME"
    prod_inactive_last_name_with_typo = "PROD CLIENT1 LAST NAAA"
    prod_inactive_dob = "01/01/2010"
    all_status = "All"

    yes = "Yes"
    yes_small = "yes"
    approve = "Approve"
    provider = "Provider"
    
    """Values_on Case List"""
    zero = "0"
    one = "1"
    two = "2"
    five = "5"
    six = "6"
    pending_status = "Pending"
    pending = "[pending]"
    discharged = "Discharged"
    username = "Username"
    creation_date = "Creation date"
    no_potential_match_found = "No potential client matches. Proceed to admit new client."

    # CLR staging
    staging_case_link = "https://staging.commcarehq.org/a/co-carecoordination-test/reports/case_data/b4d15f46-8f55-4630-ba33-6dcf267c22b0/"
    potential_duplicate = "potential_duplicate_case_ids"
    staging_potential_duplicate_case_id = "b46e5cb0-0add-4ff9-8c8f-38c53df63847"

    staging_duplicate_case_link = "https://staging.commcarehq.org/a/co-carecoordination-test/reports/case_data/b46e5cb0-0add-4ff9-8c8f-38c53df63847/"
    potential_duplicate_index = "potential_duplicate_index_case_ids"
    staging_potential_duplicate_index_case_id = "b4d15f46-8f55-4630-ba33-6dcf267c22b0"

    # CLR prod
    prod_case_link = "https://www.commcarehq.org/a/co-carecoordination-test/reports/case_data/93fddbd7-7376-4e18-a7dd-59338c89524d/"
    prod_potential_duplicate_case_id = "71265f9a41e14841ae3fe4f2c6af338f"

    prod_duplicate_case_link = "https://www.commcarehq.org/a/co-carecoordination-test/reports/case_data/71265f9a41e14841ae3fe4f2c6af338f/"
    prod_potential_duplicate_index_case_id = "93fddbd7-7376-4e18-a7dd-59338c89524d"

    # Messaging History
    clinic_admission_request = "Clinic Admission Request"
    clinic_admission_request_content = "A admission request was submitted by"

    clinic_same_admit_discahrge = "Clinic Same Admit/Discharge"
    clinic_same_admit_discahrge_content = "An admission and discharge form were submitted by"

    clinic_update_lock_status = "Clinic Update Lock Status"
    clinic_update_lock_status_content = "A lock status request was submitted by"

    state_determination_lock_status = "State Determination Lock Status"
    state_determination_lock_status_content = "The lock status request submitted by"

    screens = {
        "login": "login.png",
        "login_1" : "login_page.png",
        "home_screen": "home_screen.png",
        "central_registry_app": "central_registry_app.png",
        "search_and_admit": "search_and_admit.png"
        }

