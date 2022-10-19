import time

from common_utilities.selenium.base_page import BasePage
from common_utilities.generate_random_string import fetch_random_string

from selenium.webdriver.common.by import By

""""Contains test page elements and functions related to the User's Roles and Permissions module"""


class RolesPermissionPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.role_name_created = "role_" + fetch_random_string()
        self.role_rename_created = "role_rename_" + fetch_random_string()
        self.roles_menu = (By.XPATH, "//a[@data-title='Roles & Permissions']")
        self.add_new_role = (
        By.XPATH, "//button[@data-bind='click: function () {$root.setRoleBeingEdited($root.defaultRole)}']")
        self.role_name = (By.ID, "role-name")
        self.edit_web_user_checkbox = (By.ID, "edit-web-users-checkbox")
        self.save_button = (By.XPATH, "//button[@class='btn btn-primary disable-on-submit']")
        self.role_created = (By.XPATH, "//span[text()='" + str(self.role_name_created) + "']")
        self.edit_created_role = (By.XPATH, "//th[.//span[.='" + str(
            self.role_name_created) + "']]/following-sibling::td//*[@class='fa fa-edit']")
        self.delete_role = (By.XPATH, "//th[.//span[.='" + str(
            self.role_name_created) + "']]/following-sibling::td//i[@class='fa fa-trash']")
        self.edit_mobile_worker_checkbox = (By.ID, "edit-commcare-users-checkbox")
        self.role_renamed = (By.XPATH, "//span[text()='" + str(self.role_rename_created) + "']")
        self.confirm_role_delete = (By.XPATH, "//div[@class='btn btn-danger']")

    def roles_menu_click(self):
        self.wait_to_click(self.roles_menu)
        assert "Roles & Permissions : Users :: - CommCare HQ" in self.driver.title

    def add_role(self):
        self.wait_to_click(self.add_new_role)
        self.wait_to_clear_and_send_keys(self.role_name, self.role_name_created)
        self.click(self.edit_web_user_checkbox)
        self.move_to_element_and_click(self.save_button)
        assert self.is_present_and_displayed(self.role_created), "Role not added successfully!"

    def edit_role(self):
        self.wait_to_click(self.edit_created_role)
        self.wait_to_clear_and_send_keys(self.role_name, self.role_rename_created)
        self.move_to_element_and_click(self.edit_mobile_worker_checkbox)
        self.move_to_element_and_click(self.save_button)
        assert self.is_present_and_displayed(self.role_renamed), "Role not edited successfully!"
        time.sleep(1)

    def cleanup_role(self):
        self.wait_to_click(self.delete_role)
        self.wait_to_click(self.confirm_role_delete)

    def delete_test_roles(self):
        list_profile = self.driver.find_elements(By.XPATH, "//th[.//span[contains(text(),'role_')]]")
        print(list_profile)
        if len(list_profile) > 0:
            for i in range(len(list_profile))[::-1]:
                text = list_profile[i].text
                print(text)
                self.driver.find_element(By.XPATH,
                                         "(//th[.//span[contains(text(),'role_')]]//following-sibling::td//button[@class='btn btn-danger'])[" + str(
                                             i + 1) + "]").click()
                self.wait_to_click(self.confirm_role_delete)
                time.sleep(2)
                list_profile = self.driver.find_elements(By.XPATH, "//th[.//span[contains(text(),'role_')]]")
        else:
            print("There are no test roles")
