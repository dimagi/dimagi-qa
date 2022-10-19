import time

from common_utilities.selenium.base_page import BasePage
from common_utilities.generate_random_string import fetch_random_string

from selenium.webdriver.common.by import By

""""Contains test page elements and functions related to the User's Groups module"""


class GroupPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.created_group = "group_" + fetch_random_string()
        self.renamed_group = self.created_group + "_rename"

        self.created_group_path = (By.LINK_TEXT, self.created_group)
        self.group_name = (By.ID, "id_group_name")
        self.add_group_button = (By.XPATH, "//button[@type='submit' and @class='btn btn-primary']")
        self.group_menu_xpath = (By.XPATH, "//a[@data-title='Groups']")
        self.users_drop_down = (By.XPATH, "//span[@class='select2-selection select2-selection--multiple']")
        self.select_user = (By.XPATH,  "//li[text()='" + "username_" + fetch_random_string() + "']")
        self.update_button = (By.ID, "submit-id-submit")
        self.group_created_success = (By.XPATH, "//h1[text()[contains(.,'Editing Group')]]")
        self.edit_settings = (By.LINK_TEXT, "Edit Settings")
        self.group_name_input = (By.ID, "group-name-input")
        self.save_button = (By.XPATH, "//button[@type='submit' and text()='Save']")
        self.success_alert = (By.ID, "save-alert")
        self.remove_user = (By.XPATH, "//button[@title='Remove item']")
        self.delete_group = (By.XPATH, "//a[@class='btn btn-danger pull-right']")
        self.confirm_delete = (By.XPATH, "//button[@class='btn btn-danger disable-on-submit']")
        self.delete_success_message = (By.XPATH, "//div[@class='alert alert-margin-top fade in html alert-success']")
        self.renamed_group_link = (By.LINK_TEXT, self.renamed_group)

    def click_group_menu(self):
        self.wait_to_click(self.group_menu_xpath)

    def add_group(self):
        self.click_group_menu()
        self.wait_to_clear_and_send_keys(self.group_name, self.created_group)
        self.wait_to_click(self.add_group_button)
        assert self.is_visible_and_displayed(self.group_created_success), "Group not created successfully"
        print("Group Added")

    def add_user_to_group(self, username):
        self.send_keys(self.users_drop_down, username)
        self.wait_to_click(self.select_user)
        self.wait_to_click(self.update_button)
        print(self.driver.current_url)
        group_id_value = self.driver.current_url.split("/")[-2]
        time.sleep(2)
        self.click_group_menu()
        assert self.is_visible_and_displayed(self.created_group_path), "User could not be assigned to the group"
        self.accept_pop_up()
        print("User Added to Group")
        return group_id_value

    def edit_existing_group(self):
        self.click_group_menu()
        time.sleep(2)
        self.wait_to_click(self.created_group_path)
        self.accept_pop_up()
        self.wait_to_click(self.edit_settings)
        self.wait_to_clear_and_send_keys(self.group_name_input, self.renamed_group)
        self.click(self.save_button)
        assert self.is_visible_and_displayed(self.success_alert), "Group could not be renamed"
        print("Renamed a group")

    def remove_user_from_group(self):
        time.sleep(3)
        self.js_click(self.remove_user)
        self.js_click(self.update_button)
        assert self.is_visible_and_displayed(self.success_alert), "User deletion from group not successful"
        print("Removed added user from group")
        time.sleep(2)

    def cleanup_group(self):
        self.wait_to_click(self.renamed_group_link)
        self.wait_to_click(self.delete_group)
        self.wait_to_click(self.confirm_delete)
        assert self.is_visible_and_displayed(self.delete_success_message), "Group deletion not successful"
        print("Clean up added group")

    def delete_test_groups(self):
        list_profile = self.driver.find_elements(By.XPATH,"//td//a[contains(text(),'group_')]")
        print(list_profile)
        if len(list_profile) > 0:
            for i in range(len(list_profile))[::-1]:
                text = list_profile[i].text
                print(text)
                list_profile[i].click()
                self.wait_to_click(self.delete_group)
                self.wait_to_click(self.confirm_delete)
                assert self.is_visible_and_displayed(self.delete_success_message), "Group deletion not successful"
                time.sleep(2)
                list_profile = self.driver.find_elements(By.XPATH,"//td//a[contains(text(),'group_')]")
        else:
             print("There are no test groups")