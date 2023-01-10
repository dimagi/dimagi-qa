import time
import random
import re

from selenium.webdriver.common.keys import Keys

from Formplayer.testPages.webapps.webapps_basics import WebAppsBasics
from common_utilities.generate_random_string import fetch_random_string, fetch_phone_number, fetch_random_digit, \
    fetch_random_digit_with_range
from common_utilities.selenium.base_page import BasePage
from Formplayer.userInputs.user_inputs import UserData

from selenium.webdriver.common.by import By

""""Contains test page elements and functions related to the WebApps Access/Basics of Commcare"""


class BasicTestAppPreview(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.name_input1 = "basic test1 " + fetch_random_string()
        self.name_input2 = "basic test2 " + fetch_random_string()
        self.name_input3 = "basic test3 " + fetch_random_string()
        self.changed_name_input = "basic test changed " + fetch_random_string()
        self.case_reg_neg = "app_negcase_" + fetch_random_string()
        self.case_reg_pos = "app_poscase_" + fetch_random_string()
        self.subcase_pos = "sub_case" + fetch_random_string()
        self.unicode_text = "Unicode_app_" + fetch_random_string() + UserData.unicode
        self.update_unicode = fetch_random_string() + UserData.unicode_new

        self.test_question = "Test " + fetch_random_string()
        self.input_dict = {
            "phone": fetch_phone_number(),
            "Singleselect": "A",
            "Multiselect": ["A", "C"],
            "Text": "text update" + fetch_random_string(),
            "intval": fetch_random_digit_with_range(1, 30)
        }
        self.application_menu_id = (By.LINK_TEXT, "Applications")

        self.back_button = (By.XPATH, "//i[@class ='fa fa-chevron-left']")
        self.form_list = (By.XPATH, "//tbody[@class='menus-container']")
        self.refresh_button = (By.XPATH, "//button[contains(@class,'btn-preview-refresh js-preview-refresh')]")
        self.toggle_button = (By.XPATH, "//button[contains(@class ,'js-preview-toggle-tablet-view')]")
        self.sync_button = (By.XPATH, "//div[@class='js-sync-item appicon appicon-sync']")
        self.start_option = (By.XPATH, "//div[@class= 'js-start-app appicon appicon-start']")
        self.settings_option = (By.XPATH, "//div[@class = 'js-settings appicon appicon-settings']/i")
        self.login_as_option = (By.XPATH, "//div[@class='js-restore-as-item appicon appicon-restore-as']")
        self.incomplete_form = (By.XPATH, "//div[@class='js-incomplete-sessions-item appicon appicon-incomplete']")

        self.case_list_menu = "//h3[contains(text(), '{}')]"
        self.registration_form = "//h3[contains(text(), '{}')]"
        self.followup_form = (By.XPATH, "//h3[contains(text(), 'Followup Form')]")
        self.name_question = (By.XPATH,
                              "//label[.//span[.='Enter a Name']]/following-sibling::div//textarea[contains(@class,'textfield form-control')]")
        self.incomplete_form_list = (By.XPATH, "//tr[@class='formplayer-request']")
        self.incomplete_list_count = (By.XPATH, "//ul/li[@data-lp]")
        self.delete_incomplete_form = "(//tr[@class='formplayer-request']/descendant::div[@aria-label='Delete form'])[{}]"
        self.edit_incomplete_form = (
            By.XPATH, "(//tr[@class='formplayer-request']/descendant::div//i[contains(@class,'fa fa-pencil')])[1]")
        self.click_today_date = (By.XPATH, "//a[@data-action='today']")
        self.close_date_picker = (By.XPATH, "//a[@data-action='close']")
        self.mobileno_question = (By.XPATH, "//label[.//span[text()='Mobile No.']]/following-sibling::div//input")
        self.submit_form_button = (By.XPATH, "//div/button[text()='Submit']")

        self.next_question = (By.XPATH, "//button[contains(@data-bind,'nextQuestion')]")
        self.complete_form = (By.XPATH, "//button[@data-bind='visible: atLastIndex(), click: submitForm']")
        self.success_message = (By.XPATH, "//p[text()='Form successfully saved!']")
        self.view_form_link = (By.LINK_TEXT, "this form")
        self.export_form_link = (By.LINK_TEXT, "form")
        self.last_form = (
            By.XPATH, "(//ul[contains(@class,'appnav-menu-nested')]//div[contains(@class,'appnav-item')])[last()]")
        self.delete_form = (By.XPATH, "(//div[contains(@class,'appnav-item')]/a[@class='appnav-delete']/i)[last()]")
        self.delete_confirm_button = (
            By.XPATH, "(//div[contains(@id,'form_confirm_delete')]//button/i[@class='fa fa-trash'])[last()]")
        self.question_display_text = (By.XPATH, "//span[text()='Name (es)']")
        self.iframe = (By.CLASS_NAME, "preview-phone-window")
        self.home_button = (By.XPATH, "//li[./i[@class='fa fa-home']]")
        self.full_menu = (By.LINK_TEXT, "Show Full Menu")
        self.delete_confirm = (By.ID, 'js-confirmation-confirm')
        self.submitted_value = "(//tbody//td[2]/div[contains(.,'{}')])[1]"
        self.table_data = (By.XPATH, "(//tbody//td[2]/div[contains(@class,'data-raw')])[1]")

        self.data_preview = (By.XPATH, "//button[contains(@aria-label,'Data Preview')]")
        self.xpath_textarea = (By.XPATH, "//textarea[@placeholder='XPath Expression']")
        self.no_queries = (By.XPATH, "//i[.='No recent queries']")
        self.recent_query = "//tbody[@data-bind='foreach: recentXPathQueries']//td/span[.='{}']"
        self.query_table = (By.XPATH, "//tbody[@data-bind='foreach: recentXPathQueries']")
        self.evaluate_button = (By.XPATH, "(//input[@value='Evaluate'])[1]")

        # Groups
        self.choose_radio_button = "//label[.//span[contains(.,'{}')]]//following-sibling::div//input[@value='{}']"
        self.county_options = "//label[.//span[contains(.,'If you select')]]//following-sibling::div//input[@value='{}']"
        self.radio_button = "//div//input[@value='{}']"
        self.display_new_text_question = (
            By.XPATH, "//span[./p[.='Display a new text question']]/preceding-sibling::input")
        self.display_new_multiple_choice_question = (
            By.XPATH, "//span[./p[.='Display a new multiple choice question']]/preceding-sibling::input")
        self.text_question = (By.XPATH, "//textarea[@class='textfield form-control vertical-resize']")
        self.clear_button = (By.XPATH, "//button[contains(@data-bind,'Clear')]")
        self.display_new_multiple_choice_question = (
            By.XPATH, "//span[./p[.='Display a new multiple choice question']]/preceding-sibling::input")
        self.multiple_choice_response = (By.XPATH,
                                         "//label[.//span[contains(.,'Display a new multiple choice question')]]//following-sibling::div//input[contains(@value,'Other')]")
        self.pop_up_message = "//span[@class='caption webapp-markdown-output'][.='{}']"

        # eofn
        self.text_area_field = "//label[.//span[.='{}']]//following-sibling::div//textarea"
        self.input_field = "//label[.//span[.='{}']]//following-sibling::div//input"
        self.breadcrumbs = "//h1[@class='page-title'][.='{}']"
        self.search_input = (By.XPATH, "//input[@id='searchText']")
        self.search_button = (By.XPATH, "//button[@id='case-list-search-button']")
        self.module_search = "//td[.='{}']"
        self.continue_button = (By.XPATH, "//button[.='Continue']")
        self.module_badge_table = (By.XPATH, "//table[contains(@class, 'module-table-case-list')]")

        # contraints
        self.success_check = (By.XPATH, "//i[@class='fa fa-check text-success']")
        self.warning = (By.XPATH, "//i[@class='fa fa-warning text-danger clickable']")
        self.error_message = "//div[contains(@data-bind,'serverError')][.={}]"
        self.location_alert = (By.XPATH,
                               "//div[contains(.,'Without access to your location, computations that rely on the here() function will show up blank.')][contains(@class,'alert')]")

        # casetest
        self.case_detail_tab = "//a[.='Case Details {}']"
        self.case_detail_table = "//th[.='{}']/following-sibling::td[.='{}']"
        self.case_detail_table_list = (By.XPATH, "//div[@class='js-detail-content']/table/tr")
        self.search_location_button = (By.XPATH, "//button[.='Search']")
        self.blank_latitude = (By.XPATH, "//td[@class='lat coordinate'][contains(.,'??')]")
        self.output = (By.XPATH, "//span[@class='caption webapp-markdown-output']")
        self.empty_list = (By.XPATH, "//div[@class='alert alert-info'][.='List is empty.']")

        # Maps
        self.location_input = (By.XPATH, "//input[@class='query form-control']")
        self.location_search_button = (By.XPATH, "//button[@class ='btn btn-default search']")
        self.submit_form_button_2 = (By.XPATH, "//button[contains(@data-bind,'enable: enableSubmitButton')]")
        self.clear_map = (By.XPATH, "//button[contains(@data-bind,'click: onClear')]")

        # toggle off one question per screen
        self.settings_option = (By.XPATH, "//div[@class = 'js-settings appicon appicon-settings']/i")
        self.turn_on_one_question_toggle_button = (By.XPATH, "//div[contains(@class,'bootstrap-switch-on')]")
        self.toggle_button_one_question = (
            By.XPATH, "//th[(text()='Use one question per screen')]/following-sibling::td//input")
        self.done_button = (By.XPATH, "//button[@class = 'btn btn-primary js-done']")

        # Sub Menu
        self.parent_menu = (By.XPATH, "//h3[contains(text(),'Parent Menu')]")
        self.parent_survey = (By.XPATH, "//h3[contains(text(),'Survey under parent menu')]")
        self.child_menu = (By.XPATH, "//h3[contains(text(),'Child Menu')]")
        self.visible_child_survey = (By.XPATH, "//h3[contains(text(),'Visible survey under child')]")
        self.submit_survey_button = (By.XPATH, "//button[@class= 'submit btn btn-primary']")
        self.child_survey_under_child_menu = (By.XPATH, "//h3[contains(text(),'Survey under child menu')]")

        # Multimedia App Logo & Menu and Forms
        self.multimedia_app_logo = (
            By.XPATH, "//div/i[@class='fcc appicon-custom appicon-icon']/following::div/h3[text()='Multimedia']")
        self.multimedia_app = (By.XPATH, "//h3[text()='Multimedia']")
        self.formplayer_tests_menu_icon = (
            By.XPATH, "//td[./h3[.='Formplayer Tests']]/preceding-sibling::td/div[contains(@style,'module3')]")
        self.formplayer_tests_audio_icon = (By.XPATH,
                                            "//h3[text()='Formplayer Tests']/following-sibling::div/div/i[@class='fa fa-volume-up module-audio-icon js-module-audio-icon']")
        self.formplayer_tests_menu = (By.XPATH, "//h3[text()='Formplayer Tests']")
        self.formplayer_multimedia_form = (By.XPATH, "//h3[text()='Formplayer Multimedia']")
        self.formplayer_multimedia_audio_icon = (By.XPATH,
                                                 "//h3[text()='Formplayer Multimedia']/following-sibling::div/div/i[@class='fa fa-volume-up module-audio-icon js-module-audio-icon']")
        self.formplayer_multimedia_menu_icon = (
            By.XPATH, "//td[./h3[.='Formplayer Multimedia']]/preceding-sibling::td/div[contains(@style,'module3')]")
        self.multimedia_gif = (By.XPATH, "//span[text()='This should play a hillarious "
                                         "gif']/following-sibling::div/img[contains(@src,'.gif')]")
        self.multimedia_image = (By.XPATH, "//div[./span[text()='This question should have image multimedia. Enter "
                                           "yes if so.']]/following::div/img[contains(@src, 'jpg')]")
        self.image_input_box = (By.XPATH, "//div[./img[contains(@src, 'jpg')]]/preceding-sibling::div[1]/textarea")
        self.multimedia_video = (By.XPATH, "//div/legend[./span[text()='Video Tests']]/following::div/video[contains("
                                           "@src, 'mp4')]")
        self.video_input_box = (By.XPATH, "//div[./video[contains(@src, 'mp4')]]/preceding-sibling::div[1]/textarea")
        self.multimedia_audio = (By.XPATH, "//div/legend[./span[text()='Audio Tests']]/following::div/audio[contains("
                                           "@src, 'mp3')]")
        self.audio_input_box = (By.XPATH, "//div[./audio[contains(@src, 'mp3')]]/preceding-sibling::div[1]/textarea")

        # Custom Badge
        self.formplayer_badge = (By.XPATH, "//h3[text()='Formplayer Specific Tests']/preceding::span[@class='badge']")
        self.case_tests_badge = (By.XPATH, "//h3[text()='Case Tests']/preceding::span[@class='badge'][2]")

    def open_form(self, case_list, form_name):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.wait_to_click((By.XPATH, self.case_list_menu.format(case_list)))
        self.wait_to_click((By.XPATH, self.registration_form.format(form_name)))
        self.switch_to_default_content()
        time.sleep(2)

    def open_case_list(self, case_list):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.wait_to_click((By.XPATH, self.case_list_menu.format(case_list)))
        self.switch_to_default_content()
        time.sleep(2)

    def open_module(self, module):
        self.switch_to_frame(self.iframe)
        self.wait_to_click((By.XPATH, self.case_list_menu.format(module)))
        self.switch_to_default_content()

    def save_incomplete_form(self, value):
        self.switch_to_frame(self.iframe)
        self.send_keys(self.name_question, value)
        self.wait_to_click(self.next_question)
        time.sleep(2)
        self.js_click(self.home_button)
        self.switch_to_default_content()
        time.sleep(2)

    def delete_all_incomplete_forms(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.incomplete_form)
        if self.is_present(self.find_elements(self.incomplete_list_count)):
            page_list = len(self.find_elements(self.incomplete_list_count)) - 4
            print(page_list)
            for page in range(page_list):
                list = self.find_elements(self.incomplete_form_list)
                print(len(list))
                if len(list) != 0:
                    for i in range(len(list)):
                        self.js_click_direct((By.XPATH, self.delete_incomplete_form.format(1)))
                        time.sleep(2)
                        self.wait_to_click(self.delete_confirm)
                        list = self.find_elements(self.incomplete_form_list)
                        print(len(list))
                else:
                    print("No incomplete form present")
                self.switch_to_default_content()
                self.wait_to_click(self.back_button)
                self.switch_to_frame(self.iframe)
                self.wait_to_click(self.incomplete_form)
        else:
            list = self.find_elements(self.incomplete_form_list)
            print(len(list))
            if len(list) != 0:
                for i in range(len(list)):
                    self.js_click_direct((By.XPATH, self.delete_incomplete_form.format(1)))
                    time.sleep(2)
                    self.wait_to_click(self.delete_confirm)
                    list = self.find_elements(self.incomplete_form_list)
                    print(len(list))
            else:
                print("No incomplete form present")
        self.switch_to_default_content()
        self.wait_to_click(self.back_button)

    def verify_number_of_forms(self, no_of_forms):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.incomplete_form)
        list = self.find_elements(self.incomplete_form_list)
        assert len(list) == no_of_forms
        self.switch_to_default_content()
        self.wait_to_click(self.back_button)

    def delete_first_form(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.incomplete_form)
        list = self.find_elements(self.incomplete_form_list)
        print(len(list))
        if len(list) != 0:
            self.js_click_direct((By.XPATH, self.delete_incomplete_form.format(1)))
            self.wait_to_click(self.delete_confirm)
        else:
            print("There are no incomplete forms")
        list_new = self.find_elements(self.incomplete_form_list)
        assert len(list) - 1 == len(list_new)
        print("deleted first incomplete form")
        self.switch_to_default_content()
        self.wait_to_click(self.back_button)

    def verify_saved_form_and_submit_unchanged(self, value):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.incomplete_form)
        list = self.find_elements(self.incomplete_form_list)
        print(len(list))
        if len(list) != 0:
            self.js_click(self.edit_incomplete_form)
            text = self.get_attribute(self.name_question, "value")
            assert text == value
            self.wait_to_click(self.next_question)
            time.sleep(2)
            self.js_click(self.submit_form_button)
            time.sleep(2)
            self.wait_for_element(self.success_message)
            print("Form submitted with unchanged value")
            time.sleep(2)
            self.wait_to_click(self.home_button)
            time.sleep(2)
        else:
            print("There are no incomplete forms")
            self.switch_to_default_content()
            self.wait_to_click(self.back_button)
            self.switch_to_frame(self.iframe)
        self.wait_to_click(self.sync_button)
        time.sleep(2)
        self.switch_to_default_content()

    def verify_saved_form_and_submit_changed(self, value):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.incomplete_form)
        list = self.find_elements(self.incomplete_form_list)
        print(len(list))
        if len(list) != 0:
            self.js_click(self.edit_incomplete_form)
            text = self.get_attribute(self.name_question, "value")
            assert text == value
            self.wait_to_clear_and_send_keys(self.name_question, self.changed_name_input)
            self.wait_to_click(self.next_question)
            time.sleep(2)
            self.js_click(self.submit_form_button)
            time.sleep(2)
            self.wait_for_element(self.success_message)
            print("Form submitted with changed value")
            time.sleep(2)
            self.wait_to_click(self.home_button)
            time.sleep(2)
        else:
            print("There are no incomplete forms")
            self.switch_to_default_content()
            self.wait_to_click(self.back_button)
            self.switch_to_frame(self.iframe)
        self.wait_to_click(self.sync_button)
        time.sleep(2)
        self.switch_to_default_content()

    def verify_submit_history(self, value, username):
        try:
            web_app = WebAppsBasics(self.driver)
            web_app.open_submit_history_form_link(UserData.basic_tests_app, username)
            print(value)
            text = self.get_text(self.table_data)
            print(str(text).strip())
            assert str(text).strip() == value
        except :
            print("The submitted form details are not yet updated in submit history")

    def random_expression(self):
        return random.choice(UserData.expressions)

    def verify_data_preview(self, expression):
        print("Expression Function: ", expression)
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.wait_to_click(self.data_preview)
        assert self.is_present(self.no_queries)
        self.wait_to_clear_and_send_keys(self.xpath_textarea, expression)
        self.click(self.evaluate_button)
        time.sleep(1)
        assert self.is_present((By.XPATH, self.recent_query.format(expression)))
        self.wait_to_click(self.data_preview)
        self.switch_to_default_content()

    def group(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.next_question)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format('First', '1')))
        self.wait_to_click((By.XPATH, self.choose_radio_button.format('Second', '2')))
        self.wait_to_click((By.XPATH, self.choose_radio_button.format('Third', '2')))
        self.wait_to_click((By.XPATH, self.choose_radio_button.format('Fourth', '3')))
        self.wait_to_click(self.next_question)
        self.wait_to_click(self.display_new_text_question)
        self.wait_for_element(self.text_question)
        self.send_keys(self.text_question, "Test")
        self.wait_to_click(self.clear_button)
        self.wait_to_click(self.display_new_multiple_choice_question)
        self.wait_to_click(self.multiple_choice_response)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.pop_up_message.format("Please continue.")))
        self.wait_to_click(self.next_question)
        self.verify_choice_selection((By.XPATH, self.choose_radio_button.format(
            'Changing your selection here should update the text below this question.', 'Choice 3')),
                                     'You selected choice_value_3')
        self.wait_to_click(self.clear_button)
        self.verify_choice_selection((By.XPATH, self.choose_radio_button.format(
            'Changing your selection here should update the text below this question.', 'Choice 2')),
                                     'You selected choice_value_2')
        self.wait_to_click(self.clear_button)
        self.verify_choice_selection((By.XPATH, self.choose_radio_button.format(
            'Changing your selection here should update the text below this question.', 'Choice 1')),
                                     'You selected choice_value_1')
        self.wait_to_click(self.next_question)
        self.verify_choice_selection((By.XPATH, self.choose_radio_button.format(
            'Changing your county selection should update the available options in the City select question below.',
            'Suffolk')),
                                     'Selected county was: sf')
        assert self.is_present((By.XPATH, self.county_options.format("Boston")))
        assert self.is_present((By.XPATH, self.county_options.format("Winthrop")))
        self.wait_to_click(self.clear_button)
        self.verify_choice_selection((By.XPATH, self.choose_radio_button.format(
            'Changing your county selection should update the available options in the City select question below.',
            'Essex')),
                                     'Selected county was: ex')
        assert self.is_present((By.XPATH, self.county_options.format("Saugus")))
        assert self.is_present((By.XPATH, self.county_options.format("Andover")))
        self.wait_to_click(self.clear_button)
        self.verify_choice_selection((By.XPATH, self.choose_radio_button.format(
            'Changing your county selection should update the available options in the City select question below.',
            'Middlesex')),
                                     'Selected county was: mx')
        assert self.is_present((By.XPATH, self.county_options.format("Billerica")))
        assert self.is_present((By.XPATH, self.county_options.format("Wilmington")))
        assert self.is_present((By.XPATH, self.county_options.format("Cambridge")))
        self.wait_to_click((By.XPATH, self.county_options.format("Cambridge")))
        self.wait_to_click(self.next_question)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            'Do you want to skip the first group?',
            'Yes')))
        self.wait_to_click(self.next_question)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "The next section tests groups within other groups. Which parts of the group do you want to skip?",
            "Outer and Inner")))
        self.wait_to_click(self.next_question)
        self.wait_to_click(self.next_question)
        self.wait_to_click(self.next_question)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Pick one of the following.", "One")))
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        print("Group Form submitted successfully")
        time.sleep(2)
        self.js_click(self.home_button)
        time.sleep(2)
        self.wait_to_click(self.sync_button)
        time.sleep(2)
        self.switch_to_default_content()

    def verify_choice_selection(self, locator, value):
        self.scroll_to_element(locator)
        self.click(locator)
        time.sleep(1)
        self.scroll_to_element((By.XPATH, self.pop_up_message.format(value)))
        assert self.is_present_and_displayed((By.XPATH, self.pop_up_message.format(value)))

    def end_of_navigation_module(self, case):
        self.switch_to_frame(self.iframe)
        self.wait_to_clear_and_send_keys(
            (By.XPATH, self.text_area_field.format("Submitting this will take you to the home screen.")),
            "home" + fetch_random_string())
        self.wait_to_click(self.next_question)
        time.sleep(2)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        assert self.is_present((By.XPATH, self.case_list_menu.format(case)))
        time.sleep(2)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()
        self.open_form(case, UserData.basic_test_app_forms["module"])
        self.switch_to_frame(self.iframe)
        self.wait_to_clear_and_send_keys(
            (By.XPATH, self.text_area_field.format("Submitting this will take you to the Module Menu.")),
            "module" + fetch_random_string())
        self.wait_to_click(self.next_question)
        time.sleep(2)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        assert self.is_present((By.XPATH, self.case_list_menu.format(case)))
        time.sleep(2)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()
        self.open_form(case, UserData.basic_test_app_forms["prev"])
        self.switch_to_frame(self.iframe)
        self.wait_to_clear_and_send_keys(self.search_input, "home" + fetch_random_string())
        self.wait_to_click(self.search_button)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format("home" + fetch_random_string())))
        self.wait_to_click((By.XPATH, self.module_search.format("home" + fetch_random_string())))
        self.wait_to_click(self.continue_button)
        time.sleep(1)
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        time.sleep(2)
        self.js_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()
        self.open_form(case, UserData.basic_test_app_forms["current"])
        self.switch_to_frame(self.iframe)
        self.wait_to_clear_and_send_keys(
            (By.XPATH, self.text_area_field.format("Submitting this form will take you to the current module.")),
            "current" + fetch_random_string())
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        time.sleep(2)
        assert self.is_present_and_displayed(
            (By.XPATH, self.case_list_menu.format(UserData.basic_test_app_forms["current"])))
        time.sleep(2)
        self.js_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()
        self.open_form(case, UserData.basic_test_app_forms["close"])
        self.switch_to_frame(self.iframe)
        self.wait_to_clear_and_send_keys(self.search_input, "home" + fetch_random_string())
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format("home" + fetch_random_string())))
        self.wait_to_click((By.XPATH, self.module_search.format("home" + fetch_random_string())))
        self.wait_to_click(self.continue_button)
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        time.sleep(3)
        assert self.is_present_and_displayed(
            (By.XPATH, self.text_area_field.format("Submitting this will take you to the home screen.")))
        time.sleep(2)
        self.js_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()
        self.open_form(case, UserData.basic_test_app_forms["another"])
        self.switch_to_frame(self.iframe)
        self.wait_to_clear_and_send_keys(
            (By.XPATH, self.text_area_field.format("Submitting this will take you to the Module Badge Check Menu.")),
            "badge" + fetch_random_string())
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        time.sleep(4)
        assert self.is_present_and_displayed(self.module_badge_table)
        time.sleep(2)
        self.js_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()

    def submit_basic_test_form(self):
        self.open_form(UserData.basic_tests_app['case_list'], UserData.basic_tests_app['form_name'])
        self.switch_to_frame(self.iframe)
        self.wait_to_clear_and_send_keys(self.name_question, fetch_random_string())
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.js_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()

    def register_negative_case(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format(
            "What is the case name? You should not be allowed to proceed if the question is empty.")),
                                         self.case_reg_neg)
        self.wait_to_click(self.next_question)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Are you sure you want to create a new case?", "Cancel - Please do not create this case.")))
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()

    def register_positive_case(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format(
            "What is the case name? You should not be allowed to proceed if the question is empty.")),
                                         self.case_reg_pos)
        self.wait_to_click(self.next_question)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Are you sure you want to create a new case?", "Confirm - Please create this case.")))
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()

    # def deny_location_permission(self):
    #     time.sleep(3)
    #     self.dismiss_popup_alert()
    #     self.switch_to_frame(self.iframe)
    #     self.wait_for_element(self.location_alert)

    def case_detail_verification(self):
        self.switch_to_frame(self.iframe)
        self.wait_for_element(self.search_input)
        self.wait_to_clear_and_send_keys(self.search_input, self.case_reg_pos)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format(self.case_reg_pos)))
        print("case search working properly")
        self.wait_to_click((By.XPATH, self.module_search.format(self.case_reg_pos)))
        self.wait_to_click((By.XPATH, self.case_detail_tab.format("1")))
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Name", self.case_reg_pos)))
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Status", "open")))
        self.wait_to_click((By.XPATH, self.case_detail_tab.format("2")))
        assert not self.is_present(self.case_detail_table_list)
        assert self.is_present(self.continue_button)
        self.wait_to_click(self.continue_button)
        time.sleep(2)
        self.wait_for_element(self.home_button)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()

    def updated_case_detail_verification(self, new_data):
        self.switch_to_frame(self.iframe)
        self.wait_for_element(self.search_input)
        self.wait_to_clear_and_send_keys(self.search_input, self.case_reg_pos)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format(self.case_reg_pos)))
        print("case search working properly")
        self.wait_to_click((By.XPATH, self.module_search.format(self.case_reg_pos)))
        self.wait_to_click((By.XPATH, self.case_detail_tab.format("1")))
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Name", self.case_reg_pos)))
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Status", "open")))
        assert self.is_present_and_displayed(
            (By.XPATH, self.case_detail_table.format("Phone Number", self.input_dict['phone'])))
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Text", self.input_dict['Text'])))
        self.wait_to_click((By.XPATH, self.case_detail_tab.format("2")))
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Data Node", new_data)))
        assert self.is_present_and_displayed(
            (By.XPATH, self.case_detail_table.format("Intval", self.input_dict["intval"])))
        try:
            assert self.is_present_and_displayed(
                (By.XPATH, self.case_detail_table.format("Singleselect", self.input_dict['Singleselect'])))
            assert self.is_present_and_displayed(
                (By.XPATH, self.case_detail_table.format(
                    "Multiselect",
                    self.input_dict['Multiselect'][0].lower() + " " + self.input_dict['Multiselect'][1].lower())))
        except:
            print("Singleselect and Multiselect details are not present in the screen")
        assert self.is_present(self.continue_button)
        self.wait_to_click(self.continue_button)
        time.sleep(2)
        self.wait_for_element(self.home_button)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()

    def update_a_case(self):
        self.switch_to_frame(self.iframe)
        self.wait_for_element(self.search_input)
        self.wait_to_clear_and_send_keys(self.search_input, self.case_reg_pos)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format(self.case_reg_pos)))
        print("case search working properly")
        self.wait_to_click((By.XPATH, self.module_search.format(self.case_reg_pos)))
        self.wait_to_click((By.XPATH, self.case_detail_tab.format("1")))
        assert self.is_present(self.continue_button)
        self.wait_to_click(self.continue_button)
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format(
            "This form will allow you to add and update different kinds of data to/from the case. Enter some text:")),
                                         self.input_dict['Text'])
        self.wait_to_click(self.next_question)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Select one of the following:", self.input_dict['Singleselect'])))
        self.wait_to_click(self.next_question)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Select one or more of the following:", self.input_dict['Multiselect'][0])))
        time.sleep(1)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Select one or more of the following:", self.input_dict['Multiselect'][1])))
        self.wait_to_click(self.next_question)
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "Enter a phone number:")), self.input_dict['phone'])
        self.wait_to_click(self.next_question)
        time.sleep(2)
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "Enter an integer:")), self.input_dict['intval'] + Keys.TAB)
        time.sleep(1)
        self.wait_to_click(self.next_question)
        time.sleep(2)
        self.scroll_to_element((By.XPATH, self.input_field.format(
            "Capture your location here:")))
        self.send_keys((By.XPATH, self.input_field.format(
            "Capture your location here:")), "Delhi" + Keys.TAB)
        self.js_click(self.search_location_button)
        time.sleep(2)
        assert not self.is_present_and_displayed(self.blank_latitude, 10)
        self.js_click(self.next_question)
        time.sleep(2)
        self.wait_to_click((By.XPATH, self.input_field.format(
            "Enter a date:")))
        self.wait_to_click(self.click_today_date)
        self.wait_to_click(self.close_date_picker)
        self.wait_to_click(self.next_question)
        time.sleep(2)
        text = self.get_text(self.output)
        number = text.split(".")
        print(str(re.findall(r'\b\d+\b', number[1])[0]))
        time.sleep(2)
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(1)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()
        return str(re.findall(r'\b\d+\b', number[1])[0])

    def create_and_verify_sub_case(self):
        self.switch_to_frame(self.iframe)
        self.wait_for_element(self.search_input)
        self.wait_to_clear_and_send_keys(self.search_input, self.case_reg_pos)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format(self.case_reg_pos)))
        print("case search working properly")
        self.wait_to_click((By.XPATH, self.module_search.format(self.case_reg_pos)))
        assert self.is_present(self.continue_button)
        self.js_click(self.continue_button)
        time.sleep(1)
        self.wait_to_click(self.next_question)
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format(
            "Enter a name for your sub case:")),
                                         self.subcase_pos)
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "Enter a number for " + self.subcase_pos + ":")), fetch_random_digit_with_range(1, 20))
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Do you want to create the sub case?", "Confirm - Please create " + self.subcase_pos + ".")))
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()
        self.open_case_list(UserData.basic_test_app_forms['subcaseone'])
        self.switch_to_frame(self.iframe)
        self.wait_for_element(self.search_input)
        self.wait_to_clear_and_send_keys(self.search_input, self.subcase_pos)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format(self.subcase_pos)))
        print("case search working properly")
        self.wait_to_click((By.XPATH, self.module_search.format(self.subcase_pos)))
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Name", self.subcase_pos)))
        assert self.is_present_and_displayed(
            (By.XPATH, self.case_detail_table.format("Parent Case Name", self.case_reg_pos)))
        assert self.is_present(self.continue_button)
        self.wait_to_click(self.continue_button)
        self.wait_to_click((By.XPATH, self.case_list_menu.format(UserData.basic_test_app_forms['close_subcase'])))
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Do you want to close the case?", "Yes")))
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        self.switch_to_default_content()

    def close_case(self):
        self.switch_to_frame(self.iframe)
        self.wait_for_element(self.search_input)
        self.wait_to_clear_and_send_keys(self.search_input, self.case_reg_pos)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format(self.case_reg_pos)))
        print("case search working properly")
        self.wait_to_click((By.XPATH, self.module_search.format(self.case_reg_pos)))
        assert self.is_present(self.continue_button)
        self.wait_to_click(self.continue_button)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Are you sure you want to close this case?", "Confirm - Please close this case.")))
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        self.switch_to_default_content()
        self.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['caselist'])
        self.switch_to_frame(self.iframe)
        self.wait_for_element(self.search_input)
        self.wait_to_clear_and_send_keys(self.search_input, self.case_reg_pos)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed(self.empty_list)
        print("case search working properly")

    def unicode_verification_case(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format(
            "What is the case name? You should not be allowed to proceed if the question is empty.")),
                                         self.unicode_text)
        self.wait_to_click(self.next_question)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Are you sure you want to create a new case?", "Confirm - Please create this case.")))
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()
        self.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['update_case'])
        self.switch_to_frame(self.iframe)
        self.wait_for_element(self.search_input)
        self.wait_to_clear_and_send_keys(self.search_input, self.unicode_text)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format(self.unicode_text)))
        print("case search working properly")
        self.wait_to_click((By.XPATH, self.module_search.format(self.unicode_text)))
        self.wait_to_click((By.XPATH, self.case_detail_tab.format("1")))
        assert self.is_present(self.continue_button)
        self.wait_to_click(self.continue_button)
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format(
            "This form will allow you to add and update different kinds of data to/from the case. Enter some text:")),
                                         self.update_unicode)
        self.wait_to_click(self.next_question)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Select one of the following:", self.input_dict['Singleselect'])))
        self.wait_to_click(self.next_question)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Select one or more of the following:", self.input_dict['Multiselect'][0])))
        time.sleep(1)
        self.wait_to_click(self.next_question)
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "Enter a phone number:")), self.input_dict['phone'])
        self.wait_to_click(self.next_question)
        time.sleep(2)
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "Enter an integer:")), self.input_dict['intval'] + Keys.TAB)
        time.sleep(1)
        self.wait_to_click(self.next_question)
        time.sleep(2)
        self.scroll_to_element((By.XPATH, self.input_field.format(
            "Capture your location here:")))
        self.send_keys((By.XPATH, self.input_field.format(
            "Capture your location here:")), "Delhi" + Keys.TAB)
        self.js_click(self.search_location_button)
        time.sleep(2)
        assert not self.is_present_and_displayed(self.blank_latitude, 10)
        self.js_click(self.next_question)
        time.sleep(2)
        self.wait_to_click((By.XPATH, self.input_field.format(
            "Enter a date:")))
        self.wait_to_click(self.click_today_date)
        self.wait_to_click(self.close_date_picker)
        self.wait_to_click(self.next_question)
        time.sleep(2)
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()

    def verify_updated_unicode(self):
        self.switch_to_frame(self.iframe)
        self.wait_for_element(self.search_input)
        self.wait_to_clear_and_send_keys(self.search_input, self.unicode_text)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format(self.unicode_text)))
        print("case search working properly")
        self.wait_to_click((By.XPATH, self.module_search.format(self.unicode_text)))
        self.wait_to_click((By.XPATH, self.case_detail_tab.format("1")))
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Name", self.unicode_text)))
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Status", "open")))
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Text", self.update_unicode)))
        assert self.is_present(self.continue_button)
        self.wait_to_click(self.continue_button)
        time.sleep(2)
        self.wait_for_element(self.home_button)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()

    def turn_off_one_question_per_screen(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.settings_option)
        time.sleep(2)
        isChecked = self.is_present(self.turn_on_one_question_toggle_button)
        print(isChecked)
        time.sleep(2)
        if isChecked is True:
            # self.driver.execute_script("arguments[0].click();", self.driver.find_element(By.XPATH, "//th[(text()='Use one question per screen')]/following-sibling::td//input"))
            self.js_click_direct(self.toggle_button_one_question)
            time.sleep(10)
            print("Toggled OFF")
            self.js_click_direct(self.done_button)
        self.switch_to_default_content()

    def maps_record_location(self):
        self.switch_to_frame(self.iframe)
        time.sleep(5)
        self.send_keys(self.location_input, UserData.map_input)
        time.sleep(5)
        self.wait_to_click(self.location_search_button)
        time.sleep(5)
        self.wait_to_click(self.clear_button)
        time.sleep(3)
        assert self.is_present(self.blank_latitude), "Coordinates not cleared"
        time.sleep(3)
        self.wait_to_click(self.submit_form_button_2)
        time.sleep(10)
        self.switch_to_default_content()

    def sub_menus(self):
        self.switch_to_frame(self.iframe)
        time.sleep(5)
        self.wait_to_click(self.start_option)
        self.js_click(self.parent_menu)
        self.is_present_and_displayed(self.parent_survey)
        self.is_present_and_displayed(self.child_menu)
        self.is_present_and_displayed(self.visible_child_survey)
        self.wait_to_click(self.parent_survey)
        self.wait_to_click(self.submit_survey_button)
        self.js_click(self.parent_menu)
        self.wait_to_click(self.child_menu)
        self.is_present_and_displayed(self.child_survey_under_child_menu)
        self.wait_to_click(self.child_survey_under_child_menu)
        self.wait_to_click(self.submit_survey_button)
        self.js_click(self.parent_menu)
        self.is_present_and_displayed(self.visible_child_survey)
        self.wait_to_click(self.visible_child_survey)
        self.wait_to_click(self.submit_survey_button)
        self.switch_to_default_content()

    def multimedia_forms_menus(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.is_displayed(self.formplayer_tests_audio_icon)
        self.is_displayed(self.formplayer_tests_menu_icon)
        self.js_click(self.formplayer_tests_menu)
        self.is_displayed(self.formplayer_multimedia_audio_icon)
        self.is_displayed(self.formplayer_multimedia_menu_icon)
        self.switch_to_default_content()

    def multimedia_form_navigation(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.js_click(self.formplayer_tests_menu)
        self.js_click(self.formplayer_multimedia_form)
        self.is_displayed(self.multimedia_gif)
        print('entered the form')
        image_present = self.is_displayed(self.multimedia_image)
        assert image_present is True
        print('Image is Present')
        self.send_keys(self.image_input_box, 'Yes')
        video_present = self.is_displayed(self.multimedia_video)
        assert video_present is True
        self.send_keys(self.video_input_box, 'yes')
        audio_present = self.is_displayed(self.multimedia_audio)
        assert audio_present is True
        self.send_keys(self.audio_input_box, 'yes')
        self.wait_to_click(self.submit_form_button)
        self.switch_to_default_content()

    def custom_badge(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.is_present_and_displayed(self.formplayer_badge)
        self.is_present_and_displayed(self.case_tests_badge)
        self.switch_to_default_content()

