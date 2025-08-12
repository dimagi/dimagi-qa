import logging
import random
import string

import time
import uuid
from datetime import datetime

import requests
from locust import SequentialTaskSet, between, task, tag, events
from locust.exception import InterruptTaskSet

from common_utilities.path_settings import PathSettings
from user.models import UserDetails, BaseLoginCommCareUser
from common.args import file_path
from common.utils import RandomItems, load_json_data, load_yaml_data
import coloredlogs

logger = logging.getLogger(__name__)
level_styles = {
    'critical': {'color': 'red', 'bold': True},
    'error': {'color': 'red'},
    'warning': {'color': 'yellow'},
    'debug': {'color': 'green', 'bold': True},
    'notset': {'color': 'cyan'},
    'info': {'color': 'white'}
    }
coloredlogs.install(logger=logger, level='DEBUG', level_styles=level_styles
                    )  # install a handler on the root logger with level debug


@events.init_command_line_parser.add_listener
def _(parser):
    # Use below command to execute these tests:
    # locust -f .\LocustScripts\update-scripts\oncho_load\commcarehq-v2-rc.py --domain alafiacomm --build-id e9737bf399694c39910a5f885a0956d4 --app-id 08a1b1951e554a459f3bc6c8d08cd42e --app-config .\LocustScripts\update-scripts\project-config\alafiacomm-perf\app_config_v2_rc.json --user-details .\LocustScripts\update-scripts\project-config\alafiacomm-perf\mobile_worker_rc_credentials.json

    parser.add_argument("--domain", help="CommCare domain", required=True, env_var="COMMCARE_DOMAIN")
    parser.add_argument("--user-details", help="Path to user details file", required=True)


CONFIG = {}
# APP_CONFIG = {}
USERS_DETAILS = RandomItems()


@events.init.add_listener
def _(environment, **kw):
    try:
        config_path = file_path(environment.parsed_options.test_config)
        CONFIG.update(load_yaml_data(config_path))
        logging.info("Loaded config")
    except Exception as e:
        logging.error("Error loading app config: %s", e)
        raise InterruptTaskSet from e
    # try:
    #     app_config_path = file_path(environment.parsed_options.app_config)
    #     APP_CONFIG.update(load_json_data(app_config_path))
    #     logger.info("Loaded app config")
    # except Exception as e:
    #     logger.error("Error loading app config: %s", e)
    #     raise InterruptTaskSet from e
    try:
        user_path = file_path(environment.parsed_options.user_details)
        user_data = load_json_data(user_path)["user"]
        USERS_DETAILS.set([UserDetails(**user) for user in user_data])
        logger.info("Loaded %s users", len(USERS_DETAILS.items))
    except Exception as e:
        logger.error("Error loading users: %s", e)
        raise InterruptTaskSet from e


class WorkloadModelSteps(SequentialTaskSet):
    wait_time = between(0, 1)

    def on_start(self):
        self.filepath = PathSettings.ROOT + "/RequestAPI/Payloads/"
        self.input_file = "Test_XML_cca.xml"
        self.uri = f"{CONFIG['host']}/a/{CONFIG['domain']}"
        # self.api_key = self.user.user_detail.api_key
        self.headers = {'Content-Type': 'application/xml',
                        'Authorization': 'ApiKey ' + self.user.user_detail.username + ':' + self.user.user_detail.api_key}


    @tag('modify_case_properties')
    @task
    def modify_case_properties(self):
        logger.info("Open Home Screen for mobile worker " + self.user.user_detail.username)
        file = open(self.filepath + self.input_file, "r")
        # request_input = file.read()
        property_count = [90, 101]
        lines_of_file = file.readlines()
        file.close()
        self.new_filename = "Test_XML_cca_" + str(property_count[0]) + "_" + str(property_count[1]) + ".xml"
        logger.info("New Filename: ", self.new_filename)
        outFile = open(self.filepath + self.new_filename, "w")
        for i in range(property_count[0], property_count[1]):
            lines_of_file.insert(-14, "<n0:property" + str(i) + ">testvalue" + str(i) + "</n0:property" + str(i) + ">")
        outFile.writelines(lines_of_file)
        outFile.close()
        return self.new_filename

    @tag('ges_men')
    @task
    def ges_men(self):
        URL = self.uri + 'receiver/'
        user_count = [200000, 400001]
        for i in range(user_count[0], user_count[1]):
            logger.info(f"Replacing case_name with Kank_Name{i}")
            file = open(self.filepath + self.input_file, "r")
            request_input = file.read()
            form = request_input.replace("<n0:case_name>Test_Name</n0:case_name>",
                                         "<n0:case_name>Test_Name" + str(i) + "</n0:case_name>"
                                         )
            form = form.replace("b7c169c1-ae74-489a-b1f0-c683b2e4a7fe", str(uuid.uuid4()))
            form = form.replace("5b4dd8f0-39dd-4ec6-b842-561419719c25", str(uuid.uuid4()))
            form = form.replace("ddbf905262bed0abb6012e901f410e40", self.user.user_detail.ownerid)
            # with open(self.filepath + input_file, 'w') as f:
            #     f.write(request_input)
            # file = open(self.filepath + input_file, "r")
            # request_input = file.read()
            logger.info(form, URL)
            # file.close()
            # self.post_api(URL, form, self.headers, "xml")
            file.close()
            logger.info("Open 'Ges Men' Menu for mobile worker " + self.user.user_detail.username)

    def post_api(self, URL, input_payload, header, type="json"):
        if type == "json":
            self.response = requests.post(URL, json=input_payload, headers=header)
            # logger.info(response.json())
        else:
            self.response = requests.post(URL, data=input_payload, headers=header)
        logger.info("URL", URL)
        logger.info(self.response.status_code)
        logger.info(self.response.text)
        # logger.info(response.headers)

        assert self.response.status_code == 201
        return self.response
    
    @task
    def stop(self):
        self.interrupt()

class LoginCommCareHQWithUniqueUsers(BaseLoginCommCareUser):
    tasks = [WorkloadModelSteps]
    wait_time = between(3, 7)

    def on_start(self):
        super().on_start(
            domain=self.environment.parsed_options.domain,
            host=self.environment.parsed_options.host,
            user_details=USERS_DETAILS,
            )
