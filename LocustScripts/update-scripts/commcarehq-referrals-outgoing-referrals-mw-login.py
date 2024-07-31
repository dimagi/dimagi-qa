import logging
import time
import random

from locust import SequentialTaskSet, between, task, tag, events
from locust.exception import InterruptTaskSet

from user.models import UserDetails, BaseLoginCommCareUser
from common.args import file_path
from common.utils import RandomItems, load_json_data


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--domain", help="CommCare domain", required=True, env_var="COMMCARE_DOMAIN")
    parser.add_argument("--app-id", help="CommCare app id", required=True, env_var="COMMCARE_APP_ID")
    parser.add_argument("--app-config", help="Configuration of CommCare app", required=True)
    parser.add_argument("--user-details", help="Path to user details file", required=True)

APP_CONFIG = {}
USERS_DETAILS = RandomItems()
class WorkloadModelSteps(SequentialTaskSet):
    wait_time = between(5, 15)

    def on_start(self):
        self.FUNC_OUTGOING_REFERRALS_MENU = APP_CONFIG["FUNC_OUTGOING_REFERRALS_MENU"]
        self.FUNC_ENTER_GENDER = APP_CONFIG["FUNC_ENTER_GENDER"]
        self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM = APP_CONFIG["FUNC_OUTGOING_REFERRAL_DETAILS_FORM"]
        self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM_SUBMIT = APP_CONFIG["FUNC_OUTGOING_REFERRAL_DETAILS_FORM_SUBMIT"]
        self.cases_per_page = 100

    @tag('outgoing_referrals_menu')
    @task
    def outgoing_referrals_menu(self):
        self.user.hq_user.navigate(
            "Open Outgoing Referrals Menu",
            data={"selections": [self.FUNC_OUTGOING_REFERRALS_MENU['selections']]},
            expected_title=self.FUNC_OUTGOING_REFERRALS_MENU['title']
        )

    @tag('perform_a_search')
    @task
    def perform_a_search(self):
        extra_json = {
            "query_data": {
                "search_command.m10_results": {
                    "inputs": {
                        self.FUNC_ENTER_GENDER['input']: self.FUNC_ENTER_GENDER['inputValue']
                    },
                    "execute": True,
                    "force_manual_search": True}
            },
            "cases_per_page": self.cases_per_page,
            "selections": [self.FUNC_OUTGOING_REFERRALS_MENU["selections"]],
        }

        data = self.user.hq_user.navigate(
            "Perform a Search",
            data=extra_json,
            expected_title=self.FUNC_OUTGOING_REFERRALS_MENU['title']
        )

        self.entities = data["entities"]
        self.page_count = data["pageCount"]
        assert len(self.entities) > 0, "entities is empty"

    @tag('select_case')
    @task
    def select_case(self):
        self.selected_case_id = None

        page_num = 0
        while (not self.selected_case_id and page_num < self.page_count):
            for entity in self.entities:
                # When a case goes through this entire workflow, its status is changed to "resolved"
                # or "client_placed". However, it stays in the caselist. The workflow and form defined
                # in this test is specific to and work only if the case selected has status "open".
                if "open" in entity["data"]:
                    self.selected_case_id = entity["id"]
                    break
            if self.selected_case_id:
                break

            page_num+=1
            offset = page_num * self.cases_per_page

            extra_json={
                "selections": [self.FUNC_OUTGOING_REFERRALS_MENU['selections']],
                "cases_per_page": self.cases_per_page,
                "offset": offset,
            }
            data = self.user.hq_user.navigate(
                "Paginate for Case Selection",
                data=extra_json,
                expected_title=self.FUNC_OUTGOING_REFERRALS_MENU['title']
            )
            self.entities = data["entities"]

        assert self.selected_case_id != None, (
            "No case with status 'open' is available to be selected. "
            "A valid case needs to be created first "
        )
        logging.info("selected cases are " + str(
            self.selected_case_id) + " for mobile worker " + self.user.user_detail.login_as)

    @tag('enter_outgoing_referral_details_form')
    @task
    def enter_create_profile_and_refer_form(self):
        data = self.user.hq_user.navigate(
            "Enter 'Outgoing Referral Details' Form",
            data={"selections": [self.FUNC_OUTGOING_REFERRALS_MENU['selections'],
                                 self.selected_case_id,
                                 self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM['selections']
                                ]
                },
            expected_title=self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM['title']
        )
        self.session_id = data['session_id']

    @tag('answer_outgoing_referral_details_form_questions')
    @task
    def answer_outgoing_referral_details_form_questions(self):
        for question in self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM["questions"].values():
            extra_json = {
                    "ix": question["ix"],
                    "answer": question["answer"],
                    "session_id": self.session_id,
                }

            data = self.user.hq_user.answer(
                "Answer 'Outgoing Referral Details' Question",
                data=extra_json,
            )
            rng = random.randrange(1,3)
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
            if item.get('ix') == "10":
                self.attached_referral_requests_answers = find_question_ix(item)

    @tag('submit_outgoing_referral_details_form')
    @task
    def submit_outgoing_referral_details_form(self):
        utc_time_tuple = time.gmtime(time.time() - 86400) #ensure we're not picking a date that would be tomorrow in local time
        formatted_date = "{:04d}-{:02d}-{:02d}".format(utc_time_tuple.tm_year, utc_time_tuple.tm_mon,
                                                       utc_time_tuple.tm_mday)

        answers = {
            "2,0": 1,
            "3,1,0": 1,
            "3,1,5": formatted_date,
            "7,0": "OK",
            "8,0": "OK",
            "8,1": "OK",
            "8,2": None,
            "8,3,0": "OK",
            "8,3,1": "OK",
            "8,3,2": "OK",
            "8,3,3": "OK",
            "8,3,4": "OK",
            "8,3,5": "OK",
            "8,3,6": "OK",
            "8,3,7": "OK",
            "8,3,8": "OK",
            "8,3,9": "OK",
            "8,3,10": "OK",
            "8,3,11": "OK",
            "8,3,12": "OK",
            "8,3,13": "OK",
            "8,3,14": "OK",
            "8,3,15": "OK",
            "8,3,16": "OK",
            "8,3,17": "OK",
            "8,3,18": "OK",
            "8,3,19": "OK",
            "8,3,20": "OK",
            "8,3,21":"OK",
        }
        answers.update(self.attached_referral_requests_answers)
        input_answers= {d["ix"]: d["answer"] for d in self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM["questions"].values()}
        answers.update(input_answers)

        extra_json = {
            "answers": answers,
            "prevalidated": True,
            "debuggerEnabled": True,
            "session_id": self.session_id,
        }
        self.user.hq_user.submit_all(
            "Submit Outgoing Referral Details Form",
            extra_json,
            expected_response_message=self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM_SUBMIT['submitResponseMessage']
        )

@events.init.add_listener
def _(environment, **kw):
    try:
        app_config_path = file_path(environment.parsed_options.app_config)
        APP_CONFIG.update(load_json_data(app_config_path))
        logging.info("Loaded app config")
    except Exception as e:
        logging.error("Error loading app config: %s", e)
        raise InterruptTaskSet from e
    try:
        user_path = file_path(environment.parsed_options.user_details)
        user_data = load_json_data(user_path)["user"]
        USERS_DETAILS.set([UserDetails(**user) for user in user_data])
        logging.info("Loaded %s users", len(USERS_DETAILS.items))
    except Exception as e:
        logging.error("Error loading users: %s", e)
        raise InterruptTaskSet from e

class LoginCommCareHQWithUniqueUsers(BaseLoginCommCareUser):
    tasks = [WorkloadModelSteps]
    wait_time = between(5, 10)

    def on_start(self):
        super().on_start(
            domain=self.environment.parsed_options.domain,
            host=self.environment.parsed_options.host,
            user_details=USERS_DETAILS,
            app_id=self.environment.parsed_options.app_id
        )
