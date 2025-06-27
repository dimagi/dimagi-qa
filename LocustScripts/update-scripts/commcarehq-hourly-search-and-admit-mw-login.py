import logging
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
    # ogin.py --domain co-carecoordination-perf --build-id  2ae6dcfc44834e40a703155ebedd3bec --app-id 77bbaaa1d7e5404781bbe680ce9a90d2 --app-config .\LocustScripts\update-scripts\project-config\co-careco
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
        self.FUNC_SEARCH_AND_ADMIT_MENU = APP_CONFIG['FUNC_SEARCH_AND_ADMIT_MENU']
        self.FUNC_ADMIT_CLIENT_FORM = APP_CONFIG['FUNC_ADMIT_CLIENT_FORM']
        self.SEARCH_AND_ADMIT_INPUTS = self.FUNC_SEARCH_AND_ADMIT_MENU["inputs"]
        self.CLIENT_FORM_ANSWERS_A = self.FUNC_ADMIT_CLIENT_FORM["answers_a"]
        self.CLIENT_FORM_ANSWERS_B = self.FUNC_ADMIT_CLIENT_FORM["answers_b"]

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

    @tag('open_search_and_admit_menu')
    @task
    def open_search_and_admit_menu(self):
        self.user.hq_user.navigate(
            "Open 'Search And Admit' Menu",
            data={"selections": [self.FUNC_SEARCH_AND_ADMIT_MENU['selections']]},
            expected_title=self.FUNC_SEARCH_AND_ADMIT_MENU['title']
        )
        logger.info("Open 'Search and Admit' Menu  for user " + self.user.user_details.username
                    )

    @tag('search_and_admit_input')
    @task
    def search_and_admit_input(self):
        names = fetch_random_string()
        text = str(self.user.user_details.username).split('@')[0]
        user_text = text.replace('+','_')
        dob = (datetime.today() - timedelta(days=random.randint(18 * 365, 79 * 365))).strftime("%Y-%m-%d")
        self.inputs = {
            "first_name": "first_"+user_text +"_"+ names,
            "last_name": "last_"+user_text +"_"+ names,
            "case_search_ts": self.SEARCH_AND_ADMIT_INPUTS["INPUT_CASE_SEARCH_TS"],
            "fuzzy_match_dob": self.SEARCH_AND_ADMIT_INPUTS["INPUT_FUZZY_MATCH_DOB"],
            "dob": dob,
            "reason_for_no_ssn": self.SEARCH_AND_ADMIT_INPUTS["INPUT_REASON_FOR_NO_SSN"],
            "consent_collected": self.SEARCH_AND_ADMIT_INPUTS["INPUT_CONSENT_COLLECTED"]
            }
        extra_json = {
                "query_data": {
                    "m11_results:inline": {
                        "inputs": self.inputs,
                        "execute": False,
                        "force_manual_search": True,
                        "selections": [self.FUNC_SEARCH_AND_ADMIT_MENU["selections"]]
                    }
                },
                "selections": [self.FUNC_SEARCH_AND_ADMIT_MENU["selections"]]
            }

        self.user.hq_user.navigate(
                "Input for fields in 'Search and Admit' Menu",
                data=extra_json,
                expected_title=self.FUNC_SEARCH_AND_ADMIT_MENU['title']
            )
        logger.info("Entered 'Search and Admit' Inputs  for user " + self.user.user_details.username
                        )
        rng = random.randrange(1, 3)
        time.sleep(rng)


    @tag('click_add_new_client')
    @task
    def click_add_new_client(self):
        try:
            logger.info(f"Entering 'Admit Client' form for user " + self.user.user_details.username
                        )
            extra_json = {
            "query_data": {
                "m11_results:inline": {
                    "inputs": self.inputs,
                    "execute": True,
                    "force_manual_search": True,
                    "selections": [self.FUNC_SEARCH_AND_ADMIT_MENU["selections"]]
                }
            },
            "selections": self.FUNC_ADMIT_CLIENT_FORM["selections"]
            }

            data=self.user.hq_user.navigate(
                "Clicking 'Add a new Client' form",
                data=extra_json,
                expected_title=self.FUNC_ADMIT_CLIENT_FORM['title_a']
            )
            if not data or "session_id" not in data:
                logger.error(
                    f"Session ID not found in response for user {self.user.user_details.username}.Resubmitting."
                    )
                extra_json = {
                    "query_data": {
                        "m11_results:inline": {
                            "inputs": self.inputs,
                            "execute": True,
                            "force_manual_search": True,
                            "selections": [self.FUNC_SEARCH_AND_ADMIT_MENU["selections"]]
                            }
                        },
                    "selections": [self.FUNC_SEARCH_AND_ADMIT_MENU["selections"]]
                    }

                data = self.user.hq_user.navigate(
                    "Clicking 'Add a new Client' form",
                    data=extra_json,
                    expected_title=self.FUNC_ADMIT_CLIENT_FORM['title_b']
                    )


            self.session_id = data['session_id']
            self.page_title = data['title']
            logger.info("Entered 'Admit Client' form Inputs  for user " + self.user.user_details.username
                        )
            return self.session_id, self.page_title
        except Exception as e:
            logger.exception(f"Task click_add_new_client failed, stopping user {self.user.user_details.username}")
            self.user.stop()

    @task
    def submit_client_form(self):
        self.answer_admit_client_form_questions(self.session_id)
        self.submit_admit_client_form_form(self.session_id)
        self.user.stop()

    @tag('answer_admit_client_form_questions')
    def answer_admit_client_form_questions(self, session_id):
        # First, call hq_user.answer with a temporary payload to fetch the tree structure
        for candidate in [
            self.FUNC_ADMIT_CLIENT_FORM["questions"]["QUESTION_ENTERED_ADMISSION_DATA"],
            self.FUNC_ADMIT_CLIENT_FORM["questions"]["QUESTION_ENTERED_ADMISSION_DATA_ALT"]
            ]:
            temp_json = {
                "ix": candidate["ix"],
                "answer": candidate["answer"],
                "session_id": session_id,
                }

            data = self.user.hq_user.answer(
                "Determine which admit question to use", data=temp_json
                )

            # Check if tree has either ix = "1" or ix = "5"
            def tree_has_ix(tree, target_ix):
                for node in tree:
                    if node.get("ix") == target_ix:
                        return True
                    if "children" in node and tree_has_ix(node["children"], target_ix):
                        return True
                return False

            if tree_has_ix(data.get("tree", []), candidate["ix"]):
                question = candidate
                break
        else:
            logger.error("Neither ix '1' nor '5' found in form tree. Aborting.")
            self.user.stop()
            return

        # Continue with selected question
        extra_json = {
            "ix": question["ix"],
            "answer": question["answer"],
            "session_id": session_id,
            }

        data = self.user.hq_user.answer(
            "Answer 'Admit Client Form' Question",
            data=extra_json,
            )
        time.sleep(random.randint(1, 2))

        def find_ix(data, target_ixs):
            found_ixs = set()
            for item in data.get("children", []):
                if item.get("ix") in target_ixs:
                    found_ixs.add(item["ix"])
                if "children" in item:
                    found_ixs |= find_ix(item, target_ixs)
            return found_ixs

        found = set()
        for tree_node in data.get("tree", []):
            found |= find_ix(tree_node, {"4", "7"})

        if "4" in found:
            self.selected_answer_type = "answers_a"
        elif "7" in found:
            self.selected_answer_type = "answers_b"
        else:
            self.selected_answer_type = "answers_c"

        self.attached_admit_client_answers = {ix: "OK" for ix in found}

    @tag('submit_admit_client_form_form')
    def submit_admit_client_form_form(self, session_id):
        try:
            mountain_now = datetime.now(timezone("US/Mountain"))
            formatted_date = mountain_now.strftime("%Y-%m-%d")
            current_time = mountain_now.strftime("%H:%M")

            answers = {}

            # Include attached answers found in the form tree
            attached_answers = getattr(self, "attached_admit_client_answers", {})
            if isinstance(attached_answers, dict):
                answers.update(attached_answers)

            # Include form-configured answers depending on what questions appeared
            answer_type = getattr(self, "selected_answer_type", None)
            if answer_type:
                config_answers = self.FUNC_ADMIT_CLIENT_FORM.get(answer_type, {})
                answers.update(config_answers)

            # Inject correct dynamic values if present
            if "8" in answers:
                answers["8"] = formatted_date
            if "10" in answers:
                answers["10"] = current_time

            extra_json = {
                "answers": answers,
                "prevalidated": True,
                "debuggerEnabled": True,
                "session_id": session_id,
                }

            self.user.hq_user.submit_all(
                "Submit Admit Client Form",
                extra_json,
                expected_response_message=f"'{self.page_title}' successfully saved!"
                )
            logger.info(
                f"{self.page_title} submitted successfully - user: {self.user.user_details.username}; session: {session_id}"
                )

        except Exception as e:
            logger.exception("Task submit_client_form failed, stopping user")
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
            base = 3600 / TOTAL_USERS
            delay = base * idx
            logger.info(f"User {self.user_details.username} sleeping for {delay:.2f} seconds before starting")
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

