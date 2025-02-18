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

        self.created_group_path = "//a[contains(.,'{}')]"# (By.LINK_TEXT, self.created_group)
        self.group_name = (By.ID, "id_group_name")
        self.add_group_button = (By.XPATH, "//button[@type='submit' and @class='btn btn-primary']")
        self.group_menu_xpath = (By.XPATH, "//a[@data-title='Groups']")
        self.users_drop_down = (By.XPATH, "//span[@class='select2-selection select2-selection--multiple']")
        self.select_user =  "//li[text()='{}']"
        self.update_button = (By.ID, "submit-id-submit")
        self.group_created_success = (By.XPATH, "//h1[text()[contains(.,'Editing Group')]]")
        self.edit_settings = (By.LINK_TEXT, "Edit Settings")
        self.group_name_input = (By.ID, "group-name-input")
        self.save_button = (By.XPATH, "//button[@type='submit' and text()='Save']")
        self.success_alert = (By.XPATH, "//div[contains(@class,'alert-success')]")
        self.remove_user = (By.XPATH, "//button[@title='Remove item']")
        self.delete_group = (By.XPATH, "//a[contains(@class,'danger')]")
        self.group_list = (By.XPATH, "//td//a[contains(text(),'group_')]")
        self.group_name_link = "(//td//a[contains(text(),'{}')])[1]"

        self.confirm_delete = (By.XPATH, "//button[contains(@class,'danger disable-on-submit')]")
        self.delete_success_message = (By.XPATH, "//div[contains(@class, 'alert-success')]")
        # self.renamed_group_link = (By.LINK_TEXT, self.renamed_group)
        self.group_loading = (By.XPATH, "//div[@id='membership_updating'][@style='display: none;']")
        self.table_body = (By.XPATH, "//table//tbody")

    def click_group_menu(self):
        self.wait_to_click(self.group_menu_xpath)

    def add_group(self):
        self.click_group_menu()
        self.wait_to_clear_and_send_keys(self.group_name, self.created_group)
        self.wait_to_click(self.add_group_button)
        assert self.is_visible_and_displayed(self.group_created_success), "Group not created successfully"
        print("Group Added")
        return self.created_group

    def add_user_to_group(self, username, group_name):
        self.send_keys(self.users_drop_down, username)
        self.wait_to_click((By.XPATH, self.select_user.format(username)))
        time.sleep(20)
        self.wait_for_element(self.users_drop_down, 400)
        self.wait_to_click(self.update_button)
        time.sleep(15)
        assert self.is_visible_and_displayed(self.success_alert, 100), "Group settings not be saved"
        print(self.driver.current_url)
        group_id_value = self.driver.current_url.split("/")[-2]
        time.sleep(2)
        self.click_group_menu()
        assert self.is_visible_and_displayed((By.XPATH, self.created_group_path.format(group_name))), "User could not be assigned to the group"
        self.accept_pop_up()
        print("User Added to Group")
        return group_id_value

    def edit_existing_group(self, group_name):
        self.click_group_menu()
        time.sleep(2)
        self.wait_to_click((By.XPATH, self.created_group_path.format(group_name)))
        self.accept_pop_up()
        self.wait_to_click(self.edit_settings)
        renamed_group = group_name+"_rename"
        self.wait_to_clear_and_send_keys(self.group_name_input, renamed_group)
        self.click(self.save_button)
        assert self.is_visible_and_displayed(self.success_alert), "Group could not be renamed"
        print("Renamed a group")
        return renamed_group

    def remove_user_from_group(self):
        time.sleep(3)
        try:
            self.js_click(self.remove_user)
            self.js_click(self.update_button)
            time.sleep(15)
            assert self.is_visible_and_displayed(self.success_alert, 100), "User deletion from group not successful"
            print("Removed added user from group")
            time.sleep(2)
        except Exception:
            print("No user group present")

    def cleanup_group(self, renamed_group):
        try:
            self.wait_to_click((By.XPATH, self.created_group.format(renamed_group)))
            self.wait_to_click(self.delete_group)
            self.wait_to_click(self.confirm_delete)
            assert self.is_visible_and_displayed(self.delete_success_message), "Group deletion not successful"
            print("Clean up added group")
        except Exception:
            print("Group deletion might not have been successful")

    def delete_test_groups(self):
        list_profile = self.find_elements(self.group_list)
        print(len(list_profile))
        group_names = []
        if len(list_profile) > 0:
            for i in range(len(list_profile)):
                text = list_profile[i].text
                group_names.append(text)
        print(group_names)
        try:
            if len(group_names) > 0:
                for i in range(len(group_names)):
                    time.sleep(2)
                    self.scroll_to_element((By.XPATH, self.group_name_link.format(group_names[i])))
                    self.click((By.XPATH, self.group_name_link.format(group_names[i])))
                    self.wait_for_element(self.delete_group)
                    self.click(self.delete_group)
                    self.wait_for_element(self.confirm_delete)
                    self.click(self.confirm_delete)
                    assert self.is_visible_and_displayed(self.delete_success_message), "Group deletion not successful"
                    print("Deleted group: "+group_names[i])
                    time.sleep(5)
                    self.click_group_menu()
                    self.wait_for_element(self.table_body)
            else:
                print("There are no test groups")
        except:
            print("There are no test groups")