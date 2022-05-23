import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from HQSmokeTests.testPages.base.base_page import BasePage
from HQSmokeTests.userInputs.user_inputs import UserData

""""Contains test page elements and functions related to the Reassign Cases module"""


class ReassignCasesPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.reassign_cases_menu = (By.LINK_TEXT, "Reassign Cases")
        self.apply = (By.ID, "apply-btn")
        self.case_type = (By.ID, "report_filter_case_type")
        self.case_type_option_value = (By.XPATH, "//option[@value='reassign']")
        self.select_first_case = (By.XPATH, "(//input[@type='checkbox'])[1]")
        self.first_case_name = (By.XPATH, "(//a[contains(@class, 'ajax_dialog')])[1]")
        self.user_search_dropdown = (By.ID, "select2-reassign_owner_select-container")
        self.user_to_be_reassigned = (By.XPATH, "(//li[contains(.,'Active Mobile Worker')])[1]")
        self.submit = (By.XPATH, "(//button[text()='Reassign'])[1]")
        self.new_owner_name = (By.XPATH, "((//td)[4])[1]")
        self.out_of_range = (By.XPATH, "(//span[@class='label label-warning'])[1]")
        self.search_query = (By.ID, "report_filter_search_query")

    def get_cases(self):
        self.wait_to_click(self.reassign_cases_menu)
        self.select_by_value(self.case_type, UserData.case_reassign)
        self.wait_to_click(self.apply)

    def reassign_case(self):
        self.wait_to_click(self.select_first_case)
        case_being_reassgined = self.get_text(self.first_case_name)
        self.wait_to_click(self.user_search_dropdown)
        assigned_username = self.get_text(self.user_to_be_reassigned).split('"')[0]
        self.move_to_element_and_click(self.user_to_be_reassigned)
        self.wait_to_click(self.submit)
        self.is_visible_and_displayed(self.out_of_range)
        self.driver.refresh()
        self.wait_to_clear_and_send_keys(self.search_query, case_being_reassgined)
        self.send_keys(self.search_query, Keys.TAB)
        self.wait_to_click(self.apply)
        time.sleep(5)
        self.wait_for_element(self.new_owner_name)
        reassigned_username = self.get_text(self.new_owner_name).split('"')[0]
        assert reassigned_username in assigned_username
