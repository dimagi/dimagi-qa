import csv
import json
import logging
import os
import random
import socket
import string

import time
import uuid
from datetime import datetime

import requests
from locust import SequentialTaskSet, between, task, tag, events
from locust.exception import InterruptTaskSet

from common_utilities.generate_random_string import chars
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
    #  locust -f .\LocustScripts\update-scripts\commcarehq-cca-json.py --domain cca-load-test --h
    # ost https://www.commcarehq.org/ --user-details .\LocustScripts\update-scripts\project-config\co-carecoordination-perf\web_users_credentials_cca_api.json
    #  --build-id 88e13dbdbabec8c810828cd337de276c --app-id 88e13dbdbabec8c810828cd337de276c --logfile=.\LocustScripts\update-scripts\cca_logs_18_03.log


    parser.add_argument("--domain", help="CommCare domain", required=True, env_var="COMMCARE_DOMAIN")
    parser.add_argument("--user-details", help="Path to user details file", required=True)
    parser.add_argument("--build-id", help="CommCare build id", required=True, env_var="COMMCARE_APP_ID")
    parser.add_argument("--app-id", help="CommCare app id", required=True, env_var="COMMCARE_APP_ID")


CONFIG = {}
USERS_DETAILS = RandomItems()


@events.init.add_listener
def _(environment, **kw):
    try:
        user_path = file_path(environment.parsed_options.user_details)
        user_data = load_json_data(user_path)["user"]
        USERS_DETAILS.set([UserDetails(**user) for user in user_data])
        logger.info("Loaded %s users", len(USERS_DETAILS.items))
    except Exception as e:
        logger.error("Error loading users: %s", e)
        raise InterruptTaskSet from e


class WorkloadModelSteps(SequentialTaskSet):
    wait_time = between(1, 3)

    def on_start(self):
        self.filepath = PathSettings.ROOT + "/dimagi-qa/LocustScripts/update-scripts/project-config/co-carecoordination-perf/"
        self.input_file = "Test_CCA_10_CP.json"
        self.cca_api_url = "https://commcare-analytics.dimagi.com/commcarehq_dataset/change/"
        self.json_header = {
            'Authorization': 'Bearer ',
            'Content-Type': 'application/json',
            'content-length': '399'
            }
        self.datasource_id = "0a194584ff35d96d39ca6bc8de156f84"
        self.USER_INPUT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        
    @task
    def create_cca_api(self):
        URL = self.cca_api_url
        # property_count = [1, 1001, 5] # for 5 users and 5k data
        # property_count = [1, 1001, 10] # for 10 user, 10k data
        # property_count = [1, 401, 15] # for 15 users
        property_count = [1, 501, 20] # for 20 users, 10k data
        # count = property_count[1] - property_count[0]
        file = open(self.filepath + self.input_file, "r")
        csv_file_name = f"Records_for_10_CP_{str(property_count[2])}_users_{self.user.user_detail.username}.csv"
        request_input = json.loads(file.read())
        # self.create_csv_file(csv_file_name)
        for i in range(property_count[0], property_count[1]):
            doc_id = str(uuid.uuid4())
            request_input["data"][0]["doc_id"] = doc_id
            request_input["data"][0]["computed_owner_name"] = self.user.user_detail.password
            request_input["doc_id"] = doc_id
            request_input["data_source_id"] = self.datasource_id
            random_string = ''.join(random.choices(chars, k=8))
            name = "Test_Name_" + random_string + "_" + str(i)
            request_input["data"][0]["name"] = name
            self.post_api(csv_file_name, URL, request_input, self.json_header, str(i), self.user.user_detail.username,
                          type="json"
                          )
        logging.info(f"Iterations ended for User {self.user.user_detail.username}")
        self.user.stop()


    @tag('post_api')
    def post_api(self, filename, URL, input_payload, header, loop_count, user, type="json"):
        if type == "json":
            start_time = datetime.now()
            response = requests.post(URL, json=input_payload, headers=header, timeout=60)
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
        else:
            start_time = datetime.now()
            response = requests.post(URL, data=input_payload, headers=header, timeout=60)
            end_time = datetime.now()
            total_time = (end_time - start_time).total_seconds()
            logging.info(response.status_code)
        self.write_to_csv(filename, user, response.status_code, loop_count, total_time)
        if response.status_code == 201 or response.status_code == 202:
            logging.info(f"Success with {response.status_code} within {total_time} seconds, Row count: {loop_count}, User: {user}.")
        elif response.status_code == 500 or response.status_code == 503:
            logging.info(f"API Request limit reached. Status code: {response.status_code}, Row count: {loop_count}, User: {user}.")
            self.user.stop()
        elif response.status_code == 443:
            logging.info(f"Max retries. Status code: {response.status_code}, Row count: {loop_count}, User: {user}.")
            self.user.stop()
        else:
            logging.info(f"Failed request with {response.status_code} within {total_time} seconds, Row count: {loop_count}, User: {user}.")
            self.user.stop()

    @tag('write_to_csv')
    def write_to_csv(self, filename, user, status_code, loop_count, total_time):
        data = [user, status_code, loop_count, total_time]
        print(data)
        filename = os.path.abspath(os.path.join(self.USER_INPUT_BASE_DIR,
                                                filename
                                                )
                                   )
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
        csvfile.close()

    # @tag('create_csv_file')
    # def create_csv_file(self, filename):
    #     filename = os.path.abspath(os.path.join(self.USER_INPUT_BASE_DIR,
    #                                             filename
    #                                             )
    #                                )
    #     with open(filename, 'w', newline='') as csvfile:
    #         fieldnames = ['users', 'status_code', 'loop_count', 'response_time']
    #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #         writer.writeheader()
    #     csvfile.close()

    @task
    def on_stop(self):
        logging.info(f"Stopped Test for {self.user.user_detail.username}")


class LoginCommCareHQWithUniqueUsers(BaseLoginCommCareUser):
    tasks = [WorkloadModelSteps]
    wait_time = between(1, 4)

    def on_start(self):
        super().on_start(
            domain=self.environment.parsed_options.domain,
            host=self.environment.parsed_options.host,
            user_details=USERS_DETAILS,
            build_id=self.environment.parsed_options.build_id,
            app_id=self.environment.parsed_options.app_id
            )
