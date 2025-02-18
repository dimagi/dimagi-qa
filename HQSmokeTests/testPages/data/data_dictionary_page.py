import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from common_utilities.generate_random_string import fetch_random_string
from common_utilities.selenium.base_page import BasePage
from common_utilities.path_settings import PathSettings
from HQSmokeTests.testPages.users.org_structure_page import latest_download_file


""""Contains test page elements and functions related to data dictionary module"""


class DataDictionaryPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.case_type_name = "case type " + str(fetch_random_string())
        self.case_type_created = "//a[@href='#" + self.case_type_name + "']"
        self.dictionary_name = "Dictionary " + str(fetch_random_string())
        self.dictionary_description = "Test dictionary"

        self.data_dictionary_link = (By.LINK_TEXT, "Data Dictionary")
        self.export_button = (By.XPATH, "//a[contains(@href,'export')]/i[contains(@class,'fa-cloud')]")
        self.import_button = (By.XPATH, "//a[contains(@href,'import')]/i[contains(@class,'fa-cloud')]")
        self.choose_file = (By.XPATH, "//input[@data-bind ='value: file']")
        self.upload = (By.XPATH, "//button[@data-bind ='disable: !file()']")
        self.success_message = (By.XPATH , "//div[@class= 'alert alert-margin-top fade in alert-success']")


    def open_data_dictionary_case_page(self):
        self.wait_to_click(self.data_dictionary_link)
        print("waiting for page to load completely....")
        time.sleep(20)

    def export_data_dictionary(self):
        try:
            self.wait_for_element(self.export_button)
            self.js_click(self.export_button)
            time.sleep(6)
            newest_file = latest_download_file()
            self.assert_downloaded_file(newest_file, "data_dictionary"), "Download Not Completed!"
            print("File download successful")
        except TimeoutException:
            print("TIMEOUT ERROR: Still preparing for download..Celery might be down..")
            assert False


    def import_data_dictionary(self):
        try:
            self.wait_for_element(self.import_button)
            self.js_click(self.import_button)
            newest_file = latest_download_file()
            file_that_was_downloaded = PathSettings.DOWNLOAD_PATH / newest_file
            time.sleep(5)
            self.send_keys(self.choose_file, str(file_that_was_downloaded))
            self.wait_and_sleep_to_click(self.upload)
            time.sleep(10)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Could not upload file")
        assert self.is_present_and_displayed(self.success_message), "Upload Not Completed!"
        print("File uploaded successfully")

