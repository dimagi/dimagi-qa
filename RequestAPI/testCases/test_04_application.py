import pytest

from RequestAPI.testMethods.application_methods import ApplicationMethods
from RequestAPI.testMethods.mobile_worker_methods import MobileWorkerMethods
from RequestAPI.userInputs.user_inputs import UserData

test_data = dict()
test_data["app_id"] = None

@pytest.mark.run(order=0)
def test_case_14_list_of_application(settings):
    uri = settings["url"] + UserData.domain + UserData.post_domain_url
    mw = ApplicationMethods(settings)
    test_data["app_id"] = mw.get_application_list(uri, settings['login_user'], settings['login_pass'])
    print(test_data["app_id"])
    return test_data["app_id"]


def test_case_15_application_structure(settings):
    if test_data["app_id"] == None:
        pytest.skip("Application ID is not created")
    uri = settings["url"] + UserData.domain + UserData.post_domain_url
    mw = ApplicationMethods(settings)
    mw.get_application_structure(uri, test_data["app_id"], settings['login_user'], settings['login_pass'])


@pytest.mark.xfail
def test_case_16_sms_mobile_worker_registration_api(settings):
    uri = settings["url"] + UserData.domain + UserData.post_domain_url
    mw = MobileWorkerMethods(settings)
    mw.sms_mobile_worker_registration_api(uri, test_data["app_id"], "POST_sms_mobile_worker.json",
                                          settings['login_user'], settings['login_pass'])


@pytest.mark.xfail
def test_case_17_send_cc_install_info_over_sms(settings):
    uri = settings["url"] + UserData.domain + UserData.post_domain_url
    mw = MobileWorkerMethods(settings)
    mw.sms_cc_install_over_sms(uri, test_data["app_id"], "POST_sms_mobile_worker.json",
                               settings['login_user'], settings['login_pass'])
