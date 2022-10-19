import time
import glob
import os.path
from pathlib import Path

import pandas as pd


from selenium.webdriver.common.by import By
from HQSmokeTests.testPages.data.export_data_page import ExportDataPage
from common_utilities.Excel.excel_manage import ExcelManager
from common_utilities.generate_random_string import fetch_random_string
from common_utilities.selenium.base_page import BasePage

""""Contains test page elements and functions related to the Lookup Table module"""


class LookUpTablePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.table_id_name = "lookuptable_" + str(fetch_random_string())
        self.dummyid = "!@@#%%^^ Lookup"
        self.table_id_fields = "(//label[.='Table ID'][@class='control-label col-sm-2']//following-sibling::div/input[@type='text' and @class = 'form-control'])"
        self.description_fields = "(//label[.='Description'][@class='control-label col-sm-2']//following-sibling::div/input[@type='text' and @class = 'form-control'])"
        self.table_created = "(//td/span[text()='" + self.table_id_name + "'])[1]"
        self.Data = (By.XPATH, "/html/body/div[1]/div[1]/div/nav/ul/li[3]/a")
        self.view_all = (By.LINK_TEXT, "View All")
        self.manage_tables_link = (By.LINK_TEXT, "Manage Tables")
        self.upload_table = (By.ID, "bulk_upload_file")
        self.upload = (By.XPATH, "(//*[@id='uploadForm']/div/div/button)")
        self.successmsg = (By.XPATH, "(//*[@class='alert alert-success']/p)")
        self.errormsg = (By.XPATH, "//*[@id='FailText']/p")
        self.all = (By.LINK_TEXT, "all")
        self.none = (By.LINK_TEXT, "none")
        self.edit = (By.XPATH, "(//tr[td[span[text()='upload_1']]]//button)[1]")
        self.edit_field = (
        By.XPATH, "//div[div[h4[span[text()='upload_1']]]]//input[contains(@data-bind,'description')]")
        self.new_field = (By.XPATH, "//div[div[h4[span[text()='upload_1']]]]//button[@data-bind='click: addField']")
        self.new_value = (By.XPATH,
                          "//div[div[h4[span[text()='upload_1']]]]/div[@class='modal-body form-horizontal']/div/table[@class='table table-striped table-bordered']/tbody/tr[2]/td[1]/input[@type='text']")
        self.edit_save = (By.XPATH, "//div[div[h4[span[text()='upload_1']]]]//button[@data-bind='click: saveEdit']")
        self.edit_tableid = (By.XPATH, "//div[div[h4[span[text()='upload_1']]]]//input[contains(@data-bind,'tag')][1]")
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
        self.column_name = (By.XPATH, "(//div[contains(i/following-sibling::text(), '" + self.table_id_name + "')])[1]")
        self.delete_table = (
            By.XPATH, self.table_created + "//following::button[@data-bind='click: $root.removeDataType'][1]")
        self.select_checkbox = (By.XPATH, "//*[text() = '"+ self.table_id_name +"'][1] /../../ td / label / input")
       # // *[text() = "lookuptable_6s9sd2"][1]/../../td/label/input
        #self.select_checkbox = (By.XPATH,"//*[@id='fixtures-ui']/div[2]/table/tbody/tr[2]/td[1]/span[text()=" +self.table_id_name+ "][1] /../../ td / label / input")
        # self.select_checkbox=(By.XPATH,"(//td/span[text()="+self.table_created_path+"])[1]/../../td/label/input[@type='checkbox']")
        self.click_download = (By.XPATH, "//*[@id='fixtures-ui']/div[1]/p/a")
        self.download_file = (By.XPATH, "//*[@id='download-progress']/div/form/a")
        self.closedownloadpopup = (By.XPATH, "//*[@id='download-progress']/../../div/button[@class='close']")


    def create_lookup_table(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.add_table)
        self.send_keys(self.table_id, self.table_id_name)
        self.send_keys(self.table_id_description, self.table_id_name)
        self.wait_to_click(self.add_field)
        self.send_keys(self.field_name, self.table_id_name)
        print(self.table_id_name)
        self.wait_to_click(self.save_table)
        time.sleep(2)
        assert self.is_present_and_displayed(self.table_created_path)
        print("LookUp Table created successfully!")
        return self.table_id_name

    def view_lookup_table(self):
        self.wait_to_click(self.view_tables_link)
        print(self.table_id_name)
        self.wait_to_click(self.select_table_drop_down)
        self.select_by_text(self.select_table, self.table_id_name)
        # self.wait_to_click(self.select_table_drop_down)
        # self.wait_to_click(self.select_table_from_dropdown)
        self.js_click(self.view_table)
        assert self.is_present_and_displayed(self.column_name)
        print("LookUp Table can be viewed successfully!")

    def delete_lookup_table(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.delete_table)
        obj = self.driver.switch_to.alert
        obj.accept()
        print("LookUp Table deleted successfully!")

    def upload_1(self,filepath):
        self.wait_to_click(self.Data)
        self.wait_to_click(self.view_all)
        self.wait_to_click(self.manage_tables_link)
        self.send_keys(self.upload_table,filepath)
        self.wait_to_click(self.upload)
        self.wait_for_element(self.successmsg, 5)
        sucess = self.get_text(self.successmsg)
        assert sucess == "Successfully uploaded 1 tables."
        self.wait_to_click(self.manage_tables_link)

    def selects_deselects(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.all)
        self.wait_to_click(self.none)

    def edit_table(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.edit)
        self.send_keys(self.edit_field, 'testing')
        self.wait_to_click(self.edit_save)
        self.wait_to_click(self.edit)
        self.wait_to_click(self.edit_save)

    def create_dummyid(self):
        self.wait_to_click(self.Data)
        self.wait_to_click(self.view_all)
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.add_table)
        self.send_keys(self.table_id, self.dummyid)
        self.send_keys(self.table_id_description, self.dummyid)
        self.wait_to_click(self.add_field)
        self.send_keys(self.field_name, self.dummyid)
        print(self.dummyid)
        self.wait_to_click(self.save_table)
        fail = self.get_text(self.errormsg)
        assert fail == "Could not update table because field names were not correctly formatted"
        print("error message displayed")
        self.wait_to_click(self.manage_tables_link)

    def edit_dummy_data(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.edit)
        self.wait_to_click(self.new_field)
        self.send_keys(self.new_value, '@!@$#%$^%&^*')
        self.wait_to_click(self.edit_save)
        fail = self.get_text(self.errormsg)
        assert fail == "Could not update table because field names were not correctly formatted"
        print("error message displayed")
        self.wait_to_click(self.manage_tables_link)

    def download1(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.select_checkbox)
        print(self.select_checkbox)
        self.wait_to_click(self.click_download)
        print("Downloading the file")
        self.wait_to_click(self.download_file)
        time.sleep(3)
        self.wait_to_click(self.closedownloadpopup)


    def error_upload1(self):
            Location_path = str(Path.home() / "Downloads")
            print(Location_path)
            file_type = r'\*xlsx'
            files = glob.glob(Location_path + file_type)
            max_file = max(files, key=os.path.getctime)
            print(max_file)
            return max_file

