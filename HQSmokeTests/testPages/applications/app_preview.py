import random
import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from HQSmokeTests.userInputs.user_inputs import UserData
from common_utilities.selenium.base_page import BasePage

""""Contains test page elements and functions related to the app preview"""


class AppPreviewPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.sidebar_open_app_preview = (By.XPATH, "//div[@class='preview-toggler js-preview-toggle']")
        self.iframe_app_preview = (By.XPATH, "//iframe[@class='preview-phone-window']")
        self.app_preview_model = (By.XPATH, "//div[@class='preview-phone-container']")
        self.start = (By.ID, "single-app-start-heading")
        self.case_list = (By.XPATH, "//div[@class='module-menu-container']//h3[.='Case List']")
        self.followup_form = (By.XPATH, "//h3[text()='Followup Form']")
        self.first_case_on_case_list = (By.XPATH, "(//td[@class='module-case-list-column'])[1]")
        self.continue_button = (By.ID, "select-case")
        self.next_button = (By.XPATH, "(//button[@class='btn btn-formnav btn-formnav-next'])[1]")
        self.complete_button = (By.XPATH, "//button[@class='btn btn-success btn-formnav-submit']")
        self.submit = (By.XPATH, "(//button[@class='submit btn btn-primary'])[1]")
        self.submit_success = (By.XPATH, "//p[contains(text(),'successfully saved')]")
        self.search_users_button = (By.XPATH, "//*[@class='fa fa-search']")
        self.search_worker = (By.XPATH, "//input[@placeholder='Filter workers']")
        self.login_as_button = (
            By.XPATH, "//div[@aria-labelledby='single-app-login-as-heading']/descendant::h3[.='Log in as']")
        self.username_in_list = "//h3[./b[text() ='{}']]"
        self.webapp_login_confirmation = (By.ID, 'js-confirmation-confirm')
        self.webapp_working_as = (By.XPATH, "//div[@class='restore-as-banner module-banner']/b")
        self.case_list_menu = "//h3[contains(text(), '{}')]"
        self.start_option = (By.XPATH, "//div[@class= 'js-start-app appicon appicon-start']")
        self.location_field = (By.XPATH, "//input[@class='query form-control']")
        self.location_search = (By.XPATH, "//span/button[.='Search']")
        self.clear_map = (By.XPATH, "//button[.='Clear map']")
        self.longitude = (By.XPATH, "//td[@class='lon coordinate']")
        self.latitude = (By.XPATH, "//td[@class='lat coordinate']")
        self.next_question = (By.XPATH, "//button[contains(@data-bind,'nextQuestion')]")
        self.prev_question = (By.XPATH, "//button[contains(@data-bind,'prevQuestion')]")
        self.next_question_force = (By.XPATH, "//button[contains(@data-bind,'clickedNextOnRequired')]")
        self.complete_form = (By.XPATH, "//button[@data-bind='visible: atLastIndex(), click: submitForm']")
        self.success_message = (By.XPATH, "//p[contains(text(),'successfully saved')]")
        self.home_button = (By.XPATH, "//li[./i[@class='fa fa-home']]")
        self.sync_button = (By.XPATH, "//div[@class='js-sync-item appicon appicon-sync']")
        self.sync_message = (By.XPATH, "//p[contains(text(),'successfully synced')]")


    def check_access_to_app_preview(self):
        if not self.is_visible_and_displayed(self.app_preview_model):
            self.wait_to_click(self.sidebar_open_app_preview)
        self.is_visible_and_displayed(self.app_preview_model)
        self.driver.switch_to.frame(self.find_element(self.iframe_app_preview))
        self.wait_to_click(self.start)
        self.is_visible_and_displayed(self.case_list)

    def submit_form_on_app_preview(self):
        self.wait_to_click(self.case_list)
        self.wait_to_click(self.followup_form)
        self.wait_to_click(self.first_case_on_case_list)
        time.sleep(2)
        self.wait_to_click(self.continue_button)
        time.sleep(2)
        if self.is_displayed(self.next_button):
            self.wait_to_click(self.next_button)
            self.js_click(self.complete_button)
        self.is_visible_and_displayed(self.submit_success)
        self.driver.switch_to.default_content()

    def submit_form_with_loc(self):
        if not self.is_visible_and_displayed(self.app_preview_model):
            self.wait_to_click(self.sidebar_open_app_preview)
        self.is_visible_and_displayed(self.app_preview_model)
        self.driver.switch_to.frame(self.find_element(self.iframe_app_preview))
        self.login_as_app_preview()
        self.wait_to_click(self.start_option)
        time.sleep(2)
        self.wait_for_element((By.XPATH, self.case_list_menu.format(UserData.case_list_name)))
        self.wait_to_click((By.XPATH, self.case_list_menu.format(UserData.case_list_name)))
        time.sleep(2)
        self.wait_for_element((By.XPATH, self.case_list_menu.format("Reg Form")))
        self.wait_to_click((By.XPATH, self.case_list_menu.format("Reg Form")))
        self.wait_for_element(self.clear_map)
        self.wait_to_click(self.clear_map)
        time.sleep(1)
        loc = random.choice(UserData.location_list)
        print(loc)
        self.wait_to_click(self.location_field)
        self.send_keys(self.location_field, loc)
        self.wait_to_click(self.location_search)
        time.sleep(1)
        lat = self.get_text(self.latitude)
        lon = self.get_text(self.longitude)
        self.js_click(self.next_question)
        time.sleep(2)
        self.js_click(self.complete_form)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        print("Form submitted")
        time.sleep(2)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.wait_for_element(self.sync_button)
        self.js_click(self.sync_button)
        time.sleep(2)
        self.switch_to_default_content()
        print("Sleeping for sometime so the form data is updated")
        time.sleep(30)
        print("Latitude: ", lat, "Longitude: ", lon)
        return lat, lon

    def login_as_app_preview(self, username = UserData.app_login):
        self.wait_to_click(self.login_as_button)
        time.sleep(2)
        self.wait_for_element(self.search_worker)
        self.wait_to_clear_and_send_keys(self.search_worker, username)
        self.wait_for_element(self.search_users_button)
        self.js_click(self.search_users_button)
        time.sleep(2)
        self.wait_for_element((By.XPATH, self.username_in_list.format(username)))
        self.js_click((By.XPATH, self.username_in_list.format(username)))
        time.sleep(2)
        self.wait_for_element(self.webapp_login_confirmation)
        self.js_click(self.webapp_login_confirmation)
        time.sleep(2)
        logged_in_username = self.get_text(self.webapp_working_as)
        assert logged_in_username == username, "Logged in"

