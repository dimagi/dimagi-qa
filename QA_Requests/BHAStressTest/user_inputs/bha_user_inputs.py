""""Contains test data that are used as user inputs across various areass used in the project"""
import os


class BhaUserInput:
    """Test Data"""
    USER_INPUT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    """App Name"""
    bha_app_name = "QA-7414" #"BHA Provider Services"  # check for both staging & prod

    """Menus"""
    case_list = "Ben\'s test"

    """Forms"""
    registration_form = "Survey"

    "Labels"
    textarea_label = "Enter stress testing round number"

    csv_file_1MB_1st = "recorded_time__new_1MB_1st.csv"
    csv_file_1MB_2nd = "recorded_time__new_1MB_2nd.csv"
    csv_file_1MB_3rd = "recorded_time__new_1MB_3rd.csv"

    csv_file_2MB_1st = "recorded_time__new_2MB_1st.csv"
    csv_file_2MB_2nd = "recorded_time__new_2MB_2nd.csv"
    csv_file_2MB_3rd = "recorded_time__new_2MB_3rd.csv"

    csv_file_3MB_1st = "recorded_time__new_3MB_1st.csv"
    csv_file_3MB_2nd = "recorded_time__new_3MB_2nd.csv"
    csv_file_3MB_3rd = "recorded_time__new_3MB_3rd.csv"

    csv_file_4MB_1st = "recorded_time__new_4MB_1st.csv"
    csv_file_4MB_2nd = "recorded_time__new_4MB_2nd.csv"
    csv_file_4MB_3rd = "recorded_time__new_4MB_3rd.csv"

    random_text_1MB = "1mb_pdf.pdf"
    random_text_2MB = "random_text_2MB.pdf"
    random_text_3MB = "random_text_3MB.pdf"
    random_text_4MB = "random_text_4MB.pdf"