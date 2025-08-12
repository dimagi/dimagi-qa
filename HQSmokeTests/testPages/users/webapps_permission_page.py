from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from common_utilities.selenium.base_page import BasePage

""""Contains test page elements and functions related to the User's Webapps Permissions module"""


class WebAppPermissionPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.web_app_permissions_menu = (By.LINK_TEXT, "Web Apps Permissions")
        self.first_radio_button = (By.XPATH, "//input[@name='ko_unique_1']")
        self.second_radio_button = (By.XPATH, "//input[@name='ko_unique_2']")
        self.save_button = (By.XPATH, "//div[@class='btn btn-primary']")
        self.after_save = (By.XPATH, "//div[@class='btn btn-primary disabled']")
        self.error_403 = (By.XPATH, "//h1[text()='403 Forbidden']")

    def webapp_permission_option_toggle(self):
        try:
            self.click(self.web_app_permissions_menu)
        except NoSuchElementException:
            if self.is_displayed(self.error_403):
                self.driver.back()
        self.driver.implicitly_wait(2)
        if self.is_selected(self.first_radio_button):
            self.click(self.second_radio_button)
        else:
            self.click(self.first_radio_button)
        self.click(self.save_button)
        self.wait_for_element(self.after_save)
        print("Webapps permissions toggled")
