import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(isatty=True, logger=logger, level='DEBUG')

def post(command, client, app_details, user_details, extra_json=None, name=None, validation=None):
    formplayer_host = "/formplayer"
    data = {
        "app_id": app_details.id,
        "domain": app_details.domain,
        "locale": "en",
        "username": user_details.username,
        "windowWidth": 1280
        }
    if extra_json:
        data.update(extra_json)
    name = name or command

    if 'XSRF-TOKEN' not in client.cookies:
        response = client.get(f"{formplayer_host}/serverup")
        response.raise_for_status()

    xsrf_token = client.cookies['XSRF-TOKEN']
    headers = {'X-XSRF-TOKEN': xsrf_token}
    client.headers.update(headers)
    with client.post(f"{formplayer_host}/{command}", json=data, name=name,
                     catch_response=True
                     ) as response:
        # logger.info("json submitted: "+ str(data))
        # logger.info("response"+str(response.json()))
        if command == 'submit-all':
            logger.info(f"{formplayer_host}/{command}/")
            # logger.info("json submitted: "+ str(data))
            # logger.info("response"+str(response.json()))
        if command == 'get_endpoint':
            logger.info(f"response status: {str(response.status_code)}")
        if validation:
            validate_response(response, validation)
        return response.json()

# def get_session_data(client, session_id):
#     url = f"/formplayer/answer"
#     try:
#         response = client.get(url, name="Get Session Data")
#         response.raise_for_status()
#         return response.json()
#     except Exception as e:
#         logger.error(f"Error fetching session data for session_id {session_id}: {e}")
#         return {}


@dataclass
class ValidationCriteria:
    key_value_pairs:  Optional[Union[Dict[str, Optional[str]], List[Dict[str, Optional[str]]]]] = field(default_factory=dict)
    length_check: Optional[Dict[str, int]] = field(default_factory=dict)


def validate_response(response, validation: ValidationCriteria):
    data = response.json()
    for checkKey, checkValue in validation.key_value_pairs.items():
        if "commands" in checkKey:
            if isinstance(checkValue, dict):
                data_command = data["commands"]
                for dicts in data_command:
                    all(item in checkValue for item in dicts)
            else:
                msg = "ERROR::- mismatch in values" + checkValue + " and " + data["commands"]
                response.failure(msg)
                raise FormplayerResponseError("ERROR::- mismatch in values" + checkValue + " and " + data["commands"])
        else:
            checkLen = validation.length_check.get(checkKey, None)
            if "notification" in data and data["notification"]:
                if data["notification"]["type"] == "error":
                    msg = "ERROR::-" + data["notification"]["message"]
                    response.failure(msg)
                    raise FormplayerResponseError("ERROR::-" + data["notification"]["message"])
            if "exception" in data:
                msg = "ERROR::exception error--" + data['exception']
                response.failure(msg)
                raise FormplayerResponseError(msg)
            elif checkKey and checkKey not in data:
                msg = "error::" + checkKey + " not in data"
                response.failure(msg)
                raise FormplayerResponseError(msg)
            elif checkKey and checkLen:
                if len(data[checkKey]) != checkLen:
                    msg = "ERROR::len(data['" + checkKey + "']) != " + checkLen
                    response.failure(msg)
                    raise FormplayerResponseError(msg)
            elif checkKey and checkValue:
                if checkValue not in data[checkKey]:
                    msg = "ERROR::data['" + checkKey + "'], " + data[checkKey] + " does not have " + checkValue
                    response.failure(msg)
                    raise FormplayerResponseError(msg)


class FormplayerResponseError(Exception):
    pass
