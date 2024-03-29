from RequestAPI.testMethods.base import Base
from common_utilities.path_settings import PathSettings


class CasesMethods(Base):
    def __init__(self, settings):
        self.filepath = PathSettings.ROOT + "/RequestAPI/Payloads/"
        self.password = settings["password"]
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'ApiKey ' + settings['login_user'] + ':' + settings['api_key']}

    def get_all_cases_list(self, uri, login_user, login_pass):
        URL = uri + 'case/'
        result = self.get_api(URL, login_user, login_pass, self.headers)
        json_response = result.json()
        print(result.status_code)
        # print(json_response['objects'][0]['id'])
        # return json_response['objects'][0]['id']

    def get_case_data(self, uri, login_user, login_pass):
        URL = uri + 'case/'
        result = self.get_api(URL, login_user, login_pass, self.headers)
        print(result.status_code)
