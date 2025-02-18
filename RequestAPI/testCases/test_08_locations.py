from RequestAPI.testMethods.location_methods import LocationMethods
from RequestAPI.userInputs.user_inputs import UserData


def test_case_24_list_of_location(settings):
    uri = settings["url"] + UserData.domain + UserData.post_domain_url
    mw = LocationMethods(settings)
    mw.get_location_list(uri, settings['login_user'], settings['login_pass'])


def test_case_25_location_data(settings):
    uri = settings["url"] + UserData.domain + UserData.post_domain_url
    mw = LocationMethods(settings)
    mw.get_location_data(uri, settings['login_user'], settings['login_pass'])


def test_case_26_list_of_location_type(settings):
    uri = settings["url"] + UserData.domain + UserData.post_domain_url
    mw = LocationMethods(settings)
    mw.get_location_type_list(uri, settings['login_user'], settings['login_pass'])


def test_case_27_location_type_data(settings):
    uri = settings["url"] + UserData.domain + UserData.post_domain_url
    mw = LocationMethods(settings)
    mw.get_location_type_data(uri, settings['login_user'], settings['login_pass'])
