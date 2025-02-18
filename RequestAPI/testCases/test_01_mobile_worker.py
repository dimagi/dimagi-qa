import pytest
from RequestAPI.testMethods.mobile_worker_methods import MobileWorkerMethods
from RequestAPI.userInputs.user_inputs import UserData

""""Contains all test cases that aren't specifically related any menu modules"""

test_data = dict()
test_data["mobile_user_id"] = None

@pytest.mark.run(order=0)
def test_case_1_mobile_worker_creation(settings):
    uri = settings["url"] + UserData.domain + UserData.post_domain_url
    mw = MobileWorkerMethods(settings)
    mobile_user_id = mw.mobile_worker_creation(uri, "POST_mobile_worker_user.json", settings['login_user'],
                                               settings['login_pass'])
    test_data["mobile_user_id"] = mobile_user_id
    print(test_data["mobile_user_id"])
    return test_data["mobile_user_id"]


def test_case_2_mobile_worker_edit(settings):
    if test_data["mobile_user_id"] == None:
        pytest.skip("Mobile User ID is not created")
    uri = settings["url"] + UserData.domain + UserData.post_domain_url
    mw = MobileWorkerMethods(settings)
    print(test_data["mobile_user_id"])
    mw.mobile_worker_edit(uri, test_data["mobile_user_id"], "PUT_mobile_worker_user.json", settings['login_user'],
                          settings['login_pass'])


def test_case_3_mobile_worker_get(settings):
    if test_data["mobile_user_id"] == None:
        pytest.skip("Mobile User ID is not created")
    uri = settings["url"] + UserData.domain + UserData.post_domain_url
    print(test_data["mobile_user_id"])
    mw = MobileWorkerMethods(settings)
    mw.mobile_worker_get(uri, test_data["mobile_user_id"], settings['login_user'],
                         settings['login_pass'])


def test_case_4_mobile_worker_delete(settings):
    if test_data["mobile_user_id"] == None:
        pytest.skip("Mobile User ID is not created")
    uri = settings["url"] + UserData.domain + UserData.post_domain_url
    print(test_data["mobile_user_id"])
    mw = MobileWorkerMethods(settings)
    mw.mobile_worker_delete(uri, test_data["mobile_user_id"], settings['login_user'],
                            settings['login_pass'])
