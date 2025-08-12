import logging
import os

from openpyxl import load_workbook
import random
import time
from datetime import datetime, timedelta
import random
from pytz import timezone
import re

from locust import SequentialTaskSet, between, task, tag, events
from locust.exception import InterruptTaskSet, StopUser

from common_utilities.generate_random_string import fetch_random_string
from user.models import UserDetails, BaseLoginCommCareUser, UserDetailsManager, HQUser, AppDetails
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
# locust -f .\LocustScripts\update-scripts\commcarehq-central-registry-search-and-admit-mw-l
    # ogin.py --domain co-carecoordination-perf --build-id  b9a1ef9ff5ba4b61957f1e0524f0dd03 --app-id 6283b3d054f141c88345c584a8f2c48f --app-config .\LocustScripts\update-scripts\project-config\co-careco
    # ordination-perf\app_config_central-registry.json --user-details .\LocustScripts\update-scripts\project-config\co-carecoordination-perf\mobile_worker_cre
    # dentials.json --cases-to-select .\LocustScripts\update-scripts\client-cases-import-example.xlsx

    parser.add_argument("--user-details", help="Path to user details file", required=True)
    parser.add_argument("--app-config", help="Configuration of CommCare app", required=True)
    parser.add_argument("--domain", help="CommCare domain", required=True, env_var="COMMCARE_DOMAIN")
    parser.add_argument("--app-id", help="CommCare app id", required=True, env_var="COMMCARE_APP_ID")
    parser.add_argument("--build-id", help="CommCare build id", required=True, env_var="COMMCARE_APP_ID")
    # parser.add_argument("--cases-to-select", help="Path to file containing cases to use for case search", required=True)

APP_CONFIG = {}
USERS_DETAILS = RandomItems()
TOTAL_USERS = 0


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
        current_hour = datetime.now(timezone("US/Mountain")).strftime("%H")
        manager = UserDetailsManager(user_path)
        USERS_DETAILS.set(manager.get_users_by_hour(current_hour))
        full_data = load_json_data(user_path)["users_by_hour"]
        user_data = full_data.get(current_hour, [])
        if not user_data:
            logger.warning(f"No users found for hour {current_hour}. Stopping execution.")
            raise InterruptTaskSet("No users for current hour")
        global TOTAL_USERS
        TOTAL_USERS = len(user_data)
        # Safe initialization of custom dict
        if not hasattr(environment, "user_classes_count"):
            environment.user_classes_count = {}
        environment.user_classes_count["LoginCommCareHQWithUniqueUsers"] = TOTAL_USERS
        logger.info("Loaded %s users for hour %s", len(USERS_DETAILS.items), current_hour)
        logger.info("Mountain Time hour: %s", current_hour)
        logger.debug("Available hours: %s", list(full_data.keys()))
    except Exception as e:
        logger.error("Error loading users: %s", e)
        raise InterruptTaskSet from e


class WorkloadModelSteps(SequentialTaskSet):
    wait_time = between(5, 15)

    def on_start(self):
        self.FUNC_HOME_SCREEN = APP_CONFIG['FUNC_HOME_SCREEN']
        self.FUNC_BED_AVAILABILITY_MENU = APP_CONFIG['FUNC_BED_AVAILABILITY_MENU']
        self.FUNC_BED_AVAILABILITY_FORM_SUBMIT = APP_CONFIG['FUNC_BED_AVAILABILITY_FORM_SUBMIT']
        # self.BED_AVAILABILITY_INPUTS = self.FUNC_BED_AVAILABILITY_FORM_SUBMIT["inputs"]

    @tag('home_screen')
    @task
    def home_screen(self):
        try:
            logger.info("Opening 'Home Screen' for user " + self.user.user_details.username+" to enter "+self.FUNC_HOME_SCREEN['title']
                    )
            self.user.hq_user.navigate_start(expected_title=self.FUNC_HOME_SCREEN['title'])
            self.wait()
        except AttributeError as e:
            logger.error(f"user_detail not found: {e}")
            raise StopUser()

    @tag('open_update_bed_availability_menu')
    @task
    def open_update_bed_availability_menu(self):
        self.data=self.user.hq_user.navigate(
            "Open 'Update Bed Availability' Menu",
            data={"selections": [self.FUNC_BED_AVAILABILITY_MENU['selections']]},
            expected_title=self.FUNC_BED_AVAILABILITY_MENU['title']
        )
        logger.info(f"Response: {self.data}")
        self.session_id=self.data["session_id"]
        logger.info(f"Open 'Update Bed Availability' Menu  for user {self.user.user_details.username} with session ID: {self.session_id}"
                    )

    @task
    def submit_update_bed_availability_form(self):
        all_answers=self.extract_question_answers(self.data)
        keys_to_check=self.get_first_5_numeric_ixs(all_answers)
        # self.answer_bed_avail_questions(self.data, keys_to_check)
        final_answers = self.extract_bed_data_from_caption(keys_to_check, self.data, all_answers)
        self.submit_update_bed_avail_form(final_answers, self.session_id)
        self.user.stop()

    @tag("extract_question_answers")
    def extract_question_answers(self, data):
        answers = {}

        def recurse(obj):
            if isinstance(obj, dict):
                if obj.get("type") == "question" and "ix" in obj and "answer" in obj:
                    answers[obj["ix"]] = obj["answer"]
                for v in obj.values():
                    recurse(v)
            elif isinstance(obj, list):
                for item in obj:
                    recurse(item)

        recurse(data)
        logger.info(f"Answers extracted")
        return answers

    def get_first_5_numeric_ixs(self, answers):
        numeric_ixs = [ix for ix, ans in answers.items() if isinstance(ans, (int, float))]
        return numeric_ixs[:5]

    # def answer_bed_avail_questions(self, response_data, keys_to_check):
    #     answers = {}
    #
    #     bed_metadata = self.extract_bed_data_from_caption(response_data, keys_to_check)
    #     form_config = self.FUNC_BED_AVAILABILITY_FORM_SUBMIT
    #     units = form_config.get("units", {})
    #
    #     for unit_label, unit_data in units.items():
    #         ix = unit_data.get("ix")
    #         if not ix:
    #             continue
    #
    #         question_key = unit_data.get("question")
    #         answer_key = unit_data.get("answer")
    #
    #         question_data = form_config.get(question_key, {})
    #         answer_data = form_config.get(answer_key, {})
    #
    #         # Handle FORM_UNIT_ONE
    #         if unit_label == "FORM_UNIT_ONE":
    #             for bed_label, q_info in question_data.items():
    #                 bed_ix = q_info["ix"]
    #                 original_answer = q_info.get("answer")
    #                 metadata = bed_metadata.get(bed_ix)
    #                 logger.info(f"original_answer: {original_answer}")
    #
    #                 if original_answer == 0:
    #                     answers[bed_ix] = 0
    #                 elif metadata and metadata.get("max_capacity") is not None:
    #                     answers[bed_ix] = max(0, metadata["max_capacity"] - 1)
    #         if unit_label != "FORM_UNIT_ONE":
    #             # Handle FORM_UNIT_TWO to FORM_UNIT_FIVE
    #             for bed_label, q_info in question_data.items():
    #                 bed_ix = q_info.get("ix")
    #                 if not bed_ix:
    #                     continue
    #                 # Only skip if value is None, not if key exists with valid value
    #                 response_value = response_data.get("answer", {}).get(bed_ix)
    #                 logger.info(f"response_value: {response_value}")
    #                 if response_value is not None:
    #                     answers[bed_ix] = response_value
    #
    #         # Merge static answer values for the unit
    #         for k, v in answer_data.items():
    #             answers[k] = v
    #
    #     self.attached_bed_avail_answers = answers

    def extract_bed_data_from_caption(self, keys_to_check, response_json, answers):
        def recurse(obj):
            if isinstance(obj, dict):
                if obj.get("type") == "question" and "ix" in obj and "caption" in obj:
                    ix = obj["ix"]
                    if ix in keys_to_check:
                        match = re.search(r"Max Capacity:\s*(\d+)", obj["caption"])
                        if match:
                            max_capacity = int(match.group(1))
                            answers[ix] = random.randint(1, max_capacity)
                for v in obj.values():
                    recurse(v)
            elif isinstance(obj, list):
                for item in obj:
                    recurse(item)

        recurse(response_json)
        return answers

    @tag('submit_update_bed_avail_form')
    def submit_update_bed_avail_form(self, final_answers, session_id):
        try:
            answers = {}
            answers.update(final_answers)

            # Include form-configured answers depending on what questions appeared
            # answer_type = getattr(self, "selected_answer_type", None)
            # if answer_type:
            #     config_answers = self.FUNC_BED_AVAILABILITY_FORM_SUBMIT.get(answer_type, {})
            #     answers.update(config_answers)

            extra_json = {
                "answers": answers,
                "prevalidated": True,
                "debuggerEnabled": True,
                "session_id": session_id,
                }

            self.user.hq_user.submit_all(
                "Submit Update Bed Availability Form",
                extra_json,
                status="success"
                # expected_response_message=self.FUNC_BED_AVAILABILITY_FORM_SUBMIT["submitResponseMessage"]
                )
            logger.info(extra_json)
            logger.info(
                f"{self.FUNC_BED_AVAILABILITY_FORM_SUBMIT["submitResponseMessage"]} - user: {self.user.user_details.username}; session: {session_id}"
                )
        except Exception as e:
            logger.exception("Task submit_update_bed_avail_form failed, stopping user")
            self.user.stop()

    def on_stop(self):
        logger.info(f"User {self.user.user_details.username} has finished all tasks and is stopping.")

class LoginCommCareHQWithUniqueUsers(BaseLoginCommCareUser):
    tasks = [WorkloadModelSteps]
    # wait_time = between(5, 10)
    # @staticmethod
    def wait_time(self):
        try:
            idx = getattr(USERS_DETAILS.last_returned.index, "index", 0)
            base = 3600 / TOTAL_USERS
            return between(base * idx, base * idx + 5)
        except Exception:
            return between(5, 10)


    def on_start(self):
        self.user_details = USERS_DETAILS.get()
        if hasattr(self, "user_details") and getattr(self.user_details, "index", None) is not None:
            idx = self.user_details.index
            total_users = TOTAL_USERS

            # Use remaining seconds from env or default to 3600
            try:
                total_duration = int(os.environ.get("REMAINING_SECONDS", "3600"))
            except ValueError:
                total_duration = 3600

            base_delay = total_duration / total_users
            delay = base_delay * idx
            logger.info(
                f"User {self.user_details.username} sleeping for {delay:.2f} seconds (based on {total_duration}s)"
                )
            time.sleep(delay)
        else:
            logger.warning("User index not set, skipping delay")

        if self.user_details is None:
            logger.warning("No available user credentials for this hour. User exiting.")
            self.environment.runner.quit()
            raise StopUser()

        domain = self.environment.parsed_options.domain
        host = self.environment.parsed_options.host
        build_id = self.environment.parsed_options.build_id
        app_id = self.environment.parsed_options.app_id

        app_details = AppDetails(domain=domain, app_id=app_id, build_id=build_id)
        self.hq_user = HQUser(self.client, self.user_details, app_details)
        self.hq_user.login(domain, host)
        self.hq_user.app_details.build_id, self.hq_user.app_details.app_id = self._get_build_info(build_id, app_id,
                                                                                                  domain
                                                                                                  )

    def _get_build_info(self, build_id, app_id, domain):
        # Placeholder logic to simulate actual retrieval
        return build_id, app_id

