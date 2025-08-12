import logging
import random
import string

import time
from datetime import datetime

from locust import SequentialTaskSet, between, task, tag, events
from locust.exception import InterruptTaskSet

from user.models import UserDetails, BaseLoginCommCareUser
from common.args import file_path
from common.utils import RandomItems, load_json_data
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
    # locust -f .\LocustScripts\update-scripts\commcarehq-v2-it.py --domain alafiacomm --build-id e010117e07ab3f47a1fdad6da7f0bfb9 --app-id 791fcbb98a0c4ffeb4aa38f20fd3544b --app-config .\LocustScripts\update-scripts\project-config\co-carecoordination-perf\app_config_v2_it_test.json --user-details .\LocustScripts\update-scripts\project-config\co-carecoordination-perf\mobile_worker_it_credentials.json

    parser.add_argument("--domain", help="CommCare domain", required=True, env_var="COMMCARE_DOMAIN")
    parser.add_argument("--build-id", help="CommCare build id", required=True, env_var="COMMCARE_APP_ID")
    parser.add_argument("--app-id", help="CommCare app id", required=True, env_var="COMMCARE_APP_ID")
    parser.add_argument("--app-config", help="Configuration of CommCare app", required=True)
    parser.add_argument("--user-details", help="Path to user details file", required=True)


APP_CONFIG = {}
USERS_DETAILS = RandomItems()


@events.init.add_listener
def _(environment, **kw):
    try:
        app_config_path = file_path(environment.parsed_options.app_config)
        APP_CONFIG.update(load_json_data(app_config_path))
        logger.info("Loaded app config")
    except Exception as e:
        logger.error("Error loading app config: %s", e)
        raise InterruptTaskSet from e
    try:
        user_path = file_path(environment.parsed_options.user_details)
        user_data = load_json_data(user_path)["user"]
        USERS_DETAILS.set([UserDetails(**user) for user in user_data])
        logger.info("Loaded %s users", len(USERS_DETAILS.items))
    except Exception as e:
        logger.error("Error loading users: %s", e)
        raise InterruptTaskSet from e


class WorkloadModelSteps(SequentialTaskSet):
    wait_time = between(3, 7)

    def on_start(self):
        self.FUNC_HOME_SCREEN = APP_CONFIG['FUNC_HOME_SCREEN']
        self.FUNC_REAF_MEN = APP_CONFIG['FUNC_REAF_MEN']
        self.FUNC_ANSWER_HOUSEHOLD = APP_CONFIG['FUNC_ANSWER_HOUSEHOLD']
        self.FUNC_REASSIGN_HOUSEHOLD_FORM = APP_CONFIG["FUNC_REASSIGN_HOUSEHOLD_FORM"]
        self.FUNC_HOUSEHOLD_FORM_SUBMIT = APP_CONFIG['FUNC_HOUSEHOLD_FORM_SUBMIT']

    @tag('home_screen')
    @task
    def home_screen(self):
        self.user.hq_user.navigate_start(expected_title=self.FUNC_HOME_SCREEN['title'])
        logger.info("Open Home Screen for mobile worker " + self.user.user_detail.username)

    @task
    def answer_and_submit_reassign_household_form(self):
        logging.info("Generating names")
        if "kb_test_1" in self.user.user_detail.username:
            n = 2
        else:
            n = 3
        for i in range(1, n):
            rc_list = list(range(1, i + 1))
            session_id = self.reaf_men(str(i))
            self.submit_reassign_household_form(session_id, rc_list, str(i))

    @tag('open_reaf_men_form')
    # @task
    def reaf_men(self, count):
        wrong_string = self.FUNC_REAF_MEN['title']
        title = wrong_string.encode('latin1').decode('utf-8')
        data = self.user.hq_user.navigate(
            "Open 'Reassign Household' Form",
            data={"selections": self.FUNC_REAF_MEN['selections']},
            expected_title=title
            )
        self.session_id = data['session_id']
        logger.info("Open 'Reassign Household' Form with session id: " + str(self.session_id
                                                                        ) + " for mobile worker " + self.user.user_detail.username +
                    " for loop count" + str(count)
                    )
        return self.session_id

    @tag('submit_add_household_form')
    def submit_reassign_household_form(self, session_id, rc_list, count):
            logging.info(str(session_id)+" "+count)
            logging.info(rc_list)
            answers = {
                "1": 1,
                "2,0": 1,
                "2,1": 1,
                "2,2": 1,
                "2,3": 2,
                "2,4": "OK",
                "2,5,0": rc_list,
                "3,1": "OK",
                "4,0": 1,
                "4,1": 1,
                "4,2": 1,
                "4,3": 1,
                "4,4": "OK",
                "5,1": "OK",
                "5,2": "OK",
                "5,3": 1
        }
            # input_answers = {d["ix"]: d["answer"] for d in self.FUNC_REASSIGN_HOUSEHOLD_FORM["questions"].values()}
            # answers.update(input_answers)

            extra_json = {
                "answers": answers,
                "prevalidated": True,
                "debuggerEnabled": True,
                "session_id": session_id,
                }
            wrong_string = self.FUNC_HOUSEHOLD_FORM_SUBMIT['submitResponseMessage']
            expected_response_message = wrong_string.encode('latin1').decode('utf-8')
            self.user.hq_user.submit_all(
                "Submit Reassign Household Form",
                extra_json,
                expected_response_message=expected_response_message
                )
            logging.info(
                "Reassign Household submitted successfully - mobile worker:" + self.user.user_detail.username + " and session id: " + str(
                    session_id
                    ) + " for loop count" + str(count)+" ; request: submit_all"
                )
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
            build_id=self.environment.parsed_options.build_id,
            app_id=self.environment.parsed_options.app_id
            )
