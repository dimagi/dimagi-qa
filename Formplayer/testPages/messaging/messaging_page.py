import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from Formplayer.userInputs.user_inputs import UserData
from common_utilities.selenium.base_page import BasePage


class MessagingPage(BasePage):
    def __init__(self, driver, settings):
        super().__init__(driver)

        self.dashboard_link = settings['url'] + "/dashboard/project/"
        self.messaging_menu_id = (By.ID, "MessagingTab")
        self.view_all = (By.LINK_TEXT, "View All")
        self.show_full_menu = (By.ID, "commcare-menu-toggle")
        self.keywords_link = (By.LINK_TEXT, "Keywords")

        self.DASHBOARD_TITLE = "CommCare HQ"
        self.MESSAGING_TITLE = "Dashboard : Messaging :: - CommCare HQ"
        self.KEYWORDS_TITLE = "Keywords : Messaging :: - CommCare HQ"

        self.keyword_delete_button = "//td[.//a[.='{}']]//following-sibling::td/a[contains(@data-bind,'delete')]"
        self.confirm_delete = "//td[.//a[.='{}']]//following-sibling::td//a[.='Cancel']//preceding-sibling::a[contains(@class,'confirm')]/i[@class='fa fa-remove']"

        self.add_keyword_button = (By.XPATH, "//a[contains(@href,'keywords/normal/add/')]")
        self.keyword_field = (By.XPATH, "//input[@id='id_keyword']")
        self.description_field = (By.XPATH, "//input[@id='id_description']")
        self.send_to_sender = (By.XPATH, "//select[@id='id_sender_content_type']")
        self.survey = (By.XPATH, "//select[@id='id_sender_app_and_form_unique_id']")
        self.save_button = (By.XPATH, "//button[.='Save']")


    def open_reports_menu(self):
        if self.is_present(self.show_full_menu):
            self.js_click(self.show_full_menu)
        self.driver.get(self.dashboard_link)
        self.wait_for_element(self.messaging_menu_id)
        self.wait_to_click(self.messaging_menu_id)
        self.wait_to_click(self.view_all)
        assert self.MESSAGING_TITLE in self.driver.title, "This is not the Messaging menu page."

    def open_keywords_link(self):
        self.open_reports_menu()
        self.wait_to_click(self.keywords_link)
        assert self.KEYWORDS_TITLE in self.driver.title, "This is not the Keywords page."

    def add_keywords(self, list):
        self.wait_for_element(self.add_keyword_button)
        self.delete_keywords(list)
        for items, surveys in zip(list, UserData.sms_survey_list):
            self.wait_to_click(self.add_keyword_button)
            self.wait_to_clear_and_send_keys(self.keyword_field, items)
            self.wait_to_clear_and_send_keys(self.description_field, items)
            self.select_by_text(self.send_to_sender,"SMS Survey")
            self.wait_for_element(self.survey)
            self.select_by_text(self.survey, surveys)
            self.scroll_to_element(self.save_button)
            self.wait_to_click(self.save_button)
            time.sleep(2)
            self.driver.refresh()
            time.sleep(5)




    def delete_keywords(self, list):
        for items in list:
            if self.is_present_and_displayed((By.LINK_TEXT, items),10):
                self.wait_to_click((By.XPATH, self.keyword_delete_button.format(items)))
                self.wait_to_click((By.XPATH,self.confirm_delete.format(items)))
                time.sleep(2)
                self.driver.refresh()
            else:
                print("Keyword "+items+" is not present")
