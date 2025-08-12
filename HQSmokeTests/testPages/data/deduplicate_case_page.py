import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from common_utilities.generate_random_string import fetch_random_string
from common_utilities.selenium.base_page import BasePage
from HQSmokeTests.userInputs.user_inputs import UserData


""""Contains test page elements and functions related to deduplicate case module"""


class DeduplicateCasePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.rule_name = "rule " + str(fetch_random_string())
        self.rule_created = "//a/strong[text()='" + self.rule_name + "']"
        self.success = "Successfully created deduplication rule: " + self.rule_name

        self.deduplicate_case_link = (By.LINK_TEXT, 'Deduplicate Cases')
        self.add_rule_button = (By.ID, 'add-new')
        self.add_rule_name = (By.XPATH, "//input[@type='text']")
        self.case_type = (By.XPATH, "//span[@class='selection']")
        self.case_type_option_value = (By.XPATH, "//option[@value = 'pregnancy']")
        self.case_property = (By.XPATH, "//input[@class='textinput form-control' and contains(@data-bind, 'caseProperty.name')]")
        self.save_rule_button = (By.XPATH, "//button[@type = 'submit']")
        self.success_message = (By.XPATH, "//a[@data-dismiss='alert']")
        self.delete_rule = (By.XPATH, "//button[@class = 'btn btn-danger']")
        self.delete_confirm = (By.XPATH, "//button[@class = 'btn btn-danger delete-item-confirm']")
        self.rule_created_path = (By.XPATH, self.rule_created)
        self.case_property_drop_down = (By.XPATH, "//select[contains(@data-bind, 'casePropertyNames')]")
        self.case_property_input = (By.XPATH, "//input[@class = 'select2-search__field']")
        self.case_type_drop_down = (By.XPATH, "//select[@name='case_type']")

    def open_deduplicate_case_page(self):
        self.wait_to_click(self.deduplicate_case_link)

    def add_new_rule(self):
        self.wait_to_click(self.add_rule_button)
        self.send_keys(self.add_rule_name, self.rule_name)
        self.select_by_value(self.case_type_drop_down, UserData.case_pregnancy)
        if self.is_present(self.case_property):
            self.send_keys(self.case_property, UserData.case_property)
        else:
            self.select_by_value(self.case_property_drop_down, UserData.case_property)
        self.wait_to_click(self.save_rule_button)
        time.sleep(2)
        assert self.is_present_and_displayed(self.success_message)
        print("New Rule to find Deduplicate Cases created successfully!")

    def remove_rule(self):
        self.open_deduplicate_case_page()
        self.wait_to_click(self.delete_rule)
        self.wait_to_click(self.delete_confirm)
        self.reload_page()
        time.sleep(2)
        try:
            isPresent = self.is_present(self.rule_created_path)
            
        except (TimeoutException, NoSuchElementException):
            isPresent = False
            
        assert isPresent == False
        print("Rule removed successfully!")


