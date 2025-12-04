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
    application_description = 'Enter app description here'
    case_properties = 'property'+ str(fetch_random_string())
    group_description = 'description' + str(fetch_random_string())
    updated_group_description_value = 'description updated'+ str(fetch_random_string())
    name_group = 'group'+ str(fetch_random_string())
    case_type = 'dd_case'
    case_data_link_staging = 'https://staging.commcarehq.org/a/qa-automation/reports/case_data/b54d86cb-6838-4dfd-9414-fedcb96a4ec6/'
    case_data_link_prod = 'https://www.commcarehq.org/a/qa-automation-prod/reports/case_data/4090aff0-bdf3-47ad-899c-bc2f8b5db8e2/'
    english_value ='English'
    plain ='Plain'
    multiple_choice = 'Multiple Choice'
    randomvalue = 'dyfuyvh'
    value = 'opened_date'
    number ='Number'
    updated_input = 'English'
    age_property_description = 'Testing the age property description'
    model_value = 'case'
    data_upload_path = "import_file.xlsx"
    p1p2_user = "p1p2.web.user@gmail.com"
    file = os.path.abspath(os.path.join(user_input_base_dir, "dd_case.xlsx"))
    lookup_function = '=(F2)'
    new_property_description ="property description is updated"
