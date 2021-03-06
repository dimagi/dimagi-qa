import os
import time


from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from UserInputs.generateUserInputs import fetch_random_string
from UserInputs.userInputsData import UserInputsData
from Pages.organisationStructurePage import latest_download_file


class MessagingPage:
    def __init__(self, driver):
        self.driver = driver
        # Messaging Dashboard
        self.messaging_menu_id = "MessagingTab"
        self.dashboard_linked_text = "Dashboard"
        self.dashboard_elements = "//div[@id='messaging_dashboard']"
        # Compose SMS
        self.compose_sms_menu = "Compose SMS Message"
        self.recipients_textarea = "//textarea[@name='recipients']"
        self.select_recipient = "(//ul[@role='listbox']/li)[1]"
        self.message_textarea = "//textarea[@name='message']"
        self.send_message = "(//button[@class='btn btn-primary' and @type='submit'])[1]"
        self.message_sent_success_msg = "//div[@class='alert alert-margin-top fade in alert-success']"
        # Broadcasts
        self.broadcasts = "Broadcasts"
        self.add_broadcast = "//div[@class='btn-group']"
        self.broadcast_name = "//input[@name='schedule-schedule_name']"
        self.recipients = "(//ul[@class='select2-selection__rendered'])[1]"
        self.user_recipient = "(//span[@class='select2-selection select2-selection--multiple'])[2]"
        self.select_value_dropdown = "(//ul[@class='select2-results__options']/li)[2]"
        self.broadcast_message = "(//textarea[@data-bind='value: nonTranslatedMessage'])[2]"
        self.send_broadcast = "//button[@data-bind='text: saveBroadcastText()']"
        self.broadcast_created = "//a[text()='" + "broadcast_" + fetch_random_string() + "']"
        # Conditional Alerts
        self.cond_alerts = "Conditional Alerts"
        self.add_cond_alert = "New Conditional Alert"
        self.cond_alert_name = "//input[@name='conditional-alert-name']"
        self.continue_button_basic_tab = "//button[@data-bind='click: handleBasicNavContinue, enable: basicTabValid']"
        self.case_type = "//select[@data-bind='value: caseType']"
        self.case_type_option_value = "//option[@value='case']"
        self.continue_button_rule_tab = "//button[@data-bind='click: handleRuleNavContinue, enable: ruleTabValid']"
        self.cond_alert_created = "//a[text()='" + "cond_alert_" + fetch_random_string() + "']"
        self.select_recipient_type = "(//ul[@id='select2-id_schedule-recipient_types-results']/li)[1]"
        self.save_id = "conditional-alert-save-btn"
        self.delete_cond_alert = "//a[text()='" + "cond_alert_" + fetch_random_string() + "']//preceding::button[@class='btn btn-danger'][1]"
        # Condition Alerts : Download and Upload
        self.bulk_upload_button = "Bulk Upload SMS Alert Content"
        self.download_id = "download_link"
        self.choose_file = "//input[@name='bulk_upload_file']"
        self.upload = "//button[@class='btn btn-primary disable-on-submit']"
        self.upload_success_message = "//div[@class='alert alert-margin-top fade in alert-success']"
        # Keywords
        self.keywords = "Keywords"
        self.add_keyword = "Add Keyword"
        self.keyword_name = "//input[@name='keyword']"
        self.keyword_description = "//input[@name='description']"
        self.keyword_message = "//input[@name='sender_message']"
        self.keyword_created = "//a[text()='" + "KEYWORD_" + fetch_random_string().upper() + "']"
        self.add_structured_keyword = "Add Structured Keyword"
        self.keyword_survey = "(//span[@class='select2-selection select2-selection--single'])[1]"
        self.survey_option_select = "(//li[@class='select2-results__option'])[2]"
        self.structured_keyword_created = "//a[text()='" + "STRUCTURED_KEYWORD_" + fetch_random_string().upper() + "']"
        self.delete_keyword = self.keyword_created + "//following::a[@class='btn btn-danger'][1]"
        self.delete_structured_keyword = self.structured_keyword_created + "//following::a[@class='btn btn-danger'][1]"
        self.confirm_delete_keyword = self.keyword_created + \
                                      "//following::a[@class='btn btn-danger delete-item-confirm'][1]"
        self.confirm_delete_structured_keyword = self.structured_keyword_created + \
                                                 "//following::a[@class='btn btn-danger delete-item-confirm'][1]"
        # Chat
        self.chat = "Chat"
        self.contact_table = "contact_list"
        # SMS Connectivity
        self.sms_connectivity = "SMS Connectivity"
        self.add_gateway = "(//button[@class='btn btn-primary'])[1]"
        self.gateway_name = "//input[@name='name']"
        self.host_and_port = "//input[@name='host_and_port']"
        self.username = "//input[@name='user_name']"
        self.password = "//input[@name='password']"
        self.sender_id = "//input[@name='sender_id']"
        self.client_name = "//input[@name='circle_name']"
        self.campaign_name = "//input[@name='campaign_name']"
        self.gateway_created = "//a[text()='" + "gateway_" + fetch_random_string() + "']"
        # General Settings
        self.general_settings = "General Settings"
        self.disable_button = "(//div[@class='btn-group-separated'])/button[1]"
        self.enable_button = "(//div[@class='btn-group-separated'])/button[2]"
        self.time_input = "(//input[@data-bind='value: end_time'])[2]"
        self.settings_success_msg = ""
        # Languages
        self.languages = "Languages"
        self.add_lang = "//button[@data-bind='click: addLanguage, disable: addLanguageDisabled']"
        self.lang_input_textarea = "(//span[@role='combobox'])[last()]"
        self.select_first_lang = "(//li[@role='treeitem'])[1]"
        self.select_second_lang = "(//li[@role='treeitem'])[2]"
        self.save_lang = "(//div[@class='btn btn-primary'])[1]"
        self.delete_lang = "(//a[@data-bind='click: $root.removeLanguage'])[last()]"
        # Message Translation
        self.msg_translation_menu = "//a[text()='Messaging Translations']"
        # Project and Subscription Settings
        self.settings_bar = "//a[@data-action='Click Gear Icon']"
        self.subscription_menu = "Current Subscription"
        self.subscription_elements_id = "subscriptionSummary"
        self.project_settings_menu = "Project Settings"
        self.project_settings_elements = "//form[@class='form form-horizontal']"

    def wait_to_click(self, *locator, timeout=3):
        clickable = ec.element_to_be_clickable(locator)
        WebDriverWait(self.driver, timeout).until(clickable).click()

    def open_dashboard_page(self):
        assert True == self.driver.find_element(By.XPATH, self.dashboard_elements).is_displayed()
        print("Messaging dashboard loaded successfully!")

    def compose_sms(self):
        self.driver.find_element(By.LINK_TEXT, self.compose_sms_menu).click()
        self.driver.find_element(By.XPATH, self.recipients_textarea).send_keys("[send to all]")
        self.driver.find_element(By.XPATH, self.message_textarea).send_keys("sms_" + fetch_random_string())
        self.driver.find_element(By.XPATH, self.send_message).click()
        assert True == WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((
            By.XPATH, self.message_sent_success_msg))).is_displayed()
        print("SMS composed successfully!")

    def send_broadcast_message(self):
        self.wait_to_click(By.LINK_TEXT, self.broadcasts)
        self.wait_to_click(By.XPATH, self.add_broadcast)
        self.driver.find_element(By.XPATH, self.broadcast_name).send_keys("broadcast_" + fetch_random_string())
        self.wait_to_click(By.XPATH, self.recipients)
        self.wait_to_click(By.XPATH, self.select_recipient_type)
        self.wait_to_click(By.XPATH, self.user_recipient)
        self.wait_to_click(By.XPATH, self.select_value_dropdown)
        self.driver.find_element(By.XPATH, self.broadcast_message).send_keys("Test Broadcast:" + "broadcast_"
                                                                             + fetch_random_string())
        self.wait_to_click(By.XPATH, self.send_broadcast)
        assert True == WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((
            By.XPATH, self.broadcast_created))).is_displayed()
        print("Broadcast created successfully!")

    def create_cond_alert(self):
        self.wait_to_click(By.LINK_TEXT, self.cond_alerts)
        self.wait_to_click(By.LINK_TEXT, self.add_cond_alert)
        WebDriverWait(self.driver, 2).until(ec.element_to_be_clickable((
            By.XPATH, self.cond_alert_name))).send_keys("cond_alert_" + fetch_random_string())
        self.wait_to_click(By.XPATH, self.continue_button_basic_tab)
        self.wait_to_click(By.XPATH, self.case_type)
        self.wait_to_click(By.XPATH, self.case_type_option_value)
        self.wait_to_click(By.XPATH, self.continue_button_rule_tab)
        self.wait_to_click(By.XPATH, self.recipients)
        self.wait_to_click(By.XPATH, self.select_recipient_type)
        WebDriverWait(self.driver, 2).until(ec.element_to_be_clickable((
            By.XPATH, self.broadcast_message))).send_keys("Test Alert:" + "cond_alert_" + fetch_random_string())
        self.wait_to_click(By.ID, self.save_id)
        assert True == WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((
            By.XPATH, self.cond_alert_created))).is_displayed()
        print("Conditional Alert created successfully!")

    def cond_alert_download(self):
        self.wait_to_click(By.LINK_TEXT, self.cond_alerts)
        self.wait_to_click(By.LINK_TEXT, self.bulk_upload_button)
        self.wait_to_click(By.ID, self.download_id)
        time.sleep(2)
        print("Conditional Alert downloaded successfully!")

    def cond_alert_upload(self):
        newest_file = latest_download_file()
        file_that_was_downloaded = UserInputsData.download_path / newest_file
        self.driver.find_element(By.XPATH, self.choose_file).send_keys(str(file_that_was_downloaded))
        self.wait_to_click(By.XPATH, self.upload)
        assert True == self.driver.find_element(By.XPATH, self.upload_success_message).is_displayed()
        print("Conditional Alert uploaded successfully!")

    def add_keyword_trigger(self):
        self.wait_to_click(By.LINK_TEXT, self.keywords)
        self.wait_to_click(By.LINK_TEXT, self.add_keyword)
        self.driver.find_element(By.XPATH, self.keyword_name).send_keys("keyword_" + fetch_random_string())
        self.driver.find_element(By.XPATH, self.keyword_description).send_keys("keyword_" + fetch_random_string())
        self.driver.find_element(By.XPATH, self.keyword_message).send_keys("Test Message: " + "keyword_"
                                                                           + fetch_random_string())
        self.driver.find_element(By.XPATH, self.send_message).click()
        assert True == WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((
            By.XPATH, self.keyword_created))).is_displayed()
        print("Keyword created successfully!")

    def add_structured_keyword_trigger(self):
        self.wait_to_click(By.LINK_TEXT, self.keywords)
        self.wait_to_click(By.LINK_TEXT, self.add_structured_keyword)
        WebDriverWait(self.driver, 3).until(ec.element_to_be_clickable((By.XPATH, self.keyword_name))).send_keys(
            "structured_keyword_" + fetch_random_string())
        WebDriverWait(self.driver, 3).until(ec.element_to_be_clickable((
            By.XPATH, self.keyword_description))).send_keys("structured_keyword_" + fetch_random_string())
        self.wait_to_click(By.XPATH, self.keyword_survey)
        self.wait_to_click(By.XPATH, self.survey_option_select)
        WebDriverWait(self.driver, 3).until(ec.element_to_be_clickable((By.XPATH, self.keyword_message))).send_keys(
            "Test Message" + "structured_keyword_" + fetch_random_string())
        self.wait_to_click(By.XPATH, self.send_message)
        assert True == WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((
            By.XPATH, self.structured_keyword_created))).is_displayed()
        print("Structured keyword created successfully!")

    def chat_page(self):
        self.driver.find_element(By.LINK_TEXT, self.chat).click()
        assert True == self.driver.find_element(By.ID, self.contact_table).is_displayed()
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
        self.driver.find_element(By.LINK_TEXT, self.general_settings).click()
        time.sleep(1)
        if self.driver.find_element(By.XPATH, self.disable_button).is_enabled():
            self.driver.find_element(By.XPATH, self.enable_button).click()
            self.driver.find_element(By.XPATH, self.time_input).send_keys("23:59")
        else:
            self.driver.find_element(By.XPATH, self.disable_button).click()
        self.driver.find_element(By.XPATH, self.send_message).click()
        assert True == WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((
            By.XPATH, self.message_sent_success_msg))).is_displayed()
        print("Settings page updated successfully!")

    def languages_page(self):
        self.wait_to_click(By.LINK_TEXT, self.languages)
        time.sleep(1)
        self.wait_to_click(By.XPATH, self.add_lang)
        self.wait_to_click(By.XPATH, self.lang_input_textarea)
        time.sleep(1)
        self.wait_to_click(By.XPATH, self.select_first_lang)
        self.wait_to_click(By.XPATH, self.save_lang)
        self.wait_to_click(By.XPATH, self.lang_input_textarea)
        time.sleep(1)
        self.wait_to_click(By.XPATH, self.select_second_lang)
        self.wait_to_click(By.XPATH, self.save_lang)
        self.wait_to_click(By.XPATH, self.delete_lang)
        self.wait_to_click(By.XPATH, self.save_lang)
        time.sleep(1)
        print("Language added and deleted successfully!")

    def remove_keyword(self):
        self.wait_to_click(By.LINK_TEXT, self.keywords)
        self.wait_to_click(By.XPATH, self.delete_keyword)
        self.wait_to_click(By.XPATH, self.confirm_delete_keyword)
        self.driver.refresh()
        try:
            isPresent = self.driver.find_element(By.XPATH, self.keyword_created).is_displayed()
        except NoSuchElementException:
            isPresent = False
        if not isPresent:
            assert True
            print("Keyword removed successfully!")
        else:
            assert False

    def remove_structured_keyword(self):
        self.wait_to_click(By.LINK_TEXT, self.keywords)
        self.wait_to_click(By.XPATH, self.delete_structured_keyword)
        self.wait_to_click(By.XPATH, self.confirm_delete_structured_keyword)
        self.driver.refresh()
        try:
            isPresent = self.driver.find_element(By.XPATH, self.structured_keyword_created).is_displayed()
        except NoSuchElementException:
            isPresent = False
        if not isPresent:
            assert True
            print("Structured keyword removed successfully!")
        else:
            assert False

    def remove_cond_alert(self):
        self.wait_to_click(By.LINK_TEXT, self.cond_alerts)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((
            By.XPATH, self.delete_cond_alert))).click()
        obj = self.driver.switch_to.alert
        obj.accept()
        self.driver.refresh()
        try:
            isPresent = self.driver.find_element(By.XPATH, self.cond_alert_created).is_displayed()
        except NoSuchElementException:
            isPresent = False
        if not isPresent:
            assert True
            print("Cond Alert removed successfully!")
        else:
            assert False

    def msg_trans_download(self):
        self.wait_to_click(By.LINK_TEXT, self.languages)
        self.wait_to_click(By.XPATH, self.msg_translation_menu)
        self.wait_to_click(By.ID, self.download_id)
        time.sleep(2)
        print("Msg Trans downloaded successfully!")

    def msg_trans_upload(self):
        newest_file = latest_download_file()
        file_that_was_downloaded = UserInputsData.download_path / newest_file
        self.driver.find_element(By.XPATH, self.choose_file).send_keys(str(file_that_was_downloaded))
        self.wait_to_click(By.XPATH, self.upload)
        assert True == WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((
            By.XPATH, self.upload_success_message))).is_displayed()
        print("Msg Trans uploaded successfully!")

    def project_settings_page(self):
        self.wait_to_click(By.XPATH, self.settings_bar)
        self.wait_to_click(By.LINK_TEXT, self.project_settings_menu)
        assert True == WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((
            By.XPATH, self.project_settings_elements))).is_displayed()
        print("Project Settings page loaded successfully!")

    def current_subscription_page(self):
        self.wait_to_click(By.XPATH, self.settings_bar)
        self.wait_to_click(By.LINK_TEXT, self.subscription_menu)
        assert True == WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((
            By.ID, self.subscription_elements_id))).is_displayed()
        print("Current Subscription page loaded successfully!")
