import time

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

from common_utilities.selenium.base_page import BasePage
from HQSmokeTests.userInputs.user_inputs import UserData

""""Contains test page elements and functions related to the Manage Forms module"""


class ManageFormsPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.manage_forms_link = (By.LINK_TEXT, 'Manage Forms')
        self.select_app_dropdown = (By.ID, 'report_filter_form_app_id')
        self.select_module_dropdown = (By.ID, 'report_filter_form_module')
        self.select_sub_time = (By.ID, "report_filter_sub_time")
        self.basic_tests_app = (By.XPATH, "//option[text()='Basic Tests']")
        self.apply_button = (By.XPATH, '//*[@id="apply-btn"]')
        self.select_all_checkbox = (By.XPATH, "//input[@name='select_all']")
        self.last_form_checkbox = (By.XPATH, "(//input[@type='checkbox' and @name='xform_ids'])[last()]")
        self.checkbox1 = (By.XPATH, "//*[@id='form_options']//*[@type='checkbox']")
        self.archive_button = (By.XPATH, '//*[@id="submitForms"]')
        self.restore_button = (By.XPATH, '//*[@id="submitForms" and contains(text(),"Restore")]')
        self.success_message = (By.XPATH, "//div[@class='alert alert-success']")
        self.view_form_link = (By.XPATH, "(//a[@class='ajax_dialog'])[last()]")
        self.archived_restored_dropdown = (By.XPATH, '//*[@id="select2-report_filter_archive_or_restore-container"]')
        self.archived_forms_option = (By.XPATH, '/html/body/span/span/span[2]/ul/li[2]')
        self.manage_forms_return = (By.XPATH, '//span[contains(text(),"Return to")]/a[.="Manage Forms"]')
        self.apply = (By.XPATH, "//button[@class='applyBtn btn btn-sm btn-primary']")
        self.date_range_manage_forms = (By.ID, "filter_range")
        self.date_range_type = "//li[@data-range-key='{}']"
        self.users_field = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]")
        self.users_list_item = "//ul[@role='listbox']/li[contains(.,'{}')][1]"
        self.village_app = (By.XPATH, "//option[text()='Village Health']")
        self.select_archive_restore = (By.XPATH, "//select[@name='archive_or_restore']")
        self.check_data = (By.XPATH, "//tr[@class = 'form-data-question ']")
        self.remove_buttons = (By.XPATH, "//ul//button")
        self.result_table = (By.XPATH, "(//div[@id='report-content']//table//tbody//td[1])[1]")
        self.report_content_id = (By.ID, "report-content")

    def get_normal_forms(self, url=None):
        self.wait_and_sleep_to_click(self.manage_forms_link)

        # Date Filter
        self.wait_for_element(self.date_range_manage_forms, 150)
        self.wait_and_sleep_to_click(self.date_range_manage_forms)
        self.select_by_value(self.select_archive_restore, "archive")
        self.clear(self.date_range_manage_forms)
        if url == None:
            self.send_keys(self.date_range_manage_forms, UserData.date_having_submissions)
        elif "eu" in url:
            self.send_keys(self.date_range_manage_forms, UserData.eu_date_having_submission)
        else:
            self.send_keys(self.date_range_manage_forms, UserData.india_date_having_submission)
        self.remove_default_users()
        web_user = str(UserData.web_user).strip("[]")
        self.send_keys(self.users_field, web_user)
        self.wait_to_click((By.XPATH, self.users_list_item.format(web_user)), 30)
        # Report Apply
        self.wait_and_sleep_to_click(self.apply_button)
        time.sleep(2)

    def assert_normal_form_view(self):
        link=self.get_attribute(self.view_form_link,"href")
        print("link")
        self.wait_and_sleep_to_click(self.view_form_link)
        self.switch_to_next_tab()
        verify_data = self.find_elements(self.check_data)
        assert len(verify_data) > 0, "normal_form has no data"
        print("normal_form has data")
        self.driver.close()
        self.switch_back_to_prev_tab()

    def view_normal_form(self):
        result = self.is_present_and_displayed(self.view_form_link)
        if not result:
            self.select_by_value(self.select_archive_restore, "restore")
            self.wait_to_click(self.apply_button)
            self.restore_all_forms()
            self.get_normal_forms()
            self.assert_normal_form_view()
        else:
            self.assert_normal_form_view()

    def archive_forms(self):
        self.wait_and_sleep_to_click(self.last_form_checkbox)
        self.wait_and_sleep_to_click(self.archive_button)
        assert self.is_present_and_displayed(self.success_message)
        print("Forms archival successful!!")
        time.sleep(3)

    def get_archived_forms(self):
        self.wait_and_sleep_to_click(self.manage_forms_link)
        self.wait_for_element(self.date_range_manage_forms, 150)
        self.remove_default_users()
        web_user = str(UserData.web_user).strip("[]")
        self.send_keys(self.users_field, web_user)
        self.wait_to_click((By.XPATH, self.users_list_item.format(web_user)), 30)
        self.wait_and_sleep_to_click(self.archived_restored_dropdown)
        self.wait_and_sleep_to_click(self.archived_forms_option)
        self.wait_and_sleep_to_click(self.apply_button)
        self.reload_page()
        self.wait_for_element(self.view_form_link, 200)

    def view_archived_forms(self):
        self.wait_and_sleep_to_click(self.view_form_link)
        self.switch_to_next_tab()
        normal_form_data = self.driver.page_source
        assert normal_form_data != ""  # This condition can be improvised
        print("archived_form has data")
        self.driver.close()
        self.switch_back_to_prev_tab()

    def restore_forms(self):
        self.wait_and_sleep_to_click(self.last_form_checkbox)
        self.wait_and_sleep_to_click(self.archive_button)
        assert self.is_present_and_displayed(self.success_message)
        print("Forms Restoration successful!!")

    def restore_all_forms(self):
        self.wait_and_sleep_to_click(self.select_all_checkbox)
        self.wait_and_sleep_to_click(self.restore_button)
        assert self.is_present_and_displayed(self.success_message)
        print("Forms Restoration successful!!")
        
    def remove_default_users(self):
        self.wait_for_element(self.users_field)
        count = self.find_elements(self.remove_buttons)
        print(len(count))
        for i in range(len(count)):
            count[0].click()

            if len(count) != 1:
                ActionChains(self.driver).send_keys(Keys.TAB).perform()

            count = self.find_elements(self.remove_buttons)
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()


    def weekly_archive_forms(self, app, form, date_range, sub_time):
        self.wait_for_element(self.manage_forms_link)
        self.click(self.manage_forms_link)

        # Date Filter
        self.wait_for_element(self.date_range_manage_forms, 150)
        self.wait_to_click(self.date_range_manage_forms)
        self.wait_to_click((By.XPATH, self.date_range_type.format(date_range)))
        self.select_by_text(self.select_app_dropdown, app)
        self.select_by_text(self.select_module_dropdown, form)
        self.select_by_value(self.select_sub_time, sub_time)
        self.select_by_value(self.select_archive_restore, "archive")
        self.wait_to_click(self.apply_button)
        time.sleep(2)
        try:
            self.wait_for_element(self.result_table, 300)
            self.wait_for_element(self.report_content_id, 120)
            print("Report loaded successfully!")
            time.sleep(2)
            self.wait_and_sleep_to_click(self.select_all_checkbox)
            self.wait_and_sleep_to_click(self.archive_button)
            assert self.is_present_and_displayed(self.success_message, 500)
            print("Forms archival successful!!")
        except:
            print("No forms to archive")