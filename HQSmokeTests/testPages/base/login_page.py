from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By

from HQSmokeTests.testPages.base.base_page import BasePage
from HQSmokeTests.testPages.base.generate_2FA import generate_auth_token


class LoginPage(BasePage):

    def __init__(self, driver, url):
        super().__init__(driver)

        self.username_textbox_id = (By.ID, "id_auth-username")
        self.password_textbox_id = (By.ID, "id_auth-password")
        self.submit_button_xpath = (By.XPATH, '(//button[@type="submit"])[last()]')
        self.otp_token_id = (By.ID, 'id_token-otp_token')
        self.alert_button_accept = (By.ID, "hs-eu-confirmation-button")
        self.continue_button_xpath = (By.XPATH, '//button[@class="btn btn-primary btn-lg" and @type ="button"]')
        self.close_notification = (By.XPATH, "//div[@class='frame-close']/button[1]")
        self.iframe = (By.XPATH, "//iframe[contains(@src,'/embed/frame')]")
        self.view_latest_updates = (By.XPATH, "//*[.='View latest updates']")
        self.settings = (By.XPATH, "//a[@data-action='Click Gear Icon']")
        self.sign_out = (By.XPATH, "//a[contains(@data-label,'Sign Out')]")

        self.driver.get(url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def enter_username(self, username):
        self.wait_to_clear_and_send_keys(self.username_textbox_id, username)

    def click_continue(self):
        try:
            self.click(self.continue_button_xpath)
        except (NoSuchElementException, ElementNotInteractableException):
            print("Non SSO workflow")

    def enter_password(self, password):
        self.wait_to_clear_and_send_keys(self.password_textbox_id, password)

    def click_submit(self):
        self.click(self.submit_button_xpath)

    def enter_otp(self, otp):
        try:
            self.send_keys(self.otp_token_id, otp)
            self.wait_to_click(self.submit_button_xpath)
        except TimeoutException:
            pass  # ignore if 2FA not setup

    def accept_alert(self):
        try:
            self.click(self.alert_button_accept)
        except TimeoutException:
            pass  # ignore if alert not on page

    def assert_logged_in(self):
        assert "Log In" not in self.driver.title, "Login failed"

    def dismiss_notification(self):
        try:
            self.driver.switch_to.frame(self.find_element(self.iframe))
            self.wait_for_element(self.view_latest_updates)
            self.js_click(self.close_notification)
            self.driver.switch_to.default_content()
        except TimeoutException:
            pass  # ignore if alert not on page

    def logout(self):
        self.wait_to_click(self.settings)
        self.wait_to_click(self.sign_out)

    def login(self, username, password):
        self.enter_username(username)
        self.click_continue()
        self.enter_password(password)
        self.dismiss_notification()
        self.accept_alert()
        self.click_submit()
        self.assert_logged_in()

    def two_factor_auth(self, username, password, secret):
        self.logout()
        self.enter_username(username)
        self.click_continue()
        self.enter_password(password)
        self.click_submit()
        self.enter_otp(generate_auth_token(secret))
        self.assert_logged_in()

