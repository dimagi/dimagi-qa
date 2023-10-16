import datetime
import os.path
import random
import string
import time

from selenium.webdriver.support.select import Select

from Features.Lookuptable.testCases.conftest import settings
from HQSmokeTests.testPages.home.home_page import HomePage
from common_utilities.path_settings import PathSettings
from selenium.webdriver.common.by import By
from common_utilities.Excel.excel_manage import ExcelManager
from common_utilities.generate_random_string import fetch_random_string, fetch_string_with_special_chars
from common_utilities.selenium.base_page import BasePage
from Features.Lookuptable.userInputs.user_inputs import UserData
import gettext

""""Contains test page elements and functions related to the Lookup Table module"""


class LookUpTablePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.name_lang_value = "name[@lang = jr:itext('lang-code-label')]"
        self.table_id_name = "lookuptable_" + str(fetch_random_string())
        self.dummy_id = str(fetch_string_with_special_chars(4))
        self.table_id_fields = "(//label[.='Table ID'][@class='control-label col-sm-2']//following-sibling::div/input[@type='text' and @class = 'form-control'])"
        self.description_fields = "(//label[.='Description'][@class='control-label col-sm-2']//following-sibling::div/input[@type='text' and @class = 'form-control'])"
        self.table_created = "(//td/span[text()='" + self.table_id_name + "'])[1]"
        self.data_link = (By.LINK_TEXT, "Data")
        self.view_all = (By.LINK_TEXT, "View All")
        self.manage_tables_link = (By.LINK_TEXT, "Manage Tables")
        self.upload_table = (By.ID, "bulk_upload_file")
        self.upload = (By.XPATH, "(//*[@id='uploadForm']/div/div/button)")
        self.success_msg = (By.XPATH, "(//*[@class='alert alert-success']/p)")
        self.error_upload_msg = (By.XPATH, "//*[@id='hq-messages-container']/div/div/div[1]")
        self.error_msg = (By.XPATH, "//p/span[@id='FailText']")
        self.all = (By.LINK_TEXT, "all")
        self.none = (By.LINK_TEXT, "none")
        self.edit = (By.XPATH, "//tr[td[span[text()='upload_1']]]/td/button[1]")
        self.edit_field = (
            By.XPATH, "//div[div[h4[span[text()='upload_1']]]]//input[contains(@data-bind,'description')]")
        self.new_field = (By.XPATH, "//div[div[h4[span[text()='upload_1']]]]//button[@data-bind='click: addField']")
        self.new_value = (By.XPATH,
                          "//div[div[h4[span[text()='upload_1']]]]//div[4]/table/tbody/tr/td/input[@class='form-control']")
        self.edit_save = (By.XPATH, "//div[div[h4[span[text()='upload_1']]]]//button[@data-bind='click: saveEdit']")
        self.edit_table_id = (By.XPATH, "//div[div[h4[span[text()='upload_1']]]]//input[contains(@data-bind,'tag')][1]")
        self.fail_text = (By.XPATH, "//*[@id='editFailure']")
        self.add_table = (By.XPATH, "//button[@data-bind='click: $root.addDataType']")
        self.table_id = (By.XPATH, self.table_id_fields + "[last()]")
        self.table_id_description = (By.XPATH, self.description_fields + "[last()]")
        self.add_field = (By.XPATH, "(//button[@data-bind='click: addField'])[last()]")
        self.field_name = (By.XPATH, "(//input[contains(@data-bind,'value: tag, valueUpdate: ')])[last()]")
        self.save_table = (By.XPATH, "(//button[contains(text(),'Save')][@data-bind='click: saveEdit'])[last()]")
        self.table_created_path = (By.XPATH, self.table_created)
        self.view_tables_link = (By.LINK_TEXT, "View Tables")
        self.select_table = (By.XPATH, "//select[@id='report_filter_table_id']")
        self.select_table_drop_down = (By.ID, "select2-report_filter_table_id-container")
        self.select_table_from_dropdown = (By.XPATH, "//li[contains(.,'" + self.table_id_name + "')]")
        self.view_table = (By.ID, "apply-btn")
        self.panel_title = (By.CLASS_NAME, "panel-title")
        self.column_name = (By.XPATH, "(//div[contains(i/following-sibling::text(), '" + self.table_id_name + "')])[1]")
        self.delete_table = "//td[./span[text()='{}']]//following-sibling::td/button[@data-bind='click: $root.removeDataType']"
        self.select_checkbox = "//td[./span[text() = '{}']]//following-sibling::td/label/input[@type='checkbox']"
        self.select_hypertension_checkbox = (By.XPATH, "//*[text() = 'hypertension'][1] /../../ td / label / input")
        self.click_download = (By.XPATH, "//*[@id='fixtures-ui']/div[1]/p/a")
        self.download_file = (By.XPATH, "//*[@id='download-progress']/div/form/a")
        self.please_complete = (By.XPATH, "//p[@class='alert alert-success'][.='Process complete.']")

        self.close_download_popup = (By.XPATH, "(//button[@aria-label='Close'])[last()]")
        self.error_alert_msg = (By.XPATH, "//*[@class='alert alert-danger']/h3")
        self.replace_table = (By.XPATH, "//input[@id='replace'][@type='checkbox']")
        self.rowcount = (By.XPATH, "//*[@id='report_table_view_lookup_tables_info']")
        self.restore_id = (By.XPATH, "//*[contains(text(),'" + self.table_id_name + "')]")
        # self.delete_state_table = (
        #     By.XPATH, "(//td/span[text()='state'])[1]//following::button[@data-bind='click: $root.removeDataType'][1]")

        # in-app effect
        self.applications_menu_id = (By.ID, "ApplicationsTab")
        self.application = (By.LINK_TEXT, UserData.application)
        self.add_module = (By.XPATH, "//a[@class='appnav-add js-add-new-item']")
        self.add_case_list = (By.XPATH, "//button[@data-type='case']")
        self.delete_popup = (By.XPATH, "(//*[@class='disable-on-submit btn btn-danger'])[1]")
        self.add_questions = (By.XPATH, "//a[contains(@class,'fd-add-question')]")
        self.lookup_question = (By.XPATH,
                                "//ul[@class='dropdown-menu multi-level']/li[@class='dropdown-submenu']/a[contains(.,'Lookup Tables')]")
        self.checkbox_question = (By.XPATH, "//a[@data-qtype='MSelectDynamic']")
        self.question_display_text = (By.XPATH, "(//div[@role='textbox'])[1]")
        self.question_display_text_en = (By.XPATH, "//*[@name='itext-en-label']")
        self.question_display_text_hin = (By.XPATH, "//*[@name='itext-hin-label']")
        self.dropdown_logic = (By.XPATH, "//*[@class='btn btn-default dropdown-toggle']")
        self.logic = (By.XPATH, "(//*[@data-slug='logic'])[1]")
        self.question_id = (By.XPATH, "(//*[@id='property-nodeID'])")
        self.display_condition = (By.XPATH, "(//*[@name='property-relevantAttr'])")
        self.save_button = (By.XPATH, "//span[text()='Save']")
        self.question_display_text_name = "select lookuptable"
        self.lookup_table_data = (By.XPATH, "//a[@class='jstree-anchor'][@aria-level='2']")
        self.grid = (
            By.XPATH, "/html/body/div[1]/div[4]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[4]/div[1]/ul/li/ul/li/a")
        self.select_lookup_table = (By.XPATH, "//*[@name='property-itemsetData']")
        self.lookup_table_options = (By.XPATH, "//*[@name='property-itemsetData']/option")
        self.value_field = (By.XPATH, "//*[@id='property-valueRef']")
        self.display_field = (By.XPATH, "//*[@id='property-labelRef']")
        self.select_logic = (By.XPATH, "//*[@class='btn btn-default dropdown-toggle']")
        self.add_logic = (By.XPATH, "//*[@class='btn btn-default dropdown-toggle']/../ul/li/a[@data-slug='logic']")
        self.filter = (By.XPATH, "//*[@contenteditable='true'][@name='property-filter']")
        self.edit_filter = (By.XPATH, "//*[@class='fd-edit-button btn btn-default btn-block']/i")
        self.expression_editor = (By.XPATH, "//*[@class='fd-scrollable full']")
        self.app_name = (By.XPATH, "//*[@class='variable-app_name appname-text']")
        self.make_new_build = (By.XPATH, "//*[@id='releases-table']/p[2]/button")
        self.release = (By.XPATH, "//*[@id='releases-table']/div[6]/div[1]/div[1]/div/div/button[1]")
        self.login_user = (By.XPATH, "//*[@class='fa fa-user appicon-icon']")
        self.select_user = "//*[@aria-label='{}']"
        self.login = (By.XPATH, "//*[@id='js-confirmation-confirm']")
        self.start = (By.XPATH, "//*[@class='ff ff-start-fg appicon-icon appicon-icon-fg']")
        self.inapp_case_list = (By.XPATH, "//*[@class='formplayer-request']")
        self.inapp_registration_form = (By.XPATH, "//h3[text()='Registration Form']")
        self.inapp_select_option = (By.XPATH, "//*[(@class='sel clear')]//div/div[1]/label/span/p")
        self.inapp_next = (By.XPATH, "//*[@class='btn btn-formnav btn-formnav-next'][1]")
        self.inapp_continue = (By.XPATH, "//*[@class='btn btn-success btn-formnav-submit'][1]")
        self.inapp_success_message = (By.XPATH, "//*[@class='alert alert-success']")
        self.case_list = (By.XPATH, "//*[@aria-label='Case List']")
        self.delete_success = (By.XPATH, "//div[contains(@class,'alert-success')][contains(.,'You have deleted')]")
        self.registration_form = (By.XPATH, "//*[@aria-label='Registration Form']")
        self.preview = (By.XPATH, "//*[@class='preview-toggler js-preview-toggle']")
        self.confirm = (By.XPATH, "//*[contains(text(),'Yes, log in as this user')]")
        self.specific_registration_form = (
            By.XPATH, "(/html/body/div[1]/div[4]/div/div[1]/nav/ul[1]/li/ul/li[1]/div/a[2])[last()]")
        self.revist_lookup_tabble = (By.XPATH, "//*[@class='fd-scrollable fd-scrollable-tree']/div/ul/li/ul/li/a")
        self.value_error = (
            By.XPATH, "//*[@class='fd-scrollable fd-props-scrollable']/form/fieldset/div/div/div[2]/div/div/div/div")
        self.display_error = (
            By.XPATH, "//*[@class='fd-scrollable fd-props-scrollable']/form/fieldset/div/div/div[3]/div/div/div")
        self.auto_selected_value = (By.XPATH, "//ul[@class='atwho-view-ul']/li[@class='cur'] ")
        self.auto_selected_value_1 = (
            By.XPATH, "//*[@id='atwho-ground-property-labelRef']//ul[@class='atwho-view-ul']/li[@class='cur']")
        self.edit_state_table = (By.XPATH, "(//tr[td[span[text()='state']]]//button)[1]")
        self.select_column = (
            By.XPATH, "(//div[div[h4[span[text()='state']]]]/div[2]/fieldset/div[4]/table/tbody/tr/td[2]/input)[1]")
        self.save_state = (By.XPATH, "//div[div[h4[span[text()='state']]]]//button[@data-bind='click: saveEdit']")
        self.e_case_list = (By.XPATH, "(//*[@data-label='Edit Pen'])[1]")
        self.error_message = (By.XPATH, "(//*[@class='messages'])[1]")
        self.saved_button = (By.XPATH, "//span[@class='btn btn-info disabled'][.='Saved']")
        self.number_of_questions = (By.XPATH, "//*[@id='formdesigner']/div[1]/div[1]/div[1]/div[4]/div[1]/ul/li")
        self.child_node = (By.XPATH, "//*[@id='formdesigner']/div[1]/div[1]/div[1]/div[4]/div[1]/ul/li/ul")
        self.home = (By.XPATH, "//*[@id='breadcrumb-region']/div/div/ol/li[1]")
        self.sync = (By.XPATH, "//*[@class='ff ff-sync appicon-icon']")
        self.label = (By.XPATH, "//*[@data-qtype='Trigger']")
        self.settings = (By.XPATH, "//*[@class='fa fa-gear appicon-icon']")
        self.app_language = (By.XPATH, "//*[@class='form-control js-lang']")
        self.done = (By.XPATH, "//*[@class='btn btn-primary js-done']")
        self.selected_caselist = (By.XPATH, "(//*[@class='appnav-item ']/a[@class='appnav-delete'])[1]")

    def create_lookup_table(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_for_element(self.add_table)
        if self.is_present_and_displayed(self.table_created_path, 15):
            print("Lookup table is already present!")
        else:
            self.wait_to_click(self.add_table)
            self.send_keys(self.table_id, self.table_id_name)
            self.send_keys(self.table_id_description, self.table_id_name)
            self.wait_to_click(self.add_field)
            self.send_keys(self.field_name, self.table_id_name)
            self.wait_to_click(self.save_table)
            time.sleep(2)
            assert self.is_present_and_displayed(self.table_created_path)
            print("LookUp Table created successfully!")
        return self.table_id_name

    def create_download_lookup_table_without_field(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_for_element(self.add_table)
        if self.is_present_and_displayed(self.table_created_path, 15):
            print("Lookup table is already present!")
        else:
            self.wait_to_click(self.add_table)
            self.wait_to_clear_and_send_keys(self.table_id, self.table_id_name)
            self.wait_to_clear_and_send_keys(self.table_id_description, self.table_id_name)
            self.wait_to_click(self.save_table)
            time.sleep(2)
            assert self.is_present_and_displayed(self.table_created_path)
            print("LookUp Table created successfully! ", self.table_id_name )
            self.download1(self.table_id_name)
            return self.table_id_name

    def view_lookup_table(self, table_id_name):
        self.wait_for_element(self.view_tables_link)
        self.wait_to_click(self.view_tables_link)
        self.wait_for_element(self.select_table)
        self.select_by_text(self.select_table, table_id_name)
        time.sleep(1)
        self.js_click(self.view_table)
        self.wait_for_element(self.panel_title, 20)
        print("LookUp Table can be viewed successfully!")

    def delete_lookup_table(self, table):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click((By.XPATH, self.delete_table.format(table)))
        self.accept_pop_up()
        print("LookUp Table deleted successfully!")

    def upload_1(self, filepath, table_count):
        filepath = str(PathSettings.DOWNLOAD_PATH / filepath)
        print("File Path: ", filepath)
        self.wait_to_click(self.manage_tables_link)
        self.scroll_to_bottom()
        self.send_keys(self.upload_table, filepath)
        self.wait_to_click(self.upload)
        self.wait_for_element(self.success_msg, 10)
        success = self.get_text(self.success_msg)
        success_msg = "Successfully uploaded " + table_count + " tables."
        assert success == success_msg
        self.wait_to_click(self.manage_tables_link)

    def upload_2(self, filepath, table_count):
        filepath = str(UserData.user_input_base_dir + "//" + filepath)
        print("File Path: ", filepath)
        self.wait_to_click(self.manage_tables_link)
        self.scroll_to_bottom()
        self.send_keys(self.upload_table, filepath)
        self.wait_to_click(self.upload)
        self.wait_for_element(self.success_msg, 10)
        success = self.get_text(self.success_msg)
        success_msg = "Successfully uploaded " + table_count + " tables."
        assert success == success_msg
        self.wait_to_click(self.manage_tables_link)

    def create_new_lookuptable(self):
        self.table_id_name = "lookuptable_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        print("new id:", self.table_id_name)
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.add_table)
        self.send_keys(self.table_id, self.table_id_name)
        self.send_keys(self.table_id_description, self.table_id_name)
        self.wait_to_click(self.add_field)
        self.send_keys(self.field_name, self.table_id_name)
        self.wait_to_click(self.save_table)
        time.sleep(2)
        assert self.is_present_and_displayed(self.table_created_path)
        print("LookUp Table created successfully!")
        return self.table_id_name

    def err_upload(self, filepath):
        if str(PathSettings.DOWNLOAD_PATH) in filepath or str(UserData.user_input_base_dir) in filepath:
            print("Complete Path: ", filepath)
        else:
            filepath = str(PathSettings.DOWNLOAD_PATH / filepath)
            print("File path: ", filepath)
        self.wait_to_click(self.manage_tables_link)
        self.wait_for_element(self.upload_table)
        self.scroll_to_bottom()
        time.sleep(1)
        self.send_keys(self.upload_table, filepath)
        time.sleep(2)
        self.wait_for_element(self.replace_table)
        time.sleep(2)
        self.js_click(self.replace_table)
        time.sleep(2)
        self.js_click(self.upload)
        time.sleep(10)
        print("Upload successful")

    def invalid_data_assert(self):
        invalid_data = self.get_text(self.error_alert_msg)
        assert invalid_data == UserData.invalid_data_assert

    def missing_data_assert(self):
        missing_data = self.get_text(self.error_upload_msg)
        print("Error msg: ", missing_data)
        assert UserData.missing_data_assert in missing_data

    def selects_deselects(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.all)
        self.wait_to_click(self.none)

    def edit_table(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.edit)
        self.wait_to_clear_and_send_keys(self.edit_field, 'testing')
        self.wait_to_click(self.edit_save)

    def create_dummyid(self):
        self.wait_to_click(self.manage_tables_link)
        time.sleep(2)
        self.wait_to_click(self.add_table)
        time.sleep(2)
        self.wait_for_element(self.table_id)
        self.send_keys(self.table_id, self.dummy_id)
        self.send_keys(self.table_id_description, self.dummy_id)
        self.wait_to_click(self.add_field)
        self.wait_to_clear_and_send_keys(self.field_name, self.dummy_id)
        self.wait_to_click(self.save_table)
        time.sleep(5)
        self.wait_for_element(self.error_msg)
        fail = self.get_text(self.error_msg)
        print(fail)
        assert "Could not update table because field names were not correctly formatted" in fail
        print("error message displayed")
        self.wait_to_click(self.manage_tables_link)

    def edit_dummy_data(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.edit)
        time.sleep(2)
        self.wait_to_click(self.new_field)
        time.sleep(1)
        self.send_keys(self.new_value, '@!@$#%$^%&^*')
        self.wait_to_click(self.edit_save)
        time.sleep(5)
        fail = self.get_text(self.error_msg)
        assert "Could not update table because field names were not correctly formatted" in fail
        print("error message displayed")

    def select_multiple_tables_checkbox(self, tablename):
        self.wait_for_element((By.XPATH, self.select_checkbox.format(tablename)))
        self.wait_to_click((By.XPATH, self.select_checkbox.format(tablename)))

    def select_multiple_tables_download(self, tablenames, n):
        self.wait_to_click(self.manage_tables_link)
        for i in range(0, n):
            tablename = str.split(tablenames, ":")[i]
            print("tablename : ", tablename)
            self.select_multiple_tables_checkbox(tablename)
        self.click_download_button()

    def click_download_button(self):
        self.wait_to_click(self.click_download)
        self.wait_for_element(self.download_file, 60)
        self.wait_to_click(self.download_file)
        time.sleep(3)
        self.wait_to_click(self.close_download_popup)

    def download1(self, tablename):
        self.wait_to_click(self.manage_tables_link)
        self.wait_for_element((By.XPATH, self.select_checkbox.format(tablename)))
        self.wait_to_click((By.XPATH, self.select_checkbox.format(tablename)))
        self.wait_to_click(self.click_download)
        self.wait_for_element(self.close_download_popup)
        if self.is_present(self.please_complete):
            self.wait_to_click(self.close_download_popup)
            self.driver.refresh()
            self.wait_for_element((By.XPATH, self.select_checkbox.format(tablename)))
            self.wait_to_click((By.XPATH, self.select_checkbox.format(tablename)))
            self.wait_to_click(self.click_download)
        self.wait_for_element(self.download_file, 60)
        self.wait_to_click(self.download_file)
        time.sleep(3)
        self.wait_to_click(self.close_download_popup)

    def download1_specific_table(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.select_hypertension_checkbox)
        self.wait_to_click(self.click_download)
        self.wait_for_element(self.download_file, 60)
        self.wait_to_click(self.download_file)
        time.sleep(3)
        self.wait_to_click(self.close_download_popup)

    def latest_download_file(self, type=".xlsx"):
        cwd = os.getcwd()
        try:
            os.chdir(PathSettings.DOWNLOAD_PATH)
            all_specific_files = filter(lambda x: x.endswith(type), os.listdir(os.getcwd()))
            files = sorted(all_specific_files, key=os.path.getctime)
            if files[-1].endswith(".log"):
                newest = sorted(files, key=os.path.getctime)[-2]
            elif files[-1].endswith(".xlsx"):
                newest = sorted(files, key=os.path.getctime)[-1]
            else:
                newest = max(files, key=os.path.getctime)
            print("File downloaded: " + newest)
            modTimesinceEpoc = (PathSettings.DOWNLOAD_PATH / newest).stat().st_mtime
            modificationTime = datetime.datetime.fromtimestamp(modTimesinceEpoc)
            timeNow = datetime.datetime.now()
            diff_seconds = round((timeNow - modificationTime).total_seconds())
            print("Last Modified Time : ", str(modificationTime) + 'Current Time : ', str(timeNow),
                  "Diff: " + str(diff_seconds))
            return newest
        finally:
            print("Restoring the path...")
            os.chdir(cwd)
            print("Current directory is-", os.getcwd())

    def create_download_lookuptable(self):
        table_name = self.create_lookup_table()
        self.download1(table_name)
        return table_name

    def write_data_excel(self, table_id, path):
        excel = ExcelManager(path)
        for x in UserData.col_headers:
            for i in range(1, 2):
                col = excel.col_size(table_id)
                excel.write_excel_data(table_id, 1, col + i, x)
            excel.write_data(table_id, UserData.data_list1)
            excel.write_data(table_id, UserData.data_list2)

    def update_excel_user_value(self, table_id, path):
        excel = ExcelManager(path)
        col = excel.col_size(table_id)
        excel.write_excel_data(table_id, 1, col + 1, "user 1")
        excel.upload_to_path(table_id, UserData.data_list)

    def update_excel_group_value(self, table_id, path):
        excel = ExcelManager(path)
        col = excel.col_size(table_id)
        excel.write_excel_data(table_id, 1, col + 1, "group 1")
        excel.upload_to_path(table_id, UserData.data_list)

    def compare_excel(self, df1, df2, compareflag):
        if (compareflag == 0):
            assert df1 == df2
            print("Data is same")
        else:
            assert df1 != df2
            print("Data is different in both excels")

    def download_update_7(self, tableid, path):
        excel = ExcelManager(path)
        df1 = excel.read_excel(tableid)
        self.err_upload(path)
        df2 = excel.read_excel(tableid)
        return df1, df2

    def download_update_8(self, path, table_id):
        excel = ExcelManager(path)
        col = excel.col_size(table_id)
        excel.write_excel_data(table_id, 1, col + 1, "user 1")
        excel.write_excel_data(table_id, 1, col + 2, "group 1")
        excel.write_data(table_id, UserData.data_list1)
        self.err_upload(path)
        d1 = excel.read_excel(table_id)
        print("data1", d1)
        excel.write_excel_data(table_id, 2, 4, 'kiran')
        excel.write_excel_data(table_id, 2, 5, '123')
        self.err_upload(path)
        d2 = excel.read_excel(table_id)
        print("data2", d2)
        return d1, d2

    def replace_existing_table(self, filepath):
        self.err_upload(filepath)
        print("Upload successful")
        self.wait_to_click(self.manage_tables_link)

    def delete_row_from_table(self, download_path, tablename):
        excel = ExcelManager(download_path)
        excel.write_data(tablename, UserData.data_list1)
        self.err_upload(download_path)
        self.download1(tablename)
        # self.view_lookup_table(tablename)
        row_count_before = self.row_count_table(tablename)
        print("Row count before: ", row_count_before)
        download_path_1 = self.latest_download_file()
        excel = ExcelManager(download_path_1)
        excel.delete_row(tablename, 2)
        self.replace_existing_table(download_path_1)
        # self.view_lookup_table(tablename)
        row_count_after = self.row_count_table(tablename)
        print("Row count after: ", row_count_after)
        assert row_count_before > row_count_after
        print("Row got successfully Deleted")

    def row_count_table(self, tablename):
        self.view_lookup_table(tablename)
        text = self.get_text(self.rowcount)
        print(text)
        rowcount = text[18:20].strip()
        return rowcount

    def update_delete_field(self, download_path, tablename):
        excel = ExcelManager(download_path)
        excel.upload_to_path(tablename, UserData.data_list)
        self.err_upload(download_path)
        # self.view_lookup_table(tablename)
        row_count_before = self.row_count_table(tablename)
        download_path_1 = self.latest_download_file()
        excel = ExcelManager(download_path_1)
        excel.write_excel_data(tablename, 3, 2, 'Y')
        self.replace_existing_table(download_path_1)
        # self.view_lookup_table(tablename)
        row_count_after = self.row_count_table(tablename)
        assert row_count_before > row_count_after
        print("Row got successfully Deleted")

    def attribute_2(self, download_path, tablename):
        excel = ExcelManager(download_path)
        excel.write_excel_data("types", 1, 4, 'field 1')
        excel.write_excel_data("types", 2, 4, 'C1')
        excel.write_excel_data("types", 1, 5, 'field 2')
        excel.write_excel_data("types", 2, 5, 'C2')
        excel.write_excel_data(tablename, 1, 3, 'field:C1')
        excel.write_excel_data(tablename, 1, 4, 'field:C2')
        excel.write_data(tablename, UserData.new_datalist)
        time.sleep(2)
        self.err_upload(download_path)
        print("sleeping for some time")
        time.sleep(10)
        ui_rows = self.row_count_table(tablename)
        self.download1(tablename)
        excel_rows = excel.row_size(tablename)
        print(str(ui_rows) + " and " + str(excel_rows - 1))
        assert int(ui_rows) == (excel_rows - 1)

    def bulkupload_1(self, tablenames, n, upload_path):
        before = ""
        after = ""
        for i in range(0, n):
            tablename = str.split(tablenames, ":")[i]
            row_count_before = self.row_count_table(tablename)
            before = before + "," + row_count_before
        before = str.split(before, ",", 1)[1].strip()
        self.err_upload(upload_path)
        for i in range(0, n):
            tablename = str.split(tablenames, ":")[i]
            row_count_after = self.row_count_table(tablename)
            after = after + "," + row_count_after
        after = str.split(after, ",", 1)[1].strip()
        for i in range(0, n):
            b_row = str.split(before, ',')[0]
            a_row = str.split(after, ',')[0]
            print(b_row, a_row)
            assert b_row < a_row

    def delete_field_columns(self, downloadpath, tablename):
        excel = ExcelManager(downloadpath)
        col_TypeSheet_before = excel.col_size("types")
        col1 = excel.col_size(tablename)
        excel.delete_column('types', 4)
        excel.delete_column(tablename, 3)
        self.err_upload(downloadpath)
        self.view_lookup_table(tablename)
        col_TypeSheet = excel.col_size("types")
        col2 = excel.col_size(tablename)
        assert col_TypeSheet_before > col_TypeSheet
        assert col1 > col2
        print("Fields got deleted")

    def restore_attribute_1(self):
        time.sleep(20)
        self.is_present_and_displayed(self.restore_id, 10)
        a = self.get_text(self.restore_id)
        print(a)
        print("OTA Restore succesfully with newely created properties")

    def test_13(self, download_path, tablename):
        self.write_data_excel(tablename, download_path)
        self.err_upload(download_path)
        self.download1(tablename)
        download_path_1 = self.latest_download_file()
        excel = ExcelManager(download_path_1)
        e1 = excel.get_cell_value(tablename, 1, 2)
        self.download1(tablename)
        download_path_2 = self.latest_download_file()
        excel = ExcelManager(download_path_2)
        e2 = excel.get_cell_value(tablename, 1, 2)
        assert e1 == e2
        print("UID for existing rows is same")

    def test_15(self, download_path, tablename):
        excel = ExcelManager(download_path)
        excel.write_data(tablename, UserData.data_list1)
        self.err_upload(download_path)
        self.download1(tablename)
        download_path_1 = self.latest_download_file()
        excel = ExcelManager(download_path_1)
        UID_before = excel.get_cell_value(tablename, 3, 2)
        UID1 = excel.get_cell_value(tablename, 1, 2)
        print("After UID is:" + UID_before, UID1)
        excel.write_excel_data(tablename, 2, 3, "dnckse")
        download_path_2 = self.latest_download_file()
        self.replace_existing_table(download_path_2)
        excel = ExcelManager(download_path_2)
        self.download1(tablename)
        UID_before = excel.get_cell_value(tablename, 3, 2)
        UID1 = excel.get_cell_value(tablename, 1, 2)
        print("After UID is:" + UID_before, UID1)
        download_path_3 = self.latest_download_file()
        excel = ExcelManager(download_path_3)
        UID_after = excel.get_cell_value(tablename, 3, 2)
        UID2 = excel.get_cell_value(tablename, 1, 2)
        print("After UID is:" + UID_after, UID2)
        assert UID1 != UID2
        print("UID for updated row has changed")

    def delete_caselist(self):
        self.wait_to_click(self.selected_caselist)
        self.wait_to_click(self.delete_popup)
        self.accept_pop_up()
        self.wait_for_element(self.delete_success, 100)

    def test_application(self):
        self.wait_to_click(self.add_module)
        time.sleep(1)
        self.wait_to_click(self.add_case_list)
        time.sleep(2)
        self.wait_for_element(self.add_questions, 50)
        self.js_click(self.add_questions)
        time.sleep(2)
        self.wait_to_click(self.lookup_question)
        time.sleep(2)
        # self.wait_to_click(self.multiplechoice)
        time.sleep(2)
        self.send_keys(self.question_display_text, self.question_display_text_name)
        self.wait_to_click(self.save_button)
        self.wait_for_element(self.saved_button, 50)
        self.wait_to_click(self.lookup_table_data)
        self.wait_to_click(self.grid)
        self.wait_to_click(self.select_lookup_table)
        self.wait_to_click(self.value_field)
        time.sleep(3)
        self.wait_to_click(self.display_field)
        time.sleep(3)
        self.wait_to_click(self.select_logic)
        self.wait_to_click(self.add_logic)
        time.sleep(10)
        self.send_keys(self.filter, UserData.filter_value)
        self.wait_to_click(self.edit_filter)
        assert self.is_present_and_displayed(self.expression_editor)
        print("expression editior is displayed")

    def specific_table_upload(self, tablename):
        self.wait_for_element(self.add_module)
        self.wait_to_click(self.add_module)
        time.sleep(1)
        self.wait_to_click(self.add_case_list)
        time.sleep(2)
        self.wait_to_click(self.add_questions)
        time.sleep(2)
        self.wait_to_click(self.lookup_question)
        self.send_keys(self.question_display_text, self.question_display_text_name)
        self.wait_to_click(self.lookup_table_data)
        self.wait_to_click(self.grid)
        self.wait_to_click(self.select_lookup_table)
        dd = Select(self.find_element(self.select_lookup_table))
        print("tablename:", tablename)
        dd.select_by_visible_text(tablename)
        self.wait_to_click(self.save_button)
        self.wait_for_element(self.saved_button, 50)

    def create_new_form(self):
        self.wait_to_click(self.add_module)
        time.sleep(1)
        self.wait_to_click(self.add_case_list)
        time.sleep(2)
        self.wait_to_click(self.add_questions)
        time.sleep(2)
        self.wait_to_click(self.lookup_question)
        self.send_keys(self.question_display_text, self.question_display_text_name)
        self.wait_to_click(self.lookup_table_data)
        self.wait_to_click(self.grid)
        self.wait_to_click(self.select_lookup_table)
        time.sleep(5)
        self.wait_to_click(self.save_button)
        time.sleep(2)
        self.wait_for_element(self.saved_button, 50)

    def adding_questions(self):
        time.sleep(3)
        self.wait_for_element(self.add_questions)
        self.js_click(self.add_questions)
        time.sleep(3)
        self.wait_for_element(self.lookup_question)
        self.hover_and_click(self.lookup_question, self.checkbox_question)
        time.sleep(10)
        self.wait_to_click(self.save_button)
        self.wait_for_element(self.saved_button, 50)
        self.find_elements(self.number_of_questions)
        question_nodes = len(self.find_elements(self.number_of_questions))
        child_nodes = len(self.find_elements(self.child_node))
        assert int(question_nodes) == int(child_nodes)

    def lookuptable_display_list(self):
        self.wait_to_click(self.select_lookup_table)
        dropdown_values = self.find_elements_texts(self.select_lookup_table)
        print(dropdown_values)
        assert dropdown_values[0] != "Custom"
        return dropdown_values

    def navigation_to_application_tab(self):
        self.wait_to_click(self.applications_menu_id)
        self.wait_to_click(self.application)

    def navigation_to_a_caselist(self, tablename):
        self.wait_for_element(self.specific_registration_form)
        self.wait_to_click(self.specific_registration_form)
        self.wait_to_click(self.revist_lookup_tabble)
        dropdown_values = self.lookuptable_display_list()
        dropdown_values.__contains__(tablename)
        self.select_by_text(self.select_lookup_table, tablename)
        print(tablename)

    def formbuilder_4(self):
        self.clear(self.value_field)
        self.is_present_and_displayed(self.value_error)
        a = self.get_text(self.value_error)
        b = "Value Field is required."
        assert b in a
        print(b)
        self.clear(self.display_field)
        self.is_present_and_displayed(self.display_error)
        a1 = self.get_text(self.display_error)
        b1 = "Display Text Field is required."
        assert b1 in a1
        print(b1)

    def formbuilder_5(self):
        self.clear(self.value_field)
        self.wait_to_click(self.value_field)
        self.wait_to_click(self.auto_selected_value)
        self.clear(self.display_field)
        self.wait_to_click(self.display_field)
        self.wait_to_click(self.auto_selected_value_1)
        self.wait_to_click(self.save_button)
        time.sleep(3)
        self.wait_for_element(self.saved_button, 50)

    def edit_state(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.edit_state_table)
        self.wait_for_element(self.select_column)
        self.click(self.select_column)
        self.wait_for_element(self.save_state)
        self.wait_to_click(self.save_state)
        time.sleep(3)
        self.wait_to_click(self.applications_menu_id)
        self.wait_to_click(self.application)
        self.wait_to_click(self.e_case_list)
        self.wait_to_click(self.grid)
        self.wait_to_click(self.saved_button)
        time.sleep(5)
        assert self.is_present_and_displayed(self.error_message)
        print("warning message is displayed")

    def language_selection(self, value):
        self.wait_to_click(self.settings)
        self.select_by_text(self.app_language, value)
        self.wait_to_click(self.done)

    def submit_form_on_registration(self, value, user):
        self.wait_for_element(self.home)
        self.wait_to_click(self.home)
        # self.wait_to_click(self.login_user)
        # time.sleep(2)
        # self.wait_to_click((By.XPATH, self.select_user.format(user)))
        # time.sleep(2)
        # self.wait_for_element(self.login)
        # self.wait_to_click(self.login)
        # time.sleep(2)
        self.language_selection(value)
        self.wait_for_element(self.sync)
        self.wait_to_click(self.sync)
        time.sleep(20)
        self.wait_for_element(self.start)
        self.wait_to_click(self.start)
        self.wait_for_element(self.inapp_case_list)
        self.wait_to_click(self.inapp_case_list)
        self.wait_for_element(self.inapp_registration_form)
        self.wait_to_click(self.inapp_registration_form)
        time.sleep(3)
        if user != 'appiumtest':
            self.wait_to_click(self.inapp_select_option)
            time.sleep(3)
            value = self.get_text(self.inapp_select_option)
            self.wait_to_click(self.inapp_next)
            time.sleep(3)
            self.wait_to_click(self.inapp_continue)
            # self.send_keys(self.question_display_text, self.question_display_text_name)
            time.sleep(5)
            assert self.is_present_and_displayed(self.success_msg)
            print("form submitted succesfully:", value)
            en = "Uttar Pradesh"
            hin = "उत्तर प्रदेश"
            if value == hin:
                print("Form submitted in HINDI")
            elif value == en:
                print("Form submitted in ENGLISH")
        else:
            print(
                "Make sure the 'Inapp' lookup table is available, and that its contents are accessible to the current user.")

    def language_check(self):
        self.clear(self.value_field)
        self.wait_to_click(self.value_field)
        self.send_keys(self.value_field, "id")
        self.clear(self.display_field)
        self.wait_to_click(self.display_field)
        self.send_keys(self.display_field, self.name_lang_value)
        self.wait_to_click(self.add_questions)
        time.sleep(2)
        self.wait_to_click(self.label)
        self.wait_to_click(self.dropdown_logic)
        self.wait_to_click(self.logic)
        self.send_keys(self.question_display_text_en, "en")
        self.clear(self.question_display_text_hin)
        self.send_keys(self.question_display_text_hin, "hin")
        self.send_keys(self.question_id, "lang-code")
        self.send_keys(self.display_condition, '1=2')
        self.wait_to_click(self.save_button)
        time.sleep(3)
        self.wait_for_element(self.saved_button, 50)

    def multiple_groups(self, path, table_id):
        excel = ExcelManager(path)
        col = excel.col_size(table_id)
        excel.write_excel_data(table_id, 1, col + 1, "user 1")
        excel.write_excel_data(table_id, 1, col + 2, "group 1")
        excel.write_excel_data(table_id, 1, col + 3, "group 2")
        excel.write_data(table_id, UserData.multiple_values)
        self.err_upload(path)

    def download_bulk_tables(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.all)
        self.wait_to_click(self.click_download)
        self.wait_for_element(self.download_file, 60)
        self.wait_to_click(self.download_file)
        time.sleep(15)
        self.wait_to_click(self.close_download_popup)

    def compare_and_delete(self, download_path):
        excel = ExcelManager(download_path)
        i = excel.row_size("types")
        for val in range(1, i):
            j = excel.get_cell_value("types", 2, val)
            print(val)

            print(j)
            if (str(j).startswith("lookuptable")):
                print("Value to be updated")
                excel.write_excel_data("types", val, 1, "Y")
        self.replace_existing_table(download_path)

    def loop_submit_form_on_registration(self):
        for i in range(len(UserData.user_ids_list)):
            self.submit_form_on_registration("en", UserData.user_ids_list[i])

    def bulk_upload_verification(self, download_path, value):
        self.err_upload(download_path)
        self.download1(value)
        self.row_count_table(value)
        row_value = self.row_count_table(value)
        excel = ExcelManager(download_path)
        assert row_value == str((excel.row_size(value) - 1))

    def verify_missing_data_alert(self, download_path):
        print("Sleeping for some time")
        time.sleep(40)
        self.wait_to_click(self.manage_tables_link)
        self.wait_for_element(self.click_download)
        self.err_upload(download_path)
        self.missing_data_assert()