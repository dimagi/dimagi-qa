import time

from Formplayer.testPages.webapps.webapps_basics import WebAppsBasics

from common_utilities.selenium.base_page import BasePage


from selenium.webdriver.common.by import By

""""Contains test page elements and functions related to the WebApps Access/Basics of Commcare"""

class ProjectSettingsPage(BasePage):

    def __init__(self, driver, settings):
        super().__init__(driver)
        self.webapp = WebAppsBasics(self.driver)

        self.manage_settings = (By.XPATH, "//a[@aria-label='Manage Settings']")
        self.project_settings_link = (By.XPATH, "//a[@data-label='Update Project Settings']")
        self.privacy_security = (By.XPATH, "//a[contains(.,'Privacy and Security')]")
        self.inactivity_timeout = (By.XPATH, "//input[@id='id_secure_sessions_timeout']")
        self.update_button = (By.XPATH, "//button[@type='submit'][contains(.,'Update')]")
        self.success_message = (By.XPATH, "//div[contains(@class,'alert')][contains(.,'have been saved')]")
        self.shortened_inactivity = (By.XPATH, "//input[@id='id_secure_sessions']")
        self.dashboard_link = settings['url'] + "/dashboard/project/"

    def set_inactivity_timeout(self):
        self.webapp.wait_to_click(self.manage_settings)
        self.webapp.wait_to_click(self.project_settings_link)
        self.webapp.wait_to_click(self.privacy_security)
        self.wait_for_element(self.inactivity_timeout)
        self.webapp.wait_to_click(self.shortened_inactivity)
        time.sleep(2)
        assert self.is_selected(self.shortened_inactivity)
        self.send_keys(self.inactivity_timeout, "5")
        self.scroll_to_element(self.update_button)
        self.webapp.wait_to_click(self.update_button)
        time.sleep(3)
        self.wait_for_element(self.success_message)

    def clear_inactivity_timeout(self):
        self.webapp.wait_to_click(self.manage_settings)
        self.webapp.wait_to_click(self.project_settings_link)
        self.webapp.wait_to_click(self.privacy_security)
        self.wait_for_element(self.inactivity_timeout)
        if self.is_selected(self.shortened_inactivity):
            self.webapp.wait_to_click(self.shortened_inactivity)
            time.sleep(2)
            assert not self.is_selected(self.shortened_inactivity)
            time.sleep(2)
            self.clear(self.inactivity_timeout)
            self.scroll_to_element(self.update_button)
            self.webapp.wait_to_click(self.update_button)
            time.sleep(3)
            self.wait_for_element(self.success_message)
        else:
            print("Inactivity timeout is already disabled")

    def get_new_tab(self):
        self.open_new_tab()
        self.switch_to_next_tab()
        self.driver.get(self.dashboard_link)
        self.wait_for_element(self.manage_settings)
