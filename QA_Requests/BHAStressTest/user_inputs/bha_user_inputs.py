""""Contains test data that are used as user inputs across various areass used in the project"""
import os


class BhaUserInput:
    """Test Data"""
    USER_INPUT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    """App Name"""
    bha_app_name = "QA-7414" #"BHA Provider Services"  # check for both staging & prod

    """Menus"""
    case_list = "Case List"

    """Forms"""
    registration_form = "Registration Form"

    "Labels"
    textarea_label = "Enter the stress testing round number"