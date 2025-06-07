import os
import csv
from selenium.webdriver.common.by import By
import time
import pandas as pd

from common_utilities.selenium.base_page import BasePage
from QA_Requests.BenchmarkTests.userInputs.test_data import TestData
from common_utilities.path_settings import PathSettings
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

def latest_download_file():
    os.chdir(PathSettings.DOWNLOAD_PATH)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = max(files, key=os.path.getctime)
    print("File downloaded: " + newest)
    return newest

class BenchmarkPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.close_notification = (By.XPATH, "//div[@class='frame-close']/button[1]")
        self.iframe = (By.XPATH, "//iframe[contains(@src,'/embed/frame')]")
        self.view_latest_updates = (By.XPATH, "//*[.='View latest updates']")
        self.import_cases_from_excel_link = (By.XPATH,"//a[@href='/a/qateam/data/edit/import_cases/']")
        self.choose_file = (By.XPATH, "//input[@name='file']")
        self.next_step = (By.XPATH, "//i[@class='fa fa-forward']")
        self.case_type = (By.XPATH, "//select[@id='case_type']")
        self.excel_column = (By.XPATH, "//select[@id='search_column']")
        self.case_id = (By.XPATH, "//*[.='Case ID']")
        self.handle_cases_checkbox = (By.XPATH, "//input[@id='create_new_cases']")
        self.success_status = (By.XPATH, "(//td[contains(text(), '"+TestData.case_type+"')]/preceding-sibling::td/span[@class='label label-success'])[1]")
        self.case_id_download = (By.XPATH, "(//td[contains(text(), '"+TestData.case_type+"')]/following-sibling::td//a[@data-bind='attr: {href: caseIdsUrl()}'])[1]")

        # Add Export
        self.data_dropdown = (By.LINK_TEXT, 'Data')
        self.view_all_link = (By.LINK_TEXT, 'View All')
        self.add_export_button = (By.XPATH, "//a[@href='#createExportOptionsModal']")
        self.add_export_conf = (By.XPATH, "//button[@data-bind='visible: showSubmit, disable: disableSubmit']")
        self.export_name = (By.XPATH, '//*[@id="export-name"]')
        self.export_settings_create = (By.XPATH, "//button[@class='btn btn-lg btn-primary']")
        self.date_range = (By.ID, "id_date_range")
        self.case_owner = (By.XPATH, "//span[@class='select2-selection select2-selection--multiple']")

        # Export Form and Case data variables
        self.export_form_data_link = (By.LINK_TEXT, 'Export Form Data')
        self.export_case_data_link = (By.LINK_TEXT, 'Export Case Data')
        self.export_form_case_data_button = (By.XPATH, "(//a[@class='btn btn-primary'])[2]")
        self.prepare_export_button = (By.XPATH, "//button[@data-bind='disable: disablePrepareExport']")
        self.download_button = (By.XPATH, "//a[@class='btn btn-primary btn-full-width']")
        self.apply = (By.XPATH, "//button[@class='applyBtn btn btn-sm btn-primary']")
        self.export_button = (By.XPATH, "//a[@class='btn btn-primary'][contains(text(),'Export')]")
        self.codes = (By.XPATH, "//table//tr//code[starts-with(text(),'name')]")
        self.edit_form_case_export = (By.XPATH, "(//a[@data-bind='click: editExport'])[1]")

        # Export Modal
        self.app_type = (By.ID, "id_app_type")
        self.application = (By.ID, "id_application")
        self.module = (By.ID, "id_module")
        self.form = (By.ID, "id_form")
        self.case = (By.ID, "id_case_type")
        self.model = (By.ID, "id_model_type")
        # bulk export delete
        self.select_all_btn = (By.XPATH, '//button[@data-bind="click: selectAll"]')
        self.delete_selected_exports = (By.XPATH, '//a[@href= "#bulk-delete-export-modal"]')
        self.bulk_delete_confirmation_btn = (By.XPATH, '//button[@data-bind="click: BulkExportDelete"]')
        self.alert_button_accept = (By.ID, "hs-eu-confirmation-button")
        self.success_message = (By.XPATH, "//*[@class='alert alert-margin-top fade in alert-success']")
    # os.mkdir(TestData.output_path)
    def dismiss_notification(self):
        try:
            self.driver.switch_to.frame(self.find_element(self.iframe))
            self.wait_for_element(self.view_latest_updates)
            self.wait_to_click(self.close_notification)
            self.driver.switch_to.default_content()
        except TimeoutException:
            pass  # ignore if alert not on page

    def create_excel(self, col_start, col_end, output_path, data_dict):
        index_list = [1]
        for x in range(col_start, col_end):
            data_dict.update({'name_' + str(x): 'values_' + str(x)})

        writer = pd.ExcelWriter(output_path + '/' + 'Test_' + str(col_start) + '_to_' + str(col_end-1) + '.xlsx',
                                engine='openpyxl')
        # wb = writer.book
        df = pd.DataFrame(data=data_dict, index=index_list)
        df.to_excel(writer,
                    sheet_name=str(col_start) + '_to_' + str(col_end-1),
                    index=False)
        writer.save()
        return 'Test_' + str(col_start) + '_to_' + str(col_end-1) + '.xlsx'

    def excel_upload(self, output_path, filename):
        self.dismiss_notification()
        self.wait_to_click(self.import_cases_from_excel_link)
        newest_file = os.path.abspath(output_path+filename)
        print(newest_file)
        self.send_keys(self.choose_file, str(newest_file))
        self.wait_to_click(self.next_step)
        self.select_by_text(self.case_type,TestData.case_type)
        self.select_by_text(self.excel_column, 'caseid')
        self.wait_to_click(self.case_id)
        self.wait_to_click(self.handle_cases_checkbox)
        self.wait_to_click(self.next_step)
        self.wait_to_click(self.next_step)
        time.sleep(15)
        self.wait_for_element(self.success_status)
        print("Cases uploaded successfully!")

    def excel_download(self):
        self.wait_to_click(self.case_id_download)

    def delete_bulk_exports(self):
        try:
            self.wait_to_click(self.select_all_btn)
            self.wait_to_click(self.delete_selected_exports)
            self.wait_to_click(self.bulk_delete_confirmation_btn)
            time.sleep(2)
            # self.wait_for_element(self.success_message)
            # print("Cases uploaded successfully!")
        except TimeoutException:
            print("No exports available")

    def wait_for_export_page_load_completion(self, cols):
        self.reload_page()
        self.wait_to_click(self.export_case_data_link)
        self.wait_and_sleep_to_click(self.add_export_button)
        self.is_visible_and_displayed(self.app_type)
        self.select_by_text(self.application, TestData.benchmark_application)
        self.select_by_text(self.case, TestData.case_type)
        self.wait_to_click(self.add_export_conf)
        start_time = time.time()
        WebDriverWait(self.driver, 100000).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        res = self.wait_and_find_elements(self.codes,cols)
        count = self.find_elements(self.codes)
        print(res, len(count))
        assert len(count) >= cols, "All properties are not loaded"
        print("All properties are loaded. Total properties: ", len(count))
        # assert self.is_present_and_displayed(self.export_settings_create)
        end_time = time.time()
        total_time = end_time - start_time
        # total_time = time.strftime("%H:%M:%S", time.gmtime(total_time))
        print("Total time taken to execute the code: ", total_time)
        return str(total_time)

    def write_time_to_output(self,col_start, col_end,  output_csv,load_time):
        cols= str(col_start)+' to '+str(col_end-1)
        with open(output_csv, 'a',
                  newline='') as csvfile:  # creating the output files
            # defining the headers
            fieldnames = ['property_count','load_time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'property_count': cols,'load_time':load_time})

    def add_case_export(self, cols):
        self.reload_page()
        self.wait_to_click(self.export_case_data_link)
        self.delete_bulk_exports()
        self.wait_and_sleep_to_click(self.add_export_button)
        self.is_visible_and_displayed(self.app_type)
        self.select_by_text(self.application, TestData.benchmark_application)
        self.select_by_text(self.case, TestData.case_type)
        self.wait_to_click(self.add_export_conf)
        start_time = time.time()
        WebDriverWait(self.driver, 100000).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        res = self.wait_and_find_elements(self.codes,cols)
        count = self.find_elements(self.codes)
        print(res, len(count))
        # assert self.is_present_and_displayed(self.export_settings_create)
        self.wait_to_clear_and_send_keys(self.export_name, TestData.case_export_name)
        self.wait_to_click(self.export_settings_create)
        print("Export created!!")
        time.sleep(30)

    def edit_case_exports(self, cols):
        WebDriverWait(self.driver, 10000).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete')
        self.wait_and_sleep_to_click(self.export_case_data_link)
        time.sleep(2)
        self.wait_to_click(self.edit_form_case_export)
        start_time = time.time()
        WebDriverWait(self.driver, 100000).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete')
        res = self.wait_and_find_elements(self.codes, cols)
        count = self.find_elements(self.codes)
        print(res, len(count))
        assert len(count) >= cols, "All properties are not loaded"
        print("All properties are loaded. Total properties: ", len(count))
        # assert self.is_present_and_displayed(self.export_settings_create)
        end_time = time.time()
        total_time = end_time - start_time
        # total_time = time.strftime("%H:%M:%S", time.gmtime(total_time))
        print("Total time taken to execute the code: ", total_time)
        return str(total_time)
