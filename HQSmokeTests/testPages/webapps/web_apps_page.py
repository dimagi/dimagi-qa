import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from common_utilities.selenium.base_page import BasePage
from common_utilities.generate_random_string import fetch_random_string, fetch_random_digit
from HQSmokeTests.userInputs.user_inputs import UserData


""""Contains test page elements and functions related to the Webapps navigation and form submissions"""


class WebAppsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.case_name_created = "case_" + fetch_random_string()
        self.text_value = "text_" + fetch_random_string()
        self.random_value = fetch_random_digit()

        self.login_as_css = (By.CLASS_NAME, "js-restore-as-item")
        self.login_user = (By.XPATH, "//*[text()='" + UserData.login_as + "']")
        self.confirm_user_login = (By.XPATH, "//button[@id='js-confirmation-confirm']")
        self.sync_button = (By.XPATH, "//h3[.='Sync']")
        self.home_button = (By.XPATH, "//li[contains(@class,'home')]")
        self.apps_links = (By.XPATH, "//*[@class='fcc fcc-flower appicon-icon']")
        self.web_app_link = (By.XPATH, "//*[text()='" + UserData.reassign_cases_application + "']")
        self.case_list_link = (By.XPATH, "//*[text()='" + UserData.case_list_name + "']")
        self.update_case_change_link = (By.XPATH, "//*[text()='" + UserData.update_case_change_link + "']")
        self.case_register_form = (By.XPATH, "//*[text()='" + UserData.case_register_form + "']")
        self.case_update_form = (By.XPATH, "//*[text()='" + UserData.case_update_form + "']")
        self.enter_text_area = (By.XPATH, "//label[./div[./span[contains(text(),'Enter text')]]]/following-sibling::div[@data-bind='css: controlWidth']//div/textarea")
        self.enter_value_area = (By.XPATH, "//label[./div[./span[contains(text(),'Enter a random value')]]]/following-sibling::div[@data-bind='css: controlWidth']//div/textarea")
        self.update_value_area = (By.XPATH, "//label[./div[./span[contains(text(),'Update')]]]/following-sibling::div[@data-bind='css: controlWidth']//div/textarea")
        self.form_link = (By.XPATH, "//*[text()='" + UserData.form_name + "']")
        self.form_case_name_input = (By.XPATH, "//textarea[contains(@class,'textfield form-control')]")
        self.form_submit_button = (By.XPATH, "//div[contains(@id,'submit')]//button[contains(@class,'submit')]")
        self.success_message = (By.XPATH, "//p[contains(text(),'successfully saved')]")
        self.show_full_menu_link = (By.LINK_TEXT, "Show Full Menu")
        self.search_text = (By.XPATH, "//input[@id='searchText']")
        self.search_button = (By.XPATH, "//button[@id='case-list-search-button']")
        self.case_searched_link = (By.XPATH, "//table//tbody//td[contains(text(),'"+self.text_value+"')]")
        self.select_case = (By.ID, "select-case")
        self.this_case = (By.XPATH, "//a[.='this case']")

    def verify_apps_presence(self):
        clickable = ec.presence_of_all_elements_located(self.apps_links)
        element = WebDriverWait(self.driver, 10).until(clickable, message="Couldn't find locator: "
                                                                          + str(self.apps_links))
        count = len(element)
        if count >= 1:
            print(count, " Web apps are present in the page")
            return True
        else:
            print("No web apps are present")
            return False

    def login_as(self):
        self.wait_to_click(self.login_as_css)
        self.wait_to_click(self.login_user)
        self.wait_to_click(self.confirm_user_login)

    def submit_case_form(self):
        self.wait_to_click(self.web_app_link)
        self.wait_to_click(self.case_list_link)
        self.wait_to_click(self.form_link)
        self.wait_to_clear_and_send_keys(self.form_case_name_input, self.case_name_created)
        self.wait_to_click(self.form_submit_button)
        self.wait_for_element(self.success_message)
        assert self.is_displayed(self.success_message), "Form not submitted"
        print("Form successfully submitted")
        time.sleep(2)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.wait_for_element(self.sync_button)
        self.wait_to_click(self.sync_button)
        time.sleep(2)
        self.driver.refresh()
        return self.case_name_created

    def submit_case_change_register_form(self):
        self.wait_to_click(self.web_app_link)
        self.wait_for_element(self.web_app_link)
        self.wait_to_click(self.web_app_link)
        self.wait_for_element(self.update_case_change_link)
        self.wait_to_click(self.update_case_change_link)
        self.wait_for_element(self.case_register_form)
        self.wait_to_click(self.case_register_form)
        self.wait_to_clear_and_send_keys(self.enter_text_area, self.text_value)
        self.wait_to_clear_and_send_keys(self.enter_value_area, self.text_value+Keys.TAB)
        self.wait_to_click(self.form_submit_button)
        self.wait_after_interaction()
        time.sleep(2)
        self.wait_for_element(self.success_message)
        assert self.is_displayed(self.success_message), "Form not submitted"
        print("Form successfully submitted")
        return self.text_value

    def submit_case_update_form(self, case_name):
        self.driver.refresh()
        self.wait_to_click(self.update_case_change_link)
        self.wait_to_click(self.case_update_form)
        self.wait_to_clear_and_send_keys(self.search_text, case_name)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        self.wait_to_click(self.case_searched_link)
        self.wait_to_click(self.select_case)
        
        self.wait_to_clear_and_send_keys(self.update_value_area, self.random_value+Keys.TAB)
        self.wait_to_click(self.form_submit_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        assert self.is_displayed(self.success_message), "Form not submitted"
        print("Form successfully submitted")
        # self.wait_to_click(self.show_full_menu_link)
        return self.random_value

    def click_case_link(self):
        case_link = self.get_attribute(self.this_case, "href")
        self.driver.get(case_link)
