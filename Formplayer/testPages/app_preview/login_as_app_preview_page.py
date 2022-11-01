import time

from selenium.webdriver.common.by import By

from common_utilities.selenium.base_page import BasePage
from Formplayer.userInputs.user_inputs import UserData
from selenium.webdriver.common.keys import Keys

""""Contains test page elements and functions related to the Homepage of Commcare"""


class LoginAsAppPreviewPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.application_menu_id = (By.LINK_TEXT, "Applications")
        self.select_test_application = (By.LINK_TEXT, UserData.basic_tests_app)
        self.view_app_preview = (By.XPATH, "//i[@class ='fa fa-chevron-left js-preview-action-show']")
        self.refresh_button = (By.XPATH,"//i[@class='fa fa-refresh']")
        self.iframe = (By.CLASS_NAME, "preview-phone-window")
        self.login_as_button = (By.XPATH, "//div[@aria-labelledby='single-app-login-as-heading']/descendant::h3[.='Login as']")
        self.app_icon_container =(By.XPATH,"//div[@class='container container-appicons']")
        self.title_bar = (By.XPATH, "//li[.='"+UserData.basic_tests_app+"']")
        self.searh_user_field = (By.XPATH, "//input[@class='js-user-query form-control']")
        self.search_worker = (By.XPATH, "//input[@placeholder='Filter workers']")
        self.username = UserData.app_preview_mobile_worker
        self.start_option = (By.XPATH, "//div[@class= 'js-start-app appicon appicon-start']")
        self.basic_tests_app = (By.ID,"//ol//li[contains(.,"+UserData.basic_tests_app+")]")
        self.login_as = (By.XPATH,"//h3[text()='Login as']")
        self.search_user_input_area = (By.XPATH, "//input[@placeholder='Filter workers']")
        self.username_in_list = (By.XPATH, "//h3[./b[text() ='"+self.username+"']]")
        self.search_users_button = (By.XPATH, "//*[@class='fa fa-search']")
        self.webapp_login_confirmation = (By.ID, 'js-confirmation-confirm')
        self.webapp_working_as = (By.XPATH, "//div[@class='restore-as-banner module-banner']/b")
        self.basic_tests_case = (By.XPATH,"//tr[@aria-label='"+UserData.basic_tests_case_list+"']")
        self.basic_tests_form = (By.XPATH, "//tr[@aria-label='"+UserData.basic_tests_form_name+"']")
        self.basic_tests_answer_input = (By.XPATH,  "//label[.//span[text()='Enter a Name']]//following-sibling::div//textarea")
        self.next_button = (By.XPATH,"//button[contains(@data-bind,'click: nextQuestion')]")
        self.submit = (By.XPATH, "//button[contains(@data-bind,'click: submitForm')]")
        self.submit_success = (By.XPATH, "//p[text()='Form successfully saved!']")
        self.full_menu = (By.LINK_TEXT, "Show Full Menu")


    def open_view_app_preview(self):
        if self.is_present(self.application_menu_id):
            self.wait_to_click(self.application_menu_id)
        else:
            self.wait_to_click(self.full_menu)
            self.wait_to_click(self.application_menu_id)
        self.wait_to_click(self.select_test_application)
        self.wait_to_click(self.view_app_preview)
        self.wait_to_click(self.refresh_button)


    def login_as_app_preview_presence(self):
        self.switch_to_frame(self.iframe)
        assert self.is_visible_and_displayed(self.title_bar,10), "This is not the Webaspps menu page."
        self.wait_to_click(self.login_as_button)

    def login_as_app_preview_content(self):
        self.wait_to_clear_and_send_keys(self.search_worker, self.username)
        self.js_click(self.search_users_button)
        time.sleep(2)
        self.js_click(self.username_in_list)
        time.sleep(2)
        self.js_click(self.webapp_login_confirmation)
        time.sleep(2)
        logged_in_username = self.get_text(self.webapp_working_as)
        assert logged_in_username == self.username, "Logged in"

    def login_as_app_preview_form_submssion(self):
        self.wait_to_click(self.start_option)
        self.wait_to_click(self.basic_tests_case)
        self.wait_to_click(self.basic_tests_form)
        self.wait_to_clear_and_send_keys(self.basic_tests_answer_input, "This is just a Test")
        self.wait_to_click(self.next_button)
        self.wait_to_click(self.submit)
        assert self.is_visible_and_displayed(self.submit_success)
        self.switch_to_default_content()