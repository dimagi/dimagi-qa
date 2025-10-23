
import time
from selenium.webdriver.common.by import By
from Features.FindDataById.userInputs.user_inputs import UserData
from common_utilities.selenium.base_page import BasePage


""""Contains test page elements and functions related to the Lookup Table module"""

class FindIdPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        #FindDataById
        self.find_data_by_id= (By.LINK_TEXT, "Find Data by ID")
        self.find_id= "//*[@placeholder='{} ID']"
        self.find_button = "//fieldset[@id='find-{}']/div[@class='form-group']/div[@class='col-sm-8 col-md-9']/button[@class='btn btn-primary']"
        self.error_message ="//div[contains(text(),'Could not find {}')]"
        self.export_link = "//a[normalize-space()='{} data export']"
        self.export_page ="//h1[normalize-space()='Export {} Data']"
        self.case_id_found = (By.XPATH,"//a[normalize-space()='View']")
        self.view = "//fieldset[@id='{}']//a[contains(text(),'View')]"
        self.location_name = (By.XPATH,"//p[@class='lead' and contains(text(),' Test Location [DO NOT DELETE!!!]')]")

        # Find_Data_By_Id_Form_Level
        self.case_change = (By.XPATH, "//a[normalize-space()='Case Changes']")
        self.form_metadata = (By.XPATH, "//a[normalize-space()='Form Metadata']")
        self.form_properties = (By.XPATH, "//a[normalize-space()='Form Properties']")
        self.properties = "//a[normalize-space()='{}']"
        self.id_values = "//dt[@title='{}']//following-sibling::dd[1]"
        self.view_button = (By.XPATH, "//a[normalize-space()='View']")


    def find_data_by_id_page_ui(self):
        self.wait_to_click(self.find_data_by_id)
        self.is_present_and_displayed((By.XPATH,self.find_id.format('Case')))
        self.is_present_and_displayed((By.XPATH,self.find_id.format('Form Submission')))
        assert True, "Find case and Find Forms fields are displayed"

    def search_invalid_ids(self,type1):
        if type1 =='case':
            self.is_present_and_displayed((By.XPATH, self.find_id.format('Case')))
            self.wait_to_clear_and_send_keys((By.XPATH,self.find_id.format('Case')),UserData.invalid_id)
            self.js_click((By.XPATH,self.find_button.format('case')))
            self.is_present_and_displayed((By.XPATH,self.error_message.format('case')))
            assert True, "Could not find case submission"
        elif type1 == 'form':
            self.is_present_and_displayed((By.XPATH, self.find_id.format('Form Submission')))
            self.wait_to_clear_and_send_keys((By.XPATH,self.find_id.format('Form Submission')),UserData.invalid_id)
            self.js_click((By.XPATH, self.find_button.format('form')))
            self.is_present_and_displayed((By.XPATH,self.error_message.format('form submission')))
            assert True, "Could not find form submission"

    def verify_data_exports_link(self,value):
        if value == 'case':
            self.js_click((By.XPATH, self.export_link.format(value)))
            self.is_present_and_displayed((By.XPATH,self.export_page.format(str(value).capitalize())))
            assert True, "Case export page opened"
        elif value =='form':
            self.js_click((By.XPATH, self.export_link.format(value)))
            self.is_present_and_displayed((By.XPATH,self.export_page.format(str(value).capitalize())))
            assert True, "Form export page opened"



    def validate_location_ids(self, value_type):
        if value_type == "case":
            self.click((By.XPATH,self.find_id.format('Case')))
            url = self.get_current_url()
            if "staging" in url:
                self.send_keys((By.XPATH, self.find_id.format('Case')), str(UserData.user_details['staging'][1]))
            else:
                self.send_keys((By.XPATH, self.find_id.format('Case')), str(UserData.user_details['prod'][1]))
            self.js_click((By.XPATH, self.find_button.format(value_type)))
        elif value_type == "form":
            self.click((By.XPATH, self.find_id.format('Form Submission')))
            url = self.get_current_url()
            if "staging" in url:
                self.send_keys((By.XPATH, self.find_id.format('Form Submission')),str(UserData.user_details['staging'][1]))
            else:
                self.send_keys((By.XPATH, self.find_id.format('Form Submission')),str(UserData.user_details['prod'][1]))
            self.js_click((By.XPATH, self.find_button.format(value_type)))
        self.js_click(self.view_button)
        time.sleep(10)
        url = self.get_current_url()
        if "staging" in url:
            self.page_source_contains(UserData.user_details['staging'][1])
            assert True,("Correct location page is opened in staging environment for" ,value_type ,"field search ")
        else:
            self.page_source_contains(UserData.user_details['prod'][1])
            assert True,("Correct location page is opened in production environment for" ,value_type ,"field search ")
        self.driver.back()


    def validate_web_user_ids(self, value_type):
        if value_type == "case":
            self.click((By.XPATH, self.find_id.format('Case')))
            url = self.get_current_url()
            if "staging" in url:
                self.send_keys((By.XPATH, self.find_id.format('Case')), str(UserData.user_details['staging'][0]))
            else:
                self.send_keys((By.XPATH, self.find_id.format('Case')), str(UserData.user_details['prod'][0]))
            self.js_click((By.XPATH, self.find_button.format(value_type)))
        elif value_type == "form":
            self.click((By.XPATH, self.find_id.format('Form Submission')))
            url = self.get_current_url()
            if "staging" in url:
                self.send_keys((By.XPATH, self.find_id.format('Form Submission')), str(UserData.user_details['staging'][0]))
            else:
                self.send_keys((By.XPATH, self.find_id.format('Form Submission')), str(UserData.user_details['prod'][0]))
            self.js_click((By.XPATH, self.find_button.format(value_type)))
        self.js_click(self.view_button)
        url = self.get_current_url()
        if "staging" in url:
            self.page_source_contains(UserData.user_details['staging'][0])
            assert True,("Correct web user page is opened in staging environment for" ,value_type ,"field search ")
        else:
            self.page_source_contains(UserData.user_details['prod'][0])
            assert True,("Correct web user page is opened in production environment for" ,value_type ,"field search ")
        self.driver.back()

    def validate_group_ids(self, value_type):
        if value_type == "case":
            self.click((By.XPATH,self.find_id.format('Case')))
            url = self.get_current_url()
            if "staging" in url:
                self.send_keys((By.XPATH, self.find_id.format('Case')), str(UserData.user_details['staging'][2]))
            else:
                self.send_keys((By.XPATH, self.find_id.format('Case')), str(UserData.user_details['prod'][2]))
            self.js_click((By.XPATH, self.find_button.format(value_type)))
        elif value_type == "form":
            self.click((By.XPATH,self.find_id.format('Form Submission')))
            url = self.get_current_url()
            if "staging" in url:
                self.send_keys((By.XPATH, self.find_id.format('Form Submission')), str(UserData.user_details['staging'][2]))
            else:
                self.send_keys((By.XPATH, self.find_id.format('Form Submission')), str(UserData.user_details['prod'][2]))
            self.js_click((By.XPATH, self.find_button.format(value_type)))
        self.js_click(self.view_button)
        url = self.get_current_url()
        if "staging" in url:
            self.page_source_contains(UserData.user_details['staging'][2])
            assert True,("Correct group page is opened in staging environment for" ,value_type ,"field search ")
        else:
            self.page_source_contains(UserData.user_details['prod'][2])
            assert True,("Correct group page is opened in production environment for" ,value_type ,"field search ")


    def validate_case_form_input_id(self, value_type,value):
        if value_type == "case":
            print("case id value", value)
            self.click((By.XPATH, self.find_id.format('Case')))
            self.wait_to_clear_and_send_keys((By.XPATH, self.find_id.format('Case')),value )
            self.wait_to_click((By.XPATH, self.find_button.format('case')), 2)
        elif value_type == "form":
            print("form  id value",value)
            self.click((By.XPATH, self.find_id.format('Form Submission')))
            self.wait_to_clear_and_send_keys((By.XPATH, self.find_id.format('Form Submission')),
                                             value)
            self.wait_to_click((By.XPATH, self.find_button.format('form')), 2)
        self.is_present_and_displayed(self.case_id_found)
        time.sleep(10)
        self.wait_to_click(self.view_button)
        self.page_source_contains(value)
        assert True,("Correct ",value_type,"id page is opened")
        self.driver.back()






