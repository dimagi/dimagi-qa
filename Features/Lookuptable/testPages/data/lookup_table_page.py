import os.path
import random
import string
import time

from selenium.webdriver.support.select import Select
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

        self.table_id_name = "lookuptable_" + str(fetch_random_string())
        self.dummyid = str(fetch_string_with_special_chars(4))
        self.table_id_fields = "(//label[.='Table ID'][@class='control-label col-sm-2']//following-sibling::div/input[@type='text' and @class = 'form-control'])"
        self.description_fields = "(//label[.='Description'][@class='control-label col-sm-2']//following-sibling::div/input[@type='text' and @class = 'form-control'])"
        self.table_created = "(//td/span[text()='" + self.table_id_name + "'])[1]"
        self.Data = (By.LINK_TEXT, "Data")
        self.view_all = (By.LINK_TEXT, "View All")
        self.manage_tables_link = (By.LINK_TEXT, "Manage Tables")
        self.upload_table = (By.ID, "bulk_upload_file")
        self.upload = (By.XPATH, "(//*[@id='uploadForm']/div/div/button)")
        self.successmsg = (By.XPATH, "(//*[@class='alert alert-success']/p)")
        self.errorUploadmsg = (By.XPATH, "//*[@id='hq-messages-container']/div/div/div[1]")
        self.errormsg = (By.XPATH, "//p/span[@id='FailText']")
        self.all = (By.LINK_TEXT, "all")
        self.none = (By.LINK_TEXT, "none")
        self.edit = (By.XPATH, "//tr[td[span[text()='upload_1']]]/td/button[1]")
        self.edit_field = (
            By.XPATH, "//div[div[h4[span[text()='upload_1']]]]//input[contains(@data-bind,'description')]")
        self.new_field = (By.XPATH, "//div[div[h4[span[text()='upload_1']]]]//button[@data-bind='click: addField']")
        self.new_value = (By.XPATH,
                          "//div[div[h4[span[text()='upload_1']]]]//div[4]/table/tbody/tr/td/input[@class='form-control']")
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
        self.select_checkbox = (By.XPATH, "//*[text() = '" + self.table_id_name + "'][1] /../../ td / label / input")
        self.select_hypertensioncheckbox = (By.XPATH, "//*[text() = 'hypertension'][1] /../../ td / label / input")
        self.click_download = (By.XPATH, "//*[@id='fixtures-ui']/div[1]/p/a")
        self.download_file = (By.XPATH, "//*[@id='download-progress']/div/form/a")
        self.closedownloadpopup = (By.XPATH, "//*[@id='download-progress']/../../div/button[@class='close']")
        self.erroralert_msg=(By.XPATH,"//*[@class='alert alert-danger']/h3")
        self.replace_table=(By.ID,"replace")
        self.rowcount = (By.XPATH,"//*[@id='report_table_view_lookup_tables_info']")
        self.restore_id =(By.XPATH,"//*[contains(text(),'" + self.table_id_name + "')]")
        self.delete_statetable = (By.XPATH,"(//td/span[text()='state'])[1]//following::button[@data-bind='click: $root.removeDataType'][1]")
      # in-app effect
        self.applications_menu_id = (By.ID, "ApplicationsTab")
        self.application = (By.LINK_TEXT, "Lookuptable_tests")
        self.add_module = (By.XPATH, "//a[@class='appnav-add js-add-new-item']")
        self.add_case_list = (By.XPATH, "//button[@data-type='case']")
        self.delete_popup = (By.XPATH, "(//*[@class='disable-on-submit btn btn-danger'])[1]")
        self.add_questions = (By.XPATH, "//a[contains(@class,'fd-add-question')]")
        self.lookup_question = (By.XPATH,"//ul[@class='dropdown-menu multi-level']/li[@class='dropdown-submenu']/a[contains(.,'Lookup Tables')]")
        self.checkbox_question = (By.XPATH, "//a[@data-qtype='MSelectDynamic']")
        self.question_display_text = (By.XPATH, "(//div[@role='textbox'])[1]")
        self.question_display_text_en = (By.XPATH, "//*[@name='itext-en-label']")
        self.question_display_text_hin = (By.XPATH, "//*[@name='itext-hin-label']")
        self.dropdown_logic = (By.XPATH, "//*[@class='btn btn-default dropdown-toggle']")
        self.logic =(By.XPATH, "(//*[@data-slug='logic'])[1]")
        self.question_id = (By.XPATH, "(//*[@id='property-nodeID'])")
        self.display_condition = (By.XPATH,"(//*[@name='property-relevantAttr'])")
        self.save_button = (By.XPATH, "//span[text()='Save']")
        self.question_display_text_name = "select lookuptable"
        self.lookuptable_data =(By.XPATH,"//a[@class='jstree-anchor'][@aria-level='2']")
        self.grid = (By.XPATH,"/html/body/div[1]/div[4]/div/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[4]/div[1]/ul/li/ul/li/a")
        self.selectlookuptable = (By.XPATH,"//*[@name='property-itemsetData']")
        self.lookuptableOptions = (By.XPATH,"//*[@name='property-itemsetData']/option")
        self.value_field =(By.XPATH,"//*[@id='property-valueRef']")
        self.display_field =(By.XPATH,"//*[@id='property-labelRef']")
        self.select_logic =(By.XPATH,"//*[@class='btn btn-default dropdown-toggle']")
        self.add_logic =(By.XPATH,"//*[@class='btn btn-default dropdown-toggle']/../ul/li/a[@data-slug='logic']")
        self.filter =(By.XPATH,"//*[@contenteditable='true'][@name='property-filter']")
        self.edit_filter =(By.XPATH,"//*[@class='fd-edit-button btn btn-default btn-block']/i")
        self.expression_editor =(By.XPATH,"//*[@class='fd-scrollable full']")
        self.appname =(By.XPATH,"//*[@class='variable-app_name appname-text']")
        self.makenewbuild =(By.XPATH,"//*[@id='releases-table']/p[2]/button")
        self.release = (By.XPATH, "//*[@id='releases-table']/div[6]/div[1]/div[1]/div/div/button[1]")
        self.login_user= (By.XPATH,"//*[@class='fa fa-user appicon-icon']")
        self.select_user= "//*[@aria-label='{}']"
        self.login = (By.XPATH,"//*[@id='js-confirmation-confirm']")
        self.start= (By.XPATH,"//*[@class='ff ff-start-fg appicon-icon appicon-icon-fg']")
        self.inapp_caselist = (By.XPATH,"//*[@class='formplayer-request']")
        self.inapp_registrationform = (By.XPATH,"//h3[text()='Registration Form']")
        self.inapp_selectoption = (By.XPATH,"//*[(@class='sel clear')]//div/div[1]/label/span/p")
        self.inapp_next = (By.XPATH,"//*[@class='btn btn-formnav btn-formnav-next'][1]")
        self.inapp_continue = (By.XPATH,"//*[@class='btn btn-success btn-formnav-submit'][1]")
        self.inapp_success_message = (By.XPATH,"//*[@class='alert alert-success']")
        self.caselist= (By.XPATH,"//*[@aria-label='Case List']")
        self.registrationform= (By.XPATH,"//*[@aria-label='Registration Form']")
        self.preview= (By.XPATH,"//*[@class='preview-toggler js-preview-toggle']")
        self.confirm = (By.XPATH,"//*[contains(text(),'Yes, log in as this user')]")
        self.SPECIFIC_Registration_form = (By.XPATH,"/html/body/div[1]/div[4]/div/div[1]/nav/ul[1]/li/ul/li[1]/div/a[2]")
        self.revist_lookup_tabble = (By.XPATH,"//*[@class='fd-scrollable fd-scrollable-tree']/div/ul/li/ul/li/a")
        self.valueerror = (By.XPATH,"//*[@class='fd-scrollable fd-props-scrollable']/form/fieldset/div/div/div[2]/div/div/div/div")
        self.displayerror = (By.XPATH,"//*[@class='fd-scrollable fd-props-scrollable']/form/fieldset/div/div/div[3]/div/div/div")
        self.autoselectedvalue = (By.XPATH,"//ul[@class='atwho-view-ul']/li[@class='cur'] ")
        self.autoselectedvalue1 = (By.XPATH,"//*[@id='atwho-ground-property-labelRef']//ul[@class='atwho-view-ul']/li[@class='cur']")
        self.edit_state_table = (By.XPATH,"(//tr[td[span[text()='state']]]//button)[1]")
        self.select_column = (By.XPATH, "(//div[div[h4[span[text()='state']]]]/div[2]/fieldset/div[4]/table/tbody/tr/td[2]/input)[1]")
        self.savestate = (By.XPATH, "//div[div[h4[span[text()='state']]]]//button[@data-bind='click: saveEdit']")
        self.Ecase_list = (By.XPATH, "(//*[@data-label='Edit Pen'])[1]")
        self.errormessage = (By.XPATH, "(//*[@class='messages'])[1]")
        self.savedbutton = (By.XPATH, "//span[text()='Saved']")
        self.numberofquestions = (By.XPATH, "//*[@id='formdesigner']/div[1]/div[1]/div[1]/div[4]/div[1]/ul/li")
        self.childnode = (By.XPATH, "//*[@id='formdesigner']/div[1]/div[1]/div[1]/div[4]/div[1]/ul/li/ul")
        self.home = (By.XPATH,"//*[@id='breadcrumb-region']/div/div/ol/li[1]")
        self.sync = (By.XPATH,"//*[@class='ff ff-sync appicon-icon']")
        self.label = (By.XPATH,"//*[@data-qtype='Trigger']")
        self.settings = (By.XPATH, "//*[@class='fa fa-gear appicon-icon']")
        self.app_language = (By.XPATH,"//*[@class='form-control js-lang']")
        self.done =(By.XPATH, "//*[@class='btn btn-primary js-done']")
        self.selected_caselist =(By.XPATH, "(//*[@class='appnav-item ']/a[@class='appnav-delete'])[1]")


    def create_lookup_table(self):
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

    def create_download_lookup_table_without_field(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.add_table)
        self.send_keys(self.table_id, self.table_id_name)
        self.send_keys(self.table_id_description, self.table_id_name)
        self.wait_to_click(self.save_table)
        time.sleep(2)
        assert self.is_present_and_displayed(self.table_created_path)
        print("LookUp Table created successfully!")
        self.download1()
        return self.table_id_name

    def view_lookup_table(self,table_id_name):
        self.wait_to_click(self.view_tables_link)
        self.wait_to_click(self.select_table_drop_down)
        self.select_by_text(self.select_table, self.table_id_name)
        self.js_click(self.view_table)
        print("LookUp Table can be viewed successfully!")

    def delete_lookup_table(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.delete_table)
        obj = self.driver.switch_to.alert
        obj.accept()
        print("LookUp Table deleted successfully!")

    def upload_1(self, filepath, TableCount):
        self.wait_to_click(self.manage_tables_link)
        self.scroll_to_bottom()
        self.send_keys(self.upload_table, filepath)
        self.wait_to_click(self.upload)
        self.wait_for_element(self.successmsg, 10)
        success = self.get_text(self.successmsg)
        successmsg = "Successfully uploaded "+ TableCount + " tables."
        assert success == successmsg
        self.wait_to_click(self.manage_tables_link)

    def create_new_lookuptable(self):
        self.table_id_name ="lookuptable_"+''.join(random.choices(string.ascii_lowercase+string.digits,k=6))
        print("new id:",self.table_id_name)
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
        self.wait_to_click(self.Data)
        self.wait_to_click(self.view_all)
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_clear_and_send_keys(self.upload_table, filepath)
        self.wait_to_click(self.upload)
        time.sleep(20)

    def invalid_data_assert(self):
        invalid_data = self.get_text(self.erroralert_msg)
        assert invalid_data == UserData.invalid_data_assert

    def missing_data_assert(self):
        missing_data = self.get_text(self.errorUploadmsg)
        new = missing_data.split(':')[0]
        assert  UserData.missing_data_assert in missing_data

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
        self.send_keys(self.table_id, self.dummyid)
        self.send_keys(self.table_id_description, self.dummyid)
        self.wait_to_click(self.add_field)
        self.wait_to_clear_and_send_keys(self.field_name, self.dummyid)
        self.wait_to_click(self.save_table)
        time.sleep(5)
        self.wait_for_element(self.errormsg)
        fail = self.get_text(self.errormsg)
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
        fail = self.get_text(self.errormsg)
        assert "Could not update table because field names were not correctly formatted" in fail
        print("error message displayed")


    def select_multipleTables_checkbox(self, tablename):
        self.select_checkbox = (By.XPATH, "//*[text() = '" + tablename + "'][1] /../../ td / label / input")
        self.wait_to_click(self.select_checkbox)

    def select_multipletables_download(self,tablenames, n):
        self.wait_to_click(self.manage_tables_link)
        for i in range (0,n):
            tablename = str.split(tablenames,":")[i]
            print("tablename : ",tablename)
            self.select_multipleTables_checkbox(tablename)
        self.click_downloadbutton()
    def click_downloadbutton(self):
        self.wait_to_click(self.click_download)
        self.wait_to_click(self.download_file)
        time.sleep(3)
        self.wait_to_click(self.closedownloadpopup)


    def download1(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.select_checkbox)
        self.wait_to_click(self.click_download)
        self.wait_to_click(self.download_file)
        time.sleep(3)
        self.wait_to_click(self.closedownloadpopup)

    def download1_specificTable(self):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.select_hypertensioncheckbox)
        self.wait_to_click(self.click_download)
        self.wait_to_click(self.download_file)
        time.sleep(3)
        self.wait_to_click(self.closedownloadpopup)

    def latest_download_file(self):
        os.chdir(PathSettings.DOWNLOAD_PATH)
        files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
        max_file = max(files, key=os.path.getctime)
        path = os.path.join(PathSettings.DOWNLOAD_PATH, max_file)
        return path

    def create_download_lookuptable(self):
        self.create_lookup_table()
        self.download1()
        return self.table_id_name

    def write_data_excel(self,table_id, path,):
        excel = ExcelManager(path)
        for x in UserData.col_headers:
            for i in range(1, 2):
                col = excel.col_size(table_id)
                excel.write_excel_data(table_id, 1, col + i, x)
            excel.write_data(table_id, UserData.data_list1)
            excel.write_data(table_id, UserData.data_list2)

    def update_excel_user_value(self,table_id,path):
        excel = ExcelManager(path)
        col = excel.col_size(table_id)
        excel.write_excel_data(table_id, 1, col + 1, "user 1")
        excel.upload_to_path(table_id, UserData.data_list)

    def update_excel_group_value(self,table_id,path):
        excel = ExcelManager(path)
        col = excel.col_size(table_id)
        excel.write_excel_data(table_id, 1, col + 1, "group 1")
        excel.upload_to_path(table_id, UserData.data_list)

    def compare_excel(self,df1,df2,compareflag):
        if(compareflag ==0):
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

    def download_update_8(self,path,table_id):
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
        self.wait_to_click(self.manage_tables_link)
        self.scroll_to_bottom()
        self.send_keys(self.upload_table, filepath)
        self.wait_to_click(self.replace_table)
        self.wait_to_click(self.upload)
        time.sleep(20)
        self.wait_to_click(self.manage_tables_link)


    def delete_row_from_table(self, downloadpath, tablename):
        download_path = self.latest_download_file()
        excel = ExcelManager(download_path)
        excel.write_data(tablename, UserData.data_list1)
        self.err_upload(download_path)
        self.download1()
        self.view_lookup_table(tablename)
        row_count_before = self.rowCount_table(tablename)
        download_path_1 = self.latest_download_file()
        excel = ExcelManager(download_path_1)
        excel.delete_row(tablename, 2)
        self.replace_existing_table(download_path_1)
        self.view_lookup_table(tablename)
        row_count_after = self.rowCount_table(tablename)
        assert row_count_before > row_count_after
        print("Row got successfully Deleted")

    def rowCount_table(self, tablename):
        self.view_lookup_table(tablename)
        text = self.get_text(self.rowcount)
        rowcount = text[18:20].strip()
        return rowcount

    def update_delete_field(self,download_path,tablename):
        excel = ExcelManager(download_path)
        excel.upload_to_path(tablename, UserData.data_list)
        self.err_upload(download_path)
        self.view_lookup_table(tablename)
        row_count_before = self.rowCount_table(tablename)
        download_path_1 = self.latest_download_file()
        excel = ExcelManager(download_path_1)
        excel.write_excel_data(tablename, 3, 2, 'Y')
        self.replace_existing_table(download_path_1)
        self.view_lookup_table(tablename)
        row_count_after = self.rowCount_table(tablename)
        assert row_count_before > row_count_after
        print("Row got successfully Deleted")

    def attribute_2(self,download_path,tablename):
        download_path = self.latest_download_file()
        excel = ExcelManager(download_path)
        excel.write_excel_data("types", 1, 4, 'field 1')
        excel.write_excel_data("types", 2, 4, 'C1')
        excel.write_excel_data("types", 1, 5, 'field 2')
        excel.write_excel_data("types", 2, 5, 'C2')
        excel.write_excel_data(tablename, 1, 3, 'field:C1')
        excel.write_excel_data(tablename, 1, 4, 'field:C2')
        excel.write_data(tablename, UserData.new_datalist)
        self.err_upload(download_path)
        self.view_lookup_table(tablename)
        UIrows = self.rowCount_table(tablename)
        self.download1()
        excelrows = excel.row_size(tablename)
        assert int(UIrows) == (excelrows - 1)

    def bulkupload_1(self,tablenames, n, upload_path):
        before = ""
        after =""
        for i in range (0,n):
            tablename = str.split(tablenames,":")[i]
            row_count_before = self.rowCount_table(tablename)
            before = before +","+ row_count_before
        before=str.split(before,",",1)[1].strip()
        self.err_upload(upload_path)
        for i in range (0,n):
            tablename = str.split(tablenames,":")[i]
            row_count_After = self.rowCount_table(tablename)
            after = after +","+  row_count_After
        after = str.split(after, ",",1)[1].strip()
        for i in range (0,n):
            b_row = str.split(before,',')[0]
            a_row = str.split(after, ',')[0]
            print(b_row , a_row)
            assert b_row < a_row


    def delete_field_columns(self,downloadpath,tablename):
        downloadpath = self.latest_download_file()
        excel = ExcelManager(downloadpath)
        col_TypeSheet_before = excel.col_size("types")
        col1 = excel.col_size(tablename)
        excel.delete_column('types',4)
        excel.delete_column(tablename,3)
        self.err_upload(downloadpath)
        self.view_lookup_table(tablename)
        col_TypeSheet = excel.col_size("types")
        col2 = excel.col_size(tablename)
        assert col_TypeSheet_before > col_TypeSheet
        assert col1>col2
        print("Fields got deleted")


    def restore_attribute_1(self):
        time.sleep(20)
        self.is_present_and_displayed(self.restore_id,10)
        a = self.get_text(self.restore_id)
        print(a)
        print("OTA Restore succesfully with newely created properties")

    def test_13(self,download_path,tablename):
        excel = ExcelManager(download_path)
        self.write_data_excel(tablename, download_path)
        self.err_upload(download_path)
        self.download1()
        download_path_1 = self.latest_download_file()
        excel = ExcelManager(download_path_1)
        e1 = excel.get_cell_value(tablename, 1, 2)
        self.download1()
        download_path_2 = self.latest_download_file()
        excel = ExcelManager(download_path_2)
        e2 = excel.get_cell_value(tablename, 1, 2)
        assert e1 == e2
        print("UID for existing rows is same")


    def test_15(self,download_path,tablename):
        excel = ExcelManager(download_path)
        excel.write_data(tablename, UserData.data_list1)
        self.err_upload(download_path)
        self.download1()
        download_path_1 = self.latest_download_file()
        excel = ExcelManager(download_path_1)
        UID_before = excel.get_cell_value(tablename, 3, 2)
        UID1 = excel.get_cell_value(tablename, 1, 2)
        excel.write_excel_data(tablename, 2, 3, "dnckse")
        download_path_2 = self.latest_download_file()
        self.replace_existing_table(download_path_2)
        excel = ExcelManager(download_path_2)
        self.download1()
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
        time.sleep(20)


    def test_application(self):
        self.wait_to_click(self.applications_menu_id)
        self.wait_to_click(self.application)
        self.wait_to_click(self.add_module)
        time.sleep(1)
        self.wait_to_click(self.add_case_list)
        time.sleep(2)
        self.wait_to_click(self.add_questions)
        time.sleep(2)
        time.sleep(2)
        self.wait_to_click(self.lookup_question)
        time.sleep(2)
        #self.wait_to_click(self.multiplechoice)
        time.sleep(2)
        self.send_keys(self.question_display_text, self.question_display_text_name)
        self.wait_to_click(self.save_button)
        self.wait_to_click(self.lookuptable_data)
        self.wait_to_click(self.grid)
        self.wait_to_click(self.selectlookuptable)
        self.wait_to_click(self.value_field)
        time.sleep(3)
        self.wait_to_click(self.display_field)
        time.sleep(3)
        self.wait_to_click(self.select_logic)
        self.wait_to_click(self.add_logic)
        time.sleep(10)
        self.send_keys(self.filter,UserData.filter_value)
        self.wait_to_click(self.edit_filter)
        assert self.is_present_and_displayed(self.expression_editor)
        print("expression editior is displayed")

    def specific_table_upload(self,tablename):
        self.navigation_to_application_tab()
        self.wait_to_click(self.add_module)
        time.sleep(1)
        self.wait_to_click(self.add_case_list)
        time.sleep(2)
        self.wait_to_click(self.add_questions)
        time.sleep(2)
        self.wait_to_click(self.lookup_question)
        self.send_keys(self.question_display_text, self.question_display_text_name)
        self.wait_to_click(self.lookuptable_data)
        self.wait_to_click(self.grid)
        self.wait_to_click(self.selectlookuptable)
        dd = Select(self.find_element(self.selectlookuptable))
        print("tablename:", tablename)
        dd.select_by_visible_text(tablename)
        self.wait_to_click(self.save_button)
        time.sleep(5)

    def create_new_form(self):
        self.wait_to_click(self.applications_menu_id)
        self.wait_to_click(self.application)
        self.wait_to_click(self.add_module)
        time.sleep(1)
        self.wait_to_click(self.add_case_list)
        time.sleep(2)
        self.wait_to_click(self.add_questions)
        time.sleep(2)
        self.wait_to_click(self.lookup_question)
        self.send_keys(self.question_display_text, self.question_display_text_name)
        self.wait_to_click(self.lookuptable_data)
        self.wait_to_click(self.grid)
        self.wait_to_click(self.selectlookuptable)
        time.sleep(5)
        self.wait_to_click(self.save_button)

    def adding_questions(self):
        time.sleep(3)
        self.js_click(self.add_questions)
        time.sleep(3)
        self.wait_for_element(self.lookup_question)
        self.hover_and_click(self.lookup_question, self.checkbox_question)
        time.sleep(10)
        self.wait_to_click(self.save_button)
        self.find_elements(self.numberofquestions)
        Questionnodes = len(self.find_elements(self.numberofquestions))
        Childnodes = len(self.find_elements(self.childnode))
        assert int(Questionnodes)==int(Childnodes)



    def lookuptable_display_list(self):
        self.wait_to_click(self.selectlookuptable)
        dropdownValues = self.find_elements_texts(self.selectlookuptable)
        print(dropdownValues)
        assert dropdownValues[0] != "Custom"
        return dropdownValues

    def delete_Specificlookup_table(self,tablename):
        self.wait_to_click(self.manage_tables_link)
        if (tablename == "state"):
            self.wait_to_click(self.delete_statetable)
        obj = self.driver.switch_to.alert
        obj.accept()
        print("LookUp Table deleted successfully!")

    def navigation_to_application_tab(self):
        self.wait_to_click(self.applications_menu_id)
        self.wait_to_click(self.application)

    def Navigation_to_a_caselist(self,tablename):
        self.wait_to_click(self.SPECIFIC_Registration_form)
        self.wait_to_click(self.revist_lookup_tabble)
        dropdownvalues = self.lookuptable_display_list()
        dropdownvalues.__contains__(tablename)
        self.select_by_text(self.selectlookuptable,tablename)
        print(tablename)


    def formbuilder_4(self):
        self.clear(self.value_field)
        self.is_present_and_displayed(self.valueerror)
        a= self.get_text(self.valueerror)
        b= "Value Field is required."
        assert b in a
        print(b)
        self.clear(self.display_field)
        self.is_present_and_displayed(self.displayerror)
        a1= self.get_text(self.displayerror)
        b1= "Display Text Field is required."
        assert b1 in a1
        print(b1)

    def formbuilder_5(self):
        self.clear(self.value_field)
        self.wait_to_click(self.value_field)
        self.wait_to_click(self.autoselectedvalue)
        self.clear(self.display_field)
        self.wait_to_click(self.display_field)
        self.wait_to_click(self.autoselectedvalue1)
        self.wait_to_click(self.save_button)
        time.sleep(3)

    def edit_state(self,tablename):
        self.wait_to_click(self.manage_tables_link)
        self.wait_to_click(self.edit_state_table)
        self.wait_for_element(self.select_column)
        self.click(self.select_column)
        self.wait_for_element(self.savestate)
        self.wait_to_click(self.savestate)
        time.sleep(3)
        self.wait_to_click(self.applications_menu_id)
        self.wait_to_click(self.application)
        self.wait_to_click(self.Ecase_list)
        self.wait_to_click(self.grid)
        self.wait_to_click(self.savedbutton)
        time.sleep(5)
        assert self.is_present_and_displayed(self.errormessage)
        print("warning message is displayed")

    def language_selection(self,value):
        self.wait_to_click(self.settings)
        self.select_by_text(self.app_language, value)
        self.wait_to_click(self.done)

    def submit_form_on_registration(self,value,user):
        self.wait_for_element(self.home)
        self.wait_to_click(self.home)
        self.wait_to_click(self.login_user)
        time.sleep(2)
        self.wait_to_click((By.XPATH, self.select_user.format(user)))
        time.sleep(2)
        self.wait_for_element(self.login)
        self.wait_to_click(self.login )
        time.sleep(2)
        self.language_selection(value)
        self.wait_for_element(self.sync)
        self.wait_to_click(self.sync)
        time.sleep(20)
        self.wait_for_element(self.start)
        self.wait_to_click(self.start)
        self.wait_for_element(self.inapp_caselist)
        self.wait_to_click(self.inapp_caselist)
        self.wait_for_element(self.inapp_registrationform)
        self.wait_to_click(self.inapp_registrationform)
        time.sleep(3)
        if user != 'appiumtest':
            self.wait_to_click(self.inapp_selectoption)
            time.sleep(3)
            value = self.get_text(self.inapp_selectoption)
            self.wait_to_click(self.inapp_next)
            time.sleep(3)
            self.wait_to_click(self.inapp_continue)
            #self.send_keys(self.question_display_text, self.question_display_text_name)
            time.sleep(5)
            assert self.is_present_and_displayed(self.successmsg)
            print("form submitted succesfully:", value)
            en = "Uttar Pradesh"
            hin = "उत्तर प्रदेश"
            if value == hin:
                print("Form submitted in HINDI")
            elif value == en:
                print("Form submitted in ENGLISH")
        else:
            print("Make sure the 'Inapp' lookup table is available, and that its contents are accessible to the current user.")



    def language_check(self):
        self.clear(self.value_field)
        self.wait_to_click(self.value_field)
        self.send_keys(self.value_field, "id")
        self.clear(self.display_field)
        self.wait_to_click(self.display_field)
        self.send_keys(self.display_field, "name[@lang = jr:itext('lang-code-label')]" )
        self.wait_to_click(self.add_questions)
        time.sleep(2)
        self.wait_to_click(self.label)
        self.wait_to_click(self.dropdown_logic)
        self.wait_to_click(self.logic)
        self.send_keys(self.question_display_text_en, "en")
        self.clear(self.question_display_text_hin)
        self.send_keys(self.question_display_text_hin, "hin")
        self.send_keys(self.question_id,"lang-code")
        self.send_keys(self.display_condition,'1=2')
        self.wait_to_click(self.save_button)
        time.sleep(3)


    def multiple_groups(self,path,table_id):
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
        self.wait_to_click(self.download_file)
        time.sleep(15)
        self.wait_to_click(self.closedownloadpopup)

    def compare_and_delete(self, download_path):
        excel = ExcelManager(download_path)
        i = excel.row_size("types")
        for val in range(1, i):
            j = excel.get_cell_value("types", 2, val)
            print(val)
            print(j)
            if ( str(j).startswith("lookuptable")):
                print("Value to be updated")
                excel.write_excel_data("types",val,1,"Y")
        self.replace_existing_table(download_path)


