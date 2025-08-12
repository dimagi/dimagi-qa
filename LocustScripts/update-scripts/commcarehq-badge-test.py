import logging

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
coloredlogs.install(logger=logger, level='DEBUG', level_styles=level_styles)  # install a handler on the root logger with level debug

@events.init_command_line_parser.add_listener
def _(parser):
    # Use below command to execute these tests:
    # locust -f .\LocustScripts\update-scripts\commcarehq-badge-test.py --domain co-carecoordination-perf --build-id 36f4769e96a5a95048857850a17fa99f --app-id f22041c733f14f9b89723a9358a92a35 --app-config .\LocustScripts\update-scripts\project-config\co-carecoordination-perf\app_config_badge_test.json --user-details .\LocustScripts\update-scripts\project-config\co-carecoordination-perf\mobile_worker_credentials_badge.json

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
        self.FUNC_COUNT = APP_CONFIG['FUNC_COUNT']
        self.FUNC_CLINIC_COUNT = APP_CONFIG['FUNC_CLINIC_COUNT']
        self.FUNC_CLINIC_COUNT_FORM_SUBMIT = APP_CONFIG['FUNC_CLINIC_COUNT_FORM_SUBMIT']

    @tag('home_screen')
    @task
    def home_screen(self):
        self.user.hq_user.navigate_start(expected_title=self.FUNC_HOME_SCREEN['title'])
        logger.info("Open Home Screen for mobile worker " + self.user.user_detail.username)

    @tag('count_menu')
    @task
    def count_menu(self):
        self.user.hq_user.navigate(
            "Open 'Counts' Menu",
            data={"selections": [self.FUNC_COUNT['selections']]},
            expected_title=self.FUNC_COUNT['title']
            )
        logger.info("Open 'Counts' Menu for mobile worker " + self.user.user_detail.username)

    @tag('clinic_count_menu')
    @task
    def clinic_count_menu(self):
        data = self.user.hq_user.navigate(
            "Open 'Clinic Counts' Menu",
            data={"selections": self.FUNC_CLINIC_COUNT['selections']},
            expected_title=self.FUNC_CLINIC_COUNT['title']
            )
        self.session_id = data['session_id']
        return self.session_id
        logger.info("Open 'Clinic Counts' Menu with session id: " + str(self.session_id ) + " for mobile worker "+ self.user.user_detail.username )

    @tag('submit_clinic_count_form')
    @task
    def submit_clinic_count_form(self):
        extra_json = {
            "answers": {0: "OK"},
            "prevalidated": True,
            "debuggerEnabled": True,
            "session_id": self.session_id,
            }
        self.user.hq_user.submit_all(
            "Submit Clinic Count Form",
            extra_json,
            expected_response_message=self.FUNC_CLINIC_COUNT_FORM_SUBMIT['submitResponseMessage']
            )
        logger.info("Clinic Count Form submitted successfully - user:" + self.user.user_detail.username + " and session id: " + str( self.session_id ) + " ; request: submit_all" )

    @tag('count_menu_again')
    @task
    def count_menu_again(self):
        start_time = datetime.now()
        self.user.hq_user.navigate(
            "Open 'Counts' Menu After Form Submission",
            data={"selections": [self.FUNC_COUNT['selections']]},
            expected_title=self.FUNC_COUNT['title'],
            commands_list=self.FUNC_COUNT['commands']
            )
        end_time = datetime.now()
        total_time = (end_time - start_time).total_seconds()
        if total_time <= 3:
            logger.debug("Open 'Counts' Menu load time for mobile worker " + self.user.user_detail.username +
                         " is : " + str(total_time) + " seconds"
                         )
        else:
            logger.warning("Open 'Counts' Menu load time for mobile worker " + self.user.user_detail.username +
                            " is : " + str(total_time) + " seconds"
                            )


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
