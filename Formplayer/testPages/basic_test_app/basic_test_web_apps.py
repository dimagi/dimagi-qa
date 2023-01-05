import re
import time

from selenium.webdriver.common.keys import Keys

from Formplayer.testPages.app_preview.login_as_app_preview_page import LoginAsAppPreviewPage
from Formplayer.testPages.webapps.login_as_page import LoginAsPage
from Formplayer.testPages.webapps.webapps_basics import WebAppsBasics
from common_utilities.generate_random_string import fetch_random_string, fetch_phone_number, fetch_random_digit, \
    fetch_random_digit_with_range
from common_utilities.selenium.base_page import BasePage
from Formplayer.userInputs.user_inputs import UserData

from selenium.webdriver.common.by import By

""""Contains test page elements and functions related to the WebApps Access/Basics of Commcare"""


class BasicTestWebApps(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.name_input1 = "basic test1 " + fetch_random_string()
        self.name_input2 = "basic test2 " + fetch_random_string()
        self.name_input3 = "basic test3 " + fetch_random_string()
        self.changed_name_input = "basic test changed " + fetch_random_string()

        self.test_question = "Test " + fetch_random_string()
        self.case_reg_neg = "web_negcase_" + fetch_random_string()
        self.case_reg_pos = "web_poscase_" + fetch_random_string()
        self.subcase_pos = "sub_case"+fetch_random_string()
        self.unicode_text = "Unicode_web_"+fetch_random_string()+UserData.unicode
        self.update_unicode = fetch_random_string()+UserData.unicode_new

        self.input_dict = {
            "phone": fetch_phone_number(),
            "Singleselect": "A",
            "Multiselect": ["A", "C"],
            "Text": "text update"+ fetch_random_string(),
            "intval": fetch_random_digit_with_range(1, 30)
        }
        self.application_menu_id = (By.LINK_TEXT, "Applications")

        self.back_button = (By.XPATH, "//i[@class ='fa fa-chevron-left']")
        self.form_list = (By.XPATH, "//tbody[@class='menus-container']")
        self.refresh_button = (By.XPATH, "//button[contains(@class,'btn-preview-refresh js-preview-refresh')]")
        self.toggle_button = (By.XPATH, "//button[contains(@class ,'js-preview-toggle-tablet-view')]")
        self.sync_button = (By.XPATH,"//div[@class='js-sync-item appicon appicon-sync']")
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
        self.delete_incomplete_form = "(//tr[@class='formplayer-request']/descendant::div[@aria-label='Delete form'])[{}]"
        self.edit_incomplete_form = (By.XPATH,"(//tr[@class='formplayer-request']/descendant::div//i[contains(@class,'fa fa-pencil')])[1]")
        self.click_today_date = (By.XPATH, "//a[@data-action='today']")
        self.close_date_picker = (By.XPATH, "//a[@data-action='close']")
        self.mobileno_question = (By.XPATH, "//label[.//span[text()='Mobile No.']]/following-sibling::div//input")
        self.submit_form_button = (By.XPATH, "//button[contains(@data-bind,'SubmitButton')]")

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

        self.data_preview = (By.XPATH, "//button[@aria-label='Expand Data Preview']")
        self.xpath_textarea = (By.XPATH, "//textarea[@placeholder='XPath Expression']")
        self.no_queries = (By.XPATH, "//i[.='No recent queries']")
        self.recent_query = "//tbody[@data-bind='foreach: recentXPathQueries']//td/span[.='{}']"
        self.query_table = (By.XPATH, "//tbody[@data-bind='foreach: recentXPathQueries']")
        self.evaluate_button = (By.XPATH, "(//input[@value='Evaluate'])[1]")

        #Groups
        self.choose_radio_button = "//label[.//span[.=\"{}\"]]//following-sibling::div//input[@value='{}']"
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

        #eofn
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

    def open_form(self, case_list, form_name):
        self.scroll_to_element((By.XPATH, self.case_list_menu.format(case_list)))
        self.js_click((By.XPATH, self.case_list_menu.format(case_list)))
        self.scroll_to_element((By.XPATH, self.registration_form.format(form_name)))
        self.js_click((By.XPATH, self.registration_form.format(form_name)))

    def open_case_list(self, case_list):
        self.scroll_to_element((By.XPATH, self.case_list_menu.format(case_list)))
        self.js_click((By.XPATH, self.case_list_menu.format(case_list)))
        time.sleep(2)

    def save_incomplete_form(self, value):
        self.send_keys(self.name_question, value)
        self.wait_to_click(self.home_button)
        time.sleep(2)

    def delete_all_incomplete_forms(self):

        self.wait_to_click(self.incomplete_form)
        list = self.find_elements(self.incomplete_form_list)
        print(len(list))
        if len(list) != 0:
            for i in range(len(list)):
                self.js_click_direct((By.XPATH, self.delete_incomplete_form.format(1)))
                self.wait_to_click(self.delete_confirm)
                list = self.find_elements(self.incomplete_form_list)
        self.driver.back()

    def verify_number_of_forms(self, no_of_forms):
        self.wait_to_click(self.incomplete_form)
        list = self.find_elements(self.incomplete_form_list)
        assert len(list) == no_of_forms
        self.driver.back()

    def delete_first_form(self):
        self.wait_to_click(self.incomplete_form)
        list = self.find_elements(self.incomplete_form_list)
        print(len(list))
        if len(list) != 0:
            self.js_click_direct((By.XPATH, self.delete_incomplete_form.format(1)))
            self.wait_to_click(self.delete_confirm)
        else:
            print("There are no incomplete forms")
        list_new = self.find_elements(self.incomplete_form_list)
        assert len(list)-1 == len(list_new)
        print("deleted first incomplete form")
        self.driver.back()

    def verify_saved_form_and_submit_unchanged(self, value):
        self.wait_to_click(self.incomplete_form)
        list = self.find_elements(self.incomplete_form_list)
        print(len(list))
        if len(list) != 0:
            self.js_click(self.edit_incomplete_form)
            text = self.get_attribute(self.name_question,"value")
            assert text == value
            self.wait_to_click(self.submit_form_button)
            print("Form submitted with unchanged value")
        else:
            print("There are no incomplete forms")
        time.sleep(2)
        self.js_click(self.home_button)
        time.sleep(2)
        self.wait_to_click(self.sync_button)
        time.sleep(2)

    def verify_saved_form_and_submit_changed(self, value):
        self.wait_to_click(self.incomplete_form)
        list = self.find_elements(self.incomplete_form_list)
        print(len(list))
        if len(list) != 0:
            self.js_click(self.edit_incomplete_form)
            text = self.get_attribute(self.name_question,"value")
            assert text == value
            self.wait_to_clear_and_send_keys(self.name_question, self.changed_name_input)
            self.wait_to_click(self.submit_form_button)
            print("Form submitted with changed value")
        else:
            print("There are no incomplete forms")
        time.sleep(2)
        self.js_click(self.home_button)
        time.sleep(2)
        self.wait_to_click(self.sync_button)
        time.sleep(2)

    def verify_submit_history(self, value, username):
        web_app = WebAppsBasics(self.driver)
        web_app.open_submit_history_form_link(UserData.basic_tests_app, username)
        print(value)
        text = self.get_text(self.table_data)
        print(str(text).strip())
        assert str(text).strip() == value

    def verify_data_preview(self, expression):
        self.wait_to_click(self.data_preview)
        assert self.is_present(self.no_queries)
        self.wait_to_clear_and_send_keys(self.xpath_textarea, expression)
        self.click(self.evaluate_button)
        time.sleep(1)
        assert self.is_present((By.XPATH, self.recent_query.format(expression)))
        self.wait_to_click(self.data_preview)

    def group(self):
        self.js_click((By.XPATH, self.choose_radio_button.format('First','2')))
        time.sleep(2)
        self.js_click((By.XPATH, self.choose_radio_button.format('A', '2')))
        self.js_click((By.XPATH, self.choose_radio_button.format('Third', '2')))
        self.js_click((By.XPATH, self.choose_radio_button.format('Fourth', '3')))
        self.scroll_to_element(self.display_new_text_question)
        self.js_click(self.display_new_text_question)
        self.wait_for_element(self.text_question)
        self.send_keys(self.text_question, "Test")
        # self.js_click(self.clear_button)
        self.js_click(self.display_new_multiple_choice_question)
        self.js_click(self.multiple_choice_response)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH,self.pop_up_message.format("Please continue.")))
        self.scroll_to_element((By.XPATH, self.choose_radio_button.format(
            'Changing your selection here should update the text below this question.', 'Choice 3')))
        self.verify_choice_selection((By.XPATH, self.choose_radio_button.format(
            'Changing your selection here should update the text below this question.', 'Choice 3')), 'You selected choice_value_3')
        self.js_click(self.clear_button)
        self.verify_choice_selection((By.XPATH, self.choose_radio_button.format(
            'Changing your selection here should update the text below this question.', 'Choice 2')), 'You selected choice_value_2')
        # self.js_click(self.clear_button)
        self.verify_choice_selection((By.XPATH, self.choose_radio_button.format('Changing your selection here should update the text below this question.','Choice 1')), 'You selected choice_value_1')
        self.scroll_to_element((By.XPATH, self.choose_radio_button.format(
            'Changing your county selection should update the available options in the City select question below.', 'Suffolk')))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            'Changing your county selection should update the available options in the City select question below.', 'Suffolk')))
        assert self.is_present((By.XPATH, self.county_options.format("Boston")))
        assert self.is_present((By.XPATH, self.county_options.format("Winthrop")))

        self.js_click((By.XPATH, self.choose_radio_button.format(
            'Changing your county selection should update the available options in the City select question below.',
            'Essex')))
        assert self.is_present((By.XPATH, self.county_options.format("Saugus")))
        assert self.is_present((By.XPATH, self.county_options.format("Andover")))

        self.js_click((By.XPATH, self.choose_radio_button.format(
            'Changing your county selection should update the available options in the City select question below.',
            'Middlesex')))
        assert self.is_present((By.XPATH, self.county_options.format("Billerica")))
        assert self.is_present((By.XPATH, self.county_options.format("Wilmington")))
        assert self.is_present((By.XPATH, self.county_options.format("Cambridge")))
        self.js_click((By.XPATH, self.county_options.format("Cambridge")))
        self.scroll_to_element((By.XPATH, self.choose_radio_button.format(
            "Now we'll test other grouping structures. Do you want to skip the first group?",
            'Yes')))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "Now we'll test other grouping structures. Do you want to skip the first group?",
            'Yes')))
        self.scroll_to_element((By.XPATH, self.choose_radio_button.format(
            "The next section tests groups within other groups. Which parts of the group do you want to skip?",
            "Outer and Inner")))
        self.js_click((By.XPATH, self.choose_radio_button.format("The next section tests groups within other groups. Which parts of the group do you want to skip?",
                                                                      "Outer and Inner")))
        self.scroll_to_element((By.XPATH, self.choose_radio_button.format(
            "Pick one of the following.", "One")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "Pick one of the following.","One")))
        self.js_click(self.submit_form_button)
        print("Group Form submitted successfully")
        time.sleep(2)
        self.js_click(self.home_button)
        time.sleep(2)
        self.wait_to_click(self.sync_button)
        time.sleep(2)

    def verify_choice_selection(self, locator, value):
        self.scroll_to_element(locator)
        self.js_click(locator)
        time.sleep(1)
        self.scroll_to_element((By.XPATH, self.pop_up_message.format(value)))
        assert self.is_present_and_displayed((By.XPATH, self.pop_up_message.format(value)))

    def end_of_navigation_module(self, case):
        login = LoginAsPage(self.driver)
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format("Submitting this will take you to the home screen.")), "home"+fetch_random_string())
        # self.wait_to_click(self.next_question)
        self.wait_to_click(self.submit_form_button)
        time.sleep(2)
        assert self.is_present((By.XPATH, self.case_list_menu.format(case)))
        time.sleep(2)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
        self.open_form(case, UserData.basic_test_app_forms["module"])
        self.wait_to_clear_and_send_keys(
            (By.XPATH, self.text_area_field.format("Submitting this will take you to the Module Menu.")),
            "module" + fetch_random_string())
        # self.wait_to_click(self.next_question)
        self.wait_to_click(self.submit_form_button)
        assert self.is_present((By.XPATH, self.case_list_menu.format(case)))
        time.sleep(2)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
        self.open_form(case, UserData.basic_test_app_forms["prev"])
        self.wait_to_clear_and_send_keys(self.search_input, "home"+fetch_random_string())
        self.wait_to_click(self.search_button)
        assert self.is_present_and_displayed((By.XPATH,self.module_search.format("home"+fetch_random_string())))
        self.js_click((By.XPATH, self.module_search.format("home" + fetch_random_string())))
        self.wait_to_click(self.continue_button)
        # self.wait_to_click(self.next_question)
        self.wait_to_click(self.submit_form_button)
        time.sleep(4)
        self.js_click(self.home_button)
        time.sleep(2)
        login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
        self.open_form(case, UserData.basic_test_app_forms["current"])
        self.wait_to_clear_and_send_keys(
            (By.XPATH, self.text_area_field.format("Submitting this form will take you to the current module.")),
            "current" + fetch_random_string())
        # self.wait_to_click(self.next_question)
        self.wait_to_click(self.submit_form_button)
        time.sleep(4)
        assert self.is_present_and_displayed((By.XPATH, self.case_list_menu.format(UserData.basic_test_app_forms["current"])))
        time.sleep(2)
        self.js_click(self.home_button)
        time.sleep(2)
        login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
        self.open_form(case, UserData.basic_test_app_forms["close"])
        self.wait_to_clear_and_send_keys(self.search_input, "home" + fetch_random_string())
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format("home" + fetch_random_string())))
        self.js_click((By.XPATH, self.module_search.format("home" + fetch_random_string())))
        self.wait_to_click(self.continue_button)
        # self.wait_to_click(self.next_question)
        self.wait_to_click(self.submit_form_button)
        time.sleep(3)
        assert self.is_present_and_displayed((By.XPATH, self.text_area_field.format("Submitting this will take you to the home screen.")))
        time.sleep(2)
        self.js_click(self.home_button)
        time.sleep(2)
        login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
        self.open_form(case, UserData.basic_test_app_forms["another"])
        self.wait_to_clear_and_send_keys(
            (By.XPATH, self.text_area_field.format("Submitting this will take you to the Module Badge Check Menu.")),
            "badge" + fetch_random_string())
        # self.wait_to_click(self.next_question)
        self.wait_to_click(self.submit_form_button)
        time.sleep(4)
        assert self.is_present_and_displayed(self.module_badge_table)
        time.sleep(2)
        self.js_click(self.home_button)
        time.sleep(2)



    def submit_basic_test_form(self):
        self.open_form(UserData.basic_tests_app['case_list'],UserData.basic_tests_app['form_name'])
        self.wait_to_clear_and_send_keys(self.name_question,fetch_random_string())
        self.wait_to_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.js_click(self.home_button)
        time.sleep(2)
        self.switch_to_default_content()

    def register_negative_case(self):
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format("What is the case name? You should not be allowed to proceed if the question is empty.")),
                                         self.case_reg_neg)
        time.sleep(0.5)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Are you sure you want to create a new case?", "Cancel - Please do not create this case.")))
        time.sleep(1)
        self.scroll_to_element(self.submit_form_button)
        self.wait_to_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)



    def register_positive_case(self):
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format("What is the case name? You should not be allowed to proceed if the question is empty.")),
                                         self.case_reg_pos)
        time.sleep(0.5)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Are you sure you want to create a new case?", "Confirm - Please create this case.")))
        time.sleep(1)
        self.scroll_to_element(self.submit_form_button)
        self.wait_to_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)

    def case_detail_verification(self):
        self.wait_for_element(self.search_input)
        self.wait_to_clear_and_send_keys(self.search_input, self.case_reg_pos)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format(self.case_reg_pos)))
        print("case search working properly")
        self.wait_to_click((By.XPATH, self.module_search.format(self.case_reg_pos)))
        self.wait_to_click((By.XPATH, self.case_detail_tab.format("1")))
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Name",self.case_reg_pos)))
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Status", "open")))
        self.wait_to_click((By.XPATH, self.case_detail_tab.format("2")))
        assert not self.is_present(self.case_detail_table_list)
        assert self.is_present(self.continue_button)
        self.wait_to_click(self.continue_button)
        time.sleep(2)
        self.wait_for_element(self.home_button)
        self.wait_to_click(self.home_button)
        time.sleep(2)


    def update_a_case(self):
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

        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Select one of the following:", self.input_dict['Singleselect'])))
        self.scroll_to_element((By.XPATH, self.choose_radio_button.format(
            "Select one or more of the following:", self.input_dict['Multiselect'][0])))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "Select one or more of the following:", self.input_dict['Multiselect'][0])))
        time.sleep(1)
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "Select one or more of the following:", self.input_dict['Multiselect'][1])))
        self.scroll_to_element((By.XPATH, self.input_field.format("Enter a phone number:")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format("Enter a phone number:")), self.input_dict['phone'])
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "Enter an integer:")), self.input_dict['intval'])
        self.wait_for_element(self.blank_latitude)
        self.scroll_to_element((By.XPATH, self.input_field.format(
            "Capture your location here:")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "Capture your location here:")), "Delhi")
        self.wait_to_click(self.search_location_button)
        time.sleep(2)
        assert not self.is_present_and_displayed(self.blank_latitude, 10)
        self.wait_to_click((By.XPATH, self.input_field.format(
            "Enter a date:")))
        self.wait_to_click(self.click_today_date)
        self.wait_to_click(self.close_date_picker)
        text = self.get_text(self.output)
        number = text.split(".")
        # new_data=str(re.findall(r'\b\d+\b', number[1])[0])
        print(str(re.findall(r'\b\d+\b', number[1])[0]))
        self.wait_to_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        return str(re.findall(r'\b\d+\b', number[1])[0])

    def updated_case_detail_verification(self, new_data):
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

    def create_and_verify_sub_case(self):
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
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format(
            "Enter a name for your sub case:")),
                                         self.subcase_pos+Keys.TAB)

        time.sleep(1)
        self.wait_for_element((By.XPATH, self.input_field.format(
            "Enter a number for "+self.subcase_pos+":")))
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "Enter a number for "+self.subcase_pos+":")), fetch_random_digit_with_range(1,20)+Keys.TAB)

        time.sleep(1)
        self.wait_for_element((By.XPATH, self.choose_radio_button.format(
            "Do you want to create the sub case?", "Confirm - Please create "+self.subcase_pos+".")))
        self.js_click((By.XPATH, self.choose_radio_button.format(
            "Do you want to create the sub case?", "Confirm - Please create "+self.subcase_pos+".")))
        time.sleep(1)
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        login = LoginAsPage(self.driver)
        login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
        self.open_case_list(UserData.basic_test_app_forms['subcaseone'])
        self.wait_for_element(self.search_input)
        self.wait_to_clear_and_send_keys(self.search_input, self.subcase_pos)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.module_search.format(self.subcase_pos)))
        print("case search working properly")
        self.wait_to_click((By.XPATH, self.module_search.format(self.subcase_pos)))
        time.sleep(2)
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Name", self.subcase_pos)))
        assert self.is_present_and_displayed((By.XPATH, self.case_detail_table.format("Parent Case Name", self.case_reg_pos)))
        assert self.is_present(self.continue_button)
        self.wait_to_click(self.continue_button)
        self.wait_to_click((By.XPATH, self.case_list_menu.format(UserData.basic_test_app_forms['close_subcase'])))
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Do you want to close the case?", "Yes")))

        self.wait_to_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)


    def close_case(self):
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
        self.wait_to_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        login = LoginAsPage(self.driver)
        login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
        self.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['caselist'])
        self.wait_for_element(self.search_input)
        self.wait_to_clear_and_send_keys(self.search_input, self.case_reg_pos)
        self.wait_to_click(self.search_button)
        time.sleep(2)
        assert self.is_present_and_displayed(self.empty_list)
        print("case search working properly")

    def unicode_verification_case(self):
        self.wait_to_clear_and_send_keys((By.XPATH, self.text_area_field.format(
            "What is the case name? You should not be allowed to proceed if the question is empty.")),
                                         self.unicode_text)
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Are you sure you want to create a new case?", "Confirm - Please create this case.")))
        self.js_click(self.submit_form_button)
        time.sleep(2)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)
        login = LoginAsPage(self.driver)
        login.open_basic_tests_app(UserData.basic_tests_app['tests_app'])
        self.open_form(UserData.basic_test_app_forms['case_test'], UserData.basic_test_app_forms['update_case'])
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
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Select one of the following:", self.input_dict['Singleselect'])))
        self.wait_to_click((By.XPATH, self.choose_radio_button.format(
            "Select one or more of the following:", self.input_dict['Multiselect'][0])))
        time.sleep(1)
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "Enter a phone number:")), self.input_dict['phone'])
        time.sleep(2)
        self.wait_to_clear_and_send_keys((By.XPATH, self.input_field.format(
            "Enter an integer:")), self.input_dict['intval'] + Keys.TAB)
        time.sleep(2)
        self.scroll_to_element((By.XPATH, self.input_field.format(
            "Capture your location here:")))
        self.send_keys((By.XPATH, self.input_field.format(
            "Capture your location here:")), "Delhi" + Keys.TAB)
        self.js_click(self.search_location_button)
        time.sleep(2)
        assert not self.is_present_and_displayed(self.blank_latitude, 10)
        time.sleep(2)
        self.wait_to_click((By.XPATH, self.input_field.format(
            "Enter a date:")))
        self.wait_to_click(self.click_today_date)
        self.wait_to_click(self.close_date_picker)
        time.sleep(2)
        self.js_click(self.submit_form_button)
        self.wait_for_element(self.success_message)
        self.wait_to_click(self.home_button)
        time.sleep(2)

    def verify_updated_unicode(self):
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
