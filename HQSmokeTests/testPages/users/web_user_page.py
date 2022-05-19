import time
import re
from datetime import date
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from HQSmokeTests.testPages.base.base_page import BasePage
from HQSmokeTests.userInputs.user_inputs import UserData

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
        self.delete_confirm_button = (By.XPATH, "//button[@data-bind='click: $root.removeInvitation']")
        self.verify_user = (By.XPATH,
                            "//td[.//text()[contains(.,'" + UserData.web_user_mail + "')]]/following-sibling::td[.//text()[contains(.,'Delivered')]]")
        self.remove_user_invite = (By.XPATH,
                                   "//td[.//text()[contains(.,'" + UserData.web_user_mail + "')]]/following-sibling::td//i[@class='fa fa-trash']")
        self.login_username = (By.ID, "login-username")
        self.next_button = (By.ID, "login-signin")
        self.login_password = (By.NAME, "password")
        self.signin_button = (By.ID, "login-signin")
        self.mail_icon = (By.XPATH, "//div[@class= 'icon mail']")
        self.latest_mail = (By.XPATH, '//*[contains(text(),"Invitation from Nitin Saxena to join CommCareHQ")][1]')
        self.locator = (By.XPATH, '//div[@data-test-id="message-date"]')

    def invite_new_web_user(self, role):
        self.wait_to_click(self.users_menu_id)
        self.wait_to_click(self.web_users_menu)
        self.wait_to_click(self.invite_web_user_button)
        self.wait_to_clear_and_send_keys(self.email_input, UserData.web_user_mail)
        select_role = Select(self.driver.find_element_by_id(self.select_project_role_id))
        select_role.select_by_value(role)
        self.wait_to_click(self.send_invite)

    def go_to_gmail(self, password_mail_yahoo):
        self.driver.get("https://login.yahoo.com/")
        self.wait_to_clear_and_send_keys(self.login_username, UserData.yahoo_email_username)
        self.wait_to_click(self.next_button)
        self.wait_to_clear_and_send_keys(self.login_password, password_mail_yahoo)
        self.wait_to_click(self.signin_button)
        self.wait_to_click(self.mail_icon)
        self.wait_to_click(self.latest_mail)
        text_fetched_by_selenium = self.get_text(self.locator)
        stripped_strings = re.findall(r'\w+', text_fetched_by_selenium)
        unwanted = [0, 2]
        for ele in unwanted:
            del stripped_strings[ele]
        stripped_strings.insert(2, str(date.today().year))
        datetime_object = datetime.strptime(" ".join(stripped_strings), '%d %b %Y %I %M %p')
        print(datetime_object)
        current_time = datetime.now()
        print(current_time)
        time_difference = print(round((current_time - datetime_object).total_seconds()))
        assert time_difference not in range(0, 180), "Mail not Received"

    def assert_invite(self):
        time.sleep(5)
        self.wait_to_click(self.users_menu_id)
        self.wait_to_click(self.web_users_menu)
        self.go_to_gmail()
        assert self.is_displayed(self.verify_user), "Unable to find invite."
        print("Web user invitation sent successfully")

    def delete_invite(self, ):
        self.wait_to_click(self.remove_user_invite)
        self.wait_to_click(self.delete_confirm_button)
        print("Invitation deleted")
