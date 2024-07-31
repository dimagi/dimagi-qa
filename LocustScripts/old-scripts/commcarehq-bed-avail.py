import logging
import os
import time

import yaml
import random
import json

from collections import defaultdict
from locust import HttpUser, SequentialTaskSet, between, task, tag, TaskSet
from lxml import etree
from datetime import datetime

from common.utils import RandomItems


# CASE_IDS = [
# "cff44c8cde5649c788a1ea2ff12b9235"
# ]

# "aef93695-5638-4ffa-8acd-5748339b7eaa",
# "0b5b3fec-acf5-470f-bb7b-a7e67471224a",


# noinspection PyShadowingNames
class WorkloadModelSteps(SequentialTaskSet):
    wait_time = between(5, 15)

    def on_start(self):
        # get domain user credential and app config info
        with open(self.user.app_config) as json_file:
            data = json.load(json_file)
            self.FUNC_HOME_SCREEN = data['FUNC_HOME_SCREEN']
            self.FUNC_BED_AVAILABILITY = data['FUNC_BED_AVAILABILITY']
            self.FUNC_BED_AVAILABILITY_FORM_SUBMIT = data['FUNC_BED_AVAILABILITY_FORM_SUBMIT']

        self._log_in()
        self._get_build_info()

    # noinspection PyUnusedLocal
    def _log_in(self):
        logging.info("_log_in")
        login_url = f'/a/{self.user.domain}/login/'
        response = self.client.get(login_url)
        response = self.client.post(
            login_url,
            {
                "auth-username": self.user.username,
                "auth-password": self.user.password,
                "cloud_care_login_view-current_step": ['auth'],  # fake out two_factor ManagementForm
            },
            headers={
                "X-CSRFToken": self.client.cookies.get('csrftoken'),
                "REFERER": f'{self.user.host}{login_url}',  # csrf requires this for secure requests
            },
        )
        assert (response.status_code == 200)
        assert ('Sign In' not in response.text)  # make sure we weren't just redirected back to login

    def _get_build_info(self):
        logging.info("_get_build_info")
        response = self.client.get(f'/a/{self.user.domain}/cloudcare/apps/v2/?option=apps', name='build info')
        assert (response.status_code == 200)
        for app in response.json():
            if app['copy_of'] == self.user.app_id:
                # get build_id
                self.build_id = app['_id']
        logging.info("build_id: " + self.build_id)

    #
    # @task
    # def sync_app(self):
    #     logging.info("sync_app")
    #     data = self._formplayer_post("sync-db", name="Sync App")
    #     assert (data['status'] == "accepted")
    #
    # @task
    # def clear_user_data(self):
    #     logging.info("clear user data")
    #     data = self._formplayer_post("clear_user_data", name="Clear User Data")
    #     assert (data['type'] == "success")

    @tag('home_screen')
    @task
    def home_screen(self):
        try:
            logging.info("home_screen")
            data = self._formplayer_post("navigate_menu_start", name="Home Screen", checkKey="title",
                                         checkValue=self.FUNC_HOME_SCREEN['title'])
            assert (data['title'] == self.FUNC_HOME_SCREEN['title'])
            logging.info(
                "user: " + self.user.username + "; mobile worker: " + self.user.login_as + "; request: navigate_menu_start")
        except Exception as e:
            logging.info(
                "user: " + self.user.username + "; mobile worker: " + self.user.login_as + "; request: navigate_menu_start; exception: " + str(e))

    @task
    def submitting_form(self):
        for i in range(0, 20):
            logging.info("perform_a_search_" + str(i))
            self.open_bed_availability(i)
            self.bed_availability_form_submit(i)
            rng = random.randrange(5, 15)
            time.sleep(rng)
            logging.info("Sleeping for-->" + str(rng))

    @tag('bed_availability')
    def open_bed_availability(self, i):
        try:
            logging.info("bed_availability_" + str(i))
            start_time = time.time()
            data = self._formplayer_post("navigate_menu", extra_json={
                "selections": [self.FUNC_BED_AVAILABILITY['selections']],
            }, name="Open Bed Availability", checkKey="title", checkValue=self.FUNC_BED_AVAILABILITY['title'])
            end_time = time.time()
            total_time = end_time - start_time
            logging.info(
                "Total response time for Opening Bed Availability Form for user: " + self.user.username + " with mobile worker: " + self.user.login_as + " for loop " + str(
                    i) + " is " + str(total_time) + " seconds.")
            if not ("session_id" in data):
                logging.info("case not found -- no session_id")
                self.interrupt()
            self.session_id = data['session_id']
            assert (data['title'] == self.FUNC_BED_AVAILABILITY['title'])
            logging.info(
                "user: " + self.user.username + "; mobile worker: " + self.user.login_as + "; request: navigate_menu")
        except Exception as e:
            logging.info(
                "user: " + self.user.username + "; mobile worker: " + self.user.login_as + "; request: navigate_menu; exception: " + str(e))

    @tag('bed_availability_form_submit')
    def bed_availability_form_submit(self, i):
        try:
            logging.info("submitting bed availability form for loop " + str(i))
            start_time = time.time()
            data = self._formplayer_post("submit-all", extra_json={
                "answers": {
                    "0_0,0,0": None,
                    "0_0,0,2_0,0,1": "OK",
                    "0_0,0,2_0,0,2": None,
                    "0_0,0,2_0,0,5": "OK",
                    "0_0,0,2_0,0,6_0,0": "OK",
                    "0_0,0,2_0,0,6_0,1": "OK",
                    "0_0,0,2_0,0,6_0,2": "OK",
                    "0_0,0,2_0,0,6_0,3": random.randrange(1, 10),
                    "0_0,0,2_0,0,6_1,0": "OK",
                    "0_0,0,2_0,0,6_1,1": "OK",
                    "0_0,0,2_0,0,6_1,2": "OK",
                    "0_0,0,2_0,0,6_1,3": random.randrange(1, 10),
                    "0_0,0,2_0,0,6_2,0": "OK",
                    "0_0,0,2_0,0,6_2,1": "OK",
                    "0_0,0,2_0,0,6_2,2": "OK",
                    "0_0,0,2_0,0,6_2,3": random.randrange(1, 10),
                    "0_0,0,2_0,0,6_3,0": "OK",
                    "0_0,0,2_0,0,6_3,1": "OK",
                    "0_0,0,2_0,0,6_3,2": "OK",
                    "0_0,0,2_0,0,6_3,3": random.randrange(1, 10),
                    "0_0,0,2_0,0,6_4,0": "OK",
                    "0_0,0,2_0,0,6_4,1": "OK",
                    "0_0,0,2_0,0,6_4,2": "OK",
                    "0_0,0,2_0,0,6_4,3": random.randrange(1, 10),
                    "0_0,0,2_1,0,1": "OK",
                    "0_0,0,2_1,0,2": None,
                    "0_0,0,2_1,0,5": "OK",
                    "0_0,0,2_1,0,6_0,0": "OK",
                    "0_0,0,2_1,0,6_0,1": "OK",
                    "0_0,0,2_1,0,6_0,2": "OK",
                    "0_0,0,2_1,0,6_0,3": random.randrange(1, 10),
                    "0_0,0,2_1,0,6_1,0": "OK",
                    "0_0,0,2_1,0,6_1,1": "OK",
                    "0_0,0,2_1,0,6_1,2": "OK",
                    "0_0,0,2_1,0,6_1,3": random.randrange(1, 10),
                    "0_0,0,2_1,0,6_2,0": "OK",
                    "0_0,0,2_1,0,6_2,1": "OK",
                    "0_0,0,2_1,0,6_2,2": "OK",
                    "0_0,0,2_1,0,6_2,3": random.randrange(1, 10),
                    "0_0,0,2_1,0,6_3,0": "OK",
                    "0_0,0,2_1,0,6_3,1": "OK",
                    "0_0,0,2_1,0,6_3,2": "OK",
                    "0_0,0,2_1,0,6_3,3": random.randrange(1, 10),
                    "0_0,0,2_1,0,6_4,0": "OK",
                    "0_0,0,2_1,0,6_4,1": "OK",
                    "0_0,0,2_1,0,6_4,2": "OK",
                    "0_0,0,2_1,0,6_4,3": random.randrange(1, 10),
                    "0_0,0,2_2,0,1": "OK",
                    "0_0,0,2_2,0,2": None,
                    "0_0,0,2_2,0,5": "OK",
                    "0_0,0,2_2,0,6_0,0": "OK",
                    "0_0,0,2_2,0,6_0,1": "OK",
                    "0_0,0,2_2,0,6_0,2": "OK",
                    "0_0,0,2_2,0,6_0,3": random.randrange(1, 10),
                    "0_0,0,2_2,0,6_1,0": "OK",
                    "0_0,0,2_2,0,6_1,1": "OK",
                    "0_0,0,2_2,0,6_1,2": "OK",
                    "0_0,0,2_2,0,6_1,3": random.randrange(1, 10),
                    "0_0,0,2_2,0,6_2,0": "OK",
                    "0_0,0,2_2,0,6_2,1": "OK",
                    "0_0,0,2_2,0,6_2,2": "OK",
                    "0_0,0,2_2,0,6_2,3": random.randrange(1, 10),
                    "0_0,0,2_2,0,6_3,0": "OK",
                    "0_0,0,2_2,0,6_3,1": "OK",
                    "0_0,0,2_2,0,6_3,2": "OK",
                    "0_0,0,2_2,0,6_3,3": random.randrange(1, 10),
                    "0_0,0,2_2,0,6_4,0": "OK",
                    "0_0,0,2_2,0,6_4,1": "OK",
                    "0_0,0,2_2,0,6_4,2": "OK",
                    "0_0,0,2_2,0,6_4,3": random.randrange(1, 10),
                    "0_0,0,2_3,0,1": "OK",
                    "0_0,0,2_3,0,2": None,
                    "0_0,0,2_3,0,5": "OK",
                    "0_0,0,2_3,0,6_0,0": "OK",
                    "0_0,0,2_3,0,6_0,1": "OK",
                    "0_0,0,2_3,0,6_0,2": "OK",
                    "0_0,0,2_3,0,6_0,3": random.randrange(1, 10),
                    "0_0,0,2_3,0,6_1,0": "OK",
                    "0_0,0,2_3,0,6_1,1": "OK",
                    "0_0,0,2_3,0,6_1,2": "OK",
                    "0_0,0,2_3,0,6_1,3": random.randrange(1, 10),
                    "0_0,0,2_3,0,6_2,0": "OK",
                    "0_0,0,2_3,0,6_2,1": "OK",
                    "0_0,0,2_3,0,6_2,2": "OK",
                    "0_0,0,2_3,0,6_2,3": random.randrange(1, 10),
                    "0_0,0,2_3,0,6_3,0": "OK",
                    "0_0,0,2_3,0,6_3,1": "OK",
                    "0_0,0,2_3,0,6_3,2": "OK",
                    "0_0,0,2_3,0,6_3,3": random.randrange(1, 10),
                    "0_0,0,2_3,0,6_4,0": "OK",
                    "0_0,0,2_3,0,6_4,1": "OK",
                    "0_0,0,2_3,0,6_4,2": "OK",
                    "0_0,0,2_3,0,6_4,3": random.randrange(1, 10),
                    "0_0,0,2_4,0,1": "OK",
                    "0_0,0,2_4,0,2": None,
                    "0_0,0,2_4,0,5": "OK",
                    "0_0,0,2_4,0,6_0,0": "OK",
                    "0_0,0,2_4,0,6_0,1": "OK",
                    "0_0,0,2_4,0,6_0,2": "OK",
                    "0_0,0,2_4,0,6_0,3": random.randrange(1, 10),
                    "0_0,0,2_4,0,6_1,0": "OK",
                    "0_0,0,2_4,0,6_1,1": "OK",
                    "0_0,0,2_4,0,6_1,2": "OK",
                    "0_0,0,2_4,0,6_1,3": random.randrange(1, 10),
                    "0_0,0,2_4,0,6_2,0": "OK",
                    "0_0,0,2_4,0,6_2,1": "OK",
                    "0_0,0,2_4,0,6_2,2": "OK",
                    "0_0,0,2_4,0,6_2,3": random.randrange(1, 10),
                    "0_0,0,2_4,0,6_3,0": "OK",
                    "0_0,0,2_4,0,6_3,1": "OK",
                    "0_0,0,2_4,0,6_3,2": "OK",
                    "0_0,0,2_4,0,6_3,3": random.randrange(1, 10),
                    "0_0,0,2_4,0,6_4,0": "OK",
                    "0_0,0,2_4,0,6_4,1": "OK",
                    "0_0,0,2_4,0,6_4,2": "OK",
                    "0_0,0,2_4,0,6_4,3": random.randrange(1, 10)
                },
                "prevalidated": True,
                "debuggerEnabled": True,
                "session_id": self.session_id,
            }, name="Bed Availability Form Submit", checkKey="submitResponseMessage",
                                         checkValue=self.FUNC_BED_AVAILABILITY_FORM_SUBMIT[
                                             'submitResponseMessage'])
            end_time = time.time()
            total_time = end_time - start_time
            logging.info(
                "Total response time for Submitting Bed Availability Form for user: " + self.user.username + " with mobile worker: " + self.user.login_as + " for loop " + str(
                    i) + " is " + str(total_time) + " seconds.")
            logging.info(
                "user: " + self.user.username + "; mobile worker: " + self.user.login_as + "; request: submit-all")
        except Exception as e:
            logging.info(
                "user: " + self.user.username + "; mobile worker: " + self.user.login_as + "; request: submit-all; exception: " + str(e))

        @task
        def stop(self):
            self.interrupt()

    def _formplayer_post(self, command, extra_json=None, name=None, checkKey=None, checkValue=None, checkLen=None):
        json = {
            "app_id": self.build_id,
            "domain": self.user.domain,
            "locale": "en",
            "restoreAs": self.user.login_as,
            "username": self.user.username,
        }
        if extra_json:
            json.update(extra_json)
        name = name or command

        if 'XSRF-TOKEN' not in self.client.cookies:
            response = self.client.get(f"{self.parent.formplayer_host}/serverup")
            response.raise_for_status()

        xsrf_token = self.client.cookies['XSRF-TOKEN']
        headers = {'X-XSRF-TOKEN': xsrf_token}
        self.client.headers.update(headers)

        with self.client.post(f"{self.user.formplayer_host}/{command}/", json=json, name=name,
                              catch_response=True) as response:
            data = response.json()
            # logging.info("data-->" + str(data))
            if "exception" in data:
                logging.info("ERROR::exception error--" + data['exception'])
                logging.info("ERROR::user-info::" + self.user.username + "::" + self.user.login_as)
                response.failure("exception error--" + data['exception'])
            elif checkKey and checkKey not in data:
                logging.info("error::" + checkKey + " not in data")
                response.failure("ERROR::" + checkKey + " not in data")
            # elif checkKey and checkLen:
            #     if len(data[checkKey]) != checkLen:
            #         logging.info("ERROR::len(data['" + checkKey + "']) != " + checkLen)
            #         response.failure("error::len(data['" + checkKey + "']) != " + checkLen)
            # elif checkKey and checkValue:
            #     if data[checkKey] != checkValue:
            #         logging.info("ERROR::data['" + checkKey + "'] != " + checkValue)
            #         response.failure("error::data['" + checkKey + "'] != " + checkValue)
        return response.json()


class LoginCommCareHQWithUniqueUsers(HttpUser):
    tasks = [WorkloadModelSteps]

    formplayer_host = "/formplayer"
    project = 'co-carecoordination-perf'  # str(os.environ.get("project"))
    domain_user_credential_force = str(os.environ.get("user_credential"))
    app_config_force = str(os.environ.get("app_config_bed_tracking_tool"))
    wait_time_force = "test"

    if wait_time_force == "test":
        wait_time = between(5, 10)

    else:
        wait_time = between(45, 90)

    with open("project-config/" + project + "/config.yaml") as f:
        config = yaml.safe_load(f)
        host = config['host']
        domain = config['domain']
        app_id = config['app_id']
        if domain_user_credential_force != "None":
            domain_user_credential = "project-config/" + project + "/" + domain_user_credential_force
        else:
            domain_user_credential = config['domain_user_credential']
        if app_config_force != "None":
            app_config = "project-config/" + project + "/" + app_config_force
        else:
            app_config = config['app_config_bed_tracking_tool']

    # get domain user credential and app config info
    with open(domain_user_credential) as json_file:
        data = json.load(json_file)
        data_user = RandomItems(data['user'])

    def on_start(self):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        dt_object = datetime.fromtimestamp(timestamp)
        user_info = self.data_user.get()
        self.username = user_info['username']
        self.password = user_info['password']
        self.login_as = user_info['login_as']
        print("userinfo===>>" + str(user_info))

        logging.info("timestamp-->>>" + str(dt_object))
        logging.info("host-->>>" + self.host)
        logging.info("login_as-->>>" + self.login_as)
        logging.info("username-->>>" + self.username)
        logging.info("domain-->>>" + self.domain)
        logging.info("domain_user_credential-->>>" + self.domain_user_credential)
        logging.info("app_config-->>>" + self.app_config)
