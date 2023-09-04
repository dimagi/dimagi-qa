import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from common_utilities.selenium.base_page import BasePage
from common_utilities.generate_random_string import fetch_random_string
from HQSmokeTests.userInputs.user_inputs import UserData
from common_utilities.path_settings import PathSettings
from HQSmokeTests.testPages.users.org_structure_page import latest_download_file

""""Contains test page elements and functions related to the applications on Commcare"""


class ApplicationPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.app_name = "App " + fetch_random_string()
        self.app_p1p2_name = "App P1P2 " + fetch_random_string()
        self.question_display_text_name = "Name"
        self.field_text = fetch_random_string()
        self.field_name = "Add Text "+self.field_text
        self.question_ID = "add_text_"+self.field_text
        self.reg_form_name = "\""+fetch_random_string()+"\"'& Reg Form"
        self.followup_form_name = "\"" + fetch_random_string() + "\"'& Followup Form"

        # Create New Application
        self.applications_menu_id = (By.ID, "ApplicationsTab")
        self.new_application = (By.LINK_TEXT, "New Application")
        self.new_app_created = (By.LINK_TEXT, self.app_name)
        self.edit_app_name = (By.XPATH, '//span[@class="inline-edit-icon h3 app-title"]')
        self.app_name_textbox = (By.XPATH, "(//input[@type='text'])[1]")
        self.confirm_change = (By.XPATH, "(//button[@data-bind=\"click: save, hasFocus: saveHasFocus, visible: !isSaving()\"])[1]")
        self.add_module = (By.XPATH, "//a[@class='appnav-add js-add-new-item']")
        self.add_case_list = (By.XPATH, "//button[@data-type='case']")
        self.add_questions = (By.XPATH, "//div[@class='dropdown fd-add-question-dropdown']")
        self.text_question = (By.XPATH, "//a[@data-qtype='Text']")
        self.advanced_question = (By.XPATH, "//a[@data-qtype='Geopoint'][contains(.,'Advanced')]")
        self.location_question = (By.XPATH, "//a[@data-qtype='Geopoint'][contains(.,'GPS')]")
        self.question_display_text = (By.XPATH, "(//div[@role='textbox'])[1]")
        self.save_button = (By.XPATH, "//span[text()='Save']")
        self.app_created = "//span[text()='{}']"
        self.form_link = "//a//*[contains(.,'{}')]"


        # Delete Application
        self.settings = (By.XPATH, "//i[@class='fa fa-gear']")
        self.delete_app = (By.XPATH, "//a[@href='#delete-app-modal']")
        self.delete_confirm = (By.XPATH, "(//button[@class='disable-on-submit btn btn-danger'])[last()]")

        # Application Contents
        self.menu_settings = (By.XPATH, "//a[@class='appnav-title appnav-title-secondary appnav-responsive']")
        self.menu_settings_content = (By.ID, "js-appmanager-body")
        self.form_settings = (By.XPATH, "(//a[@data-action='View Form'])[1]")
        self.form_settings_content = (By.XPATH, "//div[@class='tabbable appmanager-tabs-container']")

        # Form XML
        self.download_xml = (By.XPATH, "//a[contains(i/following-sibling::text(), 'Download')]")
        self.upload_xml = (By.XPATH, "//a[@href='#upload-xform']")
        self.add_form_button = (By.XPATH, "(//i[@class='fa fa-plus'])[1]")
        self.register_form = (By.XPATH, "//button[@data-case-action='open']/i")
        self.new_form_settings = (By.XPATH, "(//a[@data-action='View Form'])[3]")
        self.choose_file = (By.ID, "xform_file_input")
        self.upload = (By.ID, 'xform_file_submit')
        self.same_question_present = (By.XPATH, "//a[contains(i/following-sibling::text(), 'Name')]")

        # App Settings
        self.languages_tab = (By.XPATH, "//a[@href='#languages']")
        self.languages_tab_content = (By.ID, "language-settings-options")
        self.multimedia_tab = (By.XPATH, "//a[@href='#multimedia-tab']")
        self.multimedia_tab_content = (By.ID, "multimedia-tab")
        self.actions_tab = (By.XPATH, "//a[text()='Actions']")
        self.actions_tab_content = (By.ID, "actions")
        self.add_ons_tab = (By.XPATH, "//a[@href='#add-ons']")
        self.add_ons_tab_content = (By.ID, "add-ons")
        self.advanced_settings_tab = (By.XPATH, "//a[@href='#commcare-settings']")
        self.advanced_settings_tab_content = (By.ID, "app-settings-options")
        self.form_settings_tab = (By.XPATH, "//a[@href='#form-settings']")

        # Form Field Edit
        self.add_new_form = (By.XPATH,"//a[@class='appnav-secondary js-add-new-item']")
        self.edit_form_name_icon = (By.XPATH, "//a[@href='#edit-form-name-modal']")
        self.edit_form_name_text =(By.XPATH,"//input[@data-bind='value: name']")
        self.form_edit_app = (By.XPATH,"//a[contains(text(),'"+ UserData.reassign_cases_application+"')]")
        self.form_name_save_button = (By.XPATH, "//button[text()='Save']")
        self.reg_form_head_text = (By.XPATH, "//span[@class='fd-head-text']")
        self.form_settings_btn = "//a[.//span[contains(.,'{}')]]//following-sibling::a//i[@class='fa fa-gear appnav-show-on-hover']"
        self.reg_form_variable_name = (By.XPATH, "//span[@class='variable-form_name']")
        self.add_form_question = (By.XPATH, "//*[@class='fd-add-question dropdown-toggle btn btn-purple']")
        self.field_edit_app_name =  "//span[text()='{}']"
        self.field_edit_form_name = (By.XPATH, "//span[contains(text(),'"+UserData.new_form_name+"')]")
        self.edit_field = (By.XPATH,"//*[@name='itext-en-label']")
        self.question_ID_field = (By.XPATH, "//input[@id='property-nodeID']")
        self.updates_text = (By.XPATH,"//div[@id='js-publish-status']")
        self.make_new_version_button= (By.XPATH, "//button[contains(@data-bind,'Make New Version')]")
        self.release_button = (By.XPATH, "(//button[contains(text(),'Released')])[1]")
        self.release_button_pressed = (By.XPATH, "(//button[contains(text(),'Released')])[1][contains(@class,'active')]")
        self.publish_button = (By.XPATH,"(//*[contains(@data-bind,'click: clickDeploy')])[1]")
        self.delete_form = (By.XPATH,"//a[./span[contains(text(),'"+UserData.new_form_name+"')]]/preceding-sibling::a[./i[@class='fa fa-trash-o']]")
        self.delete_form_confirm = (By.XPATH, "//div[./p[./strong[contains(text(),'Android')]]]/following-sibling::div[button]//i[@class='fa fa-trash']")
        self.code = (By.XPATH, "//code")
        self.close = (By.XPATH, "//div[.//code]/following-sibling::div//a[contains(text(),'Close')]")
        self.override_btn = (By.XPATH, "//button[contains(.,'Overwrite their work')]")
        self.enter_app_code_link = (By.LINK_TEXT, "Enter App Code")


    def create_new_application(self):
        self.wait_to_click(self.applications_menu_id)
        self.wait_to_click(self.new_application)
        self.wait_to_click(self.edit_app_name)
        self.clear(self.app_name_textbox)
        self.send_keys(self.app_name_textbox, self.app_name)
        self.wait_to_click(self.confirm_change)
        self.wait_to_click(self.add_module)
        time.sleep(1)
        self.wait_to_click(self.add_case_list)
        time.sleep(2)
        self.wait_to_click(self.add_questions)
        time.sleep(2)
        self.wait_to_click(self.text_question)
        self.send_keys(self.question_display_text, self.question_display_text_name)
        self.wait_to_click(self.save_button)
        assert self.is_present_and_displayed((By.XPATH,self.app_created.format(self.app_name)))
        print("New App created successfully!")


    def form_builder_exploration(self):
        time.sleep(2)
        self.wait_to_click(self.menu_settings)
        time.sleep(2)
        self.wait_for_element(self.menu_settings_content)
        assert self.is_displayed(self.menu_settings_content)
        print("Menu Settings loaded successfully!")
        self.wait_for_element(self.form_settings)
        self.click(self.form_settings)
        self.accept_pop_up()
        assert self.is_present_and_displayed(self.form_settings_content)
        print("Form Settings loaded successfully!")

    def delete_application(self):
        time.sleep(2)
        self.js_click(self.settings)
        self.wait_to_click(self.actions_tab)
        self.wait_to_click(self.delete_app)
        self.wait_to_click(self.delete_confirm)
        print("Deleted the application")

    def form_xml_download_upload(self):
        try:
            self.wait_to_click(self.actions_tab)
        except TimeoutException:
            self.wait_to_click(self.form_settings)
            self.wait_to_click(self.actions_tab)
        self.wait_and_sleep_to_click(self.download_xml)
        self.wait_and_sleep_to_click(self.add_form_button)
        try:
            self.wait_and_sleep_to_click(self.register_form)
        except TimeoutException:
            self.driver.refresh()
        self.wait_and_sleep_to_click(self.new_form_settings)
        self.wait_and_sleep_to_click(self.actions_tab)
        self.wait_and_sleep_to_click(self.upload_xml)
        newest_file = latest_download_file(".xml")
        file_that_was_downloaded = PathSettings.DOWNLOAD_PATH / newest_file
        self.send_keys(self.choose_file, str(file_that_was_downloaded))
        time.sleep(1)
        self.click(self.upload)
        time.sleep(5)
        assert self.is_present_and_displayed(self.same_question_present)
        print("XML copied successfully!")

    def app_settings_exploration(self):
        try:
            self.wait_to_click(self.settings)
        except TimeoutException:
            self.driver.refresh()
            self.click(self.settings)
        assert self.is_present_and_displayed(self.languages_tab_content)
        self.wait_to_click(self.multimedia_tab)
        assert self.is_present_and_displayed(self.multimedia_tab_content)
        self.wait_to_click(self.actions_tab)
        assert self.is_present_and_displayed(self.actions_tab_content)
        self.wait_to_click(self.add_ons_tab)
        assert self.is_present_and_displayed(self.add_ons_tab_content)
        time.sleep(2)
        self.wait_to_click(self.advanced_settings_tab)
        assert self.is_present_and_displayed(self.advanced_settings_tab_content)
        print("App Settings loading successfully!")


    def update_form_field(self):
        self.wait_to_click(self.applications_menu_id)
        self.wait_to_click(self.form_edit_app)
        time.sleep(2)
        # self.wait_to_click(self.add_form_button)
        # self.wait_to_click(self.register_form)
        # time.sleep(30)
        # self.wait_to_click(self.edit_form_name_icon)
        # self.wait_to_clear_and_send_keys(self.edit_form_name_text, UserData.new_form_name)
        # self.wait_to_click(self.form_name_save_button)
        # self.wait_to_click(self.add_questions)
        # time.sleep(2)
        # self.wait_to_click(self.text_question)
        # self.send_keys(self.question_display_text, self.field_name)
        # assert self.is_present_and_displayed(self.app_created)
        # print("New App created successfully!")
        # self.wait_to_click(self.add_new_form)
        # self.wait_to_click(self.field_edit_app_name)
        self.wait_to_click(self.field_edit_form_name)
        time.sleep(5)
        self.wait_to_clear_and_send_keys(self.edit_field,self.field_name)
        self.wait_to_clear_and_send_keys(self.question_ID_field,self.question_ID)
        self.wait_to_click(self.save_button)
        time.sleep(5)
        assert self.is_displayed(self.updates_text), "Fields not updated"
        print("Fields successfully updated")
        self.wait_to_click((By.XPATH, self.field_edit_app_name.format(UserData.reassign_cases_application)))
        time.sleep(2)
        self.wait_to_click(self.make_new_version_button)
        time.sleep(5)
        self.driver.refresh()
        self.wait_for_element(self.release_button)
        self.js_click(self.release_button)
        print("Sleeping for the installation code to generate")
        time.sleep(10)
        self.wait_to_click(self.publish_button)
        self.wait_to_click(self.enter_app_code_link)
        code_text = self.wait_to_get_text(self.code)
        self.wait_to_click(self.close)
        # self.wait_to_click(self.delete_form)
        # self.wait_to_click(self.delete_form_confirm)
        assert self.is_present(self.release_button_pressed), "Release button is not successfully pressed."
        return code_text, self.field_text



    def create_application_with_verifications(self):
        self.wait_to_click(self.applications_menu_id)
        self.wait_to_click(self.new_application)
        self.wait_to_click(self.edit_app_name)
        self.clear(self.app_name_textbox)
        self.send_keys(self.app_name_textbox, self.app_p1p2_name)
        self.wait_to_click(self.confirm_change)
        self.wait_to_click(self.add_module)
        time.sleep(1)
        self.wait_to_click(self.add_case_list)
        time.sleep(2)
        self.wait_to_click(self.edit_form_name_icon)
        self.wait_to_clear_and_send_keys(self.edit_form_name_text, self.reg_form_name)
        self.wait_to_click(self.form_name_save_button)
        time.sleep(2)
        assert self.check_for_html_char(self.get_text(self.reg_form_head_text)), "html characters are present"
        assert self.check_for_html_char(self.get_text(self.reg_form_variable_name)), "html characters are present"
        assert self.get_text(self.reg_form_head_text) == self.get_text(self.reg_form_variable_name)
        self.wait_to_click(self.add_questions)
        time.sleep(0.5)
        self.hover_and_click(self.advanced_question, self.location_question)
        self.wait_for_element(self.question_display_text)
        self.send_keys(self.question_display_text, "Location")
        self.wait_to_clear_and_send_keys(self.question_ID_field, "location_id")
        self.wait_to_click(self.save_button)
        time.sleep(2)
        if self.is_present(self.override_btn):
            self.wait_to_click(self.override_btn)
        time.sleep(3)
        self.hover_on_element((By.XPATH, self.form_link.format("Reg Form")))
        self.wait_to_click((By.XPATH, self.form_settings_btn.format("Reg Form")))
        time.sleep(5)
        assert self.is_present_and_displayed(self.form_settings_tab)
        self.wait_to_click((By.XPATH, self.form_link.format("Followup Form")))
        self.wait_to_click(self.edit_form_name_icon)
        self.wait_to_clear_and_send_keys(self.edit_form_name_text, self.followup_form_name)
        self.wait_to_click(self.form_name_save_button)
        time.sleep(2)
        assert self.check_for_html_char(self.get_text(self.reg_form_head_text)), "html characters are present"
        assert self.check_for_html_char(self.get_text(self.reg_form_variable_name)), "html characters are present"
        assert self.get_text(self.reg_form_head_text) == self.get_text(self.reg_form_variable_name)
        self.wait_to_click(self.add_questions)
        time.sleep(2)
        self.wait_to_click(self.text_question)
        self.wait_for_element(self.question_display_text)
        self.send_keys(self.question_display_text, "Text")
        self.wait_to_click(self.save_button)
        if self.is_present(self.override_btn):
            self.wait_to_click(self.override_btn)
        time.sleep(3)
        self.hover_on_element((By.XPATH, self.form_link.format("Followup Form")))
        self.wait_to_click((By.XPATH, self.form_settings_btn.format("Followup Form")))

        time.sleep(5)
        assert self.is_present_and_displayed(self.form_settings_tab)
        assert self.is_present_and_displayed((By.XPATH, self.app_created.format(self.app_p1p2_name)))
        print("New App created successfully!")
        self.wait_to_click((By.XPATH, self.field_edit_app_name.format(self.app_p1p2_name)))
        time.sleep(2)
        self.wait_to_click(self.make_new_version_button)
        time.sleep(5)
        self.driver.refresh()
        self.wait_for_element(self.release_button)
        self.js_click(self.release_button)
        print("Sleeping for the installation code to generate")
        time.sleep(10)
        return self.app_p1p2_name

    def check_for_html_char(self, text):
        matched = re.search(r'\b&\w+;\b', text)
        if matched:
            return False
        else:
            return True

    def delete_p1p2_application(self, app_name):
        self.wait_to_click(self.applications_menu_id)
        self.wait_to_click((By.LINK_TEXT, app_name))
        time.sleep(2)
        self.js_click(self.settings)
        self.wait_to_click(self.actions_tab)
        self.wait_to_click(self.delete_app)
        self.wait_to_click(self.delete_confirm)
        print("Deleted the application")
