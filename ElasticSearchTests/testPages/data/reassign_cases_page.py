import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from HQSmokeTests.testPages.data.copy_cases_page import CopyCasesPage
from common_utilities.selenium.base_page import BasePage
from ElasticSearchTests.userInputs.user_inputs import UserData

""""Contains test page elements and functions related to the Reassign Cases module"""


class ReassignCasesPage(BasePage):

    def __init__(self, driver, settings):
        super().__init__(driver)
        self.settings = settings

        self.env_url = settings["url"]
        self.reassign_cases_menu = (By.LINK_TEXT, "Reassign Cases")
        self.apply = (By.ID, "apply-btn")
        self.case_type = (By.ID, "report_filter_case_type")
        self.case_owner_field = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]")
        self.user_from_list = "//li[contains(.,'{}')]"
        self.remove_project_data = (By.XPATH,
                                     "//span[.='[Project Data]']//preceding-sibling::button[@class='select2-selection__choice__remove']")


        self.case_type_option_value = (By.XPATH, "//option[@value='reassign']")
        self.select_all = (By.XPATH, "(//a[@class='select-all btn btn-xs btn-default'][.='all'])[1]")
        self.select_first_case = (By.XPATH, "(//input[@type='checkbox'])[2]")
        self.first_case_name = (By.XPATH, "(//a[contains(@class, 'ajax_dialog')])[1]")
        self.user_search_dropdown = (By.ID, "select2-reassign_owner_select-container")
        self.user_to_be_reassigned = (By.XPATH, "(//li[contains(.,'Active Mobile Worker')])[1]")

        self.submit = (By.XPATH, "(//button[text()='Reassign'])[1]")
        self.new_owner_name = (By.XPATH, "((//td)[4])[1]")
        self.out_of_range = (By.XPATH, "(//span[@class='label label-warning'])[1]")
        self.search_query = (By.ID, "report_filter_search_query")
        self.reassign_to_user_dropdwon_input = (By.XPATH, "//input[@class='select2-search__field']")
        self.reassigned_user_from_list = "//li[starts-with(text(), '{}') and contains(text(), 'Active Mobile Worker')]"

        self.last_modified = (By.XPATH, "(//text()[contains(.,'Last Modified')]//preceding-sibling::i[@class='icon-white fa dt-sort-icon'])[1]")
        self.last_modified_ascending = (By.XPATH, "(//text()[contains(.,'Last Modified')]//preceding-sibling::i[@class='icon-white fa dt-sort-icon'])[1]//parent::div//parent::th[@aria-sort='ascending']")
        self.last_modified_descending = (By.XPATH, "(//text()[contains(.,'Last Modified')]//preceding-sibling::i[@class='icon-white fa dt-sort-icon'])[1]//parent::div//parent::th[@aria-sort='descending']")

    def get_cases(self, text):
        self.wait_to_click(self.reassign_cases_menu)
        self.wait_for_element(self.case_owner_field)
        self.wait_to_click(self.remove_project_data)
        self.send_keys(self.case_owner_field, UserData.user_group)
        self.wait_to_click((By.XPATH, self.user_from_list.format(UserData.user_group_shared)))
        time.sleep(2)
        ActionChains(self.driver).send_keys(Keys.TAB).perform()
        self.send_keys(self.search_query, text)
        self.wait_to_click(self.apply)
        print("Sleeping for the list to load")
        time.sleep(20)

    def reassign_case(self, text):
        self.get_cases(text)
        copy = CopyCasesPage(self.driver, self.settings)
        copy.sort_for_latest_on_top()
        time.sleep(5)
        self.wait_to_click(self.select_all)
        self.wait_to_click(self.user_search_dropdown)
        self.send_keys(self.reassign_to_user_dropdwon_input, UserData.assign_case_user)
        assigned_username = self.get_text((By.XPATH, self.reassigned_user_from_list.format(UserData.assign_case_user)))
        print("Assigned Username:", assigned_username)
        self.move_to_element_and_click((By.XPATH, self.reassigned_user_from_list.format(UserData.assign_case_user)))
        self.wait_to_click(self.submit)
        time.sleep(20)
        self.is_visible_and_displayed(self.out_of_range)
        print("Sleeping sometime for the case to get updated")
        time.sleep(10)
        self.driver.refresh()
        print("Cases reassigned")

    def sort_for_latest_on_top(self):
        self.wait_to_click(self.last_modified)
        self.wait_for_element(self.last_modified_ascending, 50)
        time.sleep(5)
        self.wait_to_click(self.last_modified)
        self.wait_for_element(self.last_modified_descending, 50)