import time

from selenium.webdriver.common.by import By

from Formplayer.testPages.base.base_page import BasePage
from Formplayer.userInputs.user_inputs import UserData

""""Contains test page elements and functions related to the Homepage of Commcare"""


class LoginAsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.basic_tests_app = (By.ID,"//ol//li[contains(.,"+UserData.basic_tests_app+")]")
        self.web_apps_menu = (By.ID, "CloudcareTab")
        self.show_full_menu = (By.ID, "commcare-menu-toggle")
        self.login_as = (By.XPATH,"//h3[text()='Login as']")
        self.WEBAPPS_TITLE = "Web Apps - CommCare HQ"
        self.search_user_input_area = (By.XPATH, "//input[@placeholder='Filter workers']")
        self.username = "webapps_user"
        self.username_in_list = (By.XPATH, "//b[text() ='"+self.username+"']")
        self.search_users_button = (By.XPATH, "//*[@class='fa fa-search']")
        self.webapp_login_confirmation = (By.ID, 'js-confirmation-confirm')
        self.webapp_working_as = (By.XPATH, "//div[@class='restore-as-banner module-banner']/b")
        self.basic_tests_menu = (By.XPATH,"(//div[@aria-label='Basic Tests']/div)[1]")
        self.basic_tests_form = (By.XPATH, "//tr[contains(@aria-label,'Basic Form')]")
        self.basic_tests_answer_input = (By.XPATH,  "//*[text()='Enter']/following::div[1]/div[@class='widget']/descendant::input")
        self.submit = (By.XPATH, "(//button[@class='submit btn btn-primary'])[1]")
        self.submit_success = (By.XPATH, "//p[text()='Form successfully saved!']")
        self.login_as_webuser= (By.XPATH, "//a[@class='js-clear-user']")

    def open_basic_tests_app(self):
        self.wait_to_click(self.basic_tests_app)

    def login_as_presence(self):
        self.wait_to_click(self.web_apps_menu)
        assert self.WEBAPPS_TITLE in self.driver.title, "This is not the Webaspps menu page."
        self.js_click(self.login_as)

    def login_as_content(self):
        self.send_keys(self.search_user_input_area, self.username)
        self.js_click(self.search_users_button)
        time.sleep(2)
        self.js_click(self.username_in_list)
        time.sleep(2)
        self.js_click(self.webapp_login_confirmation)
        logged_in_username = self.get_text(self.webapp_working_as)
        assert logged_in_username == self.username, "Logged in"

    def login_as_form_submssion(self):
        self.wait_to_click(self.basic_tests_menu)
        self.wait_to_click(self.basic_tests_form)
        self.wait_to_clear_and_send_keys("test", self.basic_tests_answer_input)
        self.wait_to_click(self.submit)
        assert self.is_visible_and_displayed(self.submit_success)




