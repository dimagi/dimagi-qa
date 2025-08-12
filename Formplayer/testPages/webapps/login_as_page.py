import time

from selenium.webdriver.common.by import By

from Formplayer.testPages.webapps.webapps_basics import WebAppsBasics
from common_utilities.generate_random_string import fetch_random_string
from common_utilities.selenium.base_page import BasePage
from Formplayer.userInputs.user_inputs import UserData

""""Contains test page elements and functions related to the Homepage of Commcare"""

class LoginAsPage(BasePage):

    def __init__(self, driver, settings):
        super().__init__(driver)
        self.webapp = WebAppsBasics(self.driver)

        self.form_input = "web app test"+fetch_random_string()
        self.form_input_no_login = "web app test without login" + fetch_random_string()
        self.username_in_list = "//h3[./b[text() ='{}']]"

        self.dashboard_link = settings['url'] + "/dashboard/project/"
        self.submitted_by_on_behalf = (By.XPATH,
                                       "//div[@class='pull-right'][contains(.,'Submitted by Web User')]/a[.='" + UserData.web_user + "']//following-sibling::text()[contains(.,'on behalf of Mobile Worker')]//following-sibling::a[.='" + UserData.app_preview_mobile_worker + "']")
        self.submitted_by = (By.XPATH, "//div[@class='pull-right'][contains(.,'Submitted by ')]/a[.='" + UserData.web_user + "']")

        self.basic_tests_app = "//div[@aria-label='{}']/descendant::h3[text()='{}']"
        self.web_apps_menu = (By.ID, "CloudcareTab")
        self.show_full_menu = (By.ID, "commcare-menu-toggle")
        self.login_as = (By.XPATH,"//h3[text()='Log in as']")
        self.WEBAPPS_TITLE = "Web Apps - CommCare HQ"
        self.search_user_input_area = (By.XPATH, "//input[@placeholder='Filter workers']")
        self.username = UserData.app_preview_mobile_worker
        self.search_users_button = (By.XPATH, "//button[@type='submit'][./i[@class = 'fa fa-search']]")
        self.webapp_login_confirmation = (By.ID, 'js-confirmation-confirm')
        self.webapp_working_as = (By.XPATH, "//span[contains(.,'Working as')]//b")
        self.basic_tests_menu = (By.XPATH,"//h3[text()='Basic Form Tests']")
        self.basic_tests_form = (By.XPATH, "//h3[contains(text(), 'Basic Form')]")
        self.basic_tests_answer_input = (By.XPATH,  "//label[.//span[contains(text(), 'Enter a Name')]]//following-sibling::div//textarea")
        self.submit = (By.XPATH, "(//button[@class='submit btn btn-primary'])[1]")
        self.submit_success = (By.XPATH, "//p[contains(text(),'successfully saved')]")
        self.login_as_webuser= (By.XPATH, "//a[@class='js-clear-user']")

    def open_basic_tests_app(self, application=UserData.basic_tests_app["tests_app"]):
        print("Open App")
        self.wait_for_element((By.XPATH, self.basic_tests_app.format(application, application)), 120)
        self.wait_to_click((By.XPATH, self.basic_tests_app.format(application, application)))

    def open_webapps_menu(self):
        self.switch_to_default_content()
        self.driver.get(self.dashboard_link)
        print("Opening Web Apps Menu")
        self.wait_for_element(self.web_apps_menu, 120)
        self.wait_to_click(self.web_apps_menu)

    def login_as_presence(self):
        self.open_webapps_menu()
        assert self.WEBAPPS_TITLE in self.driver.title, "This is not the Webaspps menu page."
        self.wait_for_element(self.login_as, 200)
        self.scroll_to_element(self.login_as)
        self.wait_to_click(self.login_as)
        time.sleep(3)

    def login_as_content(self):
        self.wait_for_element(self.search_user_input_area, 120)
        self.wait_to_clear_and_send_keys(self.search_user_input_area, self.username)
        
        self.wait_to_click(self.search_users_button)
        
        self.wait_to_click((By.XPATH, self.username_in_list.format(self.username)))
        
        self.webapp.wait_to_click(self.webapp_login_confirmation)
        time.sleep(2)
        logged_in_username = self.get_text(self.webapp_working_as)
        print(logged_in_username)
        assert logged_in_username == self.username, "Logged in"

    def login_as_form_submssion(self, input_text):
        self.open_basic_tests_app()
        
        self.wait_to_click(self.basic_tests_menu)
        
        self.wait_to_click(self.basic_tests_form)
        
        self.wait_for_element(self.basic_tests_answer_input, 120)
        self.wait_to_clear_and_send_keys(self.basic_tests_answer_input, input_text)
        self.webapp.wait_to_click(self.submit)
        self.wait_for_element(self.submit_success)

    def submit_history_verification(self):
        web_app = WebAppsBasics(self.driver)
        web_app.open_submit_history_form_link(UserData.basic_tests)
        assert self.is_displayed(self.submitted_by), "Submission verification failed"

    def login_as_user(self, username):
        self.webapp.wait_to_click(self.login_as)
        time.sleep(3)
        self.wait_for_element(self.search_user_input_area, 120)
        
        self.send_keys(self.search_user_input_area, username)
        time.sleep(3)
        self.wait_to_click(self.search_users_button)
        
        self.wait_to_click((By.XPATH, self.username_in_list.format(username)))
        
        self.wait_to_click(self.webapp_login_confirmation)
        
        logged_in_username = self.get_text(self.webapp_working_as)
        assert logged_in_username == self.username, "Logged in"
