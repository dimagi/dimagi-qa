import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from common_utilities.selenium.base_page import BasePage
from HQSmokeTests.userInputs.user_inputs import UserData

""""Contains test page elements and functions related to the Copy Cases module"""


class CopyCasesPage(BasePage):

    def __init__(self, driver, settings):
        super().__init__(driver)

        self.env_url = settings["url"]
        self.copy_cases_menu = (By.LINK_TEXT, "Copy Cases")
        self.apply = (By.ID, "apply-btn")
        self.case_type = (By.XPATH, "//select[@name='case_type']")
        self.case_type_option_value = (By.XPATH, "//option[@value='reassign']")

        self.select_first_case = (By.XPATH, "(//td[2][not(contains(.,'no name'))]//preceding-sibling::td/input[@type='checkbox'])[1]")
        self.first_case_name = (By.XPATH, "(//a[contains(@class, 'ajax_dialog')][not(contains(.,'no name'))])[1]")
        self.user_search_dropdown = (By.ID, "report_filter_individual")
        self.user_to_be_copied = (By.XPATH, "(//li[contains(.,'All Mobile Workers')])[1]")

        self.copy_btn = (By.XPATH, "(//button[text()='Copy'])[1]")
        self.new_owner_name = (By.XPATH, "((//td)[4])[1]")
        self.copied_time = (By.XPATH, "((//td)[5])[1]")
        self.last_modified = (By.XPATH, "(//text()[contains(.,'Last Modified')]//preceding-sibling::i[@class='icon-white fa dt-sort-icon'])[1]")
        self.last_modified_ascending = (By.XPATH, "(//text()[contains(.,'Last Modified')]//preceding-sibling::i[@class='icon-white fa dt-sort-icon'])[1]//parent::div//parent::th[@aria-sort='ascending']")
        self.last_modified_descending = (By.XPATH, "(//text()[contains(.,'Last Modified')]//preceding-sibling::i[@class='icon-white fa dt-sort-icon'])[1]//parent::div//parent::th[@aria-sort='descending']")
        self.search_query = (By.ID, "report_filter_search_query")
        self.out_of_range = (By.XPATH, "(//span[@class='label label-warning'])[1]")
        self.copy_dropdown = (By.ID, "select2-reassign_owner_select-container")
        self.copy_to_user_dropdown_input = (By.XPATH, "//input[@class='select2-search__field']")
        self.copied_user_from_list = "//li[starts-with(text(), '{}')]"
        self.success_message = (By.XPATH, "//*[@data-bind='html: message' and contains(.,'Cases copied')]")
        self.empty_list = (By.XPATH, "//td[.='No data available to display. Please try changing your filters.']")
        self.users_field = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]")
        self.users_list_item = "//ul[@role='listbox']/li[contains(.,'{}')]"
        self.remove_buttons = (By.XPATH, "//select[@name='case_list_filter']//following-sibling::span//ul//button")

    def sort_for_latest_on_top(self):
        self.wait_to_click(self.last_modified)
        self.wait_for_element(self.last_modified_ascending, 50)
        time.sleep(5)
        self.wait_to_click(self.last_modified)
        self.wait_for_element(self.last_modified_descending, 50)

    def remove_default_users(self):
        self.wait_for_element(self.users_field)
        count = self.find_elements(self.remove_buttons)
        print(len(count))
        for i in range(len(count)):
            count[0].click()
            time.sleep(2)
            if len(count) != 1:
                ActionChains(self.driver).send_keys(Keys.TAB).perform()
                time.sleep(2)
            count = self.find_elements(self.remove_buttons)
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

    def get_cases(self, username):
        self.wait_to_click(self.copy_cases_menu)
        self.wait_for_element(self.case_type, 60)
        self.select_by_value(self.case_type, UserData.case_reassign)
        self.remove_default_users()
        self.send_keys(self.users_field, username)
        self.wait_to_click((By.XPATH, self.users_list_item.format(username)))
        time.sleep(1)
        self.wait_to_click(self.apply)


    def copy_case(self):
        self.sort_for_latest_on_top()
        time.sleep(5)
        self.wait_to_click(self.select_first_case)
        case_being_copied = self.get_text(self.first_case_name)
        self.wait_to_click(self.copy_dropdown)
        time.sleep(1)
        self.send_keys(self.copy_to_user_dropdown_input, UserData.mobile_testuser)
        time.sleep(1)
        assigned_username = self.get_text((By.XPATH,self.copied_user_from_list.format(UserData.mobile_testuser)))
        print("Assigned Username:", assigned_username)
        self.move_to_element_and_click((By.XPATH, self.copied_user_from_list.format(UserData.mobile_testuser)))
        time.sleep(5)
        self.wait_to_click(self.copy_btn)
        time.sleep(5)
        self.wait_for_element(self.success_message, 130)
        print("Sleeping for sometimes for the case to be copied")
        time.sleep(60)
        self.driver.refresh()
        time.sleep(5)
        self.remove_default_users()
        self.send_keys(self.users_field, assigned_username)
        self.wait_to_click((By.XPATH, self.users_list_item.format(assigned_username)))
        time.sleep(3)
        self.send_keys(self.search_query, case_being_copied)
        self.wait_to_click(self.apply)
        time.sleep(5)
        self.scroll_to_bottom()
        self.sort_for_latest_on_top()
        if self.is_present(self.empty_list):
            print("No Case Copied, List is empty")
            assert False
        else:
            self.wait_for_element(self.new_owner_name, 60)
            self.sort_for_latest_on_top()
            time.sleep(5)
            self.wait_for_element(self.new_owner_name, 60)
            copied_username = self.get_text(self.new_owner_name)
            time_modified = self.get_text(self.copied_time)
            time_modified = str(time_modified).split()
            print("Copied Username:", copied_username)
            print(time_modified[0])
            print(time_modified[1])
            value = str(time_modified[0]).strip()
            assert UserData.mobile_testuser in copied_username
            if str(value).isdigit():
                assert int(value) <= 5 and "minutes" in str(time_modified[1]).strip(), "case took longer to copy"
            elif str(value).isalpha():
                assert value == 'a' and "minute" in str(time_modified[1]).strip(), "case took longer to copy"
            else:
                assert False
