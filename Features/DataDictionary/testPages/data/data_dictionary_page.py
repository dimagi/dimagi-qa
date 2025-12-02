import os.path
import time
from time import sleep

from matplotlib.widgets import EllipseSelector
from selenium.webdriver.common.by import By

from ElasticSearchTests.testCases.conftest import settings
from Features.DataDictionary.userInputs.user_inputs import UserData
from HQSmokeTests.testCases.conftest import driver
from HQSmokeTests.testPages.home.home_page import HomePage
from common_utilities.Excel.excel_manage import ExcelManager
from common_utilities.selenium.base_page import BasePage
from common_utilities.generate_random_string import fetch_random_string
from common_utilities.path_settings import PathSettings
from selenium.webdriver.support.select import Select

""""Contains test page elements and functions related to the Lookup Table module"""


class DataDictionaryPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        # data dictionary page
        self.view_data = (By.XPATH, " //*[@id='ProjectDataTab']")
        self.data = (By.LINK_TEXT, "Data")
        self.view_all = (By.LINK_TEXT, "View All")
        self.dd = (By.XPATH, "//*[@class='text-hq-nav-header']")
        self.check = (By.XPATH, "//*[@id='download-dict']")
        self.datatype = (By.XPATH, "//div[.//span[text()='select_dd_language']]/following-sibling::div/select[contains(@data-bind,'Select a data type')]")
        self.dd_language = (By.XPATH, "(//select[@class='form-control'])[1]")
        self.upload = (By.XPATH, "//*[@id='gtm-upload-dict']")
        self.choose_file_text_field = (By.XPATH, "//input[@id='file']")
        self.upload_button = (By.XPATH, "//*[@class='btn btn-primary disable-on-submit']")
        self.type_value = (By.XPATH, "//*[@id='case_type']")
        self.save = (By.XPATH, "//*[@class='pull-right savebtn-bar savebtn-bar-save']")
        self.case_type_value = (By.XPATH, "//a[@href='#dd_case']/span[contains(text(), 'dd_case')]")
        self.case_property_multiple_choice = (By.XPATH, "//div[.//span[text()='select_dd_language']]/following-sibling::div/select[contains(@data-bind,'Select a data type')]")
        self.case_property_date = (By.XPATH, "//div[.//span[text()='opened_date']]/following-sibling::div/select[contains(@data-bind,'Select a data type')]")
        self.case_property_age = (By.XPATH,"//div[.//span[text()='enter_dd_age']]/following-sibling::div/select[contains(@data-bind,'Select a data type')]")
        self.property_description_field = (By.XPATH, "(//input[@placeholder='Group_new']//following::div[contains(@class,'row-item-big') and contains(@class,'main-form')]/textarea)[1]")
        self.add_property = (By.XPATH, "//*[@placeholder='Group_new']/following::input[@placeholder='Case Property'][1]")
        self.property_value = (By.XPATH, "//input[@placeholder='Group_new']/ancestor::div[contains(@class,'row-item')]/following::input[@placeholder='Click here to add a label'][1]")
        self.add_group = (By.XPATH, "//input[@placeholder='Group Name']")
        self.add_property_button = (By.XPATH, "//*[@id='gtm-add-case-property']")
        self.added_group_description = (By.XPATH, "//input[@placeholder='Group_new']/ancestor::div[contains(@class,'row-item')]/following::div[contains(@class,'row-item-big')][1]//textarea")
        self.deprecate_button = (By.XPATH, "(//*[@id='gtm-deprecate-case-property'])[1]")
        self.show_deprecate = (By.XPATH, "//*[@data-bind='click: $root.showDeprecated, visible: !showAll()']")
        self.restore_button = (By.XPATH, "//button[@title='Restore Property']")
        self.hide_deprecate = (By.XPATH, "//*[@data-bind='click: $root.hideDeprecated, visible: showAll']")
        self.deprecate_case = (By.XPATH, "//a[@class='btn btn-default' and contains(text(),'Deprecate Case Type')]")
        self.confirm = (By.XPATH, "//*[@id='gtm-deprecate-case-type-confirm']")
        self.show_deprecate_case_type = (By.XPATH, "//*[@class='deprecate-case-type']")
        self.data_dictionary = (By.LINK_TEXT, "Data Dictionary")
        self.delete_case_property = (By.XPATH, "(//input[@placeholder='Group_new']//following::button[@title='Delete Property'])[1]")
        self.delete_property_confirm = (By.XPATH, "//button[@id='delete-case-prop-btn']")
        self.show_deprecated_case_type = (By.XPATH, "//*[@class='deprecate-case-type']")
        self.restore_case_type = (By.XPATH, "//button[@class='btn btn-default' and contains(text(),'Restore Case Type')]")
        self.restore_case_type_new = (By.XPATH, "//button[@title='Restore Property']")
        self.date_valid_values = (By.XPATH,"//span[normalize-space()='opened_date']/../../following-sibling::div//div[normalize-space()='YYYY-MM-DD']")
        self.edit_button = (By.XPATH,"//span[normalize-space()='select_dd_language']/../../following-sibling::div//a[contains(@class,'enum-edit')]")
        self.valid_value_text = (By.XPATH, "(//input[@placeholder='valid value'])")
        self.valid_description = (By.XPATH, "(//input[@placeholder='description'])")
        self.done = (By.XPATH, "(//button[@class='btn btn-primary'][normalize-space()='Done'])[1]")
        self.property_deprecate = (By.XPATH, "//div[.//span[text()='enter_dd_age']]/following-sibling::div/button[@id='gtm-deprecate-case-property']")
        self.property_deprecate_message = (By.XPATH, "//code[normalize-space()='enter_dd_age']/ancestor::span[1]/following::p[contains(.,'Property has been deprecated.')]")
        self.data_bold = (By.XPATH, "//ol[@id='hq-breadcrumbs']/li/a/strong")
        self.property_description_age = (By.XPATH, "//span[normalize-space()='enter_dd_age']/following::textarea[1]")
        self.add_property_values = "//div[@class='atwho-view'][not(contains(@style,'none'))]//li//strong[.='{}'] "
        self.delete_button_vv = (By.XPATH, "//a[@data-enum-action='remove']")
        self.upload_error_message = (By.XPATH,"//div[@id='hq-messages-container']/div[@class='row']/div[@class='col-sm-12']/div[@class='alert alert-margin-top fade in html alert-danger']")

        # In App
        self.make_new_version_button = (By.XPATH, "//button[contains(@data-bind,'Make New Version')]")
        self.case_list = (By.XPATH, "//span[contains(text(),'Case List')]")
        self.case_type_warning = (By.XPATH, "//*[@id='deprecated-case-types-warning']")
        self.applications_menu_id = (By.ID, "ApplicationsTab")
        self.case_list_warning = (By.XPATH, "//*[@id='case_type_deprecated_warning']")
        self.app_description = (By.XPATH,"//*[@placeholder='Enter app description here']")
        self.edit_icon = (By.XPATH, "//div[contains(@class,'edit-description')]//i[contains(@class,'pencil')]")
        self.save_description = (By.XPATH,
                                 "//div[.//textarea[@placeholder='Enter app description here']]/following-sibling::div[@class='form-group']/button[contains(@data-bind,'click: save')]/i")
        self.case_data_page_warning = (By.XPATH, "//*[@class='alert alert-warning']")
        self.registration_form = (By.XPATH, "//span[normalize-space()='Registration Form']")
        self.settings_icon = (By.XPATH, "//span[normalize-space()='Registration Form']/parent::a/following-sibling::a")
        self.description_text = (By.XPATH, "//div[@data-content='Testing the age property description']")
        self.app_summary_button = (By.XPATH,
                                   "//*[@class='appmanager-page-actions']/a/i[@class = 'fa-regular fa-rectangle-list']")
        self.case_summary_button = (By.XPATH, "//*[@class='fcc fcc-fd-external-case appnav-primary-icon']")
        self.description_property = (By.XPATH, "//*[contains(text(),'Testing the age property description')]")

        # Reports
        self.case_list_explorer_report = (By.LINK_TEXT, "Case List Explorer")
        self.report_case_type = (By.XPATH, "//select[contains(@id,'report_filter_case_type')]")

        # Exports
        self.export_case_data_link = (By.LINK_TEXT, 'Export Case Data')
        self.add_export_button = (By.XPATH, "//div[@id='create-export']/p/a")
        self.case_type_dropdown = (By.XPATH, "//select[@name='case_type']")
        self.daily_saved_exports_link = (By.LINK_TEXT, 'Daily Saved Exports')
        self.model_type = (By.ID, "id_model_type")
        self.export_excel_dash_int = (By.LINK_TEXT, 'Excel Dashboard Integration')
        self.powerBI_tab_int = (By.LINK_TEXT, 'PowerBi/Tableau Integration')
        self.add_export_conf = (By.XPATH, "//button[@data-bind='visible: showSubmit, disable: disableSubmit']")
        self.export_settings_create = (By.XPATH, "//button[@class='btn btn-lg btn-primary']")
        self.warning_label = (By.XPATH, "//*[@class='badge text-bg-warning']")
        self.case_type_dropdown_export = (By.XPATH, "//label[.='Case Type']//following-sibling::div/select[@name='case_type']")
        self.copy_cases_menu = (By.LINK_TEXT, "Copy Cases")
        self.reassign_cases_menu = (By.LINK_TEXT, "Reassign Cases")
        self.reassign_case_type = (By.ID, "report_filter_case_type")
        self.deduplicate_case_link = (By.LINK_TEXT, 'Deduplicate Cases')
        self.add_rule_button = (By.ID, 'add-new')
        self.add_rule_name = (By.XPATH, "//input[@type='text']")
        self.deduplicate_case_type = (By.XPATH, "//select[@name='case_type']")
        self.import_cases_menu = (By.LINK_TEXT, "Import Cases from Excel")
        self.choose_file = (By.XPATH, "//input[@id='id_bulk_upload_file']")
        self.next_step = (By.XPATH, "//button[normalize-space()='Next step']")

        # Messaging
        self.cond_alerts = (By.LINK_TEXT, "Conditional Alerts")
        self.add_cond_alert = (By.LINK_TEXT, "New Conditional Alert")
        self.messaging_menu_id = (By.ID, "MessagingTab")
        self.case_type_ca = (By.XPATH, "//select[contains(@name,'case_type')]")
        self.cond_alert_name_input = "cond_alert_" + fetch_random_string()
        self.cond_alert_name = (By.XPATH, "//input[@name='conditional-alert-name']")
        self.continue_button_basic_tab = (By.XPATH, "//button[@data-bind='click: handleBasicNavContinue, enable: basicTabValid']")

        # CLE
        self.edit_column = (By.XPATH,"//div[./label[contains(.,'Columns')]]//following-sibling::div//a[@data-parent='#case-list-explorer-columns']")
        self.properties_table = (By.XPATH, "//tbody[contains(@data-bind,'properties')]")
        self.add_property_button_cle = (By.XPATH, "//button[normalize-space()='Add Property']")
        self.property_name_input = (By.XPATH, "(//tbody[contains(@data-bind,'properties')]//td[2]//input)[last()]")
        self.apply_id = (By.ID, "apply-filters")
        self.add_property_column = (By.XPATH, "(//table[contains(@class,'datatable')]//th[5])[1]")

    def verify_data_page(self,flag):
        self.js_click(self.data_dictionary, 5)
        if self.is_present_and_displayed(self.case_type_value):
            assert self.is_present_and_displayed(self.case_type_value, 2),"dd page not opened"
        else:
            self.case_type_restore()
        if flag =='Y':
            self.wait_to_click(self.case_type_value)

    def verify_dropdown_values(self):
        self.wait_to_click(self.datatype)
        dropdown_values = self.find_elements_texts(self.datatype)
        print(dropdown_values)
        dt = ['Select a data type\nDate\nPlain\nNumber\nMultiple Choice\nBarcode\nGPS\nPhone Number\nPassword']
        assert dropdown_values == dt
        print("Below are the dropdown values")
        for data_type in dropdown_values:
            print(data_type)

    def verify_file_getting_downloaded(self):
        self.wait_to_click(self.check, 2)
        print("File is downloaded")
        time.sleep(5)


    def verify_uploading_dd(self, path):
        download_path = str(PathSettings.DOWNLOAD_PATH / path)
        self.wait_to_click(self.upload, 2)
        self.send_keys(self.choose_file, download_path)
        self.wait_to_click(self.upload_button, 2)
        if self.is_present_and_displayed(self.upload_error_message):
            print("Error in uploading file")
        else:
            print("File is upload")

    def update_case_property_description(self):
        time.sleep(10)
        self.wait_to_click(self.property_description_field)
        self.wait_to_clear_and_send_keys(self.property_description_field, UserData.new_property_description)
        self.wait_to_click(self.added_group_description)
        time.sleep(2)
        self.wait_to_clear_and_send_keys(self.added_group_description,UserData.group_description)
        self.wait_to_click(self.save)

    def add_new_case_property(self):
        self.wait_to_click(self.case_type_value, 5)
        self.wait_to_click(self.add_property)
        self.send_keys(self.add_property, UserData.case_properties)
        time.sleep(2)
        self.wait_to_click(self.add_property_button)
        self.wait_to_click(self.save)
        value_text = self.wait_to_get_value(self.property_value)
        print("new property added :", value_text)
        return value_text

    def view_case_list_explorer_report(self, value, flag):
        self.wait_to_click(self.case_list_explorer_report)
        time.sleep(30)
        self.wait_for_element(self.edit_column)
        self.wait_to_click(self.edit_column,10)
        self.wait_for_element(self.properties_table)
        self.wait_to_click(self.add_property_button_cle)
        self.wait_to_click(self.property_name_input)
        self.send_keys(self.property_name_input, value)
        time.sleep(0.5)
        if flag == "yes":
            assert self.is_present(
                (By.XPATH, self.add_property_values.format(value))), 'entered property is not displayed'
            print("entered property displayed on the dropdown")
        else:
            assert not self.is_present(
                (By.XPATH, self.add_property_values.format(value))), "Entered property is displayed"
            print("added property is deleted on data dictionary page")
        self.wait_to_click(self.apply_id)
        time.sleep(10)
        self.scroll_to_bottom()
        self.is_present_and_displayed(self.add_property_column)
        property_added = self.get_text(self.add_property_column)
        assert property_added == value
        print("Added property displayed on the CLE report result page")

    def delete_added_case_property(self):
        self.reload_page()
        self.wait_to_click(self.delete_case_property)
        self.wait_to_click(self.delete_property_confirm)
        self.wait_to_click(self.save)
        time.sleep(5)
        assert self.is_present_and_displayed(self.property_description_field),"Property is not deleted"


    def updating_group_description(self):
        self.wait_to_click(self.case_type_value, 10)
        self.wait_to_clear_and_send_keys(self.added_group_description, UserData.updated_group_description_value)
        self.wait_to_click(self.add_group)
        self.wait_to_click(self.save, 10)

    def deprecating_property(self):
        self.wait_to_click(self.case_type_value, 2)
        self.wait_to_click(self.deprecate_button, 2)
        self.wait_to_click(self.save, 5)
        self.reload_page()
        self.js_click(self.show_deprecate, 2)
        self.is_present_and_displayed(self.restore_button)
        print("Restore button is displayed")
        self.is_present_and_displayed(self.hide_deprecate)
        print("hide deprecate button is displayed")
        self.wait_to_click(self.restore_button)
        self.wait_to_click(self.save, 2)
        print("Case property  is restored")

    def case_type_deprecate(self):
        self.wait_to_click(self.case_type_value, 10)
        self.wait_to_click(self.deprecate_case, 10)
        self.wait_to_click(self.confirm, 10)
        self.wait_to_click(self.show_deprecate_case_type, 10)
        # assert self.is_present_and_displayed(self.case_type_value), "Case type is deprecated"
        # "case type not deprecated"
        self.wait_to_click(self.data_bold)

    def case_type_restore(self):
        self.wait_to_click(self.data_bold,10)
        self.js_click(self.data_dictionary,10)
        self.wait_to_click(self.show_deprecated_case_type)
        self.wait_to_click(self.case_type_value)
        self.wait_to_click(self.restore_case_type)
        assert self.is_present_and_displayed(self.case_type_value) , "case type has been restored"
        self.wait_to_click(self.data_bold)

    def validating_application(self):
        self.wait_to_click(self.edit_icon)
        self.wait_to_clear_and_send_keys(self.app_description, UserData.application_description)
        self.wait_to_click(self.save_description)
        self.wait_to_click(self.make_new_version_button)
        time.sleep(10)
        assert self.is_present_and_displayed(self.case_type_warning) ,"Property not deprecated"
        warning_message = self.wait_to_get_text(self.case_type_warning)
        print(warning_message)
        self.js_click(self.case_list, 20)
        assert self.is_present_and_displayed(self.case_list_warning), "Property not deprecated"
        print("This case type has been deprecated in the Data Dictionary on case list page")

    def validating_app_summary(self):
        self.wait_to_click(self.app_summary_button)
        self.wait_to_click(self.case_summary_button)
        self.wait_to_click(self.description_property)
        property_description_value = self.get_text(self.description_property)
        assert property_description_value == 'Testing the age property description' ,"Property is not displayed on the app summary page"
        "Descriptions of each property automatically show in the App Summary page."

    def verify_case_data_page(self):
        url = self.get_current_url()
        if "staging" in url:
            self.get_url(UserData.case_data_link_staging)
        elif "prod" in url:
            self.get_url(UserData.case_data_link_prod)
        assert self.is_present_and_displayed(self.case_data_page_warning), "casetype not depreated on the case data page"
        "This case uses a deprecated case type. See the help documentation for more information is displayed"

    def verify_reports(self):
        time.sleep(50)
        self.wait_to_click(self.case_list_explorer_report, 20)
        self.wait_for_element(self.report_case_type, 60)
        dropdown = self.get_all_dropdown_options(self.report_case_type)
        if 'dd_case' in dropdown:
            print("Active case types are displayed in the reports.")
        else:
            print("deprecated case types are not displayed in the reports.")

    def verify_exports(self):
        self.wait_to_click(self.export_case_data_link, 10)
        self.wait_for_element(self.add_export_button, 200)
        self.wait_to_click(self.add_export_button)
        time.sleep(15)
        self.wait_for_element(self.case_type_dropdown, 200)
        dropdown = self.get_all_dropdown_options(self.case_type_dropdown)
        if 'dd_case' in dropdown:
            print("Active case types are displayed in the case exports.")
        else:
            print("deprecated case types are not displayed in the  case exports.")
        self.wait_to_click(self.daily_saved_exports_link)
        self.wait_to_click(self.add_export_button, 30)
        self.is_visible_and_displayed(self.model_type, 200)
        self.wait_for_element(self.model_type, 400)
        self.select_by_value(self.model_type, UserData.model_value)
        dropdown = self.get_all_dropdown_options(self.case_type_dropdown)
        if 'dd-case' in dropdown:
            print("Active case types are displayed in the daily saved exports.")
        else:
            print("deprecated case types are not displayed in the daily saved exports.")
        self.wait_to_click(self.export_excel_dash_int)
        self.wait_to_click(self.add_export_button)
        time.sleep(5)
        self.wait_to_click(self.model_type)
        self.select_by_value(self.model_type, UserData.model_value)
        dropdown = self.get_all_dropdown_options(self.case_type_dropdown)
        if 'dd_case' in dropdown:
            print("Active case types are displayed in the excel dashboard exports.")
        else:
            print("deprecated case types are not displayed in the excel dashboard exports.")
        self.wait_to_click(self.powerBI_tab_int)
        self.wait_to_click(self.add_export_button)
        self.wait_to_click(self.model_type)
        self.select_by_value(self.model_type, UserData.model_value)
        dropdown = self.get_all_dropdown_options(self.case_type_dropdown)
        if 'dd_case' in dropdown:
            print("Active case types are displayed in the power bi exports.")
        else:
            print("deprecated case types are not displayed in the power bi exports.")

    def create_case_export(self):
        self.wait_to_click(self.export_case_data_link, 10)
        self.wait_to_click(self.add_export_button, 200)
        self.wait_to_click(self.case_type_dropdown)
        self.select_by_value(self.case_type_dropdown, UserData.case_type)
        self.wait_to_click(self.add_export_conf)
        self.wait_to_click(self.export_settings_create)
        print("Export created!!")

    def validate_exports(self):
        self.wait_to_click(self.export_case_data_link, 10)
        self.is_present_and_displayed(self.warning_label)
        print("deprecated case type label displayed on the already created export")

    def validate_exports_edit_data_section(self, filepath):
        self.js_click(self.data_bold,10)
        self.wait_to_click(self.copy_cases_menu, 200)
        self.wait_for_element(self.case_type_dropdown_export, 200)
        dropdown = self.get_all_dropdown_options(self.case_type_dropdown_export)
        if 'dd_case' in dropdown:
            print("Active case types are displayed in the copy cases page.")
        else:
            print("deprecated case types are not displayed in the copy cases page.")
        self.wait_to_click(self.reassign_cases_menu, 100)
        dropdown = self.get_all_dropdown_options(self.reassign_case_type)
        if 'dd_case' in dropdown:
            print("Active case types are displayed in the reassign cases page.")
        else:
            print("deprecated case types are not displayed in the reassign cases page.")
        self.wait_to_click(self.deduplicate_case_link, 100)
        self.wait_to_click(self.add_rule_button)
        self.send_keys(self.add_rule_name, 'deduplicate_rule')
        dropdown = self.get_all_dropdown_options(self.deduplicate_case_type)
        if 'dd_case' in dropdown:
            print("Active case types are displayed in the deduplicate page.")
        else:
            print("deprecated case types are not displayed in the deduplicate page.")
        self.wait_to_click(self.import_cases_menu, 50)
        time.sleep(5)
        filepath = os.path.abspath(os.path.join(UserData.user_input_base_dir, filepath))
        # filepath = str(UserData.user_input_base_dir + "\\" + filepath)
        print("File Path: ", filepath)
        self.wait_for_element(self.choose_file_text_field)
        self.send_keys(self.choose_file_text_field, filepath)
        self.wait_for_element(self.next_step)
        self.js_click(self.next_step)
        self.is_visible_and_displayed(self.case_type_ca)
        dropdown = self.get_all_dropdown_options(self.case_type_ca)
        if 'dd_case' in dropdown:
            print("Active case types are displayed in the import cases from excel page.")
        else:
            print("deprecated case types are not displayed in the import cases from excel page.")
        self.js_click(self.data_dictionary)


    def verify_conditional_alert_under_messaging(self):
        self.wait_to_click(self.cond_alerts)
        self.wait_to_click(self.add_cond_alert)
        self.send_keys(self.cond_alert_name, self.cond_alert_name_input)
        self.wait_to_click(self.continue_button_basic_tab)
        time.sleep(10)
        self.wait_to_click(self.case_type_ca, 10)
        dropdown = self.get_all_dropdown_options(self.case_type_ca)
        if 'dd_case' in dropdown:
            print("Active case types are displayed in the conditional alert page.")
        else:
            print("deprecated case types are not displayed in the conditional alert page.")

    def verify_valid_values_date_type(self):
        self.select_by_text(self.case_property_date, 'Plain')
        self.select_by_text(self.case_property_date,'Date')
        import_validation = self.wait_to_get_text(self.date_valid_values)
        assert import_validation == "YYYY-MM-DD","valid values not selected properly for date type"
        self.wait_to_click(self.case_property_date)
        self.wait_to_click(self.save)

    def verify_valid_values_multiple_choice_type(self):
        self.select_by_text(self.case_property_multiple_choice, 'Multiple Choice')
        self.wait_to_click(self.edit_button)
        self.wait_to_click(self.valid_value_text, 2)
        self.wait_to_clear_and_send_keys(self.valid_value_text, UserData.english_value)
        self.wait_to_click(self.valid_description, 2)
        self.wait_to_clear_and_send_keys(self.valid_description, UserData.english_value)
        self.js_click(self.done)

    def verify_excel_verification(self, download_path):
        download_path = str(PathSettings.DOWNLOAD_PATH / download_path)
        time.sleep(5)
        excel = ExcelManager()
        excel.read_excel('dd_case-vl', download_path)
        print("The valid values are displayed")

    def verify_update_excel(self, download_path):
        download_path = str(PathSettings.DOWNLOAD_PATH / download_path)
        excel = ExcelManager()
        excel.write_excel_data('dd_case', 2, 6, UserData.plain, download_path)

    def verify_updating_excel_invalid_values(self, download_path):
        download_path1 = str(PathSettings.DOWNLOAD_PATH / download_path)
        excel = ExcelManager()
        #excel.write_excel_data('dd_case-vl', 1, 1, UserData.value, download_path1)
        excel.write_excel_data('dd_case-vl', 2, 2, UserData.randomvalue, download_path1)

    def verify_updating_excel_valid_values(self, download_path):
        download_path1 = str(PathSettings.DOWNLOAD_PATH / download_path)
        excel = ExcelManager()
        #excel.write_excel_data('dd_case-vl', 1, 1, UserData.value, download_path1)
        excel.write_excel_data('dd_case-vl', 2, 2, UserData.updated_input, download_path1)

    def verify_add_property_description(self):
        self.wait_to_click(self.property_description_age)
        self.wait_to_clear_and_send_keys(self.property_description_age, UserData.age_property_description)
        self.select_by_text(self.case_property_age, 'Plain')
        self.select_by_text(self.case_property_age, 'Number')
        self.get_text(self.property_description_age)
        self.wait_to_click(self.save)

    def verify_case_management(self):
        self.wait_to_click(self.registration_form)
        self.wait_to_click(self.settings_icon)
        description = self.get_text(self.description_text)
        assert description == UserData.age_property_description

    def verify_deprecate_restore_case_property(self,flag):
        self.wait_to_click(self.property_deprecate)
        self.wait_to_click(self.save)
        time.sleep(5)
        self.wait_to_click(self.show_deprecate)
        assert self.is_present_and_displayed(self.restore_case_type_new), "case not deprecated"
        print("case type is deprecated")
        if flag =="Y":
            self.wait_to_click(self.restore_case_type_new)
            self.wait_to_click(self.save)
            print("deprecated property restored")

    def verify_warning_message(self):
        sleep(10)
        self.is_present_and_displayed(self.property_deprecate_message)
        message = self.get_text(self.property_deprecate_message)
        print(message)

    def verify_restore_case_property(self):
        self.wait_to_click(self.case_type_value)
        self.js_click(self.show_deprecate, 2)
        self.wait_to_click(self.restore_button)
        self.wait_to_click(self.save, 2)
        print("deprecated Case property  is restored")

    def verify_data_dictionary_access_page(self):
        self.wait_to_click(self.view_data, 2)
        self.wait_to_click(self.data_dictionary, 2)
        self.wait_to_click(self.case_type_value)
        if self.is_present_and_displayed(self.upload_button):
            print("both view and edit access is present for the user login")
        else:
            print("only view access is present for the user login")

    def verify_data_dictionary_revoke_access(self):
        self.wait_to_click(self.view_data, 2)
        if self.is_present_and_displayed(self.data_dictionary):
            print("access not revoked")
        else:
            print("Access revoked")
