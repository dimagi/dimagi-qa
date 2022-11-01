import time

from Formplayer.userInputs.generate_random_string import fetch_random_string, fetch_phone_number
from common_utilities.selenium.base_page import BasePage
from Formplayer.userInputs.user_inputs import UserData

from selenium.webdriver.common.by import By


""""Contains test page elements and functions related to the WebApps Access/Basics of Commcare"""


class AppPreviewBasics(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.name_input = "name" + fetch_random_string()

        self.application_menu_id = (By.LINK_TEXT, "Applications")
        self.select_test_application = (By.LINK_TEXT, UserData.test_app)
        self.form_builder_registration_form = (By.LINK_TEXT, "Registration Form")
        self.form_builder_follow_up_form = (By.LINK_TEXT, "Followup Form")
        self.add_question = (By.LINK_TEXT, "Add Question")
        self.text_question_type = (By.XPATH, "//a[@data-qtype = 'Text']")
        self.text_question_display_text = (By.XPATH, "//div[@name = 'itext-en-label']")
        self.save_question_button = (By.XPATH, "//span[contains(text(), 'Save')]")
        self.add_new_menu = (By.LINK_TEXT, "Add...")
        self.add_case_list = (By.XPATH, "//button[@class='popover-additem-option new-module'][./i[@class='fa fa-bars']]")

        self.view_app_preview = (By.XPATH, "//i[@class ='fa fa-chevron-left js-preview-action-show']")
        self.app_preview_window = (By.XPATH, "//i[@class ='preview-phone-container']")
        self.back_button = (By.XPATH, "//i[@class ='fa fa-chevron-left']")
        self.refresh_button = (By.XPATH, "//button[@class ='btn btn-hardware btn-preview-refresh js-preview-refresh']")
        self.toggle_button = (By.XPATH, "//button[@class ='btn btn-hardware btn-preview-toggle-tablet-view js-preview-toggle-tablet-view']")
        self.start_option = (By.XPATH, "//div[@class= 'js-start-app appicon appicon-start']")
        self.settings_option = (By.XPATH, "//div[@class = 'js-settings appicon appicon-settings']/i")
        self.login_as_option = (By.XPATH, "//div[@class='js-restore-as-item appicon appicon-restore-as']")
        self.case_list_menu = (By.XPATH, "//h3[contains(text(), 'Case List')]")
        self.registration_form = (By.XPATH, "//h3[contains(text(), 'Registration Form')]")
        self.followup_form = (By.XPATH, "//h3[contains(text(), 'Followup Form')]")
        self.name_question = (By.XPATH, "//textarea[@class ='textfield form-control']")
        self.dob_question = (By.XPATH,
                             '''//input[@data-bind = "attr: { id: entryId, 'aria-required': $parent.required() ? 'true' : 'false' }"]''')
        self.click_today_date = (By.XPATH, "//a[@data-action='today']")
        self.close_date_picker = (By.XPATH, "//a[@data-action='close']")
        self.mobileno_question = (By.XPATH, "//label[.//span[text()='Mobile No.']]/following-sibling::div//input")
        self.submit_form_button = (By.XPATH, "//button[@data-bind='enable: enableSubmitButton']")
        self.new_test_question = (By.XPATH, "//label[.//span[text()='Test']]")
        self.formplayer_test_question = (By.XPATH, "//a[@id='c8e668b2e915261cf463d0571d6ba3a3_anchor']")
        self.delete_button = (By.XPATH, "//button[@class='btn btn-danger fd-button-remove']")
        self.turn_on_one_question_toggle_button = (By.XPATH, "//td//div//span[text()='ON']")
        self.turn_off_one_question_toggle_button = (By.XPATH, "//td//div//span[text()='OFF']")
        self.done_button = (By.XPATH, "//button[@class = 'btn btn-primary js-done']")
        self.clear_user_data_button = (By.XPATH, "//button[text()='Clear']")
        self.clear_data_message = (By.XPATH, "//div[text()='User data successfully cleared.']")
        self.language_option = (By.XPATH, "//select[@class='form-control js-lang']")
        self.select_language = (By.XPATH, "//th[contains(text(),'application language')]/following-sibling::td/select")
        self.empty_form_error_message = (By.XPATH, "//strong[text()= 'Add a question']")
        self.next_question = (By.XPATH, "//button[@data-bind='click: nextQuestion, visible: enableNextButton() && !atLastIndex()']")
        self.complete_form = (By.XPATH, "//button[@data-bind='visible: atLastIndex(), click: submitForm']")
        self.success_message = (By.XPATH, "//p[text()='Form successfully saved!']")
        self.view_form_link = (By.LINK_TEXT, "this form")
        self.export_form_link = (By.LINK_TEXT, "form")
        self.delete_case_list_module = (By.XPATH, "(//a[./span[contains(text(),'Case List')]]/preceding-sibling::a[@class='appnav-delete']/i)[last()]")
        self.delete_confirm_button = (By.XPATH, "//button[./i[@class='fa fa-trash']]")
        self.question_display_text = (By.XPATH, "//span[text()='Name (es)']")
        self.iframe = (By.CLASS_NAME, "preview-phone-window")
        self.home_button = (By.XPATH, "//li[./i[@class='fa fa-home']]")
        self.full_menu = (By.LINK_TEXT, "Show Full Menu")

    def open_view_app_preview(self):
        if self.is_present(self.application_menu_id):
            self.wait_to_click(self.application_menu_id)
        else:
            self.wait_to_click(self.full_menu)
            self.wait_to_click(self.application_menu_id)
        self.wait_to_click(self.select_test_application)
        self.wait_to_click(self.view_app_preview)
        self.wait_to_click(self.refresh_button)

    def icons_are_present(self):
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.switch_to_default_content()
        assert self.is_present_and_displayed(self.back_button)
        print("back button")
        assert self.is_present_and_displayed(self.refresh_button), "Refresh button is not present"
        print("refesh button")
        assert self.is_present_and_displayed(self.toggle_button), "Toggle button is not present"

    def back_button_functionality(self):
        self.open_view_app_preview()
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        time.sleep(5)
        assert not self.is_present_and_displayed(self.start_option)
        time.sleep(5)
        self.switch_to_default_content()
        self.wait_to_click(self.back_button)
        self.switch_to_frame(self.iframe)
        assert self.is_present_and_displayed(self.start_option)
        print("Back button works!!")

    def refresh_button_functionality_01(self):
        self.open_view_app_preview()
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.wait_to_click(self.case_list_menu)
        self.switch_to_default_content()
        time.sleep(5)
        self.wait_to_click(self.refresh_button)
        time.sleep(3)
        self.switch_to_frame(self.iframe)
        assert self.is_present_and_displayed(self.start_option)
        print("Refresh Button works!!")

    def refresh_button_functionality_02(self):
        self.switch_to_default_content()
        self.open_view_app_preview()
        self.wait_to_click(self.form_builder_registration_form)
        self.wait_to_click(self.add_question)
        self.wait_to_click(self.text_question_type)
        self.wait_to_clear_and_send_keys(self.text_question_display_text, "Test")
        self.wait_to_click(self.save_question_button)
        self.wait_to_click(self.refresh_button)
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.wait_to_click(self.case_list_menu)
        self.wait_to_click(self.registration_form)
        assert self.is_present_and_displayed(self.new_test_question)
        self.switch_to_default_content()
        time.sleep(3)
        self.wait_to_click(self.formplayer_test_question)
        self.wait_to_click(self.delete_button)
        self.wait_to_click(self.save_question_button)
        time.sleep(3)
        self.wait_to_click(self.refresh_button)
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.wait_to_click(self.case_list_menu)
        self.wait_to_click(self.registration_form)
        assert not self.is_present_and_displayed(self.new_test_question)
        print("Refresh button works!!")

    def web_user_submission(self):
        self.open_view_app_preview()
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.wait_to_click(self.case_list_menu)
        self.wait_to_click(self.registration_form)
        self.wait_to_clear_and_send_keys(self.name_question, self.name_input)
        self.wait_to_click(self.dob_question)
        self.wait_to_click(self.click_today_date)
        self.wait_to_click(self.close_date_picker)
        self.wait_to_clear_and_send_keys(self.mobileno_question, fetch_phone_number())
        self.click(self.submit_form_button)
        assert self.is_present_and_displayed(self.success_message)
        assert self.is_present_and_displayed(self.view_form_link)
        self.wait_to_click(self.view_form_link)
        self.switch_to_next_tab()
        self.page_source_contains(self.name_input)
        assert self.is_present_and_displayed(self.export_form_link)

    def one_question_per_screen_negative(self):
        self.wait_to_click(self.application_menu_id)
        self.wait_to_click(self.select_test_application)
        self.wait_to_click(self.view_app_preview)
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        self.wait_to_click(self.case_list_menu)
        self.wait_to_click(self.registration_form)
        assert self.is_present_and_displayed(self.name_question)
        assert self.is_present_and_displayed(self.dob_question)
        assert self.is_present_and_displayed(self.mobileno_question)

    def one_question_per_screen_positive(self):
        self.wait_to_click(self.application_menu_id)
        self.wait_to_click(self.select_test_application)
        self.wait_to_click(self.view_app_preview)
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.settings_option)
        isChecked = self.driver.find_element(By.XPATH, "//th[(text()='Use one question per screen')]/following-sibling::td//input").is_selected()
        print(isChecked)
        if isChecked is True:
            self.js_click(self.turn_off_one_question_toggle_button)
            print("Toggled OFF")
        # self.wait_to_click((By.XPATH, "//th[(text()='Use one question per screen')]/following-sibling::td//input"))
        isChecked = self.driver.find_element(By.XPATH,
                                             "//th[(text()='Use one question per screen')]/following-sibling::td//input").is_selected()
        print(isChecked)
        self.wait_to_click(self.done_button)
        self.wait_to_click(self.start_option)
        self.wait_to_click(self.case_list_menu)
        self.wait_to_click(self.registration_form)

        # self.wait_to_click(self.turn_off_one_question_toggle_button)
        # self.wait_to_click(self.do    ne_button)
        # self.wait_to_click(self.start_option)
        # self.wait_to_click(self.case_list_menu)
        # self.wait_to_click(self.registration_form)
        self.wait_to_clear_and_send_keys(self.name_question, self.name_input)
        # self.wait_to_click(self.next_question)
        self.wait_to_click(self.dob_question)
        self.wait_to_click(self.click_today_date)
        self.wait_to_click(self.close_date_picker)
        # self.wait_to_click(self.next_question)
        self.wait_to_clear_and_send_keys(self.mobileno_question, fetch_phone_number())
        # self.wait_to_click(self.next_question)
        # self.wait_to_click(self.complete_form)
        # self.wait_to_click(self.home_button)
        # self.wait_to_click(self.settings_option)
        # self.wait_to_click(self.turn_off_one_question_toggle_button)
        # self.wait_to_click(self.done_button)

    def clear_user_data(self):
        self.open_view_app_preview()
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.settings_option)
        self.wait_to_click(self.clear_user_data_button)
        assert self.is_present_and_displayed(self.clear_data_message)

    def change_language(self):
        self.open_view_app_preview()
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.settings_option, 5)
        self.select_by_text(self.select_language, UserData.language)
        self.wait_to_click(self.done_button)
        self.wait_to_click(self.start_option)
        self.wait_to_click(self.case_list_menu)
        self.wait_to_click(self.registration_form)
        assert self.is_present_and_displayed(self.question_display_text)

    def add_empty_form(self):
        self.open_view_app_preview()
        self.click(self.add_case_list)
        time.sleep(3)
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        assert self.is_present_and_displayed(self.empty_form_error_message)
        self.switch_to_default_content()
        self.wait_to_click(self.delete_case_list_module)
        self.wait_to_click(self.delete_confirm_button)
        self.switch_to_frame(self.iframe)
        self.wait_to_click(self.start_option)
        assert self.is_present_and_displayed(self.registration_form)

