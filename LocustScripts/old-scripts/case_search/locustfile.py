
import logging

from locust import HttpUser, constant, events, task
from locust.exception import InterruptTaskSet, StopUser

from case_search.loader import load_query_data
from user.models import UserDetails
from common.args import file_path
from common.utils import RandomItems, load_json_data


@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--domain", help="CommCare domain", required=True, env_var="COMMCARE_DOMAIN")
    parser.add_argument("--app-id", help="CommCare app id", required=True, env_var="COMMCARE_APP_ID")
    parser.add_argument("--queries", help="Path to queries YAML file", required=True)
    parser.add_argument("--user-details", help="Path to user details file", required=True)


QUERY_DATA = []
USERS = RandomItems()


def get_random_query():
    return QUERY_DATA[-1].get_random_query()


@events.init.add_listener
def _(environment, **kw):
    try:
        queries = file_path(environment.parsed_options.queries)
        QUERY_DATA.append(load_query_data(queries))
        logging.info("Loaded %s queries and %s value sets", len(QUERY_DATA[0].queries), len(QUERY_DATA[0].value_sets))
    except Exception as e:
        logging.error("Error loading queries: %s", e)
        raise InterruptTaskSet from e

    try:
        user_path = file_path(environment.parsed_options.user_details)
        user_data = load_json_data(user_path)["user"]
        USERS.set([UserDetails(**user) for user in user_data])
        logging.info("Loaded %s users", len(USERS.items))
    except Exception as e:
        logging.error("Error loading users: %s", e)
        raise InterruptTaskSet from e


class CaseSearchUser(HttpUser):
    wait_time = constant(1)

    def on_start(self):
        self.user_details = USERS.get()
        self.login()

    def login(self):
        login_url = f"/a/{self.environment.parsed_options.domain}/login/"
        self.client.get(login_url)  # get CSRF token
        response = self.client.post(
            login_url,
            {
                "auth-username": self.user_details.username,
                "auth-password": self.user_details.password,
                "cloud_care_login_view-current_step": ['auth'],  # fake out two_factor ManagementForm
            },
            headers={
                "X-CSRFToken": self.client.cookies.get('csrftoken'),
                "REFERER": f"{self.environment.parsed_options.host}{login_url}",  # csrf requires this
            },
        )
        if not response.status_code == 200:
            raise StopUser(f"Login failed for user {self.user_details.username}: {response.status_code}")
        if 'Sign In' in response.text:
            raise StopUser(f"Login failed for user {self.user_details.username}: Sign In failed")

    @task
    def search_case(self):
        url = f"/a/{self.environment.parsed_options.domain}/phone/search/{self.environment.parsed_options.app_id}/"
        name, query = get_random_query()
        with self.client.post(
            url,
            data=query,
            name=f"Search cases: {name}",
            catch_response=True,
        ) as resp:
            if resp.status_code == 400:
                logging.error("Bad request for query '%s': %s", name, resp.text)
