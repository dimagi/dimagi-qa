import time

from selenium.webdriver.common.by import By

from common_utilities.generate_random_string import fetch_random_string
from common_utilities.selenium.base_page import BasePage
from Formplayer.userInputs.user_inputs import UserData
from selenium.webdriver.common.keys import Keys
from Formplayer.testPages.webapps.webapps_basics import WebAppsBasics

""""Contains test page elements and functions related to the Homepage of Commcare"""


class LoginAsAppPreviewPage(BasePage):

    def __init__(self, driver, settings):
        super().__init__(driver)

        self.dashboard_link = settings['url'] + "/dashboard/project/"
        self.form_input_no_login = "app preview test without login" + fetch_random_string()
        self.form_input_login = "app preview test" + fetch_random_string()
        self.submitted_by_on_behalf = (By.XPATH, "//div[@class='pull-right'][contains(.,'Submitted by Web User')]/a[.='" + UserData.web_user + "']//following-sibling::text()[contains(.,'on behalf of Mobile Worker')]//following-sibling::a[.='" + UserData.app_preview_mobile_worker + "']")
        self.submitted_by = (
        By.XPATH, "//div[@class='pull-right'][contains(.,'Submitted by Web User')]/a[.='" + UserData.web_user + "']")
        self.application_menu_id = (By.LINK_TEXT, "Applications")
        self.select_test_application = "//a[contains(.,'{}')]"
        self.view_app_preview = (By.XPATH, "//i[@class ='fa fa-chevron-left js-preview-action-show']")
        self.view_app_preview_show = (By.XPATH, "//i[@class ='fa fa-chevron-left js-preview-action-show hide']")
        self.refresh_button = (By.XPATH, "//i[@class='fa fa-refresh']")
        self.iframe = (By.CLASS_NAME, "preview-phone-window")
        self.login_as_button = (
        By.XPATH, "//div[@aria-labelledby='single-app-login-as-heading']/descendant::h3[.='Login as']")
        self.app_icon_container = (By.XPATH, "//div[@class='container container-appicons']")
        self.title_bar = (By.XPATH, "//li[.='" + UserData.basic_tests['tests_app'] + "']")
        self.searh_user_field = (By.XPATH, "//input[@class='js-user-query form-control']")
        self.search_worker = (By.XPATH, "//input[@placeholder='Filter workers']")
        self.username = UserData.app_preview_mobile_worker
        self.start_option = (By.XPATH, "//div[@class= 'js-start-app appicon appicon-start']")
        self.basic_tests_app = (By.ID, "//ol//li[contains(.," + UserData.basic_tests["tests_app"] + ")]")
        self.login_as = (By.XPATH, "//h3[text()='Login as']")
        self.clear_user = (By.XPATH, "//a[@class='js-clear-user']")
        self.search_user_input_area = (By.XPATH, "//input[@placeholder='Filter workers']")
        self.username_in_list =  "//h3[./b[text() ='{}']]"
        self.search_users_button = (By.XPATH, "//*[@class='fa fa-search']")
        self.webapp_login_confirmation = (By.ID, 'js-confirmation-confirm')
        self.webapp_working_as = (By.XPATH, "//div[@class='restore-as-banner module-banner']/b")
        self.basic_tests_case = (By.XPATH, "//tr[@aria-label='" + UserData.basic_tests["case_list"] + "']")
        self.basic_tests_form = (By.XPATH, "//tr[@aria-label='" + UserData.basic_tests["form_name"] + "']")
        self.basic_tests_answer_input = (
        By.XPATH, "//label[.//span[text()='Enter a Name']]//following-sibling::div//textarea")
        self.next_button = (By.XPATH, "//button[contains(@data-bind,'click: nextQuestion')]")
        self.submit = (By.XPATH, "//button[contains(@data-bind,'click: submitForm')]")
        self.submit_success = (By.XPATH, "//p[contains(text(),'successfully saved')]")
        self.full_menu = (By.LINK_TEXT, "Show Full Menu")

    def open_view_app_preview(self, test_app=UserData.basic_tests['tests_app']):
        self.switch_to_default_content()
        self.driver.get(self.dashboard_link)
        self.wait_for_element(self.application_menu_id)
        if self.is_present(self.application_menu_id):
            self.wait_to_click(self.application_menu_id)
        else:
            self.wait_to_click(self.full_menu)
            self.wait_to_click(self.application_menu_id)
        self.wait_to_click((By.XPATH, self.select_test_application.format(test_app)))
        if not self.is_present(self.view_app_preview_show):
            self.wait_to_click(self.view_app_preview)
        else:
            print("App preview is already open")
        self.wait_to_click(self.refresh_button)
        time.sleep(3)

    def login_as_app_preview_presence(self):
        self.switch_to_frame(self.iframe)
        time.sleep(2)
        assert self.is_visible_and_displayed(self.title_bar), "This is not the Webaspps menu page."
        self.wait_to_click(self.login_as_button)


    def login_as_app_preview_content(self):
        self.wait_to_clear_and_send_keys(self.search_worker, self.username)
        self.js_click(self.search_users_button)
        time.sleep(2)
        self.js_click((By.XPATH, self.username_in_list.format(self.username)))
        time.sleep(2)
        self.js_click(self.webapp_login_confirmation)
        time.sleep(2)
        logged_in_username = self.get_text(self.webapp_working_as)
        assert logged_in_username == self.username, "Logged in"
        self.switch_to_default_content()

    def login_as_app_preview_form_submission(self, text):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.wait_to_click(self.basic_tests_case)
        self.wait_to_click(self.basic_tests_form)
        self.wait_to_clear_and_send_keys(self.basic_tests_answer_input, text+Keys.TAB)
        self.js_click(self.next_button)
        time.sleep(2)
        self.js_click(self.submit)
        time.sleep(2)
        assert self.is_visible_and_displayed(self.submit_success)
        self.switch_to_default_content()


    def submit_history_verification(self, type, username):
        web_app = WebAppsBasics(self.driver)
        web_app.open_submit_history_form_link(UserData.basic_tests, username)
        if type == "no login":
            assert self.is_displayed(self.submitted_by), "Submission verification failed"
        elif type == "login":
            assert self.is_displayed(self.submitted_by_on_behalf), "Submission verification failed"

    def login_as_user(self, username):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.login_as_button)
        self.wait_to_clear_and_send_keys(self.search_worker, username)
        self.js_click(self.search_users_button)
        time.sleep(2)
        self.js_click((By.XPATH, self.username_in_list.format(self.username)))
        time.sleep(2)
        self.js_click(self.webapp_login_confirmation)
        time.sleep(2)
        logged_in_username = self.get_text(self.webapp_working_as)
        assert logged_in_username == self.username, "Logged in"
        self.switch_to_default_content()