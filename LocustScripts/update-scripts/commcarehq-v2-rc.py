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
    # locust -f .\LocustScripts\update-scripts\oncho_load\commcarehq-v2-rc.py --domain alafiacomm --build-id e9737bf399694c39910a5f885a0956d4 --app-id 08a1b1951e554a459f3bc6c8d08cd42e --app-config .\LocustScripts\update-scripts\project-config\alafiacomm-perf\app_config_v2_rc.json --user-details .\LocustScripts\update-scripts\project-config\alafiacomm-perf\mobile_worker_rc_credentials.json

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
        self.FUNC_GES_MEN = APP_CONFIG['FUNC_GES_MEN']
        self.FUNC_ADD_HOUSEHOLD = APP_CONFIG['FUNC_ADD_HOUSEHOLD']
        self.FUNC_HOUSEHOLD_FORM = APP_CONFIG["FUNC_HOUSEHOLD_FORM"]
        self.FUNC_HOUSEHOLD_FORM_SUBMIT = APP_CONFIG['FUNC_HOUSEHOLD_FORM_SUBMIT']

    @tag('home_screen')
    @task
    def home_screen(self):
        self.user.hq_user.navigate_start(expected_title=self.FUNC_HOME_SCREEN['title'])
        logger.info("Open Home Screen for mobile worker " + self.user.user_detail.username)

    @tag('ges_men')
    @task
    def ges_men(self):
        self.user.hq_user.navigate(
            "Open 'Ges Men' Menu",
            data={"selections": [self.FUNC_GES_MEN['selections']]},
            expected_title=self.FUNC_GES_MEN['title']
            )
        logger.info("Open 'Ges Men' Menu for mobile worker " + self.user.user_detail.username)

    @task
    def answer_and_submit_add_household_form(self):
        logging.info("Generating names")
        for i in range(0, 3000):
            random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            fname = "FName" + str(i) + str(random_string)
            lname = "LName" + str(i) + str(random_string)
            address = "Home Add" + str(i) + str(random_string)
            session_id = self.move_household_form()
            # self.answer_add_household_form(session_id)
            self.submit_add_household_form(session_id, str(fname), str(lname), str(address))

    @tag('move_household_form')
    # @task
    def move_household_form(self):
        data = self.user.hq_user.navigate(
            "Open 'Add Household' Form",
            data={"selections": self.FUNC_ADD_HOUSEHOLD['selections']},
            expected_title=self.FUNC_ADD_HOUSEHOLD['title']
            )
        self.session_id = data['session_id']
        logger.info("Open 'Add Household' Form with session id: " + str(self.session_id
                                                                        ) + " for mobile worker " + self.user.user_detail.username
                    )
        return self.session_id

    @tag('submit_add_household_form')
    # @task
    def submit_add_household_form(self, session_id, fname, lname, address):
            logging.info(str(session_id)+" "+fname+" "+lname+" "+address)
            answers = {
                "3,0": "OK",
                "3,2": [53.74871079689897, 28.125699783533644],
                # "4,0":"OK",
                "4,2": fname,
                "4,3": lname,
                "4,4": 1,
                "4,5": None,
                "4,6": None,
                "4,7": 1,
                "4,8,0": 2,
                "4,8,2": 30,
                "4,8,3": 2,
                "4,8,4": 2,
                "5,0": address,
                "5,1": 1,
                "5,3": 1,
                "5,4": 1,
                "5,5": 1,
                "5,6": 1,
                "5,7,0": 2,
                "5,7,1": 2,
                "6,0": "OK",
                "6,6": "OK"
                }
            # input_answers = {d["ix"]: d["answer"] for d in self.FUNC_HOUSEHOLD_FORM["questions"].values()}
            # answers.update(input_answers)

            extra_json = {
                "answers": answers,
                "prevalidated": True,
                "debuggerEnabled": True,
                "session_id": session_id,
                }
            self.user.hq_user.submit_all(
                "Submit Add Household Form",
                extra_json,
                expected_response_message=self.FUNC_HOUSEHOLD_FORM_SUBMIT['submitResponseMessage']
                )
            logging.info(
                "Add Household submitted successfully - mobile worker:" + self.user.user_detail.username + " and session id: " + str(
                    session_id
                    ) + " ; request: submit_all"
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
