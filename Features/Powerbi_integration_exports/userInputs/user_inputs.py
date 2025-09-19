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
    reassign_cases_application = 'Reassign Cases'
    reassign_menu = 'Case List'
    reassign_form = 'Registration Form'
    reassign_case = 'reassign'
    name = 'powerbi_odatafeed1'
    updatedname = 'updated_powerbi_odatafeed1'
    description = 'testing the powerbi form report'
    Basic_tests_application = 'Basic Tests'
    Basic_menu = 'Formplayer Specific Tests'
    Repeat_form = '[Formplayer] Repeats'
    parent = 'sub_case_one'
    odata_feed_form = ''
    case='case'
