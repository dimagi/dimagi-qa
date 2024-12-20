import time

from common_utilities.hq_login.login_page import LoginPage
from common_utilities.selenium.base_page import BasePage
from common_utilities.path_settings import PathSettings
from HQSmokeTests.userInputs.user_inputs import UserData
from common_utilities.generate_random_string import fetch_random_string
from HQSmokeTests.testPages.users.org_structure_page import latest_download_file

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, \
    NoAlertPresentException
from selenium.webdriver.common.by import By

""""Contains test page elements and functions related to the various messaging mediums available on CCHQ"""


class RepeatersPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.repeater_name_input = "repeater_" + fetch_random_string()

        # Data Forwarding Dashboard
        self.menu_settings = (By.XPATH, "//*[@aria-label='Manage Settings']")
        self.project_settings = (By.XPATH, "//*[@data-label='Update Project Settings']")
        self.data_forwarding_linked_text = (By.LINK_TEXT, "Data Forwarding")
        self.add_forward_form_service = (
        By.XPATH, "//h2[.='Forward Forms']//following-sibling::a[contains(@href,'FormRepeater')]")
        self.name_input = (By.XPATH, "//label[contains(.,'Name')]//following-sibling::div/input")
        self.http_req_method_dropdown = (
        By.XPATH, "//label[contains(.,'HTTP Request Method')]//following-sibling::div/select")
        self.payload_format = (By.XPATH, "//label[contains(.,'Payload Format*')]//following-sibling::div/select")
        self.submit_button = (By.XPATH, "//button[@type='submit'][contains(.,'Forward')]")
        self.repeater_edit_button = "//td[contains(.,'{}')]//following-sibling::td/a[contains(.,'Edit')]"
        self.repeater_delete_button = "//td[contains(.,'{}')]//following-sibling::td/a[contains(.,'Delete')]"
        self.setup_success = "//div[contains(@class,'alert-success')][contains(.,'Forwarding set up to {}')]"
        self.update_success = (
        By.XPATH, "//div[contains(@class,'alert-success')][contains(.,'Forwarder Successfully Updated')]")
        self.delete_success = (
            By.XPATH, "//div[contains(@class,'alert-success')][contains(.,'Forwarding stopped!')]")
        self.close_message = (
            By.XPATH, "//div[contains(@class,'alert-success')][contains(.,'Forwarding stopped!')]/button[contains(@class,'close')]")
        self.confirm_delete_button = "//div[./p[contains(.,'{}')]]//following-sibling::div/*[contains(.,'Delete')]"
        self.test_repeater_row = (By.XPATH, "//td[starts-with(.,'repeater_')]")

    def data_forwarding(self):
        self.wait_for_element(self.data_forwarding_linked_text)
        self.wait_to_click(self.data_forwarding_linked_text)
        assert self.is_present_and_displayed(self.add_forward_form_service), "Data Forwarding is not loaded"
        print("Data Forwarding page successfully loaded")

    def add_repeater(self):
        self.data_forwarding()
        self.wait_for_element(self.add_forward_form_service)
        self.wait_to_click(self.add_forward_form_service)
        assert self.is_present_and_displayed(self.name_input), "Add service screen not loaded"
        print("Add service page successfully loaded")
        self.wait_to_clear_and_send_keys(self.name_input, self.repeater_name_input)
        self.select_by_text(self.http_req_method_dropdown, UserData.http_req_methods[1])
        self.select_by_text(self.payload_format, UserData.payload_format[0])
        time.sleep(2)
        self.scroll_to_element(self.submit_button)
        time.sleep(2)
        self.js_click(self.submit_button)
        self.wait_for_element((By.XPATH, self.setup_success.format(self.repeater_name_input)))

    def edit_repeater(self):
        self.data_forwarding()
        assert self.is_present_and_displayed(
            (By.XPATH, self.repeater_edit_button.format(self.repeater_name_input))), "Repeater edit button not present"
        print("Repeater edit button successfully loaded")
        self.wait_to_click((By.XPATH, self.repeater_edit_button.format(self.repeater_name_input)))
        self.wait_for_element(self.name_input)
        self.select_by_text(self.http_req_method_dropdown, UserData.http_req_methods[0])
        self.select_by_text(self.payload_format, UserData.payload_format[1])
        time.sleep(2)
        self.scroll_to_element(self.submit_button)
        time.sleep(2)
        self.js_click(self.submit_button)
        assert self.is_present_and_displayed(self.update_success), "Edit repeater failed"
        print("Repeater updated successfully")

    def delete_repeater(self):
        self.data_forwarding()
        assert self.is_present_and_displayed((By.XPATH, self.repeater_delete_button.format(
            self.repeater_name_input))), "Repeater edit button not present"
        print("Repeater edit button successfully loaded")
        self.wait_to_click((By.XPATH, self.repeater_delete_button.format(self.repeater_name_input)))
        self.wait_for_element((By.XPATH, self.confirm_delete_button.format(self.repeater_name_input)))
        self.wait_to_click((By.XPATH, self.confirm_delete_button.format(self.repeater_name_input)))
        assert self.is_present_and_displayed(self.delete_success), "Delete repeater failed"
        print("Repeater deleted successfully")

    def delete_all_repeaters(self):
        self.data_forwarding()
        repeater_names = []
        list_repeater = self.find_elements(self.test_repeater_row)
        if len(list_repeater) > 0:
            print("Test repeaters are present")
            for item in list_repeater:
                repeater_names.append(item.text)
            print("Test Repeater list: ", repeater_names)
            for item in repeater_names:
                self.wait_to_click((By.XPATH, self.repeater_delete_button.format(item)))
                self.wait_for_element((By.XPATH, self.confirm_delete_button.format(item)))
                self.wait_to_click((By.XPATH, self.confirm_delete_button.format(item)))
                assert self.is_present_and_displayed(self.delete_success), "Delete repeater failed"
                print("Repeater deleted successfully", item)
                self.wait_to_click(self.close_message)
                time.sleep(3)
            print("All test repeaters deleted")
        else:
            print("No test repeaters present")
