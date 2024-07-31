import logging

from locust import SequentialTaskSet, constant_pacing, events, run_single_user, tag, task
from locust.exception import InterruptTaskSet

from common.args import file_path
from common.utils import RandomItems, load_json_data, load_yaml_data
from user.models import UserDetails, BaseLoginCommCareUser


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--test-config", help="Configuration of test", required=True)


CONFIG = {}
APP_CONFIG = {}
USERS_DETAILS = RandomItems()


@events.init.add_listener
def _(environment, **kw):
    try:
        config_path = file_path(environment.parsed_options.test_config)
        CONFIG.update(load_yaml_data(config_path))
        logging.info("Loaded config")
    except Exception as e:
        logging.error("Error loading app config: %s", e)
        raise InterruptTaskSet from e

    try:
        config_path = file_path(CONFIG["app_config_bed_tracking_tool"])
        APP_CONFIG.update(load_json_data(config_path))
        logging.info("Loaded config")
    except Exception as e:
        logging.error("Error loading app config: %s", e)
        raise InterruptTaskSet from e

    try:
        user_path = file_path(CONFIG["domain_user_credential"])
        user_data = load_json_data(user_path)["user"]
        USERS_DETAILS.set([UserDetails(**user) for user in user_data])
        logging.info("Loaded %s users", len(USERS_DETAILS.items))
    except Exception as e:
        logging.error("Error loading users: %s", e)
        raise InterruptTaskSet from e


class WorkloadModelSteps(SequentialTaskSet):

    def on_start(self):
        # get domain user credential and app config info
        self.FUNC_HOME_SCREEN = APP_CONFIG['FUNC_HOME_SCREEN']
        self.FUNC_SEARCH_FOR_BEDS_MENU = APP_CONFIG['FUNC_SEARCH_FOR_BEDS_MENU']
        self.FUNC_ENTER_AGE = APP_CONFIG['FUNC_ENTER_AGE']
        self.FUNC_GENDER_IDENTITY = APP_CONFIG['FUNC_GENDER_IDENTITY']
        self.FUNC_INVOLUNTARY_CLIENT = APP_CONFIG['FUNC_INVOLUNTARY_CLIENT']
        self.FUNC_JUSTICE_INVOLVED_CLIENT = APP_CONFIG['FUNC_JUSTICE_INVOLVED_CLIENT']
        self.FUNC_CARE_TYPE = APP_CONFIG['FUNC_CARE_TYPE']
        self.FUNC_FACILITY_NAME = APP_CONFIG['FUNC_FACILITY_NAME']
        self.FUNC_RESIDENTIAL_SERVICE = APP_CONFIG['FUNC_RESIDENTIAL_SERVICE']
        self.FUNC_POPULATION_SPECIALTY = APP_CONFIG['FUNC_POPULATION_SPECIALTY']
        self.FUNC_INSURANCE_ACCEPTED = APP_CONFIG['FUNC_INSURANCE_ACCEPTED']
        self.FUNC_ACCOMMODATIONS = APP_CONFIG['FUNC_ACCOMMODATIONS']
        self.FUNC_LANGUAGE_SERVICES = APP_CONFIG['FUNC_LANGUAGE_SERVICES']
        self.FUNC_OPEN_BEDS = APP_CONFIG['FUNC_OPEN_BEDS']
        self.FUNC_PERFORM_A_SEARCH = APP_CONFIG['FUNC_PERFORM_A_SEARCH']

    # @tag('sync_app')
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
        self.user.hq_user.navigate_start(expected_title=self.FUNC_HOME_SCREEN['title'])

    @tag('search_for_beds_menu')
    @task
    def search_for_beds_menu(self):
        data = {"selections": [self.FUNC_SEARCH_FOR_BEDS_MENU['selections']]}
        self.user.hq_user.navigate(
            "Open Search for Beds Menu",
            data=data, expected_title=self.FUNC_SEARCH_FOR_BEDS_MENU['title']
        )

    @tag('non_facet_search')
    @task
    def perform_a_non_facet_search(self):
        for i in range(20):
            data = {
                "query_data": {
                    "m1_results.inline": {
                        "inputs": {},
                        "execute": True
                    }
                },
                "selections": ["0"],
            }
            self.user.hq_user.navigate("Perform a non-faceted search", data=data)
            self.wait()

    @tag('facet_search')
    @task
    def perform_a_facet_search(self):
        for i in range(20):
            data = {
                "query_data": {
                    "m1_results.inline": {
                        "inputs": {
                            self.FUNC_ENTER_AGE['input']: self.FUNC_ENTER_AGE['inputValue'],
                            self.FUNC_GENDER_IDENTITY['input']: self.FUNC_GENDER_IDENTITY['inputValue'],
                            self.FUNC_INVOLUNTARY_CLIENT['input']: self.FUNC_INVOLUNTARY_CLIENT['inputValue'],
                            self.FUNC_JUSTICE_INVOLVED_CLIENT['input']: self.FUNC_JUSTICE_INVOLVED_CLIENT[
                                'inputValue'],
                            self.FUNC_CARE_TYPE['input']: self.FUNC_CARE_TYPE['inputValue'],
                            self.FUNC_FACILITY_NAME['input']: self.FUNC_FACILITY_NAME['inputValue'],
                            self.FUNC_RESIDENTIAL_SERVICE['input']: self.FUNC_RESIDENTIAL_SERVICE['inputValue'],
                            self.FUNC_POPULATION_SPECIALTY['input']: self.FUNC_POPULATION_SPECIALTY['inputValue'],
                            self.FUNC_INSURANCE_ACCEPTED['input']: self.FUNC_INSURANCE_ACCEPTED['inputValue'],
                            self.FUNC_ACCOMMODATIONS['input']: self.FUNC_ACCOMMODATIONS['inputValue'],
                            self.FUNC_LANGUAGE_SERVICES['input']: self.FUNC_LANGUAGE_SERVICES['inputValue'],
                            self.FUNC_OPEN_BEDS['input']: self.FUNC_OPEN_BEDS['inputValue']
                        },
                        "execute": True}
                },
                "selections": ["0"],
            }
            self.user.hq_user.navigate("Perform a faceted search", data=data)
            self.wait()

    @task
    def stop(self):
        logging.info("stopping - mobile worker: %s", self.user.user_detail)
        self.interrupt()

class LoginCommCareHQWithUniqueUsers(BaseLoginCommCareUser):
    tasks = [WorkloadModelSteps]
    wait_time = constant_pacing(5)

    def on_start(self):
        super().on_start(
            domain=CONFIG["domain"],
            host=CONFIG["host"],
            user_details=USERS_DETAILS,
            app_id=CONFIG["app_id"]
        )

if __name__ == "__main__":
    run_single_user(LoginCommCareHQWithUniqueUsers)
