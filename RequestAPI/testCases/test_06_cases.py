from RequestAPI.testMethods.cases_methods import CasesMethods
from RequestAPI.userInputs.user_inputs import UserData


def test_case_20_list_of_all_cases(settings):
    uri = settings["url"]+UserData.domain+UserData.post_domain_url
    mw = CasesMethods(settings)
    mw.get_all_cases_list(uri, settings['login_user'], settings['login_pass'])



def test_case_21_case_data_list(settings):
    uri = settings["url"]+UserData.domain+UserData.post_domain_url
    mw = CasesMethods(settings)
    mw.get_case_data(uri ,settings['login_user'], settings['login_pass'])
