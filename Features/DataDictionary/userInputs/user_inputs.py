""""Contains test data that are used as user inputs across various areasn in CCHQ"""
import os
import random
import string

from common_utilities.generate_random_string import fetch_random_string
from common_utilities.path_settings import PathSettings


class UserData:


    """User Test Data"""
    user_input_base_dir = os.path.dirname(os.path.abspath(__file__))
    application = "Data_Dictionary"
    application_description = 'dd' + str(fetch_random_string())
    case_properties = 'property'+ str(fetch_random_string())
    name_group = 'group'+ str(fetch_random_string())
    case_type = 'case_dd'
    case_data_link = 'https://staging.commcarehq.org/a/qa-automation/reports/case_data/d57fa5c7fb184d219e7fe155dabdbb6a/'
    english_value ='English'
    plain1 ='Plain'
    randomvalue1 = 'dyfuyvh'
    date1 = 'Date'
    number ='Number'
    updated_input = 'English'
    age_property_description = 'Testing the age property description'
    model_value = 'case'
    data_upload_path = "import_file.xlsx"
    p1p2_user = "p1p2.web.user@gmail.com"
    file = os.path.abspath(os.path.join(user_input_base_dir, "case_dd.xlsx"))
    lookup_function = '=(F2)'
