import logging
from locust.exception import StopUser
from app_script.actions import Action
from user.models import BaseLoginCommCareUser

logger = logging.getLogger("runner")


class AppScriptRunner:
    def __init__(self, name, user: BaseLoginCommCareUser, script: list[Action]):
        self.name = name
        self.user = user
        self.script = script
        self.client_session = {}
        self.formplayer_session = {}

    def run(self):
        with self.user.events.request.measure("APP-SCRIPT", self.name):
            try:
                for step in self.script:
                    logger.info("Executing: %s for %s", step.name, self.user.hq_user)
                    self.client_session = step.get_data(self.client_session, self.formplayer_session)
                    logger.debug("Request data:\n\t%s", self.client_session)
                    self.formplayer_session = step.invoke(self.user, self.client_session, self.formplayer_session)
                    # logger.debug("Step response: %s", step_response)

                    self.persist_session_keys(["queryKey", "query_data", "session_id"])

                    if step.timing:
                        self.user._taskset_instance._sleep(step.timing)
            except StopUser as e:
                logger.error(e)
                raise e

    def persist_session_keys(self, fields):
        """Some fields aren't returned by Formplayer, so we need to maintain their value across requests"""
        for field in fields:
            if self.client_session.get(field) and not self.formplayer_session.get(field):
                self.formplayer_session[field] = self.client_session[field]
