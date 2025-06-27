import logging
import os

import coloredlogs
from common.web_apps import get_app_build_info
import formplayer
from flask import json
from locust import HttpUser
from locust.exception import StopUser
import pydantic

logger = logging.getLogger(__name__)
coloredlogs.install(isatty=True, logger=logger, level='DEBUG')

class UserDetails(pydantic.BaseModel):
    username: str
    password: str
    login_as: str | None = None
    index: int | None = None

    # def __str__(self):
    #     if self.login_as:
    #         return f"{self.username} as {self.login_as}"
    #     return self.username

class UserDetailsManager:
    def __init__(self, json_file_path):
        self.items = []
        self.users_by_hour = {}
        self._load_users(json_file_path)

    def _load_users(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        if "users_by_hour" in data:
            self.users_by_hour = data["users_by_hour"]
        elif "user" in data:
            self.items = [UserDetails(**user) for user in data["user"]]
        else:
            raise ValueError("Invalid user JSON format")

    def get_users_by_hour(self, hour):
        users = self.users_by_hour.get(hour, [])
        return [UserDetails(**user) for user in users]

    def get(self):
        if self.items:
            return self.items.pop()
        raise IndexError("No users left to get")

    def set(self, users):
        self.items = users



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
        if os.environ.get("CI") == "true":
            password = os.environ.get("DIMAGIQA_LOCUST_PASSWORD")
        else:
            password = self.user_details.password
        response = self.client.post(
            login_url,
            {
                "auth-username": self.user_details.username,
                "auth-password": password,
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
        logger.info("User logged in: " + self.user_details.username)

    def navigate_start(self, expected_title=None):
        validation = None
        if expected_title:
            validation = formplayer.ValidationCriteria(key_value_pairs={"title": expected_title})
        return self.post_formplayer(
            "navigate_menu_start",
            name="Home Screen",
            validation=validation
            )

    def navigate(self, name, data, expected_title=None, commands_list=None):
        validation = None
        if expected_title:
            validation = formplayer.ValidationCriteria(key_value_pairs={"title": expected_title})
        if commands_list:
            for command in commands_list:
                validation = formplayer.ValidationCriteria(key_value_pairs={"commands": command})
        return self.post_formplayer(
            "navigate_menu", data, name=name, validation=validation
            )

    def answer(self, name, data):
        return self.post_formplayer("answer", data, name=name)

    def submit_all(self, name, data, expected_response_message=None, status=None):
        validation = None
        if expected_response_message:
            validation = formplayer.ValidationCriteria(key_value_pairs={
                "submitResponseMessage": expected_response_message
                }
                )
        elif status:
            validation = formplayer.ValidationCriteria(key_value_pairs={
                "status": status
                }
                )
        return self.post_formplayer(
            "submit-all", data, name=name, validation=validation
            )

    def post_formplayer(self, command, extra_json=None, name=None, validation=None):
        logger.info("User: %s; Request: %s; Name: %s", self.user_details.username, command, name)
        try:
            return formplayer.post(
                command, self.client, self.app_details, self.user_details, extra_json, name, validation
                )
        except Exception as e:
            logger.error(f"user: {self.user_details.username}; request: {command}; name:{name}; exception: {str(e)}")


class BaseLoginCommCareUser(HttpUser):
    abstract = True

    def on_start(self, domain, host, user_details, build_id, app_id):
        # self.user_detail = user_details.get()
        logger.info(f"User_details: {self.user_detail}")

        app_details = AppDetails(
            domain=domain,
            app_id=app_id,
            build_id=build_id
            )
        self.hq_user = HQUser(self.client, self.user_detail, app_details)
        self.hq_user.login(domain, host)
        self.hq_user.app_details.build_id, self.hq_user.app_details.app_id = self._get_build_info(build_id, app_id, domain)

    def _get_build_info(self, build_id, app_id, domain):
        build_id = get_app_build_info(self.client, domain, build_id)
        app_id = get_app_build_info(self.client, domain, app_id)
        if build_id:
            logger.info("Using app build: %s", build_id)
        else:
            logger.warning("No build found for app: %s and build: %s", app_id, build_id)
        return build_id, app_id