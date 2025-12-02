
import time
from selenium.webdriver.common.by import By
from Features.FindDataById.userInputs.user_inputs import UserData
from common_utilities.selenium.base_page import BasePage


""""Contains test page elements and functions related to the Lookup Table module"""

class FindDataPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        #FindDataById
        self.find_data_by_id= (By.LINK_TEXT, "Find Data by ID")
        self.find_id= "//*[@placeholder='{} ID']"
        self.find_button = "//fieldset[@id='find-{}']//button[@type='button'][normalize-space()='Find']"
        self.error_message ="//div[contains(text(),'Could not find {}')]"
        self.export_link = "//a[normalize-space()='{} data export']"
        self.export_page ="//h1[normalize-space()='Export {} Data']"
        self.case_id_found = (By.XPATH,"//a[normalize-space()='View']")
        self.view = "//fieldset[@id='{}']//a[contains(text(),'View')]"

        # Find_Data_By_Id_Form_Level
        self.case_change = (By.XPATH, "//a[normalize-space()='Case Changes']")
        self.form_metadata = (By.XPATH, "//a[normalize-space()='Form Metadata']")
        self.form_properties = (By.XPATH, "//a[normalize-space()='Form Properties']")
        self.properties = "//a[normalize-space()='{}']"
        self.id_values = "//dt[@title='{}']//following-sibling::dd[1]"
        self.view_button = (By.XPATH, "//a[normalize-space()='View']")


    def find_data_by_id_page_ui(self):
        self.wait_to_click(self.find_data_by_id)
        assert self.is_present_and_displayed((By.XPATH,self.find_id.format('Case'))) , "find case field is displayed"
        assert self.is_present_and_displayed((By.XPATH,self.find_id.format('Form Submission'))) ,"find form submission field is displayed"

    def search_invalid_ids(self,submission_type):
        if submission_type =='case':
            self.is_present_and_displayed((By.XPATH, self.find_id.format('Case')))
            self.wait_to_clear_and_send_keys((By.XPATH,self.find_id.format('Case')),UserData.invalid_id)
            self.js_click((By.XPATH,self.find_button.format('case')))
            assert self.is_present_and_displayed((By.XPATH,self.error_message.format('case')))
            "Could not find case submission"
        elif submission_type == 'form':
            self.is_present_and_displayed((By.XPATH, self.find_id.format('Form Submission')))
            self.wait_to_clear_and_send_keys((By.XPATH,self.find_id.format('Form Submission')),UserData.invalid_id)
            self.js_click((By.XPATH, self.find_button.format('form')))
            assert self.is_present_and_displayed((By.XPATH,self.error_message.format('form submission')))
            "Could not find form submission"

    def verify_data_exports_link(self,value):
        if value == 'case':
            self.js_click((By.XPATH, self.export_link.format(value)))
            assert self.is_present_and_displayed((By.XPATH,self.export_page.format(str(value).capitalize())))
            "Case export page opened"
        elif value =='form':
            self.js_click((By.XPATH, self.export_link.format(value)))
            assert self.is_present_and_displayed((By.XPATH,self.export_page.format(str(value).capitalize())))
            "Form export page opened"


    def validate_web_user_location_group_data_pages(self,value_type,id_type,case_data=None):
        id_map = {
            "web_user": 0,
            "location": 1,
            "group": 2
        }
        if id_type not in id_map:
            raise ValueError(f"Invalid id_type '{id_type}'. Must be one of {list(id_map.keys())}.")
        value = "Case" if value_type == "case" else "Form Submission"
        url = self.get_current_url()
        env = "staging" if "staging" in url else "prod"
        user_id = str(UserData.user_details[env][id_map[id_type]]) if case_data is None else case_data
        self.click((By.XPATH, self.find_id.format(value)))
        self.send_keys((By.XPATH, self.find_id.format(value)), user_id)
        self.js_click((By.XPATH, self.find_button.format(value_type)))
        text = self.get_attribute(self.view_button, "href")
        print(text)
        assert user_id in text, f"{user_id} not found in URL: {text}"
        print(f"[PASS] {id_type} ID '{user_id}' is present in {text}")
        self.js_click(self.view_button)
        time.sleep(5)
        self.switch_to_next_tab()
        time.sleep(5)
        current_url = self.get_current_url()
        assert user_id in current_url, f"{user_id} not found in new tab URL: {current_url}"
        print(f"[PASS] {id_type} ID '{user_id}' is present in new tab URL {current_url}")
        self.driver.close()
        time.sleep(2)
        self.switch_back_to_prev_tab()


