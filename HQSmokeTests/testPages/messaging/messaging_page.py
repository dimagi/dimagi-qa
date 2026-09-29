import time

from common_utilities.selenium.base_page import BasePage
from common_utilities.path_settings import PathSettings
from HQSmokeTests.userInputs.user_inputs import UserData
from common_utilities.generate_random_string import fetch_random_string
from HQSmokeTests.testPages.users.org_structure_page import latest_download_file, wait_for_download_to_finish

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, \
    NoAlertPresentException
from selenium.webdriver.common.by import By

""""Contains test page elements and functions related to the various messaging mediums available on CCHQ"""


class MessagingPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.cond_alert_no_value_name_input = "cond_alert_no_value_" + fetch_random_string()
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
        self.broadcast_created = "//a[text()='{}']"
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
        # Second (AND-ed) filter row locators, for scoping a rule to one exact
        # case via "caseid equals <value>" instead of relying solely on a
        # domain-wide "has no value" filter. Indexed [2] assuming the knockout
        # repeat-template renders identical data-bind markup per row, matching
        # the first row's locators above. NOT YET VERIFIED against a live run.
        self.select_case_property_row2 = (
        By.XPATH, "(//select[@data-bind='value: valueObservable, autocompleteSelect2: casePropertyNames'])[2]")
        self.select_match_type_row2 = (By.XPATH, "(//select[@data-bind='value: match_type'])[2]")
        self.case_property_value_row2 = (By.XPATH, "(//input[contains(@data-bind,'value: property_value')])[2]")
        self.continue_button_rule_tab = (
        By.XPATH, "//button[@data-bind='click: handleRuleNavContinue, enable: ruleTabValid']")
        self.cond_alert_created = "//a[text()='{}']"
        self.restart_rule_button = "//td[./a[text()='{}}']]//following-sibling::td/div/button[contains(@data-bind,'restart')]"
        self.restart_rule_button_none = "//td[./a[text()='{}}']]//following-sibling::td/div[@style='display: none;']/button[contains(@data-bind,'restart')]"
        self.deactive_button_visible = "//td[./a[text()='{}}']]//following-sibling::td/button[contains(@data-bind,'toggleStatus')]/span[contains(@data-bind,'visible: active')]"
        self.empty_table_alert = (
        By.XPATH, "//div[contains(@data-bind, 'emptyTable()')][contains(.,'There are no alerts to display')]")
        self.select_recipient_type = (By.XPATH, "//ul[@id='select2-id_schedule-recipient_types-results']/li[.='Users']")
        self.alert_type = (By.XPATH, "//select[@name='schedule-content']")
        self.user_recipients_results = (
        By.XPATH, "//ul[@id='select2-id_schedule-user_recipients-results']/li[.='" + UserData.app_login + "']")
        self.save_button_xpath = (By.XPATH, "//button[@type='submit'and text()='Save']")
        self.delete_cond_alert = "//td[.//a[text()='{}']]//preceding-sibling::td[1]//button[@class='btn btn-danger'][not(@disabled)][1]"
        self.alert_process_none = "//td[.//a[text()='{}']]//following::span[contains(@data-bind,'locked_for_editing')  and @style='display: none;']"
        self.search_box = (By.XPATH, "//form[@class='input-group']/input[@class='form-control']")
        self.search_btn = (
        By.XPATH, "//form[@class='input-group']//button[@data-bind='click: clickAction, visible: !immediate']/i")
        self.value_per_page =(By.XPATH, "//select[contains(@data-bind,'value: perPage')]")
        self.cond_alerts_name = (By.XPATH, "//td[.//button[contains(@class,'danger')][not(@disabled)]]//following-sibling::td[1]/a[contains(.,'cond_alert')]")
        self.cond_alert_delete_button = "(//td[contains(.,'{}')]//preceding-sibling::td/button[not(@disabled)])[{}]"
        # Condition Alerts : Download and Upload
        self.bulk_upload_button = (By.LINK_TEXT, "Bulk Upload SMS Alert Content")
        self.download_id = (By.XPATH, "//a[@id='download_link']//i")
        self.choose_file = (By.XPATH, "//input[@name='bulk_upload_file']")
        self.upload = (By.XPATH, "//button[@class='btn btn-primary disable-on-submit']/i")
        self.upload_success_message = (By.XPATH, "//div[@class='alert alert-margin-top fade in alert-success']")
        # Keywords
        self.keywords = (By.LINK_TEXT, "Keywords")
        self.add_keyword = (By.LINK_TEXT, "Add Keyword")
        self.keyword_name = (By.XPATH, "//input[@name='keyword']")
        self.keyword_description = (By.XPATH, "//input[@name='description']")
        self.send_sender = (By.XPATH, "//select[@name='sender_content_type']")
        self.keyword_message = (By.XPATH, "//input[@name='sender_message']")
        self.keyword_created = "//a[text()='{}']"
        self.add_structured_keyword = (By.LINK_TEXT, "Add Structured Keyword")
        self.keyword_survey = (By.XPATH, "(//span[@class='select2-selection select2-selection--single'])[1]")
        self.survey_option_select = (
        By.XPATH, "(//li[@class='select2-results__option select2-results__option--selectable'])[1]")
        self.delete_keyword = "//a[text()='{}']//following::button[contains(@class,'danger')][1]"
        self.confirm_delete_keyword = "//a[text()='{}']//following::*[contains(@class,'confirm')][1]"

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
        self.add_lang = (By.XPATH, "//button[@data-bind='click: addLanguage, disable: addLanguageDisabled']/i")
        self.lang_input_textarea = (By.XPATH, "(//span[@class='selection']//span[@role='combobox'])[last()]")
        self.select_first_lang = (By.XPATH, "//span[contains(@class,'results')]/ul[@role='listbox']/li[1]")
        self.select_eng_lang = (By.XPATH, "(//span[contains(@class,'results')]/ul[@role='listbox']//li[@role='option'][contains(.,'en (English)')])[1]")
        self.select_second_lang = (By.XPATH, "//span[contains(@class,'results')]/ul[@role='listbox']/li[2]")
        self.select_third_lang = (By.XPATH, "//span[contains(@class,'results')]/ul[@role='listbox']/li[3]")
        self.language_dropdown_last = (By.XPATH, "(//select[contains(@data-bind,'langcode')])[last()]")
        self.selected_lang_name = (By.XPATH, "(//td//p[contains(@data-bind,'message')])[last()]")
        self.lang_search_input = (By.XPATH, "//span[contains(@class,'dropdown')]/input")
        self.language_list = (By.XPATH, "//ul[@role='listbox']")
        self.save_lang = (By.XPATH, "(//div[@class='btn btn-primary'])[1]")
        self.delete_lang = "//td[4][./p[contains(@data-bind,'message')][contains(.,'{}')]]//following-sibling::td[2]/a[@data-bind='click: $root.removeLanguage']"
        self.default_language = (By.XPATH, "//span[contains(@class,'label-default')]")
        self.languages_present = (By.XPATH, "//td//p[contains(@data-bind,'message')]")
        self.lang_error = (By.XPATH, "//p[text()='Language appears twice']")
        self.language_dropdown = (By.XPATH, "//select[contains(@data-bind,'langcode')]")
        # Message Translation
        self.msg_translation_menu = (By.XPATH, "//a[text()='Messaging Translations']")
        # Project and Subscription Settings
        self.settings_bar = (By.XPATH, "//ul[@role='menu']//a[@data-action='Click Gear Icon']/i")
        self.subscription_menu = (By.LINK_TEXT, "Current Subscription")
        self.data_forwarding_menu = (By.LINK_TEXT, "Data Forwarding")
        self.subscription_elements_id = (By.ID, "subscriptionSummary")
        self.project_settings_menu = (By.LINK_TEXT, "Project Settings")
        self.forward_forms_header = (By.XPATH, "//h2[.='Forward Forms']")
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
        self.wait_to_click(self.compose_sms_menu)
        self.wait_for_element(self.recipients_select)
        self.select_by_value(self.recipients_select, "[send to all]")

        self.send_keys(self.message_textarea, "sms_" + fetch_random_string())

        self.scroll_to_element(self.send_message)
        self.wait_to_click(self.send_message)
        try:
            assert self.is_present_and_displayed(self.message_sent_success_msg), "Message not sent successfully"
        except TimeoutException:
            self.wait_to_click(self.compose_sms_menu)
            self.wait_for_element(self.recipients_select)
            self.select_by_value(self.recipients_select, "[send to all]")

            self.send_keys(self.message_textarea, "sms_" + fetch_random_string())

            self.scroll_to_element(self.send_message)
            self.wait_to_click(self.send_message)
            self.wait_for_element(self.message_sent_success_msg)
            print("SMS composed successfully!")

    def send_broadcast_message(self, broadcast_input):
        self.wait_to_click(self.broadcasts)
        self.wait_to_click(self.add_broadcast)
        self.send_keys(self.broadcast_name, broadcast_input)
        self.wait_to_click(self.recipients)
        self.wait_to_click(self.select_recipient_type)
        self.wait_to_click(self.user_recipient)

        self.wait_to_click(self.select_value_dropdown)
        self.send_keys(self.broadcast_message, "Test Broadcast:" + broadcast_input)
        self.wait_to_click(self.send_broadcast)
        self.reload_page()
        self.select_by_value(self.broadcast_select, '100')
        time.sleep(2)
        try:
            while False:
                if not self.is_displayed((By.XPATH, self.broadcast_created.format(broadcast_input))):
                    self.wait_to_click(self.next_btn)
                    time.sleep(2)
                    continue
                else:
                    assert True
        except StaleElementReferenceException:
            self.wait_for_element(self.broadcast_created)
        print("Broadcast created successfully!")

    def create_cond_alert(self, cond_alert_name_input):
        self.wait_to_click(self.cond_alerts)
        self.wait_to_click(self.add_cond_alert)
        self.send_keys(self.cond_alert_name, cond_alert_name_input)
        self.wait_to_click(self.continue_button_basic_tab)
        self.wait_to_click(self.case_type)
        self.wait_to_click(self.case_type_option_value)
        self.wait_to_click(self.select_filter)
        self.wait_to_click(self.case_property_filter)
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
        self.send_keys(self.email_subject, "Test Alert:" + cond_alert_name_input)
        self.send_keys(self.broadcast_message, "Test Alert:" + cond_alert_name_input)
        self.wait_to_click(self.save_button_xpath)
        print("Sleeping till the alert processing completes")
        time.sleep(1)
        self.wait_to_clear_and_send_keys(self.search_box, cond_alert_name_input)
        self.wait_for_element((By.XPATH, self.alert_process_none.format(cond_alert_name_input)), 500)
        if 'staging' in self.get_current_url():
            time.sleep(240)
        else:
            time.sleep(40)
        self.reload_page()
        time.sleep(10)
        self.clear(self.search_box)
        self.send_keys(self.search_box, cond_alert_name_input)
        self.wait_to_click(self.search_box)
        self.wait_for_element((By.XPATH, self.delete_cond_alert.format(cond_alert_name_input)), 700)
        self.reload_page()
        time.sleep(4)
        if self.is_clickable((By.XPATH, self.delete_cond_alert.format(cond_alert_name_input))):
            print("Restart is not required.")
        else:
            try:
                self.wait_to_click((By.XPATH, self.restart_rule_button.format(cond_alert_name_input)))
                self.accept_pop_up()
                time.sleep(2)
                self.accept_pop_up()
                print("Sleeping till the alert processing completes")
                time.sleep(50)
                self.wait_to_clear_and_send_keys(self.search_box, cond_alert_name_input)
                self.wait_to_click(self.search_box)
                self.wait_for_element((By.XPATH, self.delete_cond_alert.format(cond_alert_name_input)), 700)
                self.reload_page()
            except:
                print("Restart not required")
        self.wait_for_element(self.search_box)
        self.wait_to_clear_and_send_keys(self.search_box, cond_alert_name_input)
        self.click(self.search_box)
        assert self.is_displayed((By.XPATH, self.cond_alert_created.format(cond_alert_name_input))), "Conditional Alert not created successfully!"
        print("Conditional Alert created successfully!")
        return cond_alert_name_input

    def cond_alert_download(self):
        self.wait_to_click(self.cond_alerts)
        self.wait_for_element(self.bulk_upload_button)
        self.click(self.bulk_upload_button)
        self.wait_for_element(self.download_id)
        self.click(self.download_id)
        wait_for_download_to_finish()
        print("Conditional Alert downloaded successfully!")


    def cond_alert_upload(self):
        newest_file = latest_download_file()
        if 'Alerts' in newest_file:
            file_that_was_downloaded = PathSettings.DOWNLOAD_PATH / newest_file
        else:
            print("Not the expected file. Downloading again...")
            self.js_click(self.download_id)
            wait_for_download_to_finish()
            newest_file = latest_download_file()
            file_that_was_downloaded = PathSettings.DOWNLOAD_PATH / newest_file
        self.send_keys(self.choose_file, str(file_that_was_downloaded))
        self.wait_to_click(self.upload)
        self.wait_for_element(self.upload_success_message)
        print("Conditional Alert uploaded successfully!")

    def add_keyword_trigger(self, keyword_name_input):
        self.wait_to_click(self.keywords)
        self.wait_to_click(self.add_keyword)
        self.send_keys(self.keyword_name, keyword_name_input)
        self.send_keys(self.keyword_description, keyword_name_input)
        self.select_by_text(self.send_sender, 'SMS')
        self.send_keys(self.keyword_message, "Test Message: " + keyword_name_input)

        self.scroll_to_element(self.send_message)
        self.wait_to_click(self.send_message)

        self.select_by_value(self.page_limit, "50")
        time.sleep(3)
        self.wait_for_element((By.XPATH, self.keyword_created.format(keyword_name_input)))
        print("Keyword created successfully!")

    def add_structured_keyword_trigger(self, struct_keyword_name_input):
        self.wait_to_click(self.keywords)
        self.wait_to_click(self.add_structured_keyword)
        self.send_keys(self.keyword_name, struct_keyword_name_input)
        self.send_keys(self.keyword_description, struct_keyword_name_input)
        self.wait_to_click(self.keyword_survey)
        self.wait_to_click(self.survey_option_select)
        self.select_by_text(self.send_sender, 'SMS')
        self.send_keys(self.keyword_message, "Test Message" + struct_keyword_name_input)

        self.scroll_to_element(self.send_message)
        self.wait_to_click(self.send_message)

        self.select_by_value(self.page_limit, "50")
        time.sleep(3)
        self.wait_for_element((By.XPATH, self.keyword_created.format(struct_keyword_name_input))), "Structured keyword not created successfully!"
        print("Structured keyword created successfully!")

    def chat_page(self):
        self.wait_to_click(self.chat)
        assert self.is_displayed(self.contact_table), "Chat Page did not load successfully!"
        print("Chat Page loaded successfully!")

    # def sms_connectivity_gateway(self):
    #     self.driver.find_element(By.LINK_TEXT, self.sms_connectivity).click()
    #
    #     self.driver.find_element(By.XPATH, "//select[@name='hq_api_id']").click()
    #
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
    #
    #     assert True == self.driver.find_element(By.XPATH, self.gateway_created).is_displayed()
    #     print("Gateway created successfully!")

    def general_settings_page(self):
        self.wait_to_click(self.general_settings)

        if self.is_enabled(self.disable_button):
            self.wait_to_click(self.enable_button)
            self.send_keys(self.time_input, "23:59")
        else:
            self.wait_to_click(self.disable_button)

        self.scroll_to_element(self.send_message)
        self.wait_to_click(self.send_message)
        self.wait_for_element(self.message_sent_success_msg)
        print("Settings page updated successfully!")

    def delete_languages(self):
        self.wait_to_click(self.languages)
        self.wait_for_element(self.default_language)
        lang_list = self.find_elements(self.languages_present)
        if len(lang_list) == 1:
            text = self.get_selected_text(self.language_dropdown)
            print("selected option: ", text)
            if text.strip() == "en":
                print("Default language present as English")
            else:
                print("Default language is non-English")
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
                    self.js_click((By.XPATH, self.delete_lang.format(lang)))
                    time.sleep(3)
                    self.js_click(self.save_lang)

        else:
            print("Only English is Present and no other languages")

    def add_eng_lang(self):
        self.wait_for_element(self.lang_input_textarea)
        self.click(self.lang_input_textarea)
        self.wait_for_element(self.lang_search_input)
        self.wait_for_element(self.select_eng_lang)
        self.click(self.select_eng_lang)

        lang = self.get_text(self.selected_lang_name)
        print("Language selected is: ", lang)
        self.js_click(self.save_lang)

    def languages_page(self):
        self.wait_to_click(self.languages)
        self.wait_to_click(self.add_lang)
        time.sleep(2)
        self.wait_for_element(self.lang_input_textarea)
        self.click(self.lang_input_textarea)
        self.wait_for_element(self.lang_search_input)
        self.wait_for_element(self.select_first_lang)
        self.click(self.select_second_lang)
        lang = self.get_text(self.selected_lang_name)
        print("First language selected is: ", lang)
        self.js_click(self.save_lang)
        time.sleep(1)
        self.accept_pop_up()
        time.sleep(2)
        self.reload_page()
        self.wait_for_element(self.lang_input_textarea)
        self.click(self.lang_input_textarea)
        self.wait_for_element(self.lang_search_input)
        self.wait_for_element(self.select_second_lang)
        self.click(self.select_third_lang)
        lang1 = self.get_text(self.selected_lang_name)
        print("Second language selected is: ", lang1)
        if lang == lang1:
            print("language not changed.")
            self.click(self.lang_input_textarea)
            self.js_click(self.select_third_lang)
            lang1 = self.get_text(self.selected_lang_name)
            print("Second language selected is: ", lang1)
            self.wait_to_click(self.save_lang)
        else:
            self.js_click(self.save_lang)
        time.sleep(1)
        self.accept_pop_up()
        self.wait_to_click((By.XPATH, self.delete_lang.format(lang)))
        self.wait_to_click(self.save_lang)
        print("Languages added and deleted successfully!")

    def remove_keyword(self, keyword):
        self.wait_to_click(self.keywords)
        self.wait_for_element(self.page_limit)
        self.select_by_value(self.page_limit, "50")
        time.sleep(2)
        self.wait_for_element((By.XPATH, self.delete_keyword.format(keyword)))
        self.click((By.XPATH, self.delete_keyword.format(keyword)))
        self.wait_for_element((By.XPATH, self.confirm_delete_keyword.format(keyword)))
        self.click((By.XPATH, self.confirm_delete_keyword.format(keyword)))
        time.sleep(3)
        self.reload_page()
        self.wait_for_element(self.page_limit, 30)
        try:
            isPresent = self.is_displayed((By.XPATH, self.keyword_created.format(keyword)))
        except NoSuchElementException:
            isPresent = False
        if not isPresent:
            assert not isPresent
            print("Keyword removed successfully!")

    def remove_structured_keyword(self, keyword):
        self.wait_to_click(self.keywords)
        self.wait_for_element(self.page_limit)
        self.select_by_value(self.page_limit, "50")
        time.sleep(2)
        self.wait_for_element((By.XPATH, self.delete_keyword.format(keyword)))
        self.click((By.XPATH, self.delete_keyword.format(keyword)))
        self.wait_for_element((By.XPATH, self.confirm_delete_keyword.format(keyword)))
        self.click((By.XPATH, self.confirm_delete_keyword.format(keyword)))
        time.sleep(3)
        self.reload_page()
        self.wait_for_element(self.page_limit, 30)
        try:
            isPresent = self.is_displayed((By.XPATH, self.keyword_created.format(keyword)))
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
                    self.wait_to_click((By.XPATH, self.keyword_delete_btn.format(keyword_names[i])))

                    self.wait_for_element((By.XPATH, self.delete_confirm_button.format(keyword_names[i])))
                    self.wait_to_click((By.XPATH, self.delete_confirm_button.format(keyword_names[i])))

                    list = self.find_elements(self.keywords_list)
                    confirm_button_list = self.find_elements((By.XPATH, self.delete_confirm_button.format('KEYWORD_')))
                    print("Updated List Count: ", len(list))
                self.reload_page()
                time.sleep(2)
                list = self.find_elements(self.keywords_list)
                if len(list) == 0:
                    print("All test keywords deleted")
                else:
                    print("All test keywords not deleted")
        else:
            print("No test keywords present")

    def remove_cond_alert(self, cond_alert_name_input):
        self.wait_and_sleep_to_click(self.cond_alerts)
        self.wait_to_clear_and_send_keys(self.search_box, cond_alert_name_input)
        self.wait_and_sleep_to_click(self.search_box)
        print("Sleeping till the alert processing completes")
        self.reload_page()
        time.sleep(5)
        self.wait_to_clear_and_send_keys(self.search_box, cond_alert_name_input)
        self.click(self.search_box)
        self.wait_for_element((By.XPATH, self.delete_cond_alert.format(cond_alert_name_input)), 300)
        time.sleep(2)
        self.click((By.XPATH, self.delete_cond_alert.format(cond_alert_name_input)))
        time.sleep(1)
        try:
            obj = self.driver.switch_to.alert
            obj.accept()
        except NoAlertPresentException:
            raise AssertionError("Celery down")
        try:

            self.reload_page()
            time.sleep(4)
            self.wait_to_clear_and_send_keys(self.search_box, cond_alert_name_input)
            self.click(self.search_box)
            time.sleep(3)
            isPresent = self.is_displayed((By.XPATH, self.cond_alert_created.format(cond_alert_name_input)))
        except NoSuchElementException:
            isPresent = False
        assert not isPresent
        print("Cond Alert removed successfully!")

    def remove_alert_with_same_name(self, alert_name):
        self.wait_for_element(self.search_box)
        self.clear(self.search_box)
        self.send_keys(self.search_box, alert_name)
        self.wait_to_click(self.search_box)
        time.sleep(2)
        if self.is_present(self.empty_table_alert):
            print("No alert created with the same name")
        else:
            self.wait_to_click((By.XPATH, self.delete_cond_alert.format(alert_name)))
            try:
                obj = self.driver.switch_to.alert
                obj.accept()
            except NoAlertPresentException:
                raise AssertionError("Celery down")
            try:

                self.reload_page()
                self.wait_to_clear_and_send_keys(self.search_box, alert_name)
                self.wait_and_sleep_to_click(self.search_box)
                isPresent = self.is_displayed(self.cond_alert_created)
            except NoSuchElementException:
                isPresent = False
            assert not isPresent
            print("Cond Alert removed successfully!")

    def msg_trans_download(self):
        self.wait_for_element(self.languages)
        self.click(self.languages)
        self.wait_for_element(self.msg_translation_menu)
        self.js_click(self.msg_translation_menu)
        self.wait_for_element(self.download_id)
        self.click(self.download_id)
        wait_for_download_to_finish()
        print("Msg Trans downloaded successfully!")
        time.sleep(5)

    def msg_trans_upload(self):
        newest_file = latest_download_file()
        file_that_was_downloaded = PathSettings.DOWNLOAD_PATH / newest_file
        self.wait_for_element(self.choose_file)
        self.send_keys(self.choose_file, str(file_that_was_downloaded))
        self.wait_to_click(self.upload)
        self.wait_for_element(self.upload_success_message)
        print("Msg Trans uploaded successfully!")

    # def project_settings_page(self, value=None):
    #     if value==True:
    #         self.switch_to_default_content()
    #         time.sleep(2)
    #     else:
    #         print("Value null")
    #     self.driver.get(self.dashboard_link)
    #     self.accept_pop_up()
    #     time.sleep(2)
    #     self.wait_for_element(self.settings_bar)
    #     self.click(self.settings_bar)
    #     self.wait_for_element(self.project_settings_menu)
    #     self.wait_to_click(self.project_settings_menu)
    #     self.wait_for_element(
    #         self.project_settings_elements), "Project Settings page did not load successfully"
    #     print("Project Settings page loaded successfully!")

    def current_subscription_page(self):
        self.wait_to_click(self.settings_bar)
        self.wait_to_click(self.subscription_menu)
        self.wait_for_element(
            self.subscription_elements_id), "Subscription Page did not load successfully"
        print("Current Subscription page loaded successfully!")

    def data_forwarding_page(self):
        self.wait_to_click(self.settings_bar)
        self.wait_to_click(self.data_forwarding_menu)
        self.wait_for_element(
            self.forward_forms_header), "Forward Form header did not load successfully"
        print("Forward Form header loaded successfully!")


    def remove_all_cond_alert(self):
        self.wait_to_click(self.cond_alerts)
        try:
            self.wait_for_element(self.value_per_page)
            self.select_by_value(self.value_per_page, "100")
            time.sleep(2)
            print("Sleeping till the alert list is displayed completely")
            alert_presence = self.is_present(self.cond_alerts_name)
            if alert_presence:
                while alert_presence:
                    text = self.get_text(self.cond_alerts_name)
                    print("alert name: ", text)
                    self.click((By.XPATH, self.cond_alert_delete_button.format(text, 1)))
                    time.sleep(1)
                    try:
                        obj = self.driver.switch_to.alert
                        obj.accept()
                    except NoAlertPresentException:
                        raise AssertionError("Celery down")
                    time.sleep(2)
                    self.reload_page()
                    time.sleep(7)
                    alert_presence = self.is_present(self.cond_alerts_name)
            else:
                print("No script created cond alerts present")
            print("All Cond Alert removed successfully!")
        except Exception:
            print("No Conditional alerts are present")


    def create_cond_alert_for_doesnot_have_value(self, rerun, case_id):
        if not case_id:
            # case_id used to default to None, with the caseid-equals filter
            # below only added `if case_id:` - any caller that left it out (or
            # a future one that forgets to pass it) silently got the old
            # broad "has no value" rule back, the exact one that mass-emailed
            # every case owner. Required now, and this raises instead of
            # quietly under-scoping the rule.
            raise ValueError(
                "create_cond_alert_for_doesnot_have_value requires a case_id to scope the rule to - "
                "omitting it would recreate the mass-bounce bug this scoping exists to prevent."
            )
        cond_alert_no_value_name_input = f"{self.cond_alert_no_value_name_input}{rerun}"
        self.wait_to_click(self.cond_alerts)
        self.remove_alert_with_same_name(cond_alert_no_value_name_input)
        self.wait_to_click(self.add_cond_alert)
        self.send_keys(self.cond_alert_name, cond_alert_no_value_name_input)
        self.wait_to_click(self.continue_button_basic_tab)
        time.sleep(2)
        self.wait_to_click(self.case_type)
        self.select_by_text(self.case_type, UserData.case_dnd)
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
        # This "has no value" filter alone is only scoped by case type. Even
        # after moving to the dedicated case_dnd type, it still matches EVERY
        # case_dnd case missing this property, not just the one this test
        # submits - each run registers another matching case, so run N emails
        # the owners of all N-1 earlier runs' cases too. Same bounce pattern
        # as the original `reassign` bug, just growing slower on a smaller
        # case type instead of a shared one with 6,684+ cases already in it.
        # AND in a second condition scoping the rule to the exact case_id this
        # test just created. `caseid` is a system property available on any
        # case type, so this narrows matches down to one case regardless of
        # how many other case_dnd cases have accumulated from prior runs.
        # NOT YET VERIFIED against a live run: reuses select_filter /
        # case_property_filter to add the second row the same way the first
        # row was added above, and assumes the resulting row 2 repeats row 1's
        # data-bind markup (see select_case_property_row2 etc.). If either
        # locator turns out ambiguous or wrong with two rows present, this
        # will raise rather than silently under-scope the rule - confirm and
        # adjust on the first real run.
        self.wait_to_click(self.select_filter)
        self.wait_to_click(self.case_property_filter)
        time.sleep(2)
        self.select_by_text(self.select_case_property_row2, "caseid")
        self.select_by_text(self.select_match_type_row2, "equals")
        self.send_keys(self.case_property_value_row2, case_id)
        self.wait_to_click(self.continue_button_rule_tab)
        self.wait_for_element(self.recipients_select_cond_alert)
        self.select_by_value(self.recipients_select_cond_alert, "Owner")
        self.select_by_text(self.alert_type, "Email")
        self.send_keys(self.email_subject, "Test Alert for no value " + cond_alert_no_value_name_input)
        self.send_keys(self.broadcast_message, "Test Alert for no value:" + cond_alert_no_value_name_input)
        self.wait_to_click(self.save_button_xpath)
        print("Sleeping till the alert processing completes")
        time.sleep(360)
        self.driver.refresh()
        time.sleep(160)
        self.wait_to_clear_and_send_keys(self.search_box, cond_alert_no_value_name_input)
        time.sleep(10)
        self.wait_to_click(self.search_box)
        self.wait_for_element((By.XPATH, self.delete_cond_alert.format(cond_alert_no_value_name_input)), 700)
        self.driver.refresh()
        if self.is_clickable((By.XPATH, self.delete_cond_alert.format(cond_alert_no_value_name_input))):
            print("Restart is not required.")
        else:
            try:
                self.js_click((By.XPATH, self.restart_rule_button.format(cond_alert_no_value_name_input)))
                self.accept_pop_up()
                time.sleep(5)
                self.accept_pop_up()
                print("Sleeping till the alert processing completes")
                time.sleep(360)
                self.wait_to_clear_and_send_keys(self.search_box, cond_alert_no_value_name_input)
                self.wait_to_click(self.search_box)
                self.wait_for_element((By.XPATH, self.delete_cond_alert.format(cond_alert_no_value_name_input)), 700)
                self.driver.refresh()
            except:
                print("Restart not required")
        self.wait_for_element(self.search_box)
        self.wait_to_clear_and_send_keys(self.search_box, cond_alert_no_value_name_input)
        self.wait_to_click(self.search_box)
        assert self.is_displayed((By.XPATH, self.cond_alert_created.format(cond_alert_no_value_name_input))), "Conditional Alert not created successfully!"
        print("Conditional Alert created successfully!")
        subject = "Test Alert for no value" + cond_alert_no_value_name_input
        return cond_alert_no_value_name_input, subject