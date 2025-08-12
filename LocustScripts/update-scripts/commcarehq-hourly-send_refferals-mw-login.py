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
        self.FUNC_SEND_REFERRALS_MENU = APP_CONFIG['FUNC_SEND_REFERRALS_MENU']
        self.FUNC_SEND_REFERRALS_SEARCH = APP_CONFIG['FUNC_SEND_REFERRALS_SEARCH']
        self.FUNC_SEARCH_AGE = APP_CONFIG['FUNC_SEARCH_AGE']
        self.FUNC_SEARCH_ACCEPTS_COMMCARE_REFFERALS = APP_CONFIG['FUNC_SEARCH_ACCEPTS_COMMCARE_REFFERALS']
        self.FUNC_SEND_REFFERALS_FORM = APP_CONFIG['FUNC_SEND_REFFERALS_FORM']
        self.FUNC_SEND_REFFERALS_FORM_QUESTIONS = self.FUNC_SEND_REFFERALS_FORM['questions']
        self.FUNC_CREATE_PROFILE_AND_REFER_FORM_SUBMIT = APP_CONFIG["FUNC_CREATE_PROFILE_AND_REFER_FORM_SUBMIT"]
        self.cases_per_page = 100

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

    @tag('open_send_referrals_menu')
    @task
    def open_send_referrals_menu(self):
        self.data_before=self.user.hq_user.navigate(
            "Open 'Send Referrals' Menu",
            data={"selections": [self.FUNC_SEND_REFERRALS_MENU['selections']]},
            expected_title=self.FUNC_SEND_REFERRALS_MENU['title']
        )
        logger.info(f"Response: {self.data_before}")
        logger.info(f"Open 'Send Referrals' Menu  for user {self.user.user_details.username}"
                    )

    @task
    def search_and_select_cases(self):
        case_id = self.mark_fav_case(self.data_before)
        after_search_data= self.search_beds()
        self.compare_first_cases(case_id, after_search_data)
        self.select_first_five_cases(after_search_data)

    @tag("mark_fav_case")
    def mark_fav_case(self, response_json):
        try:
            entities = response_json.get('entities', [])
            all_ids = list(map(lambda x: x['id'], entities))
            all_group_keys = list(map(lambda x: x['groupKey'], entities))
            # Extract first ID
            first_case_id = all_ids[0]
            first_group_key = all_group_keys[0]
            logger.info(f"First ID: {first_case_id} and groupKey: {first_group_key}")
            payload_endpoint = {
                "cases_per_page": self.cases_per_page,
                "endpoint_args": {"case_id": str(first_group_key)},
                "endpoint_id": "favoriting_icon_endpoint",
                "geo_location": None,
                "keepAPMTraces": False,
                "offset": 0,
                "query_data": {},
                "requestInitiatedByTag": "clickable_icon",
                "restoreAs": None,
                "search_text": None,
                "selections": [self.FUNC_SEND_REFERRALS_SEARCH["selections"]]
                }
            payload_detail = {
                "cases_per_page": self.cases_per_page,
                "isRefreshCaseSearch":True,
                "geo_location": None,
                "keepAPMTraces": False,
                "offset": 0,
                "query_data": {},
                "requestInitiatedByTag": "clickable_icon",
                "restoreAs": None,
                "search_text": None,
                "selections": [self.FUNC_SEND_REFERRALS_SEARCH["selections"], str(first_case_id)]
                }

            self.user.hq_user.get_endpoint(
                "Selecting first case as favorite",
                data=payload_endpoint
                )
            self.user.hq_user.get_details(
                "Selecting first case as favorite",
                data=payload_detail
                )
            time.sleep(3)
            return first_case_id
        except Exception as e:
            logger.exception(f"Task mark_fav_case failed, stopping user {self.user.user_details.username}")
            self.user.stop()

    @tag('search_beds')
    def search_beds(self):
        try:
            self.query_data = {
                    "m2_results:inline":{
                        "inputs": {
                            self.FUNC_SEARCH_AGE['input']: self.FUNC_SEARCH_AGE['inputValue'],
                            self.FUNC_SEARCH_ACCEPTS_COMMCARE_REFFERALS['input']: self.FUNC_SEARCH_ACCEPTS_COMMCARE_REFFERALS['inputValue'],
                            },
                        "execute": True
                        }
                    }
            self.search_query = {
                "query_data": self.query_data,
                "selections": [self.FUNC_SEND_REFERRALS_SEARCH['selections']],
                }
            searched_data = self.user.hq_user.navigate(
                "Searching Cases for Referrals",
                data=self.search_query,
                expected_title=self.FUNC_SEND_REFERRALS_SEARCH['title']
                )
            logger.info(f"Successfully searched beds for referral for user: {self.user.user_details.username}")
            return searched_data
        except Exception as e:
            logger.exception(f"Task search_beds failed, stopping user {self.user.user_details.username}")
            self.user.stop()

    @tag("compare_first_cases")
    def compare_first_cases(self, case_id_old, after_search_data):
        try:
            entities = after_search_data.get('entities', [])
            all_new_ids = list(map(lambda x: x['id'], entities))
            # Extract first ID after search
            new_first_case_id = all_new_ids[0]
            logger.info(f"New First Case ID: {new_first_case_id} and Old First Case ID: {case_id_old}")
            if new_first_case_id != case_id_old:
                assert True
                logger.info("Searching changed the endpoint successfully!")
            else:
                logger.warning("Searching did not change the endpoint!")
        except Exception as e:
            logger.exception(f"Task compare_first_cases failed, stopping user {self.user.user_details.username}")
            self.user.stop()

    @tag('select_cases')
    def select_first_five_cases(self, searched_data):
        try:
            logging.info(
                "Selecting Top 5 Cases - user:" + self.user.user_details.username + "; request: navigate_menu"
                )
            entities = searched_data.get('entities', [])
            # Extract first 5 IDs using lambda
            self.selected_case_ids = list(map(lambda x: x['id'], entities[:5]))

            logging.info(f"selected cases are {str(self.selected_case_ids)}for mobile worker {self.user.user_details.username}")
        except Exception as e:
            logger.exception(f"Task select_first_five_cases failed, stopping user {self.user.user_details.username}")
            self.user.stop()

    @tag('enter_create_profile_and_refer_form')
    @task
    def enter_create_profile_and_refer_form(self):
        try:
            logging.info("Entering form - user:" + self.user.user_details.username + "; request: navigate_menu")

            extra_json = {
                "selected_values": (list(self.selected_case_ids)),
                "query_data": self.query_data,
                "selections": [self.FUNC_SEND_REFFERALS_FORM['selections'], "use_selected_values"],
                }

            self.form_data = self.user.hq_user.navigate(
                "Enter 'Create Profile and Refer' Form",
                data=extra_json,
                expected_title=self.FUNC_SEND_REFFERALS_FORM['title']
                )
            self.session_id = self.form_data['session_id']
        except Exception as e:
            logger.exception(f"Task enter_create_profile_and_refer_form failed, stopping user {self.user.user_details.username}")
            self.user.stop()

    @tag('answer_create_profile_and_refer_form_questions')
    @task
    def answer_create_profile_and_refer_form_questions(self):
        try:
            for question in self.FUNC_SEND_REFFERALS_FORM_QUESTIONS.values():
                extra_json = {
                    "ix": question["ix"],
                    "answer": question["answer"],
                    "session_id": self.session_id,
                    }

                data = self.user.hq_user.answer(
                    "Answer 'Outgoing Referral Details' Question",
                    data=extra_json,
                    )
                rng = random.randrange(1, 3)
                time.sleep(rng)

            def find_question_ix(data, result=dict()):
                nested_items = data.get('children', {})
                for children in nested_items:
                    # If the current item matches the target_ix, check if it's a question
                    if children.get('type') == 'question':
                        result[children.get('ix')] = "OK"
                    if 'children' in children:
                        # If the current item has children, recursively call the function on them
                        find_question_ix(children, result)
                return result

            # Question ix 10 is a count repeat group that varies depending on the case selected.
            # So the "answer" with the appropriate ix keys need to be dynamically generated to be used in submit
            for item in data["tree"]:
                if item.get('ix') == "1.3":
                    self.attached_referral_requests_answers = find_question_ix(item)

        except Exception as e:
            logger.exception(f"Task answer_create_profile_and_refer_form_questions failed, stopping user {self.user.user_details.username}")
            self.user.stop()

    @tag('submit_create_profile_and_refer_form')
    @task
    def submit_create_profile_and_refer_form(self):
        try:
            logging.info("Submitting form - mobile worker:" + self.user.user_details.username + " and session id: " + str(
                self.session_id
                ) + " ; request: submit_all"
                         )
            mountain_now = datetime.now(timezone("US/Mountain"))
            formatted_date = mountain_now.strftime("%Y-%m-%d")
            answers = {
                "3": "OK",
                "8": "OK",
                "9": "OK",
                "1,1,0": "OK",
                # "1,1,1": 17,
                # "1,1,2": 1,
                "1,1,3": formatted_date,
                # "1,1,4": "Reason 1",
                # "1,1,5": "LOC 1",
                # "1,1,6": "Symptom 1",
                # "1,1,7": 1,
                "1,1,8": None,
                "1,1,9": None,
                "1,1,10": None,
                "1,1,11": None,
                "1,1,12": None,
                "1,1,13": None,
                # "1,3": 1,
                "1,7,0": [1],
                "4_0,5,0,0": "OK",
                "4_0,5,0,1": "OK",
                "4_0,5,0,2": "OK",
                "4_0,5,0,3": "OK",
                "4_0,5,0,4": "OK",
                "4_0,5,0,5": "OK",
                "4_0,6": None
                }
            attached_answers = getattr(self, "attached_referral_requests_answers", {})
            if isinstance(attached_answers, dict):
                answers.update(attached_answers)
            input_answers = {d["ix"]: d["answer"] for d in self.FUNC_SEND_REFFERALS_FORM_QUESTIONS.values()}
            answers.update(input_answers)
            logger.info(answers)
            extra_json = {
                "answers": answers,
                "prevalidated": True,
                "debuggerEnabled": True,
                "session_id": self.session_id,
                }

            self.user.hq_user.submit_all(
                "Submit Create Profile and Refer Form",
                extra_json,
                # status="success"
                expected_response_message=self.FUNC_CREATE_PROFILE_AND_REFER_FORM_SUBMIT['submitResponseMessage']
                )
            logging.info(
                "Create Profile and Refer Form submitted successfully - mobile worker:" + self.user.user_details.username + " and session id: " + str(
                    self.session_id
                    ) + " ; request: submit_all"
                )
            self.user.stop()
        except Exception as e:
            logger.exception(f"Task enter_create_profile_and_refer_form failed, stopping user {self.user.user_details.username}")
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

