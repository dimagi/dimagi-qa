import logging
import random
import time

from locust import SequentialTaskSet, between, events, tag, task
from locust.exception import InterruptTaskSet

from common.args import file_path
from common.utils import RandomItems, load_json_data
from user.models import UserDetails, BaseLoginCommCareUser


@events.init_command_line_parser.add_listener
def _(parser):
    #     """
    #     Use below command to execute this test:
    #     locust -f .\LocustScripts\update-scripts\commcarehq-referrals-search-for-beds-mw-login_sin
    # gle_case.py --domain co-carecoordination-perf --build-id b62974969e57051ad70160a798ed79e8 --app-id 3271c8c86a5344e59554dfcb3e4628b8 --app-config .\LocustScripts\upd
    # ate-scripts\project-config\co-carecoordination-perf\app_config_referrals_platform.json --user-details .\LocustScripts\update-scripts\project-config\co-c
    # arecoordination-perf\mobile_worker_credentials.json

    parser.add_argument("--domain", help="CommCare domain", required=True, env_var="COMMCARE_DOMAIN")
    parser.add_argument("--build-id", help="CommCare build id", required=True, env_var="COMMCARE_APP_ID")
    parser.add_argument("--app-id", help="CommCare app id", required=True, env_var="COMMCARE_APP_ID")
    parser.add_argument("--app-config", help="Configuration of CommCare app", required=True)
    parser.add_argument("--user-details", help="Path to user details file", required=True)


APP_CONFIG = {}
USERS_DETAILS = RandomItems()

class WorkloadModelSteps(SequentialTaskSet):
    wait_time = between(5, 15)

    def on_start(self):
        self.FUNC_HOME_SCREEN = APP_CONFIG['FUNC_HOME_SCREEN']
        self.FUNC_SEARCH_FOR_BEDS_MENU = APP_CONFIG['FUNC_SEARCH_FOR_BEDS_MENU']
        self.FUNC_CREATE_PROFILE_AND_REFER_FORM = APP_CONFIG['FUNC_CREATE_PROFILE_AND_REFER_FORM']
        self.FUNC_CREATE_PROFILE_AND_REFER_FORM_QUESTIONS = self.FUNC_CREATE_PROFILE_AND_REFER_FORM["questions"]
        self.FUNC_CREATE_PROFILE_AND_REFER_FORM_SUBMIT = APP_CONFIG['FUNC_CREATE_PROFILE_AND_REFER_FORM_SUBMIT']
        self.FUNC_OUTGOING_REFERRALS_MENU = APP_CONFIG["FUNC_OUTGOING_REFERRALS_MENU"]
        self.FUNC_ENTER_STATUS = APP_CONFIG["FUNC_ENTER_STATUS"]
        self.FUNC_ENTER_GENDER = APP_CONFIG["FUNC_ENTER_GENDER"]
        self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM = APP_CONFIG["FUNC_OUTGOING_REFERRAL_DETAILS_FORM"]
        self.FUNC_OUTGOING_REFERRAL_DETAILS_FORM_SUBMIT = APP_CONFIG["FUNC_OUTGOING_REFERRAL_DETAILS_FORM_SUBMIT"]
        self.cases_per_page = 100

    @tag('home_screen')
    @task
    def home_screen(self):
        self.user.hq_user.navigate_start(expected_title=self.FUNC_HOME_SCREEN['title'])

    @tag('search_for_beds_menu')
    @task
    def search_for_beds_menu(self):
        data = self.user.hq_user.navigate(
            "Open Search for Beds Menu",
            data={
                "selections": [self.FUNC_SEARCH_FOR_BEDS_MENU['selections']],
                "cases_per_page": self.cases_per_page,
                },
            expected_title=self.FUNC_SEARCH_FOR_BEDS_MENU['title']
            )
        if data:
            self.page_count = data["pageCount"]

    @tag('select_cases')
    @task
    def select_cases(self):
        logging.info(
            "Selecting Random Cases - mobile worker:" + self.user.user_detail.username + "; request: navigate_menu"
            )
        total_qty_cases_to_select = random.randrange(1, 2)
        self.selected_case_ids = set()

        # As is, this doesn't handle if there aren't enough cases to select. Also it won't handle well
        # situations where the ratio of # cases to select: # cases available to select are too high
        # since the same random case could be chosen multiple times. But for our use case, this ratio will be very low
        max_num_iterations = total_qty_cases_to_select
        i = 0
        while len(self.selected_case_ids) < total_qty_cases_to_select:
            random_page_num = random.randrange(0, self.page_count)
            offset = random_page_num * self.cases_per_page

            random_qty_cases_to_select_per_page = random.randrange(1, total_qty_cases_to_select + 1)
            qty_cases_remaining_to_select = total_qty_cases_to_select - len(self.selected_case_ids)
            qty_to_select = min(random_qty_cases_to_select_per_page, qty_cases_remaining_to_select)

            extra_json = {
                "selections": [self.FUNC_SEARCH_FOR_BEDS_MENU['selections']],
                "cases_per_page": self.cases_per_page,
                "offset": offset,
                }

            data = self.user.hq_user.navigate(
                "Paginate for Case Selection",
                data=extra_json,
                expected_title=self.FUNC_SEARCH_FOR_BEDS_MENU['title']
                )

            entities = data["entities"]
            ids = [entity["id"] for entity in entities if entity["id"] not in self.selected_case_ids]
            if len(ids) < qty_to_select:
                self.selected_case_ids.update(ids)
            else:
                for _ in range(qty_to_select):
                    random_case_index = random.randrange(0, len(ids))
                    self.selected_case_ids.add(ids[random_case_index])

            # crude way to avoid looping infinitely
            i += 1
            assert i < max_num_iterations, "exceeded allowed number of iterations to select cases for mobile worker " + self.user.user_detail.username
            rng = random.randrange(1, 3)
            time.sleep(rng)
        logging.info("selected cases are " + str(
            self.selected_case_ids
            ) + " for mobile worker " + self.user.user_detail.username
                     )

    @tag('enter_create_profile_and_refer_form')
    @task
    def enter_create_profile_and_refer_form(self):
        logging.info("Entering form - mobile worker:" + self.user.user_detail.username + "; request: navigate_menu")

        extra_json = {
            "selected_values": (list(self.selected_case_ids)),
            "query_data": {},
            "selections": [self.FUNC_SEARCH_FOR_BEDS_MENU['selections'], "use_selected_values"],
            }

        data = self.user.hq_user.navigate(
            "Enter 'Create Profile and Refer' Form",
            data=extra_json,
            expected_title=self.FUNC_CREATE_PROFILE_AND_REFER_FORM['title']
            )
        self.session_id = data['session_id']

    @tag('answer_create_profile_and_refer_form_questions')
    @task
    def answer_create_profile_and_refer_form_questions(self):
        logging.info("Answering Questions - mobile worker:" + self.user.user_detail.username + "; request: answer")
        for question in self.FUNC_CREATE_PROFILE_AND_REFER_FORM_QUESTIONS.values():
            extra_json = {
                "ix": question["ix"],
                "answer": question["answer"],
                "session_id": self.session_id,
                }
            self.user.hq_user.answer(
                "Answer 'Create Profile and Refer' Question",
                data=extra_json,
                )
            rng = random.randrange(1, 3)
            time.sleep(rng)

    @tag('submit_create_profile_and_refer_form')
    @task
    def submit_create_profile_and_refer_form(self):
        logging.info("Submitting form - mobile worker:" + self.user.user_detail.username + " and session id: " + str(self.session_id) +" ; request: submit_all")
        utc_time_tuple = time.gmtime(time.time())
        formatted_date = "{:04d}-{:02d}-{:02d}".format(utc_time_tuple.tm_year, utc_time_tuple.tm_mon,
                                                       utc_time_tuple.tm_mday
                                                       )
        answers = {
            "3": "OK",
            "8": "OK",
            "9": "OK",
            "1,1,0": "OK",
            "1,1,1": 21,
            "1,1,2": 2,
            "1,1,3": formatted_date,
            "1,1,4": "Symptoms encouraged visit",
            "1,1,5": "Inpatient",
            "1,1,6": "NOT HEADACHE",
            "1,1,7": 3,
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
        input_answers = {d["ix"]: d["answer"] for d in self.FUNC_CREATE_PROFILE_AND_REFER_FORM_QUESTIONS.values()}
        answers.update(input_answers)

        extra_json = {
            "answers": answers,
            "prevalidated": True,
            "debuggerEnabled": True,
            "session_id": self.session_id,
            }

        self.user.hq_user.submit_all(
            "Submit Create Profile and Refer Form",
            extra_json,
            status="success"
            # expected_response_message=self.FUNC_CREATE_PROFILE_AND_REFER_FORM_SUBMIT['submitResponseMessage']
            )
        logging.info("Create Profile and Refer Form submitted successfully - mobile worker:" + self.user.user_detail.username + " and session id: " + str(self.session_id) +" ; request: submit_all")


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
            build_id=self.environment.parsed_options.build_id,
            app_id=self.environment.parsed_options.app_id
            )
