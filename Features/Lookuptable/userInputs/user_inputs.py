""""Contains test data that are used as user inputs across various areasn in CCHQ"""
import os

import random
import string


from common_utilities.generate_random_string import fetch_random_string
from common_utilities.path_settings import PathSettings


class UserData:

    """User Test Data"""
    user_input_base_dir = os.path.dirname(os.path.abspath(__file__))
    # Pre-setup application and case names
    field_val = 'table'+ str(fetch_random_string())
    url = "https://staging.commcarehq.org/a/qa-automation/phone/restore/?version=2.0&as=sameena.shaik@fissionlabs.com"

    restore_url = "https://staging.commcarehq.org/a/qa-automation/phone/restore/?version=2.0&as=appiumtest@qa-automation.commcarehq.org"
    data_list = [(1, 'Y', '1', 'RWS%DTUYIG*&^%'), (2, 'N', '2', '!#@$%#$RFGH:'), (3, 'N', '3', '!#@$%#$RFGH:')]

    row_value_change =[('','N','23',"appiumtest")]
    data_list_delete = [(1, 'Y', '1', 'RWS%DTUYIG*&^%'), (2, 'N', '2', '!#@$%#$RFGH:')]
    data_list1 = [(1, 'N', '1',"appiumtest"),(2, 'N', '2',"")]
    data_list2 = [(3, 'N', '3','',"123"),(4, 'N', '4','',"group2")]
    edit_data = [(1, 'N', '1', 'kiran'), (2, 'N', '2', 'henry')]
    new_datalist = [(1, 'N', '1','2'),(123, 'N', '456','789'),(987, 'N', '543', '345')]

    duplicate_values = [(1, 'N', '1'),(1, 'N', '1'),(987, 'N', '543'),(987, 'N', '543'),(987, 'N', '543')]
    type_data_list = [('N', field_val, 'yes',field_val)]
    type_sheet_headers = [('UID', 'Delete(Y/N)', 'field: '+ field_val)]
    data_upload_path = PathSettings.ROOT + "/userInputs/upload_1.xlsx"
    hypertension_upload_path = PathSettings.ROOT + "/userInputs/Hypertension.xlsx"
    print(hypertension_upload_path)
    malformed_document_upload_path = PathSettings.ROOT + "/userInputs/MalformedDocument.xlsx"
    state = PathSettings.ROOT + "/userInputs/States.xlsx"
    Inapp = PathSettings.ROOT + "/userInputs/Inapp.xlsx"
    district = PathSettings.ROOT + "/userInputs/districts.xlsx"
    invalid_data_assert = "However, we ran into the following problems:"
    missing_data_assert = "Please fix the following formatting issues in your Excel file"
    col_headers = ["user 1", "group 1"]
    filter_value = ["test"]
    application = "Lookuptable_tests"
    user_ids_list = ["kiran", "av" , "henry" , "appiumtest" ]
    multiple_values = [(1, 'N', '1',"kiran"),(2, 'N', '2',"av"),(3, 'N', '3',"","automation_user"),(4, 'N', '4',"","","group new")]

