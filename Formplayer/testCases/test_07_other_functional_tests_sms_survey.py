
from Formplayer.testPages.messaging.messaging_page import MessagingPage
from Formplayer.testPages.mobile_user.mobile_user_page import MobileUserPage
from Formplayer.userInputs.user_inputs import UserData

test_data = dict()

def test_case_32_mobile_worker_setup(driver, settings):
    mw = MobileUserPage(driver, settings)
    mw.open_users_menu()
    response = mw.add_mobile_number_mobile_user(UserData.app_preview_mobile_worker)
    print(response)

def test_case_33_keywords_setup(driver, settings):
    keyword = MessagingPage(driver, settings)
    keyword.open_keywords_link()
    keyword.add_keywords(UserData.keyword_list)