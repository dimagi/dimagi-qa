import logging

from common.web_apps import get_app_build_info
import formplayer
from locust import HttpUser
from locust.exception import StopUser
import pydantic


class UserDetails(pydantic.BaseModel):
    username: str
    password: str
    login_as: str | None = None

    # def __str__(self):
    #     if self.login_as:
    #         return f"{self.username} as {self.login_as}"
    #     return self.username


class AppDetails(pydantic.BaseModel):
    domain: str
    app_id: str
    build_id: str | None = None

    @property
    def id(self):
        return self.build_id or self.app_id


class HQUser:

    def __init__(self, client, user_details, app_details):
        self.client = client
        self.user_details = user_details
        self.app_details = app_details

    def login(self, domain, host):
        login_url = f"/a/{domain}/login/"
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
                "REFERER": f"{host}{login_url}",  # csrf requires this
            },
        )
        if not response.status_code == 200:
            raise StopUser(f"Login failed for user {self.user_details.username}: {response.status_code}")
        if 'Sign In' in response.text:
            raise StopUser(f"Login failed for user {self.user_details.username}: Sign In failed")
        logging.info("User logged in: " + self.user_details.username)

    def navigate_start(self, expected_title=None):
        validation = None
        if expected_title:
            validation = formplayer.ValidationCriteria(key_value_pairs={"title": expected_title})
        return self.post_formplayer(
            "navigate_menu_start",
            name="Home Screen",
            validation=validation
        )

    def navigate(self, name, data, expected_title=None):
        validation = None
        if expected_title:
            validation = formplayer.ValidationCriteria(key_value_pairs={"title": expected_title})
        return self.post_formplayer(
            "navigate_menu", data, name=name, validation=validation
        )

    def answer(self, name, data):
        return self.post_formplayer("answer", data, name=name)

    def submit_all(self, name, data, expected_response_message=None):
        validation = None
        if expected_response_message:
            validation = formplayer.ValidationCriteria(key_value_pairs={
                "submitResponseMessage": expected_response_message
            })
        return self.post_formplayer(
            "submit-all", data, name=name, validation=validation
        )

    def post_formplayer(self, command, extra_json=None, name=None, validation=None):
        logging.info("User: %s; Request: %s; Name: %s", self.user_details, command, name)
        try:
            return formplayer.post(
                command, self.client, self.app_details, self.user_details, extra_json, name, validation
            )
        except Exception as e:
            logging.error("user: %s; request: %s; exception: %s", self.user_details, command, str(e))

class BaseLoginCommCareUser(HttpUser):
    abstract=True

    def on_start(self, domain, host, user_details, app_id):
        self.user_detail = user_details.get()

        app_details = AppDetails(
            domain=domain,
            app_id=app_id
        )
        self.hq_user = HQUser(self.client, self.user_detail, app_details)
        self.hq_user.login(domain, host)
        self.hq_user.app_details.build_id = self._get_build_info(app_id, domain)

    def _get_build_info(self, app_id, domain):
        build_id = get_app_build_info(self.client, domain, app_id)
        if build_id:
            logging.info("Using app build: %s", build_id)
        else:
            logging.warning("No build found for app: %s", app_id)
        return build_id
