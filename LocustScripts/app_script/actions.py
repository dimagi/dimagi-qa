import dataclasses
import logging

from locust.exception import StopUser

from app_script.timing import TimingCategory
from app_script.utils import merge_dicts
from app_script.validations import ResponseValidator


logger = logging.getLogger(__file__)


@dataclasses.dataclass
class Action:
    name: str
    timing: TimingCategory = None
    validations: list[ResponseValidator] = dataclasses.field(default_factory=list)

    def invoke(self, user, data, formplayer_session):
        return formplayer_session

    def get_data(self, client_session, formplayer_session):
        return client_session

    def log_response(self, response):
        if response.get("commands"):
            logger.debug("Command response: %s", [c['displayText'] for c in response["commands"]])

    def get_request_name(self):
        return self.name


@dataclasses.dataclass
class NavigateStart(Action):

    def invoke(self, user, data, formplayer_session):
        response = user.hq_user.navigate_start(self.get_request_name(), self.validations)
        self.log_response(response)
        return response

    def get_data(self, client_session, formplayer_session):
        return {}


@dataclasses.dataclass
class Navigate(Action):
    selections: list = dataclasses.field(default_factory=list)
    replace: bool = False

    def invoke(self, user, data, formplayer_session):
        response = user.hq_user.navigate(self.get_request_name(), data, self.validations)
        self.log_response(response)
        return response

    def get_data(self, client_session, formplayer_session):
        if self.replace:
            selections = self.selections
        else:
            selections = client_session.get("selections", []) + self.selections
        return {**client_session, "selections": selections}


@dataclasses.dataclass
class Search(Navigate):
    query_key: str = None
    input_data: dict = dataclasses.field(default_factory=dict)
    execute: bool = False
    """Set to True to simulate the user pressing the 'search' button. False for automatic requests."""
    force_manual_search = True
    """This is True for validation and for 'sidebar search'. """

    def get_data(self, client_session, formplayer_session):
        data = super().get_data(client_session, formplayer_session)
        query_key = get_query_key(formplayer_session, self.query_key)
        data = {**data, **{
            "query_data": {
                query_key: {
                    "inputs": self.input_data,
                    "execute": self.execute,
                    "force_manual_search": self.force_manual_search
                }
            }
        }}
        return merge_dicts(client_session, data)

    def log_response(self, response):
        if self.execute:
            logging.debug("Search response: %s", [e["id"] for e in response.get("entities", [])])

    def get_request_name(self):
        if self.execute:
            return self.name
        return "Update search facet"


@dataclasses.dataclass
class ResetSearchInput(Navigate):
    query_key: str = ""
    input_keys: list[str] = dataclasses.field(default_factory=list)

    def get_data(self, client_session, formplayer_session):
        query_key = get_query_key(formplayer_session, self.query_key)
        query_data = client_session.get("query_data", {}).get(query_key, {})
        query_data["execute"] = False
        inputs = query_data.get("inputs", {})
        for key in self.input_keys:
            inputs.pop(key, None)
        return client_session

    def get_request_name(self):
        return "Update search facet"


@dataclasses.dataclass
class SelectEntity(Navigate):
    entity_index: int = 0

    def get_data(self, client_session, formplayer_session):
        data = super().get_data(client_session, formplayer_session)
        entities = formplayer_session.get("entities", [])
        try:
            entity_id = entities[self.entity_index]["id"]
        except IndexError:
            raise StopUser(f"Unable to select entity at {self.entity_index} from entities: {entities}")
        data["selections"].append(entity_id)
        return data


@dataclasses.dataclass
class SubmitForm(Action):
    answers: dict = dataclasses.field(default_factory=dict)
    
    def get_data(self, client_session, formplayer_session):
        session_id = formplayer_session.get("session_id")
        if not session_id:
            raise StopUser(f"Unable to submit form: No session ID: {formplayer_session}")
        return {
            "answers": self.answers,
            "prevalidated": True,
            "debuggerEnabled": True,
            "session_id": session_id,
        }

    def invoke(self, user, data, formplayer_session):
        return user.hq_user.submit_all(self.get_request_name(), data, validations=self.validations)


@dataclasses.dataclass
class UserWait(Action):
    pass


@dataclasses.dataclass
class ResetSession(Action):
    def get_data(self, client_session, formplayer_session):
        return {}


def get_query_key(formplayer_session, query_key=None):
    if not query_key:
        query_key = formplayer_session.get("queryKey")
    if not query_key:
        raise StopUser("No Query Key for search inputs")
    return query_key
