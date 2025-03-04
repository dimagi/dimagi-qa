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

    result_name_1kb_1st = "time_records_new_1kb_1st.csv"
    result_name_1kb_2nd = "time_records_new_1kb_2nd.csv"
    result_name_1kb_3rd = "time_records_new_1kb_3rd.csv"

    result_name_2kb_1st = "time_records_new_2kb_1st.csv"
    result_name_2kb_2nd = "time_records_new_2kb_2nd.csv"
    result_name_2kb_3rd = "time_records_new_2kb_3rd.csv"

    result_name_3kb_1st = "time_records_new_3kb_1st.csv"
    result_name_3kb_2nd = "time_records_new_3kb_2nd.csv"
    result_name_3kb_3rd = "time_records_new_3kb_3rd.csv"

    result_name_4kb_1st = "time_records_new_4kb_1st.csv"
    result_name_4kb_2nd = "time_records_new_4kb_2nd.csv"
    result_name_4kb_3rd = "time_records_new_4kb_3rd.csv"

    input_file_1kb = "test_data/sample_1kb.pdf"
    input_file_2kb = "test_data/sample_2kb.pdf"
    input_file_3kb = "test_data/sample_3kb.pdf"
    input_file_4kb = "test_data/sample_4kb.pdf"