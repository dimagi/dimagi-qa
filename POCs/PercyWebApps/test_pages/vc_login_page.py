from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By

from POCs.PercyWebApps.test_pages.visual_test_page import VisualTestPage
from POCs.PercyWebApps.user_inputs.bha_user_inputs import BhaUserInput
from common_utilities.selenium.base_page import BasePage
from common_utilities.hq_login.generate_2FA import generate_auth_token

""""Contains test page elements and functions to login into the application"""


class VCLoginPage(BasePage):

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
        driver.set_window_position(0, 0)
        driver.set_window_size(1920, 1080)
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        print("[DEBUG] Window size:", self.driver.get_window_size())
        print("[DEBUG] Window rect:", self.driver.get_window_rect())
        print("[DEBUG] Pixel ratio (JS):", self.driver.execute_script("return window.devicePixelRatio"))
        print("[DEBUG] Viewport (JS):", self.driver.execute_script("return [window.innerWidth, window.innerHeight]"))


    def enter_username(self, username):
        self.wait_to_clear_and_send_keys(self.username_textbox_id, username)

    def click_continue(self):
        try:
            self.click(self.continue_button_xpath)
        except (NoSuchElementException, ElementNotInteractableException):
            print("Non SSO workflow")

    def enter_password(self, password):
        self.wait_to_clear_and_send_keys(self.password_textbox_id, password)

    def enter_otp(self, otp):
        try:
            self.send_keys(self.otp_token_id, otp)
            self.wait_to_click(self.submit_button_xpath)
        except TimeoutException:
            pass  # ignore if 2FA not setup

    def click_submit(self):
        self.click(self.submit_button_xpath)

    def dismiss_notification(self):
        try:
            self.driver.switch_to.frame(self.find_element(self.iframe))
            self.wait_for_element(self.view_latest_updates)
            self.wait_to_click(self.close_notification)
            self.driver.switch_to.default_content()
        except TimeoutException:
            pass  # ignore if notification  not on page
        except NoSuchElementException:
            pass

    def accept_alert(self):
        try:
            self.click(self.alert_button_accept)
        except (TimeoutException, NoSuchElementException):
            pass  # ignore if alert not on page

    def logout(self):
        self.wait_to_click(self.settings)
        self.wait_to_click(self.sign_out)

    def assert_logged_in(self):
        assert "Log In" not in self.driver.title, "Login failed"

    def vc_login(self, username, password, user_secret=None, compare=None):
        vc = VisualTestPage(self.driver)
        vc.take_screenshots(BhaUserInput.screens['login_1'])
        self.enter_username(username)
        # self.click_continue()
        self.enter_password(password)
        self.dismiss_notification()
        self.accept_alert()
        vc.take_screenshots(BhaUserInput.screens['login'])
        self.click_submit()
        if self.is_displayed(self.otp_token_id):
            self.enter_otp(generate_auth_token(user_secret))
        self.assert_logged_in()



