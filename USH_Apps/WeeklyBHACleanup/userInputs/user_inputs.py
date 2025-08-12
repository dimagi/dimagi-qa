""""Contains test data that are used as user inputs across various areasn in CCHQ"""
import os


class UserData:
    """User Test Data"""
    USER_INPUT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Pre-setup application and case names
    cr_app = "Automated Testing - CR"
    ccs_app = "Automated Testing - CCS"
    cr_admit_client = "Admit Client."
    ccs_bed_avail = "Update Bed Availability"
    ccs_send_refferals = "Send Referrals"
    date_range = "Last 7 Days"
    sub_time = "submission"
