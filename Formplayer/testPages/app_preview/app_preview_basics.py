import time

from Formplayer.testPages.webapps.webapps_basics import WebAppsBasics
from common_utilities.generate_random_string import fetch_random_string, fetch_phone_number
from common_utilities.selenium.base_page import BasePage
from Formplayer.userInputs.user_inputs import UserData

from selenium.webdriver.common.by import By


""""Contains test page elements and functions related to the WebApps Access/Basics of Commcare"""

class AppPreviewBasics(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.webapp = WebAppsBasics(self.driver)
        
        self.name_input = "name " + fetch_random_string()
        self.test_question = "Test " + fetch_random_string()

        self.application_menu_id = (By.LINK_TEXT, "Applications")
        self.select_test_application = (By.LINK_TEXT, UserData.test_app)
        self.form_builder_registration_form = (By.LINK_TEXT, "Registration Form")
        self.form_builder_follow_up_form = (By.LINK_TEXT, "Followup Form")
        self.add_question = (By.LINK_TEXT, "Add Question")
        self.text_question_type = (By.XPATH, "//a[@data-qtype = 'Text']")
        self.text_question_display_text = (By.XPATH, "//div[@name = 'itext-en-label']")
        self.save_question_button = (By.XPATH, "//span[contains(text(), 'Save')]")
        self.add_new_menu = (By.LINK_TEXT, "Add...")
        self.add_new_form = (By.XPATH, "//*[@class='appnav-secondary js-add-new-item']/i[@class='fa fa-plus']")
        self.add_new_reg_form = (By.XPATH, "//button[@class='popover-additem-option js-new-form appnav-responsive'][./i[@class='fcc fcc-app-createform']]")

        self.view_app_preview = (By.XPATH, "//i[@class ='fa fa-chevron-left js-preview-action-show']")
        self.view_app_preview_show = (By.XPATH, "//i[@class ='fa fa-chevron-left js-preview-action-show hide']")
        self.app_preview_window = (By.XPATH, "//i[@class ='preview-phone-container']")
        self.app_preview_view = (By.XPATH, "//div[@id='js-appmanager-preview']")
        self.tablet = (By.XPATH, "//div[contains(@class,'open preview-tablet-mode small-height')]")
        self.phone = (By.XPATH, "//div[contains(@class,'open small-height')]")
        self.back_button = (By.XPATH, "//i[@class ='fa fa-chevron-left']")
        self.form_list = (By.XPATH, "//tbody[@class='menus-container']")
        self.refresh_button = (By.XPATH, "//button[contains(@class,'btn-preview-refresh js-preview-refresh')]")
        self.toggle_button = "//button[contains(@class ,'js-preview-toggle-tablet-view')]/i[{}]"
        self.start_option = (By.XPATH, "//div[@class= 'js-start-app appicon appicon-start']")
        self.settings_option = (By.XPATH, "//div[@class = 'js-settings appicon appicon-settings']/i")
        self.login_as_option = (By.XPATH, "//div[@class='js-restore-as-item appicon appicon-restore-as']")
        self.case_list_menu = (By.XPATH, "//h3[contains(text(), 'Case List')]")
        self.registration_form = (By.XPATH, "//h3[contains(text(), 'Registration Form')]")
        self.followup_form = (By.XPATH, "//h3[contains(text(), 'Followup Form')]")
        self.name_question = (By.XPATH, "//label[.//span[.='Name']]/following-sibling::div//textarea[contains(@class,'textfield form-control')]")
        self.dob_question = (By.XPATH,
                             "//label[.//span[.='DOB']]/following-sibling::div//input[contains(@id,'date')]")
        self.click_today_date = (By.XPATH, "//div[@data-action='today']/i[contains(@class,'check')]")
        self.close_date_picker = (By.XPATH, "//div[@data-action='close']/i[contains(@class,'xmark')]")
        self.mobileno_question = (By.XPATH, "//label[.//span[text()='Mobile No.']]/following-sibling::div//input")
        self.submit_form_button = (By.XPATH, "//button[contains(@data-bind,'submitForm')]")
        self.multi_question_submit_button = (By.XPATH, "//button[contains(@data-bind,'SubmitButton')]")
        self.new_test_question = (By.XPATH, "//label[.//span[text()='"+self.test_question+"']]")
        self.formplayer_test_question = (By.XPATH, "//a[.//text()='"+self.test_question+"']")
        self.delete_button = (By.XPATH, "//button[@class='btn btn-danger fd-button-remove']")
        self.turn_on_one_question_toggle_button = (By.XPATH, "//div[contains(@class,'bootstrap-switch-on')]")
        self.turn_off_one_question_toggle_button = (By.XPATH, "//div[contains(@class,'bootstrap-switch-off')]")
        self.toggle_button_one_question = (By.XPATH, "//div[contains(@class,'form-switch')]/input")
        self.done_button = (By.XPATH, "//button[@class = 'btn btn-primary js-done']")
        self.clear_user_data_button = (By.XPATH, "//button[text()='Clear']")
        self.clear_data_message = (By.XPATH, "//div[text()='User data successfully cleared.']")
        self.language_option = (By.XPATH, "//select[@class='form-control js-lang']")
        self.select_language = (By.XPATH, "//th[contains(text(),'application language')]/following-sibling::td/select")
        self.empty_form_error_message = (By.XPATH, "//div[@class='alert alert-warning alert-build']//strong[contains(.,'Add a question')]")
        self.next_question = (By.XPATH, "//button[contains(@data-bind,'nextQuestion')]")
        self.complete_form = (By.XPATH, "//button[@data-bind='visible: atLastIndex(), click: submitForm']")
        self.success_message = (By.XPATH, "//p[contains(text(),'successfully saved')]")
        self.view_form_link = (By.LINK_TEXT, "this form")
        self.export_form_link = (By.LINK_TEXT, "form")
        self.last_form = (By.XPATH, "(//ul[contains(@class,'appnav-menu-nested')]//div[contains(@class,'appnav-item')])[last()]")
        self.delete_form = (By.XPATH, "(//div[contains(@class,'appnav-item')]/a[@class='appnav-delete']/i)[last()]")
        self.delete_confirm_button = (By.XPATH, "(//text()[contains(.,'Delete Form')]//preceding-sibling::i[contains(@class,'fa-trash')])[last()]")
        self.question_display_text = (By.XPATH, "//span[text()='Name (es)']")
        self.iframe = (By.CLASS_NAME, "preview-phone-window")
        self.home_button = (By.XPATH, "//li[contains(@class,'home')]/a")
        self.full_menu = (By.LINK_TEXT, "Show Full Menu")
        self.submitted_name = (By.XPATH, "//td[@title='"+self.name_input+"']")


    def verify_toggle_functionality(self):
        mode = self.get_attribute(self.app_preview_view, 'class')
        print(mode)
        if 'preview-tablet-mode' in mode:
            print("Preview is in Tablet View")
            self.wait_to_click((By.XPATH, self.toggle_button.format(2)))
            
            mode = self.get_attribute(self.app_preview_view, 'class')
            print(mode)
            assert 'preview-tablet-mode' not in mode, "Preview mode changed to Phone View"
        else:
            print("Preview is in Phone View")
            self.wait_to_click((By.XPATH, self.toggle_button.format(1)))
            
            mode = self.get_attribute(self.app_preview_view, 'class')
            print(mode)
            assert 'preview-tablet-mode' in mode, "Preview mode changed to Tablet View"
            self.wait_to_click((By.XPATH, self.toggle_button.format(2)))
            
            mode = self.get_attribute(self.app_preview_view, 'class')
            print(mode)
            assert 'preview-tablet-mode' not in mode, "Preview mode changed to Phone View"


    def icons_are_present(self):
        self.switch_to_frame(self.iframe)
        self.webapp.wait_to_click(self.start_option)
        self.wait_for_element(self.form_list)
        self.switch_to_default_content()
        assert self.is_present_and_displayed(self.back_button)
        print("back button")
        assert self.is_present_and_displayed(self.refresh_button), "Refresh button is not present"
        print("refesh button")
        assert self.is_present_and_displayed((By.XPATH, self.toggle_button.format(1))), "Toggle button is not present"
        self.switch_to_default_content()

    def back_button_functionality(self):
        self.switch_to_frame(self.iframe)
        self.webapp.wait_to_click(self.start_option)
        self.wait_for_element(self.form_list)
        assert not self.is_present_and_displayed(self.start_option)
        
        self.switch_to_default_content()
        self.webapp.wait_to_click(self.back_button)
        self.switch_to_frame(self.iframe)
        assert self.is_present_and_displayed(self.start_option)
        print("Back button works!!")
        self.switch_to_default_content()


    def refresh_button_functionality_01(self):
        self.switch_to_frame(self.iframe)
        self.webapp.wait_to_click(self.start_option)
        self.webapp.wait_to_click(self.case_list_menu)
        self.switch_to_default_content()
        time.sleep(2)
        self.webapp.wait_to_click(self.refresh_button)
        time.sleep(3)
        self.switch_to_frame(self.iframe)
        assert self.is_present_and_displayed(self.start_option)
        print("Refresh Button works!!")
        self.switch_to_default_content()

    def refresh_button_functionality_02(self):
        self.webapp.wait_to_click(self.form_builder_registration_form)
        self.webapp.wait_to_click(self.add_question)
        self.webapp.wait_to_click(self.text_question_type)
        time.sleep(2)
        self.wait_to_clear_and_send_keys(self.text_question_display_text, self.test_question)
        self.webapp.wait_to_click(self.save_question_button)
        self.webapp.wait_to_click(self.refresh_button)
        self.switch_to_frame(self.iframe)
        self.webapp.wait_to_click(self.start_option)
        self.webapp.wait_to_click(self.case_list_menu)
        self.webapp.wait_to_click(self.registration_form)
        self.wait_to_clear_and_send_keys(self.name_question, self.name_input)
        self.wait_to_click(self.next_question)
        assert self.is_present_and_displayed(self.new_test_question)
        self.switch_to_default_content()
        time.sleep(3)
        self.webapp.wait_to_click(self.formplayer_test_question)
        self.webapp.wait_to_click(self.delete_button)
        self.webapp.wait_to_click(self.save_question_button)
        time.sleep(3)
        self.webapp.wait_to_click(self.refresh_button)
        self.switch_to_frame(self.iframe)
        self.webapp.wait_to_click(self.start_option)
        self.webapp.wait_to_click(self.case_list_menu)
        self.webapp.wait_to_click(self.registration_form)
        self.wait_to_clear_and_send_keys(self.name_question, self.name_input)
        self.wait_to_click(self.next_question)
        assert not self.is_present_and_displayed(self.new_test_question)
        print("Refresh button works!!")
        self.switch_to_default_content()

    def web_user_submission(self):
        self.switch_to_frame(self.iframe)
        self.webapp.wait_to_click(self.start_option)
        self.webapp.wait_to_click(self.case_list_menu)
        self.webapp.wait_to_click(self.registration_form)
        self.wait_to_clear_and_send_keys(self.name_question, self.name_input)
        self.wait_to_click(self.next_question)
        
        self.wait_for_element(self.dob_question)
        self.click(self.dob_question)
        self.wait_to_click(self.click_today_date)
        
        # if self.is_present(self.close_date_picker):
        #     self.wait_to_click(self.close_date_picker)
        # else:
        #     print("No calender opened")
        self.wait_to_click(self.next_question)
        
        self.wait_to_clear_and_send_keys(self.mobileno_question, fetch_phone_number())
        self.wait_to_click(self.next_question)
        
        self.wait_to_click(self.submit_form_button)
        
        self.wait_for_element(self.success_message)
        assert self.is_present_and_displayed(self.success_message)
        assert self.is_present_and_displayed(self.view_form_link)
        assert self.is_present_and_displayed(self.export_form_link)
        self.webapp.wait_to_click(self.view_form_link)
        time.sleep(4)
        self.switch_to_default_content()
        self.switch_to_next_tab()
        print(self.name_input)
        assert self.is_present_and_displayed(self.submitted_name)
        self.driver.close()
        self.switch_back_to_prev_tab()

    def one_question_per_screen_negative(self):
        self.switch_to_frame(self.iframe)
        self.webapp.wait_to_click(self.start_option)
        self.webapp.wait_to_click(self.case_list_menu)
        self.webapp.wait_to_click(self.registration_form)
        assert self.is_present_and_displayed(self.name_question)
        self.wait_to_clear_and_send_keys(self.name_question, self.name_input)
        self.webapp.wait_to_click(self.next_question)
        assert self.is_present_and_displayed(self.dob_question)
        self.click(self.dob_question)
        self.wait_for_element(self.click_today_date)
        self.wait_to_click(self.click_today_date)
        
        self.webapp.wait_to_click(self.next_question)
        assert self.is_present_and_displayed(self.mobileno_question)
        self.switch_to_default_content()

    def one_question_per_screen_positive(self):
        self.switch_to_frame(self.iframe)
        self.webapp.wait_to_click(self.settings_option)
        
        isChecked = self.is_selected(self.toggle_button_one_question)
        print(isChecked)
        
        if isChecked is True:
            # self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.XPATH, "//th[(text()='Use one question per screen')]/following-sibling::td//input"))
            self.wait_to_click(self.toggle_button_one_question)
            
            print("Toggled OFF")
        # self.webapp.wait_to_click((By.XPATH, "//th[(text()='Use one question per screen')]/following-sibling::td//input"))
        assert self.is_selected(self.toggle_button_one_question) is False
        self.webapp.wait_to_click(self.done_button)
        self.webapp.wait_to_click(self.start_option)
        self.webapp.wait_to_click(self.case_list_menu)
        self.webapp.wait_to_click(self.registration_form)
        self.wait_to_clear_and_send_keys(self.name_question, self.name_input)
        self.click(self.dob_question)
        self.webapp.wait_to_click(self.click_today_date)
        
        self.wait_to_clear_and_send_keys(self.mobileno_question, fetch_phone_number())
        
        self.wait_to_click(self.multi_question_submit_button)
        self.webapp.wait_to_click(self.home_button)
        self.wait_for_element(self.settings_option, 120)
        self.wait_to_click(self.settings_option)
        
        isChecked = self.is_selected(self.toggle_button_one_question)
        print(isChecked)
        
        if isChecked is False:
            # self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.XPATH, "//th[(text()='Use one question per screen')]/following-sibling::td//input"))
            self.wait_to_click(self.toggle_button_one_question)
            
            print("Toggled ON")
        # self.webapp.wait_to_click((By.XPATH, "//th[(text()='Use one question per screen')]/following-sibling::td//input"))
        assert self.is_selected(self.toggle_button_one_question) is True
        self.webapp.wait_to_click(self.done_button)
        self.switch_to_default_content()

    def clear_user_data(self):
        self.switch_to_frame(self.iframe)
        self.webapp.wait_to_click(self.settings_option)
        self.webapp.wait_to_click(self.clear_user_data_button)
        assert self.is_present_and_displayed(self.clear_data_message)
        self.switch_to_default_content()

    def change_language(self):
        self.switch_to_frame(self.iframe)
        self.webapp.wait_to_click(self.settings_option, 5)
        self.select_by_text(self.select_language, UserData.language)
        self.webapp.wait_to_click(self.done_button)
        self.wait_for_element(self.start_option, 120)
        self.webapp.wait_to_click(self.start_option)
        self.wait_for_element(self.case_list_menu, 120)
        self.webapp.wait_to_click(self.case_list_menu)
        self.wait_for_element(self.registration_form, 120)
        self.webapp.wait_to_click(self.registration_form)
        assert self.is_present_and_displayed(self.question_display_text)
        self.switch_to_default_content()

    def add_empty_form(self):
        self.wait_to_click(self.add_new_form)
        
        self.webapp.wait_to_click(self.add_new_reg_form)
        time.sleep(3)
        if not self.is_present(self.view_app_preview_show):
            self.webapp.wait_to_click(self.view_app_preview)
        else:
            print("App preview is already open")
        self.webapp.wait_to_click(self.refresh_button)
        self.switch_to_frame(self.iframe)
        self.webapp.wait_to_click(self.start_option)
        
        assert self.is_displayed(self.empty_form_error_message)
        self.switch_to_default_content()
        self.reload_page()
        
        self.hover_and_click(self.last_form, self.delete_form)
        self.webapp.wait_to_click(self.delete_confirm_button)
        self.webapp.wait_to_click(self.refresh_button)
        self.switch_to_frame(self.iframe)
        self.webapp.wait_to_click(self.start_option)
        assert self.is_present_and_displayed(self.case_list_menu)
        self.switch_to_default_content()
