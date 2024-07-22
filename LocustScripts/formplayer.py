from app_script.validations import DefaultValidation


def post(command, client, app_details, user_details, extra_json=None, name=None, validations=None):
    formplayer_host = "/formplayer"
    data = {
        "app_id": app_details.id,
        "domain": app_details.domain,
        "locale": "en",
        "restoreAs": user_details.login_as,
        "username": user_details.username,
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
    with client.post(f"{formplayer_host}/{command}/", json=data, name=name,
                     catch_response=True) as response:
        response_data = response.json()
        DefaultValidation().validate(response, response_data)

        if validations:
            for validation in validations:
                validation.validate(response, response_data)
        return response_data
