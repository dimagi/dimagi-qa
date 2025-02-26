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
        self.cond_alert_no_value_name_input = "cond_alert_no_value_" + fetch_random_string()
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
        self.recipients_select = (By.XPATH, "//select[@name='recipients']")
        self.select_recipient = (By.XPATH, "(//ul[@role='listbox']/li)[1]")
        self.message_textarea = (By.XPATH, "//textarea[@name='message']")
        self.send_message = (By.XPATH, "(//button[@class='btn btn-primary' and @type='submit'])[1]")
        self.message_sent_success_msg = (By.XPATH, "//div[@class='alert alert-margin-top fade in alert-success']")
        # Broadcasts
        self.broadcasts = (By.LINK_TEXT, "Broadcasts")
        self.add_broadcast = (By.XPATH, "//div[@class='btn-group']")
        self.broadcast_name = (By.XPATH, "//input[@name='schedule-schedule_name']")
        self.recipients_select_cond_alert = (By.XPATH, "//select[@name='schedule-recipient_types']")
        self.recipients = (By.XPATH, "(//span[@class='select2-selection select2-selection--multiple'])[1]")
        self.user_recipient = (By.XPATH, "(//span[@class='select2-selection select2-selection--multiple'])[2]")
        self.select_value_dropdown = (By.XPATH, "//ul[@class='select2-results__options']/li[.='"+UserData.app_login+"']")
        self.broadcast_message = (By.XPATH, "(//textarea[@data-bind='value: nonTranslatedMessage'])[2]")
        self.email_subject = (By.XPATH, "(//textarea[@data-bind='value: nonTranslatedMessage'])[1]")
        self.send_broadcast = (By.XPATH, "//button[@data-bind='text: saveBroadcastText()']")
        self.broadcast_select = (By.XPATH, "//div[@id='immediate-broadcasts']//select[@class='form-control']")
        self.broadcast_created = (By.XPATH, "//a[text()='" + self.broadcast_input + "']")
        self.next_btn = (By.XPATH, "//div[@id='immediate-broadcasts']//a[@data-bind='click: nextPage']")
        # Conditional Alerts
        self.cond_alerts = (By.LINK_TEXT, "Conditional Alerts")
        self.add_cond_alert = (By.LINK_TEXT, "New Conditional Alert")
        self.cond_alert_name = (By.XPATH, "//input[@name='conditional-alert-name']")
        self.continue_button_basic_tab = (
        By.XPATH, "//button[@data-bind='click: handleBasicNavContinue, enable: basicTabValid']")
        self.case_type = (By.XPATH, "//select[contains(@name,'case_type')]")
        self.case_type_option_value = (By.XPATH, "//option[@value='reassign']")
        self.select_filter = (By.XPATH, "//button[@class='btn btn-default dropdown-toggle']")
        self.case_property_filter = (By.XPATH, "//ul//a[.='Case property']")
        self.case_property_textbox = (
        By.XPATH, "//case-property-input//span[@class='select2-selection select2-selection--single'][@role='combobox']")
        self.select_case_property = (
        By.XPATH, "//select[@data-bind='value: valueObservable, autocompleteSelect2: casePropertyNames']")
        self.select_match_type = (By.XPATH, "//select[@data-bind='value: match_type']")
        self.case_property_value = (By.XPATH, "//input[contains(@data-bind,'value: property_value')]")
        self.case_property_input = (By.XPATH, "//input[@class='select2-search__field']")
        self.continue_button_rule_tab = (
        By.XPATH, "//button[@data-bind='click: handleRuleNavContinue, enable: ruleTabValid']")
        self.cond_alert_created = "//a[text()='{}']"
        self.restart_rule_button = "//td[./a[text()='{}']]//following-sibling::td/div/button[contains(@data-bind,'restart')]"
        self.restart_rule_button_none = "//td[./a[text()='{}']]//following-sibling::td/div[@style='display: none;']/button[contains(@data-bind,'restart')]"
        self.deactive_button_visible = "//td[./a[text()='{}']]//following-sibling::td/button[contains(@data-bind,'toggleStatus')]/span[contains(@data-bind,'visible: active')]"
        self.empty_table_alert = (
        By.XPATH, "//div[contains(@data-bind, 'emptyTable()')][contains(.,'There are no alerts to display')]")
        self.select_recipient_type = (By.XPATH, "//ul[@id='select2-id_schedule-recipient_types-results']/li[.='Users']")
        self.alert_type = (By.XPATH, "//select[@name='schedule-content']")
        self.user_recipients_results = (
        By.XPATH, "//ul[@id='select2-id_schedule-user_recipients-results']/li[.='" + UserData.app_login + "']")
        self.save_button_xpath = (By.XPATH, "//button[@type='submit'and text()='Save']")
        self.delete_cond_alert = "//a[text()='{}']//preceding::button[@class='btn btn-danger'][1]"
        self.search_box = (By.XPATH, "//form[@class='input-group']/input[@class='form-control']")
        self.search_btn = (
        By.XPATH, "//form[@class='input-group']//button[@data-bind='click: clickAction, visible: !immediate']")
        self.value_per_page =(By.XPATH, "//select[contains(@data-bind,'value: perPage')]")
        self.cond_alerts_name = (By.XPATH, "//td[.//button[contains(@class,'danger')][not(@disabled)]]//following-sibling::td[1]/a[contains(.,'cond_alert')]")
        self.cond_alert_delete_button = "(//td[contains(.,'{}')]//preceding-sibling::td/button[not(@disabled)])[{}]"
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
        self.survey_option_select = (
        By.XPATH, "(//li[@class='select2-results__option select2-results__option--selectable'])[1]")
        self.structured_keyword_created = (By.XPATH, "//a[text()='" + self.struct_keyword_name_input + "']")
        self.delete_keyword = (By.XPATH, self.keyword_created_xpath + "//following::button[contains(@class,'danger')][1]")
        self.delete_structured_keyword = (
        By.XPATH, "//a[text()='" + self.struct_keyword_name_input + "']//following::button[contains(@class,'danger')][1]")
        self.confirm_delete_keyword = (
        By.XPATH, self.keyword_created_xpath + "//following::*[contains(@class,'confirm')][1]")
        self.confirm_delete_structured_keyword = (By.XPATH,
                                                  "//a[text()='" + self.struct_keyword_name_input + "']//following::*[contains(@class,'confirm')][1]")
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
        self.select_eng_lang = (By.XPATH, "(//li[@role='option'][contains(.,'en (English)')])[1]")
        self.select_second_lang = (By.XPATH, "(//li[@role='option'])[2]")
        self.selected_lang_name = (By.XPATH, "(//td//p[contains(@data-bind,'message')])[last()]")
        self.language_list = (By.XPATH, "//ul[@role='listbox']")
        self.save_lang = (By.XPATH, "(//div[@class='btn btn-primary'])[1]")
        self.delete_lang = "//td[4][./p[contains(@data-bind,'message')][contains(.,'{}')]]//following-sibling::td[2]/a[@data-bind='click: $root.removeLanguage']"
        self.languages_present = (By.XPATH, "//td//p[contains(@data-bind,'message')]")
        self.lang_error = (By.XPATH, "//p[text()='Language appears twice']")
        # Message Translation
        self.msg_translation_menu = (By.XPATH, "//a[text()='Messaging Translations']")
        # Project and Subscription Settings
        self.settings_bar = (By.XPATH, "//ul[@role='menu']//a[@data-action='Click Gear Icon']/i")
        self.subscription_menu = (By.LINK_TEXT, "Current Subscription")
        self.subscription_elements_id = (By.ID, "subscriptionSummary")
        self.project_settings_menu = (By.LINK_TEXT, "Project Settings")
        self.project_settings_elements = (By.XPATH, "//form[@class='form form-horizontal']")
        self.page_limit = (By.XPATH, "//select[@id='pagination-limit']")
        self.keywords_list = (By.XPATH, "//td[.//span/a[contains(.,'KEYWORD_')]]")
        self.keyword_delete_btn = "//td[.//span/a[contains(.,'{}')]]//following-sibling::td/button"
        self.delete_confirm_button = "//td[.//span/a[contains(.,'{}')]]//following::a[contains(@class,'delete-item-confirm')][1]"
        self.page_empty = (By.XPATH, "//*[contains(@data-bind,'ListEmpty')]")

    def open_dashboard_page(self):
        assert self.is_displayed(self.dashboard_elements), "Dashboatd  didn't load successfully!"
        print("Messaging dashboard loaded successfully!")

    def compose_sms(self):
        self.click(self.compose_sms_menu)
        self.wait_for_element(self.recipients_select)
        self.select_by_value(self.recipients_select, "[send to all]")
        time.sleep(2)
        self.send_keys(self.message_textarea, "sms_" + fetch_random_string())
        time.sleep(2)
        self.scroll_to_element(self.send_message)
        self.js_click(self.send_message)
        try:
            assert self.is_present_and_displayed(self.message_sent_success_msg), "Message not sent successfully"
        except TimeoutException:
            self.click(self.compose_sms_menu)
            self.wait_for_element(self.recipients_select)
            self.select_by_value(self.recipients_select, "[send to all]")
            time.sleep(2)
            self.send_keys(self.message_textarea, "sms_" + fetch_random_string())
            time.sleep(2)
            self.scroll_to_element(self.send_message)
            self.js_click(self.send_message)
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
        self.remove_alert_with_same_name(self.cond_alert_name_input)
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
        self.send_keys(self.case_property_input, UserData.alert_case_property)
        self.select_by_text(self.select_case_property, UserData.alert_case_property)
        self.send_keys(self.case_property_value, UserData.alert_case_property_value)
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
        time.sleep(360)
        self.driver.refresh()
        time.sleep(140)
        self.wait_to_clear_and_send_keys(self.search_box, self.cond_alert_name_input)
        time.sleep(10)
        self.wait_to_click(self.search_box)
        self.wait_for_element((By.XPATH, self.delete_cond_alert.format(self.cond_alert_name_input)), 700)
        self.driver.refresh()
        if self.is_clickable((By.XPATH, self.delete_cond_alert.format(self.cond_alert_name_input))):
            print("Restart is not required.")
        else:
            try:
                self.js_click((By.XPATH, self.restart_rule_button.format(self.cond_alert_name_input)))
                self.accept_pop_up()
                time.sleep(5)
                self.accept_pop_up()
                print("Sleeping till the alert processing completes")
                time.sleep(360)
                self.wait_to_clear_and_send_keys(self.search_box, self.cond_alert_name_input)
                self.wait_to_click(self.search_box)
                self.wait_for_element((By.XPATH, self.delete_cond_alert.format(self.cond_alert_name_input)), 700)
                self.driver.refresh()
            except:
                print("Restart not required")
        self.wait_for_element(self.search_box)
        self.wait_to_clear_and_send_keys(self.search_box, self.cond_alert_name_input)
        self.wait_to_click(self.search_box)
        assert self.is_displayed((By.XPATH, self.cond_alert_created.format(self.cond_alert_name_input))), "Conditional Alert not created successfully!"
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
        time.sleep(2)
        self.scroll_to_element(self.send_message)
        self.js_click(self.send_message)
        time.sleep(2)
        self.select_by_value(self.page_limit, "50")
        time.sleep(3)
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
        time.sleep(2)
        self.scroll_to_element(self.send_message)
        self.js_click(self.send_message)
        time.sleep(2)
        self.select_by_value(self.page_limit, "50")
        time.sleep(3)
        assert self.is_visible_and_displayed(
            self.structured_keyword_created), "Structured keyword not created successfully!"
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
        time.sleep(2)
        self.scroll_to_element(self.send_message)
        self.js_click(self.send_message)
        assert self.is_visible_and_displayed(self.message_sent_success_msg), "Settings page not updated successfully!"
        print("Settings page updated successfully!")

    def delete_languages(self):
        self.wait_to_click(self.languages)
        time.sleep(1)
        lang_list = self.find_elements(self.languages_present)
        if len(lang_list) == 1:
            for item in lang_list:
                print(item.text)
                if item.text == 'English':
                    print("Default language present as English")
                else:
                    self.add_eng_lang()
                    print("English updated successfully")

        lang_list = self.find_elements(self.languages_present)
        if len(lang_list) > 1:
            for item in lang_list:
                if item.text == 'English':
                    print("Not Deleting English")
                else:
                    lang = item.text
                    print("Deleting language: ", lang)
                    self.wait_to_click((By.XPATH, self.delete_lang.format(lang)))
                    time.sleep(3)
                    self.wait_to_click(self.save_lang)
                    time.sleep(2)
        else:
            print("Only English is Present and no other languages")

    def add_eng_lang(self):
        self.wait_to_click(self.lang_input_textarea)
        time.sleep(2)
        self.wait_for_element(self.language_list)
        self.wait_to_click(self.select_eng_lang)
        time.sleep(2)
        lang = self.get_text(self.selected_lang_name)
        print("Language selected is: ", lang)
        self.wait_to_click(self.save_lang)

    def languages_page(self):
        self.wait_to_click(self.languages)
        time.sleep(1)
        self.wait_to_click(self.add_lang)
        self.wait_to_click(self.lang_input_textarea)
        time.sleep(2)
        self.wait_for_element(self.language_list)
        self.wait_to_click(self.select_first_lang)
        time.sleep(2)
        lang = self.get_text(self.selected_lang_name)
        print("First language selected is: ", lang)
        self.wait_to_click(self.save_lang)
        time.sleep(2)
        self.wait_to_click(self.lang_input_textarea)
        time.sleep(2)
        self.wait_for_element(self.language_list)
        self.wait_to_click(self.select_second_lang)
        time.sleep(2)
        lang = self.get_text(self.selected_lang_name)
        print("Second language selected is: ", lang)
        self.wait_to_click(self.save_lang)
        time.sleep(1)
        self.wait_to_click((By.XPATH, self.delete_lang.format(lang)))
        time.sleep(1)
        self.wait_to_click(self.save_lang)
        time.sleep(2)
        print("Languages added and deleted successfully!")

    def remove_keyword(self):
        self.wait_to_click(self.keywords)
        self.wait_for_element(self.page_limit)
        self.select_by_value(self.page_limit, "50")
        time.sleep(10)
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
        self.wait_for_element(self.page_limit)
        self.select_by_value(self.page_limit, "50")
        time.sleep(10)
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

    def remove_all_keywords(self):
        self.wait_to_click(self.keywords)
        time.sleep(3)
        if self.is_present(self.page_empty):
            print("No keywords present")
        elif self.is_present(self.page_limit):
            self.select_by_value(self.page_limit, "50")
            time.sleep(3)
            list_keyword = self.find_elements(self.keywords_list)
            confirm_button_list = self.find_elements((By.XPATH, self.delete_confirm_button.format('KEYWORD_')))
            print("List Count: ", len(list_keyword))
            keyword_names = []
            if len(list_keyword) > 0:
                for i in range(len(list_keyword)):
                    text = list_keyword[i].text
                    keyword_names.append(text)
            print(keyword_names)
            if len(keyword_names) > 0:
                for i in range(len(keyword_names))[::-1]:
                    self.scroll_to_element((By.XPATH, self.keyword_delete_btn.format(keyword_names[i])))
                    self.js_click((By.XPATH, self.keyword_delete_btn.format(keyword_names[i])))
                    time.sleep(2)
                    self.wait_for_element((By.XPATH, self.delete_confirm_button.format(keyword_names[i])))
                    self.js_click((By.XPATH, self.delete_confirm_button.format(keyword_names[i])))
                    time.sleep(2)
                    list = self.find_elements(self.keywords_list)
                    confirm_button_list = self.find_elements((By.XPATH, self.delete_confirm_button.format('KEYWORD_')))
                    print("Updated List Count: ", len(list))
                self.driver.refresh()
                time.sleep(5)
                list = self.find_elements(self.keywords_list)
                if len(list) == 0:
                    print("All test keywords deleted")
                else:
                    print("All test keywords not deleted")
        else:
            print("No test keywords present")

    def remove_cond_alert(self):
        self.wait_and_sleep_to_click(self.cond_alerts)
        self.wait_to_clear_and_send_keys(self.search_box, self.cond_alert_name_input)
        self.wait_and_sleep_to_click(self.search_box)
        print("Sleeping till the alert processing completes")
        self.driver.refresh()
        self.wait_to_clear_and_send_keys(self.search_box, self.cond_alert_name_input)
        self.wait_and_sleep_to_click(self.search_box)
        self.wait_for_element((By.XPATH, self.delete_cond_alert.format(self.cond_alert_name_input)), 300)
        time.sleep(5)
        self.wait_to_click((By.XPATH, self.delete_cond_alert.format(self.cond_alert_name_input)))
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
            isPresent = self.is_displayed((By.XPATH, self.cond_alert_created.format(self.cond_alert_name_input)))
        except NoSuchElementException:
            isPresent = False
        assert not isPresent
        print("Cond Alert removed successfully!")

    def remove_alert_with_same_name(self, alert_name):
        self.wait_to_clear_and_send_keys(self.search_box, alert_name)
        self.wait_and_sleep_to_click(self.search_box)
        time.sleep(5)
        if self.is_present_and_displayed(self.empty_table_alert):
            print("No alert created with the same name")
        else:
            self.wait_to_click((By.XPATH, self.delete_cond_alert.format(self.cond_alert_name_input)))
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
                isPresent = self.is_displayed((By.XPATH, self.cond_alert_created.format(self.cond_alert_name_input)))
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

    # def project_settings_page(self, value=None):
    #     if value==True:
    #         self.switch_to_default_content()
    #         time.sleep(5)
    #     else:
    #         print("Value null")
    #     self.driver.get(self.dashboard_link)
    #     self.accept_pop_up()
    #     time.sleep(5)
    #     self.wait_for_element(self.settings_bar)
    #     self.click(self.settings_bar)
    #     self.wait_for_element(self.project_settings_menu)
    #     self.js_click(self.project_settings_menu)
    #     assert self.is_visible_and_displayed(
    #         self.project_settings_elements), "Project Settings page did not load successfully"
    #     print("Project Settings page loaded successfully!")

    def current_subscription_page(self):
        self.wait_to_click(self.settings_bar)
        self.wait_to_click(self.subscription_menu)
        assert self.is_visible_and_displayed(
            self.subscription_elements_id), "Subscription Page did not load successfully"
        print("Current Subscription page loaded successfully!")

    def remove_all_cond_alert(self):
        self.wait_to_click(self.cond_alerts)
        self.wait_for_element(self.value_per_page)
        self.select_by_value(self.value_per_page, "100")
        time.sleep(10)
        print("Sleeping till the alert list is displayed completely")
        alert_presence = self.is_present(self.cond_alerts_name)
        if alert_presence:
            while alert_presence:
                text = self.get_text(self.cond_alerts_name)
                print("alert name: ", text)
                self.wait_to_click((By.XPATH, self.cond_alert_delete_button.format(text, 1)))
                try:
                    obj = self.driver.switch_to.alert
                    obj.accept()
                except NoAlertPresentException:
                    raise AssertionError("Celery down")
                time.sleep(5)
                self.driver.refresh()
                time.sleep(7)
                alert_presence = self.is_present(self.cond_alerts_name)
        else:
            print("No script created cond alerts present")
        print("All Cond Alert removed successfully!")

    def create_cond_alert_for_doesnot_have_value(self):
        self.wait_to_click(self.cond_alerts)
        self.remove_alert_with_same_name(self.cond_alert_no_value_name_input)
        self.wait_to_click(self.add_cond_alert)
        self.send_keys(self.cond_alert_name, self.cond_alert_no_value_name_input)
        self.wait_to_click(self.continue_button_basic_tab)
        time.sleep(2)
        self.wait_to_click(self.case_type)
        self.select_by_text(self.case_type, UserData.case_reassign)
        time.sleep(3)
        self.wait_to_click(self.select_filter)
        self.wait_to_click(self.case_property_filter)
        time.sleep(2)
        self.wait_to_click(self.case_property_textbox)
        time.sleep(1)
        # self.send_keys(self.case_property_input, UserData.alert_case_property_random_value)
        self.wait_for_element(self.select_case_property)
        time.sleep(2)
        self.select_by_text(self.select_case_property, UserData.alert_case_property_random_value)
        self.select_by_text(self.select_match_type, UserData.alert_no_value)
        self.wait_to_click(self.continue_button_rule_tab)
        self.wait_for_element(self.recipients_select_cond_alert)
        self.select_by_value(self.recipients_select_cond_alert, "Owner")
        self.select_by_text(self.alert_type, "Email")
        self.send_keys(self.email_subject, "Test Alert for no value" + self.cond_alert_no_value_name_input)
        self.send_keys(self.broadcast_message, "Test Alert for no value:" + self.cond_alert_no_value_name_input)
        self.wait_to_click(self.save_button_xpath)
        print("Sleeping till the alert processing completes")
        time.sleep(360)
        self.driver.refresh()
        time.sleep(160)
        self.wait_to_clear_and_send_keys(self.search_box, self.cond_alert_no_value_name_input)
        time.sleep(10)
        self.wait_to_click(self.search_box)
        self.wait_for_element((By.XPATH, self.delete_cond_alert.format(self.cond_alert_no_value_name_input)), 700)
        self.driver.refresh()
        if self.is_clickable((By.XPATH, self.delete_cond_alert.format(self.cond_alert_no_value_name_input))):
            print("Restart is not required.")
        else:
            try:
                self.js_click((By.XPATH, self.restart_rule_button.format(self.cond_alert_no_value_name_input)))
                self.accept_pop_up()
                time.sleep(5)
                self.accept_pop_up()
                print("Sleeping till the alert processing completes")
                time.sleep(360)
                self.wait_to_clear_and_send_keys(self.search_box, self.cond_alert_no_value_name_input)
                self.wait_to_click(self.search_box)
                self.wait_for_element((By.XPATH, self.delete_cond_alert.format(self.cond_alert_no_value_name_input)), 700)
                self.driver.refresh()
            except:
                print("Restart not required")
        self.wait_for_element(self.search_box)
        self.wait_to_clear_and_send_keys(self.search_box, self.cond_alert_no_value_name_input)
        self.wait_to_click(self.search_box)
        assert self.is_displayed((By.XPATH, self.cond_alert_created.format(self.cond_alert_no_value_name_input))), "Conditional Alert not created successfully!"
        print("Conditional Alert created successfully!")
        subject = "Test Alert for no value" + self.cond_alert_no_value_name_input
        return self.cond_alert_no_value_name_input, subject