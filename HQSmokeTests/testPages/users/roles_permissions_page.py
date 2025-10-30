import time

from selenium.common import ElementNotInteractableException
from selenium.webdriver.common.actions.interaction import KEY

from HQSmokeTests.testPages.home.home_page import HomePage
from HQSmokeTests.testPages.users.web_user_page import WebUsersPage
from common_utilities.selenium.base_page import BasePage
from common_utilities.generate_random_string import fetch_random_string

from HQSmokeTests.userInputs.user_inputs import UserData
from selenium.webdriver.common.by import By

""""Contains test page elements and functions related to the User's Roles and Permissions module"""


class RolesPermissionPage(BasePage):

    def __init__(self, driver, settings):
        super().__init__(driver)
        self.settings = settings

        self.role_name_created = "role_" + fetch_random_string()
        self.role_non_admin_created = "role_non_" + fetch_random_string()
        self.role_no_shared_export_created = "role_no_export_" + fetch_random_string()
        self.role_yes_shared_export_created = "role_yes_export_" + fetch_random_string()
        self.role_rename_created = "role_rename_" + fetch_random_string()
        self.roles_menu = (By.XPATH, "//a[@data-title='Roles & Permissions']")
        self.add_new_role = (
        By.XPATH, "//button[@data-bind='click: function () {$root.setRoleBeingEdited($root.defaultRole)}']")
        self.role_name = (By.ID, "role-name")
        self.edit_web_user_checkbox = (By.XPATH, "//input[@id='edit-web-users-checkbox']//following-sibling::label/span")
        self.save_button = (By.XPATH, "//button[@class='btn btn-primary disable-on-submit']")
        self.role_created = (By.XPATH, "//span[text()='" + str(self.role_name_created) + "']")
        self.edit_created_role = (By.XPATH, "//th[.//span[.='" + str(
            self.role_name_created) + "']]/following-sibling::td//*[@class='fa fa-edit']")
        self.delete_role = (By.XPATH, "//th[.//span[.='" + str(
            self.role_name_created) + "']]/following-sibling::td//i[@class='fa fa-trash']")
        self.edit_mobile_worker_checkbox = (By.XPATH, "//input[@id='edit-commcare-users-checkbox']//following-sibling::label/span")
        self.report_for_p1p2 = (By.XPATH, "//div[contains(@data-bind,'reportPermission')]//label/span[.='"+UserData.report_for_p1p2+"']")
        self.manage_shared_exports = (By.XPATH, "//input[@id='edit-shared-exports-checkbox']")
        self.data_checkbox = (By.XPATH, "//input[@id='edit-data-checkbox']")

        self.report_for_p1p2 = (By.XPATH, "//div[contains(@data-bind,'reportPermission')]//label[./span[.='"+UserData.report_for_p1p2+"']]")
        self.role_renamed = (By.XPATH, "//span[text()='" + str(self.role_rename_created) + "']")
        self.role_non_admin = (By.XPATH, "//span[text()='" + str(self.role_non_admin_created) + "']")
        self.role_no_shared_export = "//span[text()='{}']"
        self.confirm_role_delete = (By.XPATH, "//div[@class='btn btn-danger']")
        self.full_org_access_checkbox = (By.XPATH, "//label[contains(.,'Full Organization Access')]//following-sibling::div//input")
        self.access_all_reports_checkbox = (By.XPATH, "//input[@id='access-all-reports-checkbox']")
        self.edit_data = (By.XPATH, "//div[@id='user-roles-table']/div[@class='panel-body']/div[@class='modal fade in']/div[@class='modal-dialog']/form/div[@class='modal-content']/div[@class='modal-body']/div[@class='form form-horizontal']/fieldset/div[3]/div[@class='form-group'][7]/div[@class='col-sm-2 controls'][1]/div[@class='form-check']/label")
        self.view_data_dictionary = (By.XPATH, "//input[@id='view-data-dict-checkbox']")
        self.edit_data_dictionary = (By.XPATH, "//input[@id='edit-data-dict-checkbox']")
        self.edit_data = (By.XPATH, "//input[@id='edit-data-checkbox']")
        self.view_data_dictionary = (By.XPATH, "//input[@id='view-data-dict-checkbox']")
        self.edit_data_dictionary = (By.XPATH, "//input[@id='edit-data-dict-checkbox']")

        self.web_user_permission = "//th[./span[.='{}']]//following-sibling::td/div[contains(@data-bind,'edit_web_users')]/i[contains(@class,'check')]"
        self.mobile_worker_permission = "//th[./span[.='{}']]//following-sibling::td/div[contains(@data-bind,'edit_commcare_users')]/i[contains(@class,'check')]"
        self.managed_shared_export_permission = "//th[./span[.='{}']]//following-sibling::td/div[contains(@data-bind,'edit_shared_exports')]/i[contains(@class,'check')]"

    def roles_menu_click(self):
        self.wait_to_click(self.roles_menu)
        assert "Roles & Permissions : Users :: - CommCare HQ" in self.driver.title

    def add_role(self):
        self.wait_to_click(self.add_new_role)
        self.wait_to_clear_and_send_keys(self.role_name, self.role_name_created)
        self.js_click(self.edit_web_user_checkbox)
        self.scroll_to_element(self.save_button)
        time.sleep(0.5)
        self.wait_to_click(self.save_button)

        assert self.is_present_and_displayed(self.role_created), "Role not added successfully!"

    def edit_role(self):
        self.wait_to_click(self.edit_created_role)
        self.wait_to_clear_and_send_keys(self.role_name, self.role_rename_created)
        self.js_click(self.edit_mobile_worker_checkbox)
        self.scroll_to_element(self.save_button)
        time.sleep(0.5)
        self.wait_to_click(self.save_button)

        assert self.is_present_and_displayed(self.role_renamed), "Role not edited successfully!"


    def cleanup_role(self):
        self.wait_to_click(self.delete_role)
        self.wait_to_click(self.confirm_role_delete)

    def delete_test_roles(self):
        list_profile = self.driver.find_elements(By.XPATH, "//th[.//span[contains(text(),'role_')]]")
        print(list_profile)
        try:
            if len(list_profile) > 0:
                for i in range(len(list_profile))[::-1]:
                    text = list_profile[i].text
                    print(text)
                    self.driver.find_element(By.XPATH,
                                             "(//th[.//span[contains(text(),'role_')]]//following-sibling::td//button[@class='btn btn-danger'])[" + str(
                                                 i + 1) + "]").click()
                    self.wait_to_click(self.confirm_role_delete)

                    list_profile = self.driver.find_elements(By.XPATH, "//th[.//span[contains(text(),'role_')]]")
            else:
                print("There are no test roles")
        except ElementNotInteractableException:
            menu = HomePage(self.driver, self.settings)
            webuser = WebUsersPage(self.driver)
            menu.users_menu()
            webuser.edit_user_permission("Admin")
            menu.users_menu()
            self.roles_menu_click()
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

                   list_profile = self.driver.find_elements(By.XPATH, "//th[.//span[contains(text(),'role_')]]")
               else:
                   print("There are no test roles")



    def add_non_admin_role(self):
        self.wait_to_click(self.add_new_role)
        self.wait_to_clear_and_send_keys(self.role_name, self.role_non_admin_created)
        self.wait_to_clear_and_send_keys(self.role_name, self.role_non_admin_created)
        self.wait_for_element(self.role_name)
        self.send_keys(self.role_name, self.role_non_admin_created)
        self.wait_to_click(self.edit_mobile_worker_checkbox)
        self.scroll_to_element(self.access_all_reports_checkbox)
        is_checked = self.get_attribute(self.access_all_reports_checkbox, 'checked')
        print("All report access checked ", is_checked)
        if is_checked == True:
            self.wait_to_click(self.access_all_reports_checkbox)
            assert self.get_attribute(self.access_all_reports_checkbox, 'checked') == False, "Access is checked"
        else:
            assert True
        self.scroll_to_element(self.report_for_p1p2)
        time.sleep(0.5)
        self.js_click(self.report_for_p1p2)
        is_checked = self.get_attribute(self.full_org_access_checkbox, 'checked')
        print("All report access checked ", is_checked)
        if is_checked == True:
            self.wait_to_click(self.full_org_access_checkbox)
            assert self.get_attribute(self.full_org_access_checkbox, 'checked') == False, "Access is checked"
        else:
            assert True
        self.scroll_to_element(self.save_button)
        time.sleep(0.5)
        self.wait_to_click(self.save_button)

        assert self.is_present_and_displayed(self.role_non_admin), "Role not added successfully!"
        return self.role_non_admin_created

    def add_non_admin_role_dd(self, value):
        self.wait_to_click(self.add_new_role)
        self.wait_to_clear_and_send_keys(self.role_name, self.role_non_admin_created)
        time.sleep(1)
        self.click(self.edit_data,5)
        self.click(self.view_data_dictionary)
        if value == 1:
            print("only view access selected")
        elif value ==2:
            time.sleep(5)
            self.click(self.edit_data_dictionary)
        else:
            self.click(self.view_data_dictionary)
            self.click(self.edit_data_dictionary)
            self.click(self.edit_data_dictionary)
        print("Role added successfully")
        return self.role_non_admin_created


    def add_shared_export_role(self, name, flag='NO'):
        self.wait_to_click(self.add_new_role)
        self.wait_to_clear_and_send_keys(self.role_name, name)
        time.sleep(1)
        self.click(self.edit_mobile_worker_checkbox)
        time.sleep(0.5)
        self.click(self.edit_web_user_checkbox)
        time.sleep(0.5)
        self.click(self.data_checkbox)
        time.sleep(0.5)
        self.scroll_to_element(self.manage_shared_exports)
        if flag == 'YES':
            time.sleep(2)
            self.click(self.manage_shared_exports)
            time.sleep(2)
        time.sleep(0.5)
        self.scroll_to_element(self.access_all_reports_checkbox)
        time.sleep(1)
        self.click(self.access_all_reports_checkbox)
        time.sleep(0.5)
        self.scroll_to_element(self.save_button)
        time.sleep(0.5)
        self.click(self.save_button)
        time.sleep(2)
        return self.role_non_admin_created
        assert self.is_present_and_displayed((By.XPATH, self.role_no_shared_export.format(name))), "Role not added successfully!"
        assert self.is_present_and_displayed((By.XPATH, self.web_user_permission.format(name))), "Web User Permission not present"
        assert self.is_present_and_displayed((By.XPATH, self.mobile_worker_permission.format(name))), "Mobile Worker Permission not present"
        if flag == "NO":
            assert not self.is_present_and_displayed((By.XPATH, self.managed_shared_export_permission.format(name)), 5), "Shared Export Permission is present"
        else:
            assert self.is_present_and_displayed((By.XPATH, self.managed_shared_export_permission.format(name))), "Shared Export Permission not present"
        return self.role_non_admin_created
