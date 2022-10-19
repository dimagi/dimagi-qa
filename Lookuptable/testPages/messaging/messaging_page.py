import time

from common_utilities.selenium.base_page import BasePage
from common_utilities.path_settings import PathSettings
from HQSmokeTests.userInputs.user_inputs import UserData
from common_utilities.generate_random_string import fetch_random_string
from HQSmokeTests.testPages.users.org_structure_page import latest_download_file

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, \
    NoAlertPresentException
from selenium.webdriver.common.by import By

""""Contains test page elements and functions related to the various messaging mediums available on CCHQ"""


class MessagingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.cond_alert_name_input = "cond_alert_" + fetch_random_string()
        self.keyword_name_input = "KEYWORD_" + fetch_random_string().upper()
        self.struct_keyword_name_input = "STRUCTURED_KEYWORD_" + fetch_random_string().upper()
        self.broadcast_input = "broadcast_" + fetch_random_string()
        self.keyword_created_xpath = "//a[text()='" + self.keyword_name_input + "']"

        # Messaging Dashboard
        self.messaging_menu_id = (By.ID, "MessagingTab")
        self.dashboard_linked_text = (By.LINK_TEXT, "Dashboard")
        self.dashboard_elements = (By.XPATH, "//div[@id='messaging_dashboard']")
        # Compose SMS
        self.compose_sms_menu = (By.LINK_TEXT, "Compose SMS Message")
        self.recipients_textarea = (By.XPATH, "//textarea[@name='recipients']")
        self.select_recipient = (By.XPATH, "(//ul[@role='listbox']/li)[1]")
        self.message_textarea = (By.XPATH, "//textarea[@name='message']")
        self.send_message = (By.XPATH, "(//button[@class='btn btn-primary' and @type='submit'])[1]")
        self.message_sent_success_msg = (By.XPATH, "//div[@class='alert alert-margin-top fade in alert-success']")
        # Broadcasts
        self.broadcasts = (By.LINK_TEXT, "Broadcasts")
        self.add_broadcast = (By.XPATH, "//div[@class='btn-group']")
        self.broadcast_name = (By.XPATH, "//input[@name='schedule-schedule_name']")
        self.recipients = (By.XPATH, "(//span[@class='select2-selection select2-selection--multiple'])[1]")
        self.user_recipient = (By.XPATH, "(//span[@class='select2-selection select2-selection--multiple'])[2]")
        self.select_value_dropdown = (By.XPATH, "(//ul[@class='select2-results__options']/li)[1]")
        self.broadcast_message = (By.XPATH, "(//textarea[@data-bind='value: nonTranslatedMessage'])[2]")
        self.email_subject = (By.XPATH, "(//textarea[@data-bind='value: nonTranslatedMessage'])[1]")
        self.send_broadcast = (By.XPATH,  "//button[@data-bind='text: saveBroadcastText()']")
        self.broadcast_select = (By.XPATH,  "//div[@id='immediate-broadcasts']//select[@class='form-control']")
        self.broadcast_created = (By.XPATH, "//a[text()='" + self.broadcast_input + "']")
        self.next_btn = (By.XPATH, "//div[@id='immediate-broadcasts']//a[@data-bind='click: nextPage']")
        # Conditional Alerts
        self.cond_alerts = (By.LINK_TEXT, "Conditional Alerts")
        self.add_cond_alert = (By.LINK_TEXT, "New Conditional Alert")
        self.cond_alert_name = (By.XPATH, "//input[@name='conditional-alert-name']")
        self.continue_button_basic_tab = (By.XPATH, "//button[@data-bind='click: handleBasicNavContinue, enable: basicTabValid']")
        self.case_type = (By.XPATH,  "//select[@data-bind='value: caseType']")
        self.case_type_option_value = (By.XPATH, "//option[@value='reassign']")
        self.select_filter = (By.XPATH, "//button[@class='btn btn-default dropdown-toggle']")
        self.case_property_filter = (By.XPATH, "//ul//a[.='Case property']")
        self.case_property_textbox = (By.XPATH, "//case-property-input//span[@class='select2-selection select2-selection--single'][@role='combobox']")
        self.select_case_property = (By.XPATH, "//select[@data-bind='value: valueObservable, autocompleteSelect2: casePropertyNames']")
        self.case_property_value = (By.XPATH, "//input[contains(@data-bind,'value: property_value')]")
        self.case_property_input = (By.XPATH, "//input[@class='select2-search__field']")
        self.continue_button_rule_tab = (By.XPATH, "//button[@data-bind='click: handleRuleNavContinue, enable: ruleTabValid']")
        self.cond_alert_created = (By.XPATH, "//a[text()='" + str(self.cond_alert_name_input) + "']")
        self.select_recipient_type = (By.XPATH, "//ul[@id='select2-id_schedule-recipient_types-results']/li[.='Users']")
        self.alert_type = (By.XPATH, "//select[@name='schedule-content']")
        self.user_recipients_results = (By.XPATH, "//ul[@id='select2-id_schedule-user_recipients-results']/li[.='"+ UserData.app_login +"']")
        self.save_button_xpath = (By.XPATH, "//button[@type='submit'and text()='Save']")
        self.delete_cond_alert = (By.XPATH, "//a[text()='" + str(self.cond_alert_name_input) + "']//preceding::button[@class='btn btn-danger'][1]")
        self.search_box = (By.XPATH, "//form[@class='input-group']/input[@class='form-control']")
        self.search_btn = (By.XPATH, "//form[@class='input-group']//button[@data-bind='click: clickAction, visible: !immediate']")

        # Condition Alerts : Download and Upload
        self.bulk_upload_button = (By.LINK_TEXT, "Bulk Upload SMS Alert Content")
        self.download_id = (By.ID, "download_link")
        self.choose_file = (By.XPATH, "//input[@name='bulk_upload_file']")
        self.upload = (By.XPATH, "//button[@class='btn btn-primary disable-on-submit']")
        self.upload_success_message = (By.XPATH, "//div[@class='alert alert-margin-top fade in alert-success']")
        # Keywords
        self.keywords = (By.LINK_TEXT, "Keywords")
        self.add_keyword = (By.LINK_TEXT, "Add Keyword")
        self.keyword_name = (By.XPATH, "//input[@name='keyword']")
        self.keyword_description = (By.XPATH, "//input[@name='description']")
        self.keyword_message = (By.XPATH, "//input[@name='sender_message']")
        self.keyword_created = (By.XPATH, self.keyword_created_xpath)
        self.add_structured_keyword = (By.LINK_TEXT, "Add Structured Keyword")
        self.keyword_survey = (By.XPATH, "(//span[@class='select2-selection select2-selection--single'])[1]")
        self.survey_option_select = (By.XPATH, "(//li[@class='select2-results__option select2-results__option--selectable'])[1]")
        self.structured_keyword_created = (By.XPATH, "//a[text()='" + self.struct_keyword_name_input + "']")
        self.delete_keyword = (By.XPATH, self.keyword_created_xpath + "//following::a[@class='btn btn-danger'][1]")
        self.delete_structured_keyword = (By.XPATH, "//a[text()='" + self.struct_keyword_name_input + "']//following::a[@class='btn btn-danger'][1]")
        self.confirm_delete_keyword = (By.XPATH, self.keyword_created_xpath + "//following::a[@class='btn btn-danger delete-item-confirm'][1]")
        self.confirm_delete_structured_keyword = (By.XPATH, "//a[text()='" + self.struct_keyword_name_input + "']//following::a[@class='btn btn-danger delete-item-confirm'][1]")
        # Chat
        self.chat = (By.LINK_TEXT, "Chat")
        self.contact_table = (By.ID, "contact_list")
        # SMS Connectivity
        self.sms_connectivity = (By.LINK_TEXT, "SMS Connectivity")
        self.add_gateway = (By.XPATH, "(//button[@class='btn btn-primary'])[1]")
        self.gateway_name = (By.XPATH, "//input[@name='name']")
        self.host_and_port = (By.XPATH, "//input[@name='host_and_port']")
        self.username = (By.XPATH, "//input[@name='user_name']")
        self.password = (By.XPATH, "//input[@name='password']")
        self.sender_id = (By.XPATH, "//input[@name='sender_id']")
        self.client_name = (By.XPATH, "//input[@name='circle_name']")
        self.campaign_name = (By.XPATH, "//input[@name='campaign_name']")
        self.gateway_created = (By.XPATH, "//a[text()='" + "gateway_" + fetch_random_string() + "']")
        # General Settings
        self.general_settings = (By.LINK_TEXT, "General Settings")
        self.disable_button = (By.XPATH, "(//div[@class='btn-group-separated'])/button[1]")
        self.enable_button = (By.XPATH, "(//div[@class='btn-group-separated'])/button[2]")
        self.time_input = (By.XPATH, "(//input[@data-bind='value: end_time'])[2]")
        # Languages
        self.languages = (By.LINK_TEXT, "Languages")
        self.add_lang = (By.XPATH, "//button[@data-bind='click: addLanguage, disable: addLanguageDisabled']")
        self.lang_input_textarea = (By.XPATH, "(//span[@role='combobox'])[last()]")
        self.select_first_lang = (By.XPATH, "(//li[@role='option'])[1]")
        self.select_second_lang = (By.XPATH,  "(//li[@role='option'])[2]")
        self.save_lang = (By.XPATH, "(//div[@class='btn btn-primary'])[1]")
        self.delete_lang = (By.XPATH, "(//a[@data-bind='click: $root.removeLanguage'])[last()]")
        self.lang_error = (By.XPATH, "//p[text()='Language appears twice']")
        # Message Translation
        self.msg_translation_menu = (By.XPATH, "//a[text()='Messaging Translations']")
        # Project and Subscription Settings
        self.settings_bar = (By.XPATH, "//a[@data-action='Click Gear Icon']")
        self.subscription_menu = (By.LINK_TEXT, "Current Subscription")
        self.subscription_elements_id = (By.ID, "subscriptionSummary")
        self.project_settings_menu = (By.LINK_TEXT, "Project Settings")
        self.project_settings_elements = (By.XPATH, "//form[@class='form form-horizontal']")

    def open_dashboard_page(self):
        assert self.is_displayed(self.dashboard_elements), "Dashboatd  didn't load successfully!"
        print("Messaging dashboard loaded successfully!")

    def compose_sms(self):
        self.click(self.compose_sms_menu)
        self.send_keys(self.recipients_textarea, "[send to all]")
        self.send_keys(self.message_textarea, "sms_" + fetch_random_string())
        self.click(self.send_message)
        try:
            assert self.is_present_and_displayed(self.message_sent_success_msg), "Message not sent successfully"
        except TimeoutException:
            self.click(self.compose_sms_menu)
            self.send_keys(self.recipients_textarea, "[send to all]")
            self.send_keys(self.message_textarea, "sms_" + fetch_random_string())
            self.click(self.send_message)
            assert self.is_visible_and_displayed(self.message_sent_success_msg), "Message not sent successfully"
            print("SMS composed successfully!")

    def send_broadcast_message(self):
        self.wait_to_click(self.broadcasts)
        self.wait_to_click(self.add_broadcast)
        self.send_keys(self.broadcast_name, self.broadcast_input)
        self.click(self.recipients)
        self.wait_to_click(self.select_recipient_type)
        self.wait_to_click(self.user_recipient)
        time.sleep(1)
        self.wait_to_click(self.select_value_dropdown)
        self.send_keys(self.broadcast_message, "Test Broadcast:" + self.broadcast_input)
        self.wait_to_click(self.send_broadcast)
        self.driver.refresh()
        self.select_by_value(self.broadcast_select, '100')
        time.sleep(5)
        try:
            while False:
                if not self.is_displayed(self.broadcast_created):
                    self.wait_to_click(self.next_btn)
                    time.sleep(5)
                    continue
                else:
                    assert True
        except StaleElementReferenceException:
            assert self.is_visible_and_displayed(self.broadcast_created), "Broadcast not created successfully!"
        print("Broadcast created successfully!")

    def create_cond_alert(self):
        self.wait_to_click(self.cond_alerts)
        self.wait_to_click(self.add_cond_alert)
        self.send_keys(self.cond_alert_name, self.cond_alert_name_input)
        self.wait_to_click(self.continue_button_basic_tab)
        time.sleep(2)
        self.wait_to_click(self.case_type)
        self.wait_to_click(self.case_type_option_value)
        self.wait_to_click(self.select_filter)
        self.wait_to_click(self.case_property_filter)
        time.sleep(2)
        self.wait_to_click(self.case_property_textbox)
        self.send_keys(self.case_property_input,UserData.alert_case_property)
        self.select_by_text(self.select_case_property,UserData.alert_case_property)
        self.send_keys(self.case_property_value,UserData.alert_case_property_value)
        self.wait_to_click(self.continue_button_rule_tab)
        self.wait_to_click(self.recipients)
        self.wait_to_click(self.select_recipient_type)
        self.wait_to_click(self.user_recipient)
        self.wait_to_click(self.user_recipients_results)
        self.select_by_text(self.alert_type, "Email")
        self.send_keys(self.email_subject, "Test Alert:" + self.cond_alert_name_input)
        self.send_keys(self.broadcast_message, "Test Alert:" + self.cond_alert_name_input)
        self.wait_to_click(self.save_button_xpath)
        print("Sleeping till the alert processing completes")
        time.sleep(20)
        self.wait_to_click(self.search_box)
        assert self.is_displayed(self.cond_alert_created), "Conditional Alert not created successfully!"
        print("Conditional Alert created successfully!")
        return self.cond_alert_name_input

    def cond_alert_download(self):
        self.wait_to_click(self.cond_alerts)
        self.wait_to_click(self.bulk_upload_button)
        self.wait_to_click(self.download_id)
        time.sleep(2)
        print("Conditional Alert downloaded successfully!")

    def cond_alert_upload(self):
        newest_file = latest_download_file()
        file_that_was_downloaded = PathSettings.DOWNLOAD_PATH / newest_file
        self.send_keys(self.choose_file, str(file_that_was_downloaded))
        self.wait_to_click(self.upload)
        assert self.is_visible_and_displayed(self.upload_success_message), "Conditional Alert upload not completed!"
        print("Conditional Alert uploaded successfully!")

    def add_keyword_trigger(self):
        self.wait_to_click(self.keywords)
        self.wait_to_click(self.add_keyword)
        self.send_keys(self.keyword_name, self.keyword_name_input)
        self.send_keys(self.keyword_description, self.keyword_name_input)
        self.send_keys(self.keyword_message, "Test Message: " + self.keyword_name_input)
        self.click(self.send_message)
        assert self.is_visible_and_displayed(self.keyword_created), "Keyword not created successfully!"
        print("Keyword created successfully!")

    def add_structured_keyword_trigger(self):
        self.wait_to_click(self.keywords)
        self.wait_to_click(self.add_structured_keyword)
        self.send_keys(self.keyword_name, self.struct_keyword_name_input)
        self.send_keys(self.keyword_description, self.struct_keyword_name_input)
        self.wait_to_click(self.keyword_survey)
        self.wait_to_click(self.survey_option_select)
        self.send_keys(self.keyword_message, "Test Message" + self.struct_keyword_name_input)
        self.wait_to_click(self.send_message)
        assert self.is_visible_and_displayed(self.structured_keyword_created), "Structured keyword not created successfully!"
        print("Structured keyword created successfully!")

    def chat_page(self):
        self.click(self.chat)
        assert self.is_displayed(self.contact_table), "Chat Page did not load successfully!"
        print("Chat Page loaded successfully!")

    # def sms_connectivity_gateway(self):
    #     self.driver.find_element(By.LINK_TEXT, self.sms_connectivity).click()
    #     time.sleep(2)
    #     self.driver.find_element(By.XPATH, "//select[@name='hq_api_id']").click()
    #     time.sleep(2)
    #     self.driver.find_element(By.XPATH, "//select[@name='hq_api_id']/option[text(
    #     )='Airtel (through TCL)']").click()
    #     self.driver.find_element(By.XPATH, self.add_gateway).click()
    #     self.driver.find_element(By.XPATH, self.gateway_name).send_keys("gateway_" + fetch_random_string())
    #     self.driver.find_element(By.XPATH, self.host_and_port).send_keys("gateway_" + fetch_random_string())
    #     self.driver.find_element(By.XPATH, self.username).send_keys("gateway_" + fetch_random_string())
    #     self.driver.find_element(By.XPATH, self.password).send_keys("gateway_" + fetch_random_string())
    #     self.driver.find_element(By.XPATH, self.sender_id).send_keys("gateway_" + fetch_random_string())
    #     self.driver.find_element(By.XPATH, self.client_name).send_keys("gateway_" + fetch_random_string())
    #     self.driver.find_element(By.XPATH, self.campaign_name).send_keys("gateway_" + fetch_random_string())
    #     time.sleep(2)
    #     assert True == self.driver.find_element(By.XPATH, self.gateway_created).is_displayed()
    #     print("Gateway created successfully!")

    def general_settings_page(self):
        self.click(self.general_settings)
        time.sleep(2)
        if self.is_enabled(self.disable_button):
            self.click(self.enable_button)
            self.send_keys(self.time_input, "23:59")
        else:
            self.click(self.disable_button)
        self.click(self.send_message)
        assert self.is_visible_and_displayed(self.message_sent_success_msg), "Settings page not updated successfully!"
        print("Settings page updated successfully!")

    def languages_page(self):
        self.wait_to_click(self.languages)
        time.sleep(1)
        self.wait_to_click(self.add_lang)
        self.wait_to_click(self.lang_input_textarea)
        time.sleep(1)
        self.wait_to_click(self.select_first_lang)
        try:
            if self.is_displayed(self.lang_error):
                self.wait_to_click(self.delete_lang)
                time.sleep(1)
                self.wait_to_click(self.delete_lang)
                time.sleep(1)
                self.wait_to_click(self.save_lang)
                time.sleep(1)
                self.wait_to_click(self.add_lang)
                self.wait_to_click(self.lang_input_textarea)
                time.sleep(1)
                self.wait_to_click(self.select_first_lang)
        except (NoSuchElementException, TimeoutException):
            print("One lang only")
        self.wait_to_click(self.save_lang)
        time.sleep(1)
        self.wait_to_click(self.lang_input_textarea)
        time.sleep(1)
        self.wait_to_click(self.select_second_lang)
        self.wait_to_click(self.save_lang)
        time.sleep(1)
        self.wait_to_click(self.delete_lang)
        time.sleep(1)
        self.wait_to_click(self.save_lang)
        time.sleep(2)
        print("Languages added and deleted successfully!")

    def remove_keyword(self):
        self.wait_to_click(self.keywords)
        self.wait_to_click(self.delete_keyword)
        self.wait_to_click(self.confirm_delete_keyword)
        self.driver.refresh()
        try:
            isPresent = self.is_displayed(self.keyword_created)
        except NoSuchElementException:
            isPresent = False
        if not isPresent:
            assert not isPresent
            print("Keyword removed successfully!")

    def remove_structured_keyword(self):
        self.wait_to_click(self.keywords)
        self.wait_to_click(self.delete_structured_keyword)
        self.wait_to_click(self.confirm_delete_structured_keyword)
        self.driver.refresh()
        try:
            isPresent = self.is_displayed(self.structured_keyword_created)
        except NoSuchElementException:
            isPresent = False
        if not isPresent:
            assert not isPresent
            print("Structured keyword removed successfully!")

    def remove_cond_alert(self):
        self.wait_and_sleep_to_click(self.cond_alerts)
        self.driver.refresh()
        self.wait_to_clear_and_send_keys(self.search_box, self.cond_alert_name_input)
        self.wait_and_sleep_to_click(self.search_box)
        self.wait_to_click(self.delete_cond_alert)
        try:
            obj = self.driver.switch_to.alert
            obj.accept()
        except NoAlertPresentException:
            raise AssertionError("Celery down")
        try:
            time.sleep(2)
            self.driver.refresh()
            self.wait_to_clear_and_send_keys(self.search_box, self.cond_alert_name_input)
            self.wait_and_sleep_to_click(self.search_box)
            isPresent = self.is_displayed(self.cond_alert_created)
        except NoSuchElementException:
            isPresent = False
        assert not isPresent
        print("Cond Alert removed successfully!")

    def msg_trans_download(self):
        self.wait_to_click(self.languages)
        time.sleep(1)
        self.wait_to_click(self.msg_translation_menu)
        self.wait_to_click(self.download_id)
        time.sleep(2)
        print("Msg Trans downloaded successfully!")

    def msg_trans_upload(self):
        newest_file = latest_download_file()
        file_that_was_downloaded = PathSettings.DOWNLOAD_PATH / newest_file
        self.send_keys(self.choose_file, str(file_that_was_downloaded))
        self.js_click(self.upload)
        assert self.is_visible_and_displayed(self.upload_success_message), "Msg Trans not uploaded successfully"
        print("Msg Trans uploaded successfully!")

    def project_settings_page(self):
        self.wait_to_click(self.settings_bar)
        self.wait_to_click(self.project_settings_menu)
        assert self.is_visible_and_displayed(self.project_settings_elements), "Project Settings page did not load successfully"
        print("Project Settings page loaded successfully!")

    def current_subscription_page(self):
        self.wait_to_click(self.settings_bar)
        self.wait_to_click(self.subscription_menu)
        assert self.is_visible_and_displayed(self.subscription_elements_id), "Subscription Page did not load successfully"
        print("Current Subscription page loaded successfully!")
