import time
import random
import re
from datetime import datetime, timedelta

from selenium.webdriver.common.keys import Keys

from Formplayer.testPages.app_preview.login_as_app_preview_page import LoginAsAppPreviewPage
from Formplayer.testPages.project_settings.project_settings_page import ProjectSettingsPage
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
        self.special_character = "~`!@#$%^&*()<>?"
        self.test_question = "Test " + fetch_random_string()
        self.input_dict = {
            "phone": fetch_phone_number(),
            "Singleselect": "A",
            "Multiselect": ["A", "C"],
            "Text": "text update" + fetch_random_string(),
            "intval": fetch_random_digit_with_range(1, 30)
        }
        self.application_menu_id = (By.LINK_TEXT, "Applications")
        self.description_field_edit = (By.XPATH, "//inline-edit[contains(@params,'Enter app description here')]//i[@class='fa fa-pencil']")
        self.description_field = (
        By.XPATH, "//inline-edit[contains(@params,'Enter app description here')]//textarea")
        self.save_description = (By.XPATH, "//inline-edit[contains(@params,'Enter app description here')]//button[contains(@data-bind,'click: save')]")
        self.back_button = (By.XPATH, "//i[@class ='fa fa-chevron-left']")
        self.form_list = (By.XPATH, "//tbody[@class='menus-container']")
        self.refresh_button = (By.XPATH, "//button[contains(@class,'btn-preview-refresh js-preview-refresh')]")
        self.toggle_button = (By.XPATH, "//button[contains(@class ,'js-preview-toggle-tablet-view')]")
        self.sync_button = (By.XPATH, "//div[@class='js-sync-item appicon appicon-sync']")
        self.sync_message = (By.XPATH, "//p[contains(text(),'successfully synced')]")
        self.start_option = (By.XPATH, "//div[@class= 'js-start-app appicon appicon-start']")
        self.settings_option = (By.XPATH, "//div[@class = 'js-settings appicon appicon-settings']/i")
        self.login_as_option = (By.XPATH, "//div[@class='js-restore-as-item appicon appicon-restore-as']")
        self.incomplete_form = (By.XPATH, "//div[@class='js-incomplete-sessions-item appicon appicon-incomplete']")
        self.make_new_version_button = (By.XPATH, "//button[contains(@data-bind,'Make New Version')]")
        self.release_button = (By.XPATH, "(//button[contains(text(),'Released')])[1]")
        self.release_button_pressed = (
        By.XPATH, "(//button[contains(text(),'Released')])[1][contains(@class,'active')]")

        self.case_list_menu = "//h3[contains(text(), '{}')]"
        self.registration_form = "//h3[contains(text(), '{}')]"
        self.followup_form = (By.XPATH, "//h3[contains(text(), 'Followup Form')]")
        self.name_question = (By.XPATH,
                              "//label[.//span[.='Enter a Name']]/following-sibling::div//textarea[contains(@class,'textfield form-control')]")
        self.incomplete_form_list = (By.XPATH, "//tr[@class='formplayer-request']")
        self.incomplete_form_title = (By.XPATH, "//li[@class='breadcrumb-text'][.='Incomplete Forms']")
        self.incomplete_list_count = (By.XPATH, "//ul/li[@data-lp]")
        self.no_of_pages = (By.XPATH, "//li[contains(@class,'js-page')]")
        self.list_drop_down = (By.XPATH, "//select[@class='form-control per-page-limit']")
        self.page_number = "(//li[contains(@class,'js-page')])[{}]"
        self.page_navigation = (By.XPATH, "//nav[@class='module-pagination-container']")
        self.next_list_button = (By.XPATH, "//a[@aria-label='Next']")
        self.prev_list_button = (By.XPATH, "//a[@aria-label='Previous']")
        self.first_list_page = (By.XPATH, "//a[@aria-label='First Page']")
        self.last_list_page = (By.XPATH, "//a[@aria-label='Last Page']")
        self.go_to_page_input = (By.XPATH, "//input[@placeholder='Go to page']")
        self.go_button = (By.XPATH, "//button[@id='pagination-go-button']")
        self.delete_incomplete_form = "(//tr[@class='formplayer-request']/descendant::div[@aria-label='Delete form'])[{}]"
        self.edit_incomplete_form = (
            By.XPATH, "(//tr[@class='formplayer-request']/descendant::div//i[contains(@class,'fa fa-pencil')])[1]")
        self.click_today_date = (By.XPATH, "//a[@data-action='today']")
        self.close_date_picker = (By.XPATH, "//a[@data-action='close']")
        self.mobileno_question = (By.XPATH, "//label[.//span[text()='Mobile No.']]/following-sibling::div//input")
        self.submit_form_button = (By.XPATH, "//button[contains(@data-bind,'submitForm')]")

        self.next_question = (By.XPATH, "//button[contains(@data-bind,'nextQuestion')]")
        self.prev_question = (By.XPATH, "//button[contains(@data-bind,'prevQuestion')]")
        self.next_question_force = (By.XPATH, "//button[contains(@data-bind,'clickedNextOnRequired')]")
        self.complete_form = (By.XPATH, "//button[@data-bind='visible: atLastIndex(), click: submitForm']")
        self.success_message = (By.XPATH, "//p[contains(text(),'successfully saved')]")
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
        self.text_area_field = "//label[.//span[contains(.,'{}')]]//following-sibling::div//textarea"
        self.input_field = "//label[.//span[contains(.,'{}')]]//following-sibling::div//input"
        self.breadcrumbs = "//h1[@class='page-title'][.='{}']"
        self.search_input = (By.XPATH, "//input[@id='searchText']")
        self.search_button = (By.XPATH, "//button[@id='case-list-search-button']")
        self.module_search = "//td[.='{}']"
        self.continue_button = (By.XPATH, "//button[.='Continue']")
        self.module_badge_table = (By.XPATH, "//table[contains(@class, 'module-table-case-list')]")

        # contraints
        self.success_check = (By.XPATH, "//i[@class='fa fa-check text-success']")
        self.warning = (By.XPATH, "//i[@class='fa fa-warning text-danger clickable']")
        self.error_message = "//div[contains(@data-bind,'serverError')][.='{}']"
        self.location_alert = (By.XPATH,
                               "//div[contains(.,'Without access to your location, computations that rely on the here() function will show up blank.')][contains(@class,'alert')]")
        self.danger_warning = "//label[.//span[contains(.,'{}')]]//following-sibling::div//i[contains(@class,'text-danger')]"
        self.text_success = "//label[.//span[contains(.,'{}')]]//following-sibling::div//i[contains(@class,'text-success')]"
        self.radio_option_list = "(//label[.//span[contains(.,'{}')]]//following-sibling::div//input)[1]"

        # functions
        self.div_span = "//div/span[contains(.,'{}')]"

        # casetest
        self.case_detail_tab = "//a[.='Case Details {}']"
        self.case_detail_table = "//th[.='{}']/following-sibling::td[.='{}']"
        self.case_detail_table_list = (By.XPATH, "//div[@class='js-detail-content']/table/tr")
        self.search_location_button = (By.XPATH, "//button[.='Search']")
        self.blank_latitude = (By.XPATH, "//td[@class='lat coordinate'][contains(.,'??')]")
        self.output = (By.XPATH, "//span[@class='caption webapp-markdown-output']")
        self.empty_list = (By.XPATH, "//div[@class='alert alert-info'][.='List is empty.']")
        self.clear_select = "//label[.//span[contains(.,'{}')]]//following-sibling::div//button[contains(@data-bind,'click: onClear')][@style='']"

        # repeat group
        self.delete_repeat = "//legend/span[contains(.,'{}')]//following-sibling::button"
        self.repeat_input_field = "//div[@class='gr repetition'][.//legend/span[contains(.,'{}')]]//following-sibling::div[./fieldset[.//label[.//span[contains(.,'{}')]]]]//following-sibling::div//input"
        self.add_new_repeat = (By.XPATH, "//button[.='Add new repeat']")
        self.danger_warning_repeat = "//div[@class='gr repetition'][.//legend/span[contains(.,'{}')]]//following-sibling::div[./fieldset[.//label[.//span[contains(.,'{}')]]]]//following-sibling::div//i[contains(@class,'text-danger')]"
        self.text_success_repeat = "//div[@class='gr repetition'][.//legend/span[contains(.,'{}')]]//following-sibling::div[./fieldset[.//label[.//span[contains(.,'{}')]]]]//following-sibling::div//i[contains(@class,'text-success')]"


    def open_form(self, case_list, form_name):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        time.sleep(2)
        self.wait_for_element((By.XPATH, self.case_list_menu.format(case_list)))
        self.wait_to_click((By.XPATH, self.case_list_menu.format(case_list)))
        time.sleep(2)
        self.wait_for_element((By.XPATH, self.registration_form.format(form_name)))
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
        self.wait_for_element(self.name_question)
        print("typing value: ", value)
        self.send_keys(self.name_question, value)
        time.sleep(2)
        self.wait_to_click(self.next_question)
        time.sleep(2)
        self.js_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()
        time.sleep(2)

    def delete_all_incomplete_forms(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.incomplete_form)
        self.wait_for_element(self.incomplete_form_title)
        if self.is_present(self.find_elements(self.incomplete_list_count)):
            page_list = self.find_elements(self.incomplete_list_count)
            print(page_list)
            page_list=page_list-4
            for page in range(page_list):
                time.sleep(2)
                list = self.find_elements(self.incomplete_form_list)
                print(len(list))
                if len(list) != 0:
                    for i in range(len(list)):
                        time.sleep(2)
                        self.js_click_direct((By.XPATH, self.delete_incomplete_form.format(1)))
                        time.sleep(2)
                        self.wait_to_click(self.delete_confirm)
                        time.sleep(2)
                        list = self.find_elements(self.incomplete_form_list)
                        print(len(list))
                else:
                    print("No incomplete form present")
                self.switch_to_default_content()
                self.wait_to_click(self.back_button)
                self.switch_to_frame(self.iframe)
                self.wait_to_click(self.incomplete_form)
                self.wait_for_element(self.incomplete_form_title)
        else:
            time.sleep(2)
            list = self.find_elements(self.incomplete_form_list)
            print(len(list))
            if len(list) != 0:
                for i in range(len(list)):
                    time.sleep(2)
                    self.js_click((By.XPATH, self.delete_incomplete_form.format(1)))
                    time.sleep(2)
                    self.wait_to_click(self.delete_confirm)
                    time.sleep(2)
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
        print(value)
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.incomplete_form)
        list = self.find_elements(self.incomplete_form_list)
        print(len(list))
        if len(list) != 0:
            self.js_click(self.edit_incomplete_form)
            time.sleep(3)
            self.wait_for_element(self.name_question)
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
            time.sleep(3)
            self.wait_for_element(self.name_question)
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
            'Suffolk')), 'Selected county was: sf')
        assert self.is_present((By.XPATH, self.county_options.format("Boston")))
        assert self.is_present((By.XPATH, self.county_options.format("Winthrop")))
        self.wait_to_click(self.clear_button)
        time.sleep(3)
        self.verify_choice_selection((By.XPATH, self.choose_radio_button.format(
            'Changing your county selection should update the available options in the City select question below.',
            'Essex')), 'Selected county was: ex')
        assert self.is_present((By.XPATH, self.county_options.format("Saugus")))
        assert self.is_present((By.XPATH, self.county_options.format("Andover")))
        self.wait_to_click(self.clear_button)
        time.sleep(3)
        self.verify_choice_selection((By.XPATH, self.choose_radio_button.format(
            'Changing your county selection should update the available options in the City select question below.',
            'Middlesex')), 'Selected county was: mx')
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
        self.wait_for_element(self.sync_button)
        self.js_click(self.sync_button)
        time.sleep(3)
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
        time.sleep(2)
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
        time.sleep(2)
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

    def fixtures_form(self):
        self.switch_to_frame(self.iframe)
        self.wait_for_element(self.next_question)
        self.click(self.next_question)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format('Select at least 2!', '3')))
        self.wait_for_element(
            (By.XPATH, self.danger_warning.format("Select at least 2!")))
        self.wait_to_click((By.XPATH, self.choose_radio_button.format('Select at least 2!', '2')))
        self.wait_for_element(
            (By.XPATH, self.text_success.format("Select at least 2!")))
        time.sleep(1)
        self.js_click(self.next_question)
        time.sleep(1)
        self.wait_for_element((By.XPATH, self.radio_option_list.format('Pick a county!')))
        self.wait_to_click(self.next_question)
        time.sleep(1)
        assert not self.is_present_and_displayed((By.XPATH, self.radio_option_list.format('Select a city!')), 10)
        time.sleep(1)
        self.wait_to_click(self.prev_question)
        self.wait_for_element((By.XPATH, self.radio_option_list.format('Pick a county!')))
        self.wait_to_click((By.XPATH, self.choose_radio_button.format('Pick a county!', 'Essex')))
        time.sleep(1)
        self.js_click(self.next_question)
        assert self.is_present_and_displayed((By.XPATH, self.radio_option_list.format('Select a city!')),10)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format('Select a city!', 'Andover')))
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()

    def functions_form(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("between 1 and 50")))
        text = self.get_text((By.XPATH, self.div_span.format("between 1 and 50")))
        text = str(text).split(":")
        text = text[1].strip()
        print(text)
        assert int(text) in range(1, 50), "Number is not between 1 and 50"
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("The number \"12\" should be here")))
        self.validate_text("The number \"12\" should be here", 12)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("The number \"1\" should be displayed here")))
        self.validate_text("The number \"1\" should be displayed here", 1, "\n", 3)
        self.validate_text("The number 6 should be displayed here", 6)
        self.validate_text("The number \"0\" should be displayed here", 0)
        self.validate_text("The number \"2\" should display here", 2)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format("Return to this question, enter 0")))
        self.send_keys((By.XPATH, self.input_field.format("Return to this question, enter 0")),
                       fetch_random_digit() + Keys.TAB)
        time.sleep(3)
        self.js_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format(
            "This should only display if you entered any number other than \"0\" in the previous question."
        )))
        assert self.is_present_and_displayed((By.XPATH, self.div_span.format(
            "This should only display if you entered any number other than \"0\" in the previous question."
        )))
        self.js_click(self.prev_question)
        self.wait_for_element((By.XPATH, self.input_field.format("Return to this question, enter 0")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format("Return to this question, enter 0")),
                                         "0" + Keys.TAB)
        time.sleep(3)
        self.js_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format(
            "This should display the word, \"number\": number"
        )))
        assert self.is_present_and_displayed((By.XPATH, self.div_span.format(
            "This should display the word, \"number\": number"
        )))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format("Enter 14")))
        self.send_keys((By.XPATH, self.input_field.format("Enter 14")),
                       "14" + Keys.TAB)
        time.sleep(3)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("This should display \"15\"")))
        self.validate_text("This should display \"15\"", 15)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("This should display \"14\"")))
        self.validate_text("This should display \"14\"", 14)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("displayed here: 64")))
        self.validate_text("The answer displayed here: 64, should equal this: 64", 64,",",64)
        self.wait_to_click(self.next_question)
        time.sleep(2)
        self.wait_to_click(self.next_question)
        time.sleep(2)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()

    def validate_text(self, div_text, value, split_value=None, value2=None):
        if split_value is None:
            num = self.get_text((By.XPATH, self.div_span.format(div_text)))
            num = str(num).split(":")
            num = num[1].strip()
            print(num)
            assert int(num) == value, 'Number is not \"' + value + '\"'
        else:
            text = self.get_text((By.XPATH, self.div_span.format(div_text)))
            text = str(text).split(split_value)
            text1 = text[0].strip()
            text2 = text[1].strip()
            text1 = str(text1).split(":")
            num = text1[1].strip()
            print(num)
            assert int(num) == value, 'Number is not \"' + value + '\"'
            text2 = str(text2).split(":")
            num = text2[1].strip()
            print(num)
            assert int(num) == value2, 'Number is not \"' + value2 + '\"'


    def constraint_form(self):
        self.switch_to_frame(self.iframe)
        self.wait_for_element(self.next_question)
        self.click(self.next_question)
        self.wait_for_element((By.XPATH, self.text_area_field.format(
            "This question is required. You should not be allowed to proceed with a blank answer.")))
        self.js_click(self.next_question_force)
        assert self.is_present(self.warning)
        self.send_keys((By.XPATH, self.text_area_field.format(
            "This question is required. You should not be allowed to proceed with a blank answer.")),
                       self.test_question)
        self.wait_to_click(self.next_question)
        self.send_keys((By.XPATH, self.text_area_field.format(
            "This answer can be anything but the word, \"test\". Try a different word. An error message should display. Note this is case sensitive.")),
                       "test" + Keys.TAB)
        assert self.is_present_and_displayed((By.XPATH, self.error_message.format(
            "Your answer cannot be \"test\". Please try something else and continue.")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format(
            "This answer can be anything but the word, \"test\". Try a different word. An error message should display. Note this is case sensitive.")),
                                         "tes" + Keys.TAB)
        self.wait_to_click(self.next_question)
        self.send_keys((By.XPATH, self.text_area_field.format(
            "This answer cannot be less than 3 characters, or greater than 6 characters long. Leaving the field blank should be valid.")),
                       "aa" + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.danger_warning.format("less than 3 characters, or greater than 6 characters")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format(
            "This answer cannot be less than 3 characters, or greater than 6 characters long. Leaving the field blank should be valid.")),
                                         "aabbccdd" + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.danger_warning.format("less than 3 characters, or greater than 6 characters")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format(
            "This answer cannot be less than 3 characters, or greater than 6 characters long. Leaving the field blank should be valid.")),
                                         "aabbcc" + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.text_success.format("less than 3 characters, or greater than 6 characters")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "This answer must be greater than 20 and smaller than 8000. The question is required.")))
        self.send_keys((By.XPATH, self.input_field.format(
            "This answer must be greater than 20 and smaller than 8000. The question is required.")),
                       "11" + Keys.TAB)
        self.wait_for_element((By.XPATH, self.danger_warning.format("greater than 20 and smaller than 8000")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "This answer must be greater than 20 and smaller than 8000. The question is required.")),
                       "8011" + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.danger_warning.format("greater than 20 and smaller than 8000")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "This answer must be greater than 20 and smaller than 8000. The question is required.")),
                       "811" + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.text_success.format("greater than 20 and smaller than 8000")))
        self.wait_to_click(self.next_question)
        self.wait_for_element(
            (By.XPATH, self.text_success.format("greater than 20 and smaller than 8000")))
        self.wait_to_click((By.XPATH, self.input_field.format(
            "This date must be after today.")))
        self.wait_to_click(self.click_today_date)
        self.wait_to_click(self.close_date_picker)
        time.sleep(2)
        self.wait_for_element(
            (By.XPATH, self.danger_warning.format("This date must be after today.")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "This date must be after today.")), self.input_date_add(1) + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.text_success.format("This date must be after today.")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "This date has to be today or in the past.")))
        self.send_keys((By.XPATH, self.input_field.format(
            "This date has to be today or in the past.")), self.input_date_add(2) + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.danger_warning.format("This date has to be today or in the past.")))
        self.wait_to_click((By.XPATH, self.input_field.format(
            "This date has to be today or in the past.")))
        self.wait_to_click(self.click_today_date)
        self.wait_to_click(self.close_date_picker)
        time.sleep(2)
        self.wait_for_element(
            (By.XPATH, self.text_success.format("This date has to be today or in the past.")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "This date has to be today or in the past.")), self.input_date_subtract(1) + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.text_success.format("This date has to be today or in the past.")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "The date entered must be within the last 10 months.")))
        self.send_keys((By.XPATH, self.input_field.format(
            "The date entered must be within the last 10 months.")), self.input_date_subtract(340) + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.danger_warning.format("The date entered must be within the last 10 months.")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "The date entered must be within the last 10 months.")), self.input_date_subtract(100) + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.text_success.format("The date entered must be within the last 10 months.")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "This question should ONLY let you submit an answer with TWO significant figures after the decimal.")))
        self.send_keys((By.XPATH, self.input_field.format(
            "This question should ONLY let you submit an answer with TWO significant figures after the decimal.")),
                       "1.1" + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.danger_warning.format("TWO significant figures after the decimal")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "This question should ONLY let you submit an answer with TWO significant figures after the decimal.")),
                                         "1.123" + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.danger_warning.format("TWO significant figures after the decimal")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "This question should ONLY let you submit an answer with TWO significant figures after the decimal.")),
                                         "1.23" + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.text_success.format("TWO significant figures after the decimal")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "This question should allow you to submit an answer with two OR LESS significant figures.")))
        self.send_keys((By.XPATH, self.input_field.format(
            "This question should allow you to submit an answer with two OR LESS significant figures.")),
                       "100" + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.text_success.format("two OR LESS significant figures")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "This question should only let you submit an answer greater than 50 but less than 80.")))
        self.send_keys((By.XPATH, self.input_field.format(
            "This question should only let you submit an answer greater than 50 but less than 80.")),
                       "100" + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.danger_warning.format("greater than 50 but less than 80")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "This question should only let you submit an answer greater than 50 but less than 80.")),
                                         "60" + Keys.TAB)
        self.wait_for_element(
            (By.XPATH, self.text_success.format("greater than 50 but less than 80")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.text_area_field.format(
            "Leave this question blank and navigate to the next question. Then, navigate back to this question, enter a value and proceed.")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("You should only see this question if you left the previous one blank.")))
        self.wait_to_click(self.prev_question)
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format(
            "Leave this question blank and navigate to the next question. Then, navigate back to this question, enter a value and proceed.")),
                                         self.test_question + Keys.TAB)
        time.sleep(3)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.text_area_field.format(
            'This should automatically have a default answer of \"Yes\" inserted in the text field'
        )))
        assert self.get_attribute((By.XPATH, self.text_area_field.format(
            'This should automatically have a default answer of \"Yes\" inserted in the text field'
        )),"value") == "Yes", "Default value is not Yes"
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.choose_radio_button.format("Choose an answer.","Yes")))
        self.js_click((By.XPATH, self.choose_radio_button.format("Choose an answer.", "Yes")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("This should only appear if you selected \"Yes\" to the previous question.")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("should not be the same as")))
        text = self.get_text((By.XPATH, self.div_span.format("should not be the same as")))
        text = str(text).split(",")
        text1 = text[0].strip()
        text2 = text[1].strip()
        text1 = str(text1).split(":")
        num1 = text1[1].strip()
        print(num1)
        text2 = str(text2).split(":")
        num2 = text2[1].strip()
        print(num2)
        assert num1 != num2, 'Values are equal'
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH,self.input_field.format("Enter a score of 80.")))
        self.send_keys((By.XPATH, self.input_field.format("Enter a score of 80.")),"80"+Keys.TAB)
        time.sleep(2)
        self.wait_to_click(self.next_question)
        assert self.is_present_and_displayed((By.XPATH, self.div_span.format("GOOD - This should only appear if the score was greater than 75.")))
        self.wait_to_click(self.prev_question)
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format("Enter a score of 80.")), "60"+Keys.TAB)
        time.sleep(2)
        self.wait_to_click(self.next_question)
        assert self.is_present_and_displayed(
            (By.XPATH, self.div_span.format("FAIR - This should only appear if the score is greater than 50 and less than or equal to 75.")))
        self.wait_to_click(self.prev_question)
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format("Enter a score of 80.")), "10" + Keys.TAB)
        time.sleep(2)
        self.wait_to_click(self.next_question)
        assert self.is_present_and_displayed(
            (By.XPATH, self.div_span.format(
                "POOR - This should display if the score was less than or equal to 50.")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.choose_radio_button.format(
            "Please select 1 or 2 options and proceed.","One"
        )))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "Please select 1 or 2 options and proceed.", "One"
        )))

        self.js_click((By.XPATH, self.choose_radio_button.format(
            "Please select 1 or 2 options and proceed.", "Two"
        )))
        time.sleep(3)
        self.wait_to_click(self.next_question)
        assert self.is_present_and_displayed((By.XPATH, self.div_span.format("This msg should only display if you selected one or two items.")))
        self.wait_to_click(self.prev_question)
        self.wait_for_element((By.XPATH, self.choose_radio_button.format(
            "Please select 1 or 2 options and proceed.", "One"
        )))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "Please select 1 or 2 options and proceed.", "Three"
        )))
        time.sleep(3)
        self.wait_to_click(self.next_question)
        assert self.is_present_and_displayed((By.XPATH, self.text_area_field.format("This should only display if you selected 3 or more options in the previous question.")))
        self.send_keys((By.XPATH, self.text_area_field.format(
            "This should only display if you selected 3 or more options in the previous question.")), self.test_question)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.choose_radio_button.format(
            "You should not be able to choose all of the options here.", "One"
        )))

        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should not be able to choose all of the options here.", "One"
        )))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should not be able to choose all of the options here.", "Two"
        )))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should not be able to choose all of the options here.", "Three"
        )))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should not be able to choose all of the options here.", "Four"
        )))
        self.wait_for_element((By.XPATH, self.danger_warning.format("You should not be able to choose all of the options here.")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should not be able to choose all of the options here.", "Four"
        )))

        self.wait_for_element(
            (By.XPATH, self.text_success.format("You should not be able to choose all of the options here.")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.choose_radio_button.format(
            "You should not be able to select \"None\" and another choice.", "One"
        )))

        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should not be able to select \"None\" and another choice.", "One"
        )))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should not be able to select \"None\" and another choice.", "Two"
        )))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should not be able to select \"None\" and another choice.", "None"
        )))
        self.wait_for_element(
            (By.XPATH, self.danger_warning.format("You should not be able to select \"None\" and another choice.")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should not be able to select \"None\" and another choice.", "Two"
        )))
        self.wait_for_element(
            (By.XPATH, self.danger_warning.format("You should not be able to select \"None\" and another choice.")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should not be able to select \"None\" and another choice.", "One"
        )))
        self.wait_for_element(
            (By.XPATH, self.text_success.format("You should not be able to select \"None\" and another choice.")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format("If you capture your location, you should not see the message.")))

        self.wait_to_click(self.next_question)
        assert self.is_present_and_displayed((By.XPATH, self.div_span.format("You should only see this message if the previous question was left empty.")))

        self.wait_to_click(self.prev_question)
        self.wait_for_element(
            (By.XPATH, self.input_field.format("If you capture your location, you should not see the message.")))
        self.send_keys(
            (By.XPATH, self.input_field.format("If you capture your location, you should not see the message.")), "Delhi"+Keys.ENTER)
        time.sleep(5)
        self.wait_to_click(self.next_question)
        assert not self.is_present((By.XPATH, self.div_span.format(
            "You should only see this message if the previous question was left empty.")))
        self.wait_for_element((By.XPATH, self.choose_radio_button.format(
            "The form should not crash.", "Continue to complete the form."
        )))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "The form should not crash.", "Continue to complete the form."
        )))
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()

    def input_date_add(self, number_of_days):
        presentday = datetime.now()  # or presentday = datetime.today()
        # Get new date
        new_date = presentday + timedelta(number_of_days)
        return new_date.strftime('%m/%d/%Y')

    def input_date_subtract(self, number_of_days):
        presentday = datetime.now()
        # Get new date
        new_date = presentday - timedelta(number_of_days)
        return new_date.strftime('%m/%d/%Y')


    def questions_form(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.text_area_field.format("This question should let you enter any form of text or special characters.")))
        self.send_keys((By.XPATH, self.text_area_field.format(
            "This question should let you enter any form of text or special characters.")), self.test_question+" "+self.special_character)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "This question should only let you enter an integer.")))
        self.send_keys((By.XPATH, self.input_field.format(
            "This question should only let you enter an integer.")),"abcd"+Keys.TAB)
        self.wait_for_element(((By.XPATH, self.danger_warning.format(
            "This question should only let you enter an integer."))))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "This question should only let you enter an integer.")), fetch_random_digit() + Keys.TAB)
        time.sleep(1)

        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "This question should only let you enter a decimal number")))
        self.send_keys((By.XPATH, self.input_field.format(
            "This question should only let you enter a decimal number")), "23.45" + Keys.TAB)
        time.sleep(3)

        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "This question should only allow you to enter a date.")))
        self.send_keys((By.XPATH, self.input_field.format(
            "This question should only allow you to enter a date.")), self.input_date_add(0) + Keys.TAB)

        self.wait_to_click(self.next_question)
        time.sleep(3)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose one or more answers here.","One")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose one or more answers here.", "One")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose one or more answers here.", "Two")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose one or more answers here.", "Three")))
        self.wait_for_element((By.XPATH, self.text_success.format("You should be able to choose one or more answers here.")))

        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose only one answer here.", "One")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose only one answer here.", "One")))
        time.sleep(2)
        assert self.is_selected((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose only one answer here.", "One"))), "The option is not selected."
        self.wait_for_element((By.XPATH, self.clear_select.format("You should be able to choose only one answer here.")))
        self.wait_to_click(
            (By.XPATH, self.clear_select.format("You should be able to choose only one answer here.")))
        time.sleep(2)
        assert not self.is_selected((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose only one answer here.", "One"))), "The option is still selected."
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose only one answer here.", "Two")))
        time.sleep(2)
        assert self.is_selected((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose only one answer here.", "Two"))), "The option is not selected."

        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "This question should only allow you to enter a time.")))
        self.send_keys((By.XPATH, self.input_field.format(
            "This question should only allow you to enter a time.")), datetime.now().strftime("%H:%M") + Keys.TAB)

        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "The value of this question should be hidden, but anything can be entered.")))
        self.send_keys((By.XPATH, self.input_field.format(
            "The value of this question should be hidden, but anything can be entered.")), self.test_question + Keys.TAB)
        time.sleep(2)
        assert self.get_attribute(
            (By.XPATH, self.input_field.format(
                "The value of this question should be hidden, but anything can be entered.")), "type"
        ) == "password", "Value is not hidden"

        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "The value of this question should be hidden and only numbers are allowed.")))
        self.send_keys((By.XPATH, self.input_field.format(
            "The value of this question should be hidden and only numbers are allowed.")),
                       self.test_question + Keys.TAB)
        self.wait_for_element((By.XPATH, self.danger_warning.format(
            "The value of this question should be hidden and only numbers are allowed.")))
        time.sleep(2)
        assert self.get_attribute(
            (By.XPATH, self.input_field.format(
                "The value of this question should be hidden and only numbers are allowed.")), "type"
        ) == "password", "Value is not hidden"
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "The value of this question should be hidden and only numbers are allowed.")),
                       fetch_random_digit() + Keys.TAB)
        self.wait_for_element((By.XPATH, self.text_success.format(
            "The value of this question should be hidden and only numbers are allowed.")))

        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "You should be able to enter digits here. Enter multiple zeroes and navigate back and forth to make sure they remain.")))
        self.send_keys((By.XPATH, self.input_field.format(
            "You should be able to enter digits here. Enter multiple zeroes and navigate back and forth to make sure they remain.")),
                       "00000" + Keys.TAB)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("If using an Android device, you should be able to capture a signature. Try it out!")))
        self.wait_to_click(self.prev_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "You should be able to enter digits here. Enter multiple zeroes and navigate back and forth to make sure they remain.")))
        assert self.get_attribute((By.XPATH, self.input_field.format(
            "You should be able to enter digits here. Enter multiple zeroes and navigate back and forth to make sure they remain.")),
            "value") == "00000", "Value has changed"

        self.wait_to_click(self.next_question)
        time.sleep(3)
        self.wait_to_click(self.next_question)
        time.sleep(3)
        self.wait_to_click(self.next_question)
        time.sleep(3)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "If using an Android device, this question should allow you to capture a GPS location. Try it out")))
        assert self.is_present_and_displayed(self.blank_latitude, 10)
        self.js_send_keys((By.XPATH, self.input_field.format(
            "If using an Android device, this question should allow you to capture a GPS location. Try it out")), "Delhi")
        self.wait_to_click(self.search_location_button)
        time.sleep(2)
        assert not self.is_present_and_displayed(self.blank_latitude, 10)

        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("If available on your device, this question should allow you to take a picture or upload an image.")))
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("If available on your device, this question should allow you to record or upload audio, and then play it.")))

        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("If available on your device, this question should allow you to record or upload video, and then play it.")))

        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.div_span.format("If available on your device, this question should only allow you to record audio, and then play it.")))

        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.text_area_field.format(
            "This question should let you enter any form of text or special characters. Try different values.")))
        self.send_keys((By.XPATH, self.text_area_field.format(
            "This question should let you enter any form of text or special characters. Try different values.")),
                       self.test_question + " " + self.special_character)
        time.sleep(2)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose one or more answers here.", "One")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose one or more answers here.", "One")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose one or more answers here.", "Two")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose one or more answers here.", "Three")))
        self.wait_for_element(
            (By.XPATH, self.text_success.format("You should be able to choose one or more answers here.")))
        time.sleep(2)
        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose only one answer here.", "One")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose only one answer here.", "One")))
        time.sleep(2)
        assert self.is_selected((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose only one answer here.", "One"))), "The option is not selected."
        self.wait_for_element(
            (By.XPATH, self.clear_select.format("You should be able to choose only one answer here.")))
        self.wait_to_click(
            (By.XPATH, self.clear_select.format("You should be able to choose only one answer here.")))
        time.sleep(2)
        assert not self.is_selected((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose only one answer here.", "One"))), "The option is still selected."
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose only one answer here.", "Two")))
        time.sleep(2)
        assert self.is_selected((By.XPATH, self.choose_radio_button.format(
            "You should be able to choose only one answer here.", "Two"))), "The option is not selected."

        self.wait_to_click(self.next_question)
        self.wait_for_element((By.XPATH, self.choose_radio_button.format(
            "This is a single select lookup. You should be able to choose only one answer.", "Radhe Sham")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "This is a single select lookup. You should be able to choose only one answer.", "Radhe Sham")))
        time.sleep(2)
        assert self.is_selected((By.XPATH, self.choose_radio_button.format(
            "This is a single select lookup. You should be able to choose only one answer.", "Radhe Sham"))), "The option is not selected."
        self.wait_to_click((By.XPATH, self.clear_select.format(
            "This is a single select lookup. You should be able to choose only one answer.")))
        time.sleep(2)
        assert not self.is_selected((By.XPATH, self.choose_radio_button.format(
            "This is a single select lookup. You should be able to choose only one answer.", "Radhe Sham"))), "The option is still selected."
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "This is a single select lookup. You should be able to choose only one answer.", "Art of War")))
        time.sleep(2)
        assert self.is_selected((By.XPATH, self.choose_radio_button.format(
            "This is a single select lookup. You should be able to choose only one answer.", "Art of War"))), "The option is not selected."

        self.scroll_to_element((By.XPATH, self.choose_radio_button.format(
            "This is a checkbox lookup table and you should be able to choose more than one option.", "150")))

        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "This is a checkbox lookup table and you should be able to choose more than one option.", "150")))
        time.sleep(1)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "This is a checkbox lookup table and you should be able to choose more than one option.", "200")))
        time.sleep(2)
        self.wait_for_element(
            (By.XPATH,
             self.text_success.format("This is a checkbox lookup table and you should be able to choose more than one option.")))

        self.wait_to_click(self.next_question)
        # self.scroll_to_element(self.add_new_repeat)
        # self.js_click(self.add_new_repeat)
        # self.wait_for_element((By.XPATH, self.repeat_input_field.format("1/1","Enter a number")))
        # self.send_keys((By.XPATH, self.repeat_input_field.format("1/1", "Enter a number")), "abc"+Keys.TAB)
        # self.wait_for_element((By.XPATH, self.danger_warning_repeat.format("1/1", "Enter a number")))
        # self.wait_to_clear_and_send_keys((By.XPATH, self.repeat_input_field.format("1/1", "Enter a number")), "12"+Keys.TAB)
        # self.wait_for_element((By.XPATH, self.text_success_repeat.format("1/1", "Enter a number")))
        #
        #
        # self.scroll_to_element(self.add_new_repeat)
        # self.js_click(self.add_new_repeat)
        # self.wait_for_element((By.XPATH, self.repeat_input_field.format("2/2","Enter a number")))
        # self.send_keys((By.XPATH, self.repeat_input_field.format("2/2", "Enter a number")), "abc"+Keys.TAB)
        # self.wait_for_element((By.XPATH, self.danger_warning_repeat.format("2/2", "Enter a number")))
        # self.wait_to_clear_and_send_keys((By.XPATH, self.repeat_input_field.format("2/2", "Enter a number")), "45"+Keys.TAB)
        # self.wait_for_element((By.XPATH, self.text_success_repeat.format("2/2", "Enter a number")))
        #
        # self.wait_to_click((By.XPATH, self.delete_repeat.format("2/2")))
        # time.sleep(3)
        # self.wait_to_click((By.XPATH, self.delete_repeat.format("1/1")))
        # time.sleep(3)
        # assert not self.is_present((By.XPATH, self.repeat_input_field.format("1/1","Enter a number")))
        time.sleep(2)
        self.wait_to_click(self.next_question)
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()


    def update_description(self, settings):
        self.wait_for_element(self.description_field_edit)
        self.js_click(self.description_field_edit)
        self.wait_to_clear_and_send_keys(self.description_field,
                                         "Basic Tests Description - automation test inactivity "+datetime.now().strftime("%d-%m-%Y %H:%M")
                                         )
        self.js_click(self.save_description)
        time.sleep(2)
        project = ProjectSettingsPage(self.driver, settings)
        project.set_inactivity_timeout()
        app_preview = LoginAsAppPreviewPage(self.driver, settings)
        app_preview.open_view_app_preview(UserData.basic_tests_app['tests_app'])
        self.wait_for_element(self.make_new_version_button)
        self.wait_to_click(self.make_new_version_button)
        print("Sleeping for the new version to be ready to release")
        time.sleep(40)
        self.js_click(self.release_button)
        time.sleep(5)
        assert self.is_present(self.release_button_pressed), "Release button is not successfully pressed."
        print("Sleeping for the installation code to generate")
        time.sleep(5)
        self.switch_back_to_prev_tab()

    def verify_pagination(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.incomplete_form)
        self.wait_for_element(self.incomplete_form_title)
        if self.is_present(self.page_navigation):
            self.switch_to_default_content()
            time.sleep(3)
            self.verify_page_navigation()
            time.sleep(3)
            self.verify_goto_page_button()
            time.sleep(3)
            self.verify_list_per_page()
            self.switch_to_frame(self.iframe)
        elif self.is_present(self.page_navigation) == False and self.is_present(
                self.find_elements(self.incomplete_list_count)):
            self.switch_to_default_content()
            self.verify_list_per_page()
            self.switch_to_frame(self.iframe)
        else:
            print("No incomplete form present")
        self.driver.back()
        self.switch_to_default_content()

    def verify_list_per_page(self):
        self.switch_to_frame(self.iframe)
        if self.is_present(self.page_navigation):
            page_count = self.find_elements(self.no_of_pages)
            print(len(page_count))
            max_list_count = len(page_count) * 10
            print(max_list_count)
            min_list_count = (len(page_count) - 1) * 10
            print(min_list_count)
        else:
            page_count = 1
            max_list_count = page_count * 10
            print(max_list_count)
            min_list_count = 1
            print(min_list_count)

        for i in UserData.page_list:
            self.select_by_value(self.list_drop_down, i)
            time.sleep(5)
            latest_page_count = self.find_elements(self.no_of_pages)
            if self.is_present(self.page_navigation):
                if len(latest_page_count) > 1:
                    assert len(self.find_elements(self.incomplete_form_list)) == int(i), "List count not equal to 10"
                else:
                    assert len(self.find_elements(self.incomplete_form_list)) in range(min_list_count,
                                                                                       max_list_count), "List count is not valid"
            else:
                assert len(self.find_elements(self.incomplete_form_list)) in range(min_list_count,
                                                                                       max_list_count), "List count is not valid"
        self.switch_to_default_content()

    def verify_page_navigation(self):
        self.switch_to_frame(self.iframe)
        page_count = self.find_elements(self.no_of_pages)
        n = len(page_count)
        print(n)
        self.wait_to_click(self.last_list_page)
        time.sleep(3)
        classname = self.get_attribute((By.XPATH, self.page_number.format(n)),"class")
        print(classname)
        assert classname == "js-page active", "Click is not successful on last page"

        self.wait_to_click(self.first_list_page)
        time.sleep(3)
        classname = self.get_attribute((By.XPATH, self.page_number.format(1)), "class")
        print(classname)
        assert classname == "js-page active", "Click is not successful on first page"

        print("navigating forward")
        for i in range(len(page_count)-1)[::]:
            self.wait_to_click(self.next_list_button)
            time.sleep(3)
            classname = self.get_attribute((By.XPATH, self.page_number.format(i+2)), "class")
            print(classname)
            assert classname == "js-page active", "Click is not successful"

        print("navigating backward")
        for i in range(len(page_count)-1)[::]:
            self.wait_to_click(self.prev_list_button)
            time.sleep(3)
            classname = self.get_attribute((By.XPATH, self.page_number.format(len(page_count)-i-1)), "class")
            print(classname)
            assert classname == "js-page active", "Click is not successful"
        self.switch_to_default_content()

    def verify_goto_page_button(self):
        self.switch_to_frame(self.iframe)
        page_count = self.find_elements(self.no_of_pages)
        n = len(page_count)
        for i in range(len(page_count))[::-1]:
            self.wait_to_clear_and_send_keys(self.go_to_page_input,i+1)
            self.wait_to_click(self.go_button)
            time.sleep(4)
            classname = self.get_attribute((By.XPATH, self.page_number.format(i+1)), "class")
            print(classname)
            assert classname == "js-page active", "Click is not successful"
        self.switch_to_default_content()