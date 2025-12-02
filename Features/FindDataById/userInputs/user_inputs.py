""""Contains test data that are used as user inputs across various areasn in CCHQ"""
import os
import random
import string

from common_utilities.generate_random_string import fetch_random_string
from common_utilities.path_settings import PathSettings


class UserData:


    """User Test Data"""
    location_name = 'value="Test Location [DO NOT DELETE!!!]"'
    invalid_id = 'barff57e-c455-4887-bca6-c43b29e82dde'
    # [userid ,location_id, group_id]
    user_details = {"prod": ['06023ed31ef7c7af67ce1526f47021c6', 'deee331b540d4211be7f95bb66e79578',
                             '8e4ee9b45a2a097ef41b43e1f47b2f01'],
                    "staging": ['7ed7f6e897b973005cb9d142c12ecdfd', '72f473f6cb324667967f8113ed6b6d79',
                                '6a28737916f8bd3098ae71b23060cc54']
                    }
    reassign_cases_app_data = {
        "app_name": "Reassign Cases",
        "case_list_name": "Case List",
        "form_name": "Registration Form"
    }