import time

from selenium.webdriver.common.by import By

from Formplayer.testPages.webapps.webapps_basics import WebAppsBasics
from Formplayer.userInputs.user_inputs import UserData
from common_utilities.selenium.base_page import BasePage


class MobileUserPage(BasePage):
    def __init__(self, driver, settings):
        super().__init__(driver)
        self.webapp = WebAppsBasics(self.driver)
        self.dashboard_link = settings['url'] + "/dashboard/project/"
        self.users_menu_id = (By.ID, "ProjectUsersTab")
        self.view_all = (By.LINK_TEXT, "View All")
        self.show_full_menu = (By.ID, "commcare-menu-toggle")
        self.mobile_workers_links = (By.LINK_TEXT, "Mobile Workers")

        self.DASHBOARD_TITLE = "CommCare HQ"
        self.USERS_TITLE = "Mobile Workers : Users :: - CommCare HQ"

        self.search_mw = (By.XPATH, "//div[@class='ko-search-box']//input[@type='text']")
        self.search_button_mw = (
            By.XPATH, "//div[@class='ko-search-box']//button[@data-bind='click: clickAction, visible: !immediate']")
        self.searched_user = "//a//strong[.='{}']"
        self.phone_verify_button = (By.XPATH, "//button[contains(@class, 'verify-button')]")
        self.phone_number_delete = (By.XPATH, "//a[contains(@href, 'delete_phonenumber')]")
        self.confirm_delete_pn = (By.XPATH, "//a[.='Cancel']//following-sibling::button/i[@class='fa fa-remove']")
        self.phone_number_input = (By.XPATH, "//input[@name='phone_number']")
        self.add_number_button = (By.XPATH, "//button[.='Add Number']")
        self.number_added_success = (By.XPATH, "//div[contains(@class,'alert-success')][contains(.,'Phone number added.')]")
        self.already_in_use = (By.XPATH, "//span[.='ALREADY IN USE']")

    def open_users_menu(self):
        if self.is_present(self.show_full_menu):
            self.wait_to_click(self.show_full_menu)
        self.driver.get(self.dashboard_link)
        self.wait_for_element(self.users_menu_id)
        self.click(self.users_menu_id)
        self.wait_to_click(self.mobile_workers_links)
        assert self.USERS_TITLE in self.driver.title, "This is not the Users menu page."

    def add_mobile_number_mobile_user(self, username):
        self.wait_to_clear_and_send_keys(self.search_mw, username)#UserData.app_preview_mobile_worker)
        
        self.webapp.wait_to_click(self.search_button_mw)
        self.wait_for_element((By.XPATH, self.searched_user.format(username)))
        self.webapp.wait_to_click((By.XPATH, self.searched_user.format(username)))
        time.sleep(2)
        self.scroll_to_bottom()
        if self.is_present(self.phone_verify_button):
            self.webapp.wait_to_click(self.phone_number_delete)
            self.webapp.wait_to_click(self.confirm_delete_pn)
            time.sleep(3)
            self.scroll_to_bottom()
            assert not self.is_present(self.phone_verify_button)
        else:
            print("Phone Number not already added")

        self.wait_to_clear_and_send_keys(self.phone_number_input, UserData.text_now_number)
        self.webapp.wait_to_click(self.add_number_button)
        self.wait_for_element(self.number_added_success)
        self.scroll_to_bottom()
        if self.is_present(self.already_in_use):
            print("Number is already in use and no verification needed")
            return "No"
        else:
            self.webapp.wait_to_click(self.phone_verify_button)
            return "Yes"