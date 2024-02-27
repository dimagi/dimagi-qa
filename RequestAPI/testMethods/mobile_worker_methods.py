from RequestAPI.testMethods.base import Base
import jsonpath
import json

from common_utilities.generate_random_string import fetch_random_string, fetch_phone_number
from common_utilities.path_settings import PathSettings


class MobileWorkerMethods(Base):
    def __init__(self, settings):
        # self.filepath = "./RequestAPI/Payloads/"
        self.filepath = PathSettings.ROOT + "/Payloads/"
        self.password = settings["password"]
        self.headers = {'Content-Type': 'application/json; charset=utf-8',
                        'Authorization': 'ApiKey ' + settings['login_user'] + ':' + settings['api_key']}

    def mobile_worker_creation(self, uri, input_file, login_user, login_pass):
        URL = uri + 'user/'
        file = open(self.filepath + input_file, "r")
        request_input = json.loads(file.read())
        request_input["username"] = "Test_" + fetch_random_string()
        request_input["password"] = self.password
        request_input["first_name"] = fetch_random_string()
        request_input["last_name"] = fetch_random_string()
        request_input["email"] = "test@test.com"
        request_input["phone_numbers"] = fetch_phone_number()

        print(request_input, URL)
        result = self.post_api(URL, request_input, login_user, login_pass, self.headers)
        json_response = json.loads(result.text)
        print((jsonpath.jsonpath(json_response, "id"))[0])
        return (jsonpath.jsonpath(json_response, "id"))[0]

    def mobile_worker_edit(self, uri, mobile_user_id, input_file, login_user, login_pass):
        URL = uri + 'user/' + mobile_user_id + '/'
        file = open(self.filepath + input_file, "r")
        request_input = json.loads(file.read())
        request_input["password"] = self.password
        request_input["first_name"] = fetch_random_string() + " update"
        request_input["last_name"] = fetch_random_string() + " update"
        request_input["email"] = "test@test.com"
        request_input["phone_numbers"] = fetch_phone_number()

        print(request_input, URL)
        self.put_api(URL, request_input, login_user, login_pass, self.headers)

    def mobile_worker_delete(self, uri, mobile_user_id, login_user, login_pass):
        URL = uri + 'user/' + mobile_user_id + '/'
        self.delete_api(URL, login_user, login_pass, self.headers)

    def mobile_worker_get(self, uri, mobile_user_id, login_user, login_pass):
        URL = uri + 'user/' + mobile_user_id + '/'
        self.get_api(URL, login_user, login_pass, self.headers)

    def sms_mobile_worker_registration_api(self, uri, app_id, input_file, login_user, login_pass):
        URL = uri + 'sms_user_registration/'
        file = open(self.filepath + input_file, "r")
        request_input = json.loads(file.read())
        request_input['app_id'] = app_id
        request_input['users'][0]['phone_number'] = fetch_phone_number()
        print(request_input, URL)
        self.post_api(URL, request_input, login_user, login_pass, self.headers)

    def sms_cc_install_over_sms(self, uri, app_id, input_file, login_user, login_pass):
        URL = uri + 'sms_user_registration_reinstall/'
        file = open(self.filepath + input_file, "r")
        request_input = json.loads(file.read())
        request_input['app_id'] = app_id
        request_input['users'][0]['phone_number'] = fetch_phone_number()
        print(request_input, URL)
        self.post_api(URL, request_input, login_user, login_pass, self.headers)
