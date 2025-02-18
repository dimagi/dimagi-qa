from RequestAPI.testMethods.base import Base
from common_utilities.path_settings import PathSettings


class CurlMethods(Base):
    def __init__(self, settings):
        self.filepath = PathSettings.ROOT + "/RequestAPI/Payloads/"
        self.password = settings["password"]
        self.api_key = settings['api_key']
        self.headers = {'Content-Type': 'application/xml',
                        'Authorization': 'ApiKey ' + settings['login_user'] + ':' + settings['api_key']}

    def submission_api(self, uri, input_file, login_user, login_pass):
        URL = uri + 'receiver/'
        file = open(self.filepath + input_file, "r")
        request_input = file.read()
        print(request_input, URL)
        self.post_api(URL, request_input, login_user, login_pass, self.headers, "xml")

    def get_restore_ota(self, uri, login_user, login_pass):
        URL = uri + 'phone/restore/?version=2.0'
        headers = {'Authorization': 'ApiKey ' + login_user + ':' + self.api_key}
        result = self.get_api(URL, login_user, login_pass, headers)
        print(result.status_code)
        assert result.status_code == 200

    def post_lookup_table_upload(self, uri, input_file, login_user, login_pass):
        URL = uri + 'a/myproject/fixtures/fixapi/'
        data = {'replace': 'true'}
        file = [
            ('file-to-upload', ('case search.xlsx', open(self.filepath + input_file, 'rb'),
                                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))]
        headers = {'Authorization': 'ApiKey ' + login_user + ':' + self.api_key}
        result = self.post_api_file_upload(URL, data, login_user, login_pass, file, headers)
        assert result.status_code == 200

    def post_import_cases_from_excel(self, uri, input_file, login_user, login_pass):
        if "www" in uri:
            URL = uri + 'a/qa-automation-prod/importer/excel/bulk_upload_api/'
        else:
            URL = uri + 'a/qa-automation/importer/excel/bulk_upload_api/'
        data = {'case_type': 'form_linking',
                # 'search_field': 'external_id',
                'search_column': 'number',
                'create_new_cases': 'on'}
        file = [
            ('file', ('case search.xlsx', open(self.filepath + input_file, 'rb'),
                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))]
        headers = {'Authorization': 'ApiKey ' + login_user + ':' + self.api_key}
        result = self.post_api_file_upload(URL, data, login_user, login_pass, file, headers)
        assert result.status_code == 200
