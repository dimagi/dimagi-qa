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
#     """
#     Use the below command to execute this test:
# locust -f .\LocustScripts\update-scripts\commcarehq-referrals-outgoing-referrals-mw-login.
# py --domain co-carecoordination-perf --build-id b62974969e57051ad70160a798ed79e8 --app-id 3271c8c86a5344e59554dfcb3e4628b8 --app-config .\LocustScripts\
# update-scripts\project-config\co-carecoordination-perf\app_config_referrals_platform.json --user-details .\LocustScripts\update-scripts\project-config\c
# o-carecoordination-perf\mobile_worker_credentials.json


# """


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



class WorkloadModelSteps(SequentialTaskSet):
    wait_time = between(5, 15)

    def on_start(self):
        self.FUNC_HOME_SCREEN = APP_CONFIG['FUNC_HOME_SCREEN']
        self.FUNC_SEARCH_FOR_BEDS_MENU = APP_CONFIG['FUNC_SEARCH_FOR_BEDS_MENU']
        self.FUNC_OUTGOING_REFERRALS_MENU = APP_CONFIG["FUNC_OUTGOING_REFERRALS_MENU"]
        self.FUNC_ENTER_STATUS = APP_CONFIG["FUNC_ENTER_STATUS"]
        self.FUNC_ENTER_GENDER = APP_CONFIG["FUNC_ENTER_GENDER"]
        self.FUNC_OUTGOING_REFERRALS = APP_CONFIG["FUNC_OUTGOING_REFERRALS"]
        self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM = APP_CONFIG["FUNC_OUTGOING_REFERRAL_DETAILS_FORM"]
        self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM_SUBMIT = APP_CONFIG["FUNC_OUTGOING_REFERRAL_DETAILS_FORM_SUBMIT"]
        self.cases_per_page = 100

    @tag('home_screen')
    @task
    def home_screen(self):
        self.user.hq_user.navigate_start(expected_title=self.FUNC_HOME_SCREEN['title'])

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
        self.selected_case_ids = set()
        
        extra_json = {
            "query_data": {
                "search_command.m12_results": {
                    "inputs": {
                        self.FUNC_ENTER_STATUS['input']: self.FUNC_ENTER_STATUS['inputValue'],
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

        entities = data["entities"]
        assert len(entities) > 0, "entities is empty"
        logging.info("No of entities in result: " + str(len(entities)))
        self.selected_case_ids = {entity["id"] for entity in entities}
        self.selected_case_list = list(self.selected_case_ids)
        logging.info("selected cases are " + str(
            self.selected_case_list
            ) + " for mobile worker " + self.user.user_detail.username
                     )

    @task
    def submit_outgoing_referrals_form(self):
        random_ids = random.sample(self.selected_case_list, random.randrange(3, 7))
        logging.info("Randomly selected ids: " + str(random_ids))

        for ids in random_ids:
            logging.info("Proceeding with id: "+ str(ids))
            self.select_case(str(ids))
            session_id = self.enter_outgoing_referral_details_form(str(ids))
            self.answer_outgoing_referral_details_form_questions(session_id)
            self.submit_outgoing_referral_details_form(session_id)


    @tag('select_case')
    def select_case(self, selected_case_id):
        data = self.user.hq_user.navigate(
            "Selecting Case",
            data={"selections": [self.FUNC_OUTGOING_REFERRALS['selections'],
                                 selected_case_id,
                                 ]
                  },
            expected_title=self.FUNC_OUTGOING_REFERRALS['title']
            )
        logging.info("selecting case " + str(
            selected_case_id
            ) + " for outgoing referral for user " + self.user.user_detail.username
                     )

    @tag('enter_outgoing_referral_details_form')
    # @task
    def enter_outgoing_referral_details_form(self, selected_case_id):
        data = self.user.hq_user.navigate(
            "Enter 'Outgoing Referral Details' Form",
            data={"selections": [self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM['selections'],
                                 selected_case_id,
                                 self.FUNC_SEARCH_FOR_BEDS_MENU['selections']
                                ]
                },
            expected_title=self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM['title']
        )
        self.session_id = data['session_id']
        logging.info("Enter 'Outgoing Referral Details' Form with case id " + str(
            selected_case_id
            ) + " and session id: "+str(self.session_id)+ " for mobile worker " + self.user.user_detail.username
                     )
        return self.session_id

    @tag('answer_outgoing_referral_details_form_questions')
    # @task
    def answer_outgoing_referral_details_form_questions(self, session_id):
        for question in self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM["questions"].values():
            extra_json = {
                    "ix": question["ix"],
                    "answer": question["answer"],
                    "session_id": session_id,
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
            if item.get('ix') == "13":
                self.attached_referral_requests_answers = find_question_ix(item)

    @tag('submit_outgoing_referral_details_form')
    # @task
    def submit_outgoing_referral_details_form(self, session_id):
        utc_time_tuple = time.gmtime(time.time() - 86400) #ensure we're not picking a date that would be tomorrow in local time
        formatted_date = "{:04d}-{:02d}-{:02d}".format(utc_time_tuple.tm_year, utc_time_tuple.tm_mon,
                                                       utc_time_tuple.tm_mday)

        answers = {
            "3,0": 1,
            "4,1,0": 1,
            "4,1,5": formatted_date,
            "9,0": "OK",
            "10,0": "OK",
            "10,1": "OK",
            "10,2": None,
            "10,3,0": "OK",
            "10,3,1": "OK",
            "10,3,2": "OK",
            "10,3,3": "OK",
            "10,3,4": "OK",
            "10,3,5": "OK",
            "10,3,6": "OK",
            "10,3,7": "OK",
            "10,3,8": "OK",
            "10,3,9": "OK",
            "10,3,10": "OK",
            "10,3,11": "OK",
            "10,3,12": "OK",
            "10,3,13": "OK",
            "10,3,14": "OK",
            "10,3,15": "OK",
            "10,3,16": "OK",
            "10,3,17": "OK",
            "10,3,18": "OK",
            "10,3,19": "OK"
        }
        answers.update(self.attached_referral_requests_answers)
        input_answers = {d["ix"]: d["answer"] for d in self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM["questions"].values()}
        answers.update(input_answers)

        extra_json = {
            "answers": answers,
            "prevalidated": True,
            "debuggerEnabled": True,
            "session_id": session_id,
        }
        self.user.hq_user.submit_all(
            "Submit Outgoing Referral Details Form",
            extra_json,
            expected_response_message=self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM_SUBMIT['submitResponseMessage']
        )
        logging.info("Outgoing Referral Details Form submitted successfully - mobile worker:" + self.user.user_detail.username + " and session id: " + str(
                session_id
                ) + " ; request: submit_all"
            )


class LoginCommCareHQWithUniqueUsers(BaseLoginCommCareUser):
    tasks = [WorkloadModelSteps]
    wait_time = between(5, 10)

    def on_start(self):
        super().on_start(
            domain=self.environment.parsed_options.domain,
            host=self.environment.parsed_options.host,
            user_details=USERS_DETAILS,
            build_id=self.environment.parsed_options.build_id,
            app_id=self.environment.parsed_options.app_id
        )
