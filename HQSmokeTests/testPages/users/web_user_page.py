import time
import re
from datetime import date
from datetime import datetime

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from common_utilities.selenium.base_page import BasePage
from common_utilities.path_settings import PathSettings
from HQSmokeTests.userInputs.user_inputs import UserData
from HQSmokeTests.testPages.users.org_structure_page import latest_download_file
from selenium.common.exceptions import NoSuchElementException

""""Contains test page elements and functions related to the User's Web Users module"""


class WebUsersPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

        self.driver = driver
        self.users_menu_id = (By.ID, "ProjectUsersTab")
        self.web_users_menu = (By.LINK_TEXT, "Web Users")
        self.invite_web_user_button = (By.XPATH, "//i[@class='fa fa-plus']")
        self.email_input = (By.XPATH, "//input[@class='emailinput form-control']")
        self.select_project_role_id = "id_role"
        self.send_invite = (By.XPATH, "//button[contains(text(),'Send Invite')]")
        self.delete_confirm_invitation = (By.XPATH, "//button[@data-bind = 'click: $root.removeInvitation']")
        self.delete_confirm_webuser = (By.XPATH,
                                       "(//td[.//text()[contains(.,'" + UserData.yahoo_user_name + "')]]/following-sibling::td//i[@class='fa fa-trash'])[last()]")
        self.delete_success = (By.XPATH, "//div[@class='alert alert-margin-top fade in html alert-success']")
        self.verify_user = (By.XPATH,
                            "//td[.//text()[contains(.,'" + UserData.yahoo_user_name + "')]]/following-sibling::td[.//text()[contains(.,'Delivered')]]")
        self.remove_user_invite = (By.XPATH,
                                   "//td[.//text()[contains(.,'" + UserData.yahoo_user_name + "')]]/following-sibling::td//i[@class='fa fa-trash']")
        self.login_username = (By.ID, "login-username")
        self.next_button = (By.ID, "login-signin")
        self.login_password = (By.NAME, "password")
        self.signin_button = (By.ID, "login-signin")
        self.mail_icon = (By.XPATH, "//div[@class= 'icon mail']")
        self.latest_mail = (By.XPATH, "(//span[contains(@title,'Invitation from')])[1]")
        self.invitation_received_date = (By.XPATH, '//div[@data-test-id="message-date"]')
        self.accept_invitation = (By.XPATH, "//*[contains(text(), 'Accept Invitation')]")
        self.accept_invitation_hq = (By.XPATH, "//button[contains(text(), 'Accept Invitation')]")
        self.full_name = (By.NAME, "full_name")
        self.create_password = (By.NAME, "password")
        self.check_checkbox = (By.ID, "id_eula_confirmed")
        self.create_button = (By.XPATH, "//button[@type='submit']")
        self.settings = (By.XPATH, "//a[@data-action='Click Gear Icon']")
        self.sign_out = (By.XPATH, "//a[contains(@data-label,'Sign Out')]")
        self.creation_success = (By.XPATH, "//div[@class='alert alert-margin-top fade in alert-success']")
        self.password_textbox = (By.ID, 'id_auth-password')
        self.submit_button_xpath = (By.XPATH, '(//button[@type="submit"])[last()]')
        self.existing_error = (By.ID, 'error_1_id_email')
        self.download_worker_btn = (By.LINK_TEXT, "Download Web Users")
        self.download_filter = (By.XPATH, "//button[@class='btn btn btn-primary']")
        self.download_users_btn = (By.LINK_TEXT, "Download Users")
        self.bulk_upload_btn = (By.ID, "bulk_upload")
        self.choose_file = (By.XPATH, "//input[@id='id_bulk_upload_file']")
        self.upload = (By.XPATH, "//button[@class='btn btn-primary disable-on-submit']")
        self.import_complete = (By.XPATH, "//legend[text()='Bulk upload complete.']")

    def invite_new_web_user(self, role):
        self.wait_to_click(self.web_users_menu)
        self.wait_to_click(self.invite_web_user_button)
        self.wait_to_clear_and_send_keys(self.email_input, UserData.yahoo_user_name)
        select_role = Select(self.driver.find_element_by_id(self.select_project_role_id))
        select_role.select_by_value(role)
        self.wait_to_click(self.send_invite)
        if self.is_visible_and_displayed(self.existing_error):
            self.delete_invite()
            self.wait_to_click(self.invite_web_user_button)
            self.wait_to_clear_and_send_keys(self.email_input, UserData.yahoo_user_name)
            select_role = Select(self.driver.find_element_by_id(self.select_project_role_id))
            select_role.select_by_value(role)
            self.wait_to_click(self.send_invite)

    def assert_invitation_sent(self):
        time.sleep(10)
        self.wait_to_click(self.users_menu_id)
        self.wait_to_click(self.web_users_menu)
        assert self.is_visible_and_displayed(self.verify_user), "Unable to find delivered invite."
        print("Web user invitation sent successfully")

    def assert_invitation_received(self, mail_url, mail_username, mail_password):
        self.wait_to_click(self.settings)
        self.wait_to_click(self.sign_out)
        print("Signed out successfully")
        self.driver.get(mail_url)
        self.wait_to_clear_and_send_keys(self.login_username, mail_username)
        self.wait_and_sleep_to_click(self.next_button)
        self.wait_to_clear_and_send_keys(self.login_password, mail_password)
        self.wait_and_sleep_to_click(self.signin_button)
        self.wait_to_click(self.mail_icon)
        self.click(self.latest_mail)
        self.verify_invitation_received()

    def verify_invitation_received(self):
        received_date_on_yahoo = self.get_text(self.invitation_received_date)
        stripped_strings = re.findall(r'\w+', received_date_on_yahoo)
        unwanted = [0, 2]
        for ele in unwanted:
            del stripped_strings[ele]
        stripped_strings.insert(2, str(date.today().year))
        invitation_received_datetime = datetime.strptime(" ".join(stripped_strings), '%d %b %Y %I %M %p')
        current_time = datetime.now()
        time_difference = round((current_time - invitation_received_datetime).total_seconds())
        print(time_difference)
        assert time_difference in range(0, 200), "Unable to find invite"

    def accept_webuser_invite(self, mail_usename, mail_password):
        self.wait_to_click(self.accept_invitation)
        self.switch_to_next_tab()
        try:
            self.wait_to_clear_and_send_keys(self.full_name, mail_usename)
            self.wait_to_clear_and_send_keys(self.create_password, mail_password)
            self.wait_to_click(self.check_checkbox)
            self.wait_to_click(self.create_button)
        except TimeoutException:
            self.send_keys(self.password_textbox, mail_password)
            self.wait_to_click(self.submit_button_xpath)
        self.wait_to_click(self.accept_invitation_hq)
        assert "CommCare HQ" in self.driver.title, "Invitation Acceptance Failed"
        self.wait_to_click(self.settings)
        self.wait_to_click(self.sign_out)
        print("Signed out successfully")

    def delete_invite(self):
        self.wait_to_click(self.users_menu_id)
        self.wait_to_click(self.web_users_menu)
        self.wait_to_click(self.remove_user_invite)
        try:
            time.sleep(2)
            self.js_click(self.delete_confirm_invitation)
        except TimeoutException:
            time.sleep(2)
            self.js_click(self.delete_confirm_webuser)
        print("Invitation deleted")

    def download_web_users(self):
        time.sleep(1)
        self.wait_to_click(self.users_menu_id)
        self.wait_to_click(self.web_users_menu)
        self.wait_to_click(self.download_worker_btn)
        self.wait_to_click(self.download_filter)
        try:
            self.wait_and_sleep_to_click(self.download_users_btn)
            time.sleep(5)
        except TimeoutException:
            print("TIMEOUT ERROR: Still preparing for download..Celery might be down..")
            assert False
        # verify_downloaded_workers
        newest_file = latest_download_file()
        self.assert_downloaded_file(newest_file, "_users_"), "Download Not Completed!"
        print("File download successful")

    def upload_web_users(self):
        self.wait_to_click(self.users_menu_id)
        self.wait_to_click(self.web_users_menu)
        try:
            self.click(self.bulk_upload_btn)
            newest_file = latest_download_file()
            file_that_was_downloaded = PathSettings.DOWNLOAD_PATH / newest_file
            time.sleep(5)
            self.send_keys(self.choose_file, str(file_that_was_downloaded))
            self.wait_and_sleep_to_click(self.upload)
        except (TimeoutException, NoSuchElementException):
            print("TIMEOUT ERROR: Could not upload file")
        assert self.is_present_and_displayed(self.import_complete), "Upload Not Completed! Taking Longer to process.."
        print("File uploaded successfully")
