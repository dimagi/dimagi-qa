import logging

from locust import constant, events, run_single_user, task
from locust.exception import InterruptTaskSet

from app_script.runner import AppScriptRunner
from app_script.timing import TimingCategory
from common.args import file_path
from common.utils import load_json_data, load_yaml_data
from user.models import BaseLoginCommCareUser, UserDetails

from app_script import actions, validations


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--test-config", help="Configuration of test", required=True)


CONFIG = {}
USERS_DETAILS = []


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
        user_path = file_path(CONFIG["domain_user_credential"])
        user_data = load_json_data(user_path)["user"]
        USERS_DETAILS.extend([UserDetails(**user) for user in user_data])
        logging.info("Loaded %s users", len(USERS_DETAILS))
    except Exception as e:
        logging.error("Error loading users: %s", e)
        raise InterruptTaskSet from e


class LoginCommCareHQWithUniqueUsers(BaseLoginCommCareUser):
    wait_time = constant(1)

    def on_start(self):
        super().on_start(
            domain=CONFIG["domain"],
            host=CONFIG["host"],
            user_details=USERS_DETAILS,
            app_id=CONFIG["app_id"]
        )

    @task
    def find_matching_beds(self):
        script = [
            actions.NavigateStart(
                "Navigate Start",
                timing=TimingCategory.SIS,
                validations=[validations.ValidateTitle("Bed Tracking Tool (Linked)")]
            ),
            actions.Navigate(
                "Nav to Search for Beds", selections=["0"],
                timing=TimingCategory.SIS,
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.UserWait("Initial load", TimingCategory.SIS),
            actions.Search(
                "Search: Age -> Under 18", input_data={"age": "minors_adolescents"},
                timing=TimingCategory.SIS,
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.Search(
                "Search: Gender -> Woman", input_data={"gender": "women"},
                timing=TimingCategory.SIS,
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.Search(
                # Zip code: 80904
                "Search: Location -> Colorado Springs", input_data={"geopoint": "38.84642 -104.863753"},
                timing=TimingCategory.SIS,
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.Search(
                "Search: Distance -> 25", input_data={"distance": "25"},
                timing=TimingCategory.SIS,
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.Search(
                "Search: Care Type -> both", input_data={"facility_category": "both"},
                timing=TimingCategory.SIS,
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.Search(
                "Search: Residential Services -> Medically Assisted Therapy",
                input_data={"residential_services": "medication_assisted_therapy"},
                timing=TimingCategory.SIS,
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.Search(
                "Search: Insurance -> Medicaid", input_data={"insurance": "medicaid"},
                timing=TimingCategory.SIS,
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.Search(
                "Search: Accommodations -> Deaf", input_data={"accommodations": "deaf_hard_of_hearing"},
                timing=TimingCategory.SIS,
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.Search(
                "Search: Review no match", execute=True, timing=TimingCategory.RNO,
                validations=[
                    validations.ValidateTitle("Search for Beds"),
                    validations.HasEntityCount(max=0)
                ]
            ),
            actions.ResetSearchInput(
                "Reset Search Input: Residential Services", timing=TimingCategory.SIS,
                input_keys=["residential_services"],
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.ResetSearchInput(
                "Reset Search Input: Accommodations", timing=TimingCategory.SIS,
                input_keys=["accommodations"],
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.Search(
                "Search: Review matches", execute=True, timing=TimingCategory.RNO,
                validations=[
                    validations.ValidateTitle("Search for Beds"),
                    validations.HasEntityCount(min=1)
                ]
            ),
            actions.Search(
                "Search: Accommodations -> Deaf", timing=TimingCategory.SIS,
                input_data={"accommodations": "deaf_hard_of_hearing"},
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.Search(
                "Search: Distance -> 10", timing=TimingCategory.SIS,
                input_data={"distance": "10"},
                validations=[validations.ValidateTitle("Search for Beds")]
            ),
            actions.Search(
                "Search: Review matches", execute=True, timing=TimingCategory.RNO,
                validations=[
                    validations.ValidateTitle("Search for Beds"),
                    validations.HasEntityCount(min=1)
                ]
            ),
            actions.SelectEntity(
                "Load Form & review", entity_index=0, timing=TimingCategory.PDI,
                validations=[validations.ValidateTitle("View Facility and Unit Info")]
            ),
            actions.SubmitForm("Submit Form", answers=FACILITY_REVIEW_FORM_ANSWERS)
        ]
        AppScriptRunner("Find Matching Beds", self, script).run()


FACILITY_REVIEW_FORM_ANSWERS = {
    "0,0": "OK",
    "1_0,1,0,0,0": None,
    "1_0,1,1,0": "OK",
    "1_0,1,1,1": "OK",
    "1_0,1,1,2": "OK",
    "1_0,1,1,3": "OK",
    "1_0,1,1,4": "OK",
    "1_0,1,1,5": "OK",
    "1_0,1,1,6": "OK",
    "1_0,1,1,7": "OK",
    "1_0,1,1,8": "OK",
    "1_0,1,1,9": "OK",
    "1_0,1,1,10": "OK",
    "1_0,1,1,11": "OK",
    "1_0,1,1,12": "OK",
    "1_0,1,1,13": "OK",
    "1_0,1,1,14": "OK",
    "1_0,1,1,15": "OK",
    "1_0,1,1,16": "OK",
    "1_0,1,1,17": "OK",
    "1_0,1,1,18": "OK",
    "1_0,1,1,19": "OK",
    "1_0,1,1,20,0": "OK",
    "1_0,1,1,20,1": "OK",
    "1_0,1,2,0_0,1,0,0": "OK",
    "1_0,1,2,0_0,1,0,1": "OK",
    "1_0,1,2,0_0,1,0,2": "OK",
    "1_0,1,2,0_0,1,0,3": "OK",
    "1_0,1,2,0_0,1,0,4": "OK",
    "1_0,1,2,0_0,1,0,5": "OK",
    "1_0,1,2,0_0,1,0,6": "OK",
    "1_0,1,2,0_0,1,0,7": "OK",
    "1_0,1,2,0_0,1,0,8": "OK",
    "1_0,1,2,0_0,1,0,9": "OK",
    "1_0,1,2,0_0,1,0,10": "OK",
    "1_0,1,2,0_0,1,0,11": "OK",
    "1_0,1,2,0_0,1,0,12": "OK",
    "1_0,1,2,0_0,1,0,13": "OK",
    "1_0,1,2,0_1,1,0,0": "OK",
    "1_0,1,2,0_1,1,0,1": "OK",
    "1_0,1,2,0_1,1,0,2": "OK",
    "1_0,1,2,0_1,1,0,3": "OK",
    "1_0,1,2,0_1,1,0,4": "OK",
    "1_0,1,2,0_1,1,0,5": "OK",
    "1_0,1,2,0_1,1,0,6": "OK",
    "1_0,1,2,0_1,1,0,7": "OK",
    "1_0,1,2,0_1,1,0,8": "OK",
    "1_0,1,2,0_1,1,0,9": "OK",
    "1_0,1,2,0_1,1,0,10": "OK",
    "1_0,1,2,0_1,1,0,11": "OK",
    "1_0,1,2,0_1,1,0,12": "OK",
    "1_0,1,2,0_1,1,0,13": "OK",
    "1_0,1,2,0_2,1,0,0": "OK",
    "1_0,1,2,0_2,1,0,1": "OK",
    "1_0,1,2,0_2,1,0,2": "OK",
    "1_0,1,2,0_2,1,0,3": "OK",
    "1_0,1,2,0_2,1,0,4": "OK",
    "1_0,1,2,0_2,1,0,5": "OK",
    "1_0,1,2,0_2,1,0,6": "OK",
    "1_0,1,2,0_2,1,0,7": "OK",
    "1_0,1,2,0_2,1,0,8": "OK",
    "1_0,1,2,0_2,1,0,9": "OK",
    "1_0,1,2,0_2,1,0,10": "OK",
    "1_0,1,2,0_2,1,0,11": "OK",
    "1_0,1,2,0_2,1,0,12": "OK",
    "1_0,1,2,0_2,1,0,13": "OK",
    "1_0,1,2,0_3,1,0,0": "OK",
    "1_0,1,2,0_3,1,0,1": "OK",
    "1_0,1,2,0_3,1,0,2": "OK",
    "1_0,1,2,0_3,1,0,3": "OK",
    "1_0,1,2,0_3,1,0,4": "OK",
    "1_0,1,2,0_3,1,0,5": "OK",
    "1_0,1,2,0_3,1,0,6": "OK",
    "1_0,1,2,0_3,1,0,7": "OK",
    "1_0,1,2,0_3,1,0,8": "OK",
    "1_0,1,2,0_3,1,0,9": "OK",
    "1_0,1,2,0_3,1,0,10": "OK",
    "1_0,1,2,0_3,1,0,11": "OK",
    "1_0,1,2,0_3,1,0,12": "OK",
    "1_0,1,2,0_3,1,0,13": "OK",
    "1_0,1,2,0_4,1,0,0": "OK",
    "1_0,1,2,0_4,1,0,1": "OK",
    "1_0,1,2,0_4,1,0,2": "OK",
    "1_0,1,2,0_4,1,0,3": "OK",
    "1_0,1,2,0_4,1,0,4": "OK",
    "1_0,1,2,0_4,1,0,5": "OK",
    "1_0,1,2,0_4,1,0,6": "OK",
    "1_0,1,2,0_4,1,0,7": "OK",
    "1_0,1,2,0_4,1,0,8": "OK",
    "1_0,1,2,0_4,1,0,9": "OK",
    "1_0,1,2,0_4,1,0,10": "OK",
    "1_0,1,2,0_4,1,0,11": "OK",
    "1_0,1,2,0_4,1,0,12": "OK",
    "1_0,1,2,0_4,1,0,13": "OK"
}

if __name__ == "__main__":
    run_single_user(LoginCommCareHQWithUniqueUsers, loglevel="DEBUG")
