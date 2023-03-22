import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

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
