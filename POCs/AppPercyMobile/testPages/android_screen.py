from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time

from POCs.AppPercyMobile.testPages.visual_test_page import VisualTestPage
from common_utilities.generate_random_string import fetch_random_string
from POCs.AppPercyMobile.user_inputs.user_inputs import UserInput

""""Contains test page elements and functions related to the app installation and form submission on mobile"""


class AndroidScreen:

    def __init__(self, settings):
        # This sample code uses the Appium python client v2
        # pip install Appium-Python-Client
        # Then you can paste this into a file and simply run with Python

        self.options = UiAutomator2Options().load_capabilities({
            # Specify device and os_version for testing
            "platformName": "android",
            "appium:platformVersion": "15.0",
            "appium:deviceName": "Google Pixel 9",
            "appium:automationName": "UIAutomator2",

            # Set URL of the application under test
            "appium:app": "bs://11e29ba1f42575cb2b3406c27bcdc8a7abc5fe6e",

            "appium:autoGrantPermissions": "true",
            "appium:newCommandTimeout": 3600,
            "appium:percyOptions": {
                "enabled": True  # True by default. This can be used to disable visual testing for certain devices
                },

            # Set other BrowserStack capabilities
            'bstack:options': {
                "projectName": "First Python project",
                "buildName": "Python Android",
                "sessionName": "first_test",

                # Set your access credentials
                "userName": settings["bs_user"],
                "accessKey": settings["bs_key"]

            }
        })

        # Initialize the remote Webdriver using BrowserStack remote URL
        # and desired capabilities defined above
        self.driver = webdriver.Remote(
            "https://hub-cloud.browserstack.com:443/wd/hub",
            options=self.options
        )
        self.driver.implicitly_wait(15)

        # Locator
        self.enter_code = "//android.widget.TextView[@text='Enter Code']"
        self.profile_code = "org.commcare.dalvik:id/edit_profile_location"
        self.start_install = "org.commcare.dalvik:id/start_install"
        self.install = "//android.widget.TextView[@text='Start Install']"
        self.username = "org.commcare.dalvik:id/edit_username"
        self.password = "org.commcare.dalvik:id/edit_password"
        self.login = "org.commcare.dalvik:id/login_button"
        self.start_button = "//android.widget.TextView[@text='Start']"
        self.sync_button = "//android.widget.TextView[@text='Sync with Server']"
        self.case_list = "//android.widget.TextView[@text='"+UserInput.case_list_name+"']"
        self.form = "//android.widget.TextView[@text='"+UserInput.new_form_name+"']"
        self.text_field = "//android.widget.EditText"
        self.submit_button = "//android.widget.TextView[@text='FINISH']"


    def click_xpath(self, locator):
        element = self.driver.find_element(AppiumBy.XPATH, locator)
        element.click()

    def click_id(self, locator):
        element = self.driver.find_element(AppiumBy.ID, locator)
        element.click()

    def send_text_xpath(self, locator, user_input):
        element = self.driver.find_element(AppiumBy.XPATH, locator)
        element.send_keys(user_input)

    def send_text_id(self, locator, user_input):
        element = self.driver.find_element(AppiumBy.ID, locator)
        element.send_keys(user_input)

    def install_app_and_submit_form(self, tag, code):
        random_text = fetch_random_string()
        visual = VisualTestPage(self.driver)
        time.sleep(4)
        visual.take_screenshots(tag, UserInput.screens['app_code_install_screen_before'])
        self.driver.find_element(AppiumBy.XPATH, self.enter_code).click()
        self.driver.find_element(AppiumBy.ID, self.profile_code).send_keys(code)
        visual.take_screenshots(tag, UserInput.screens['app_code_install_screen_after'])
        self.driver.find_element(AppiumBy.ID, self.start_install).click()
        time.sleep(3)
        self.driver.find_element(AppiumBy.XPATH, self.install).click()
        time.sleep(15)
        visual.take_screenshots(tag, UserInput.screens['login_before'])
        self.driver.find_element(AppiumBy.ID, self.username).send_keys(UserInput.app_login)
        self.driver.find_element(AppiumBy.ID, self.password).send_keys(UserInput.app_password)
        visual.take_screenshots(tag, UserInput.screens['login_after'])
        self.driver.find_element(AppiumBy.ID, self.login).click()
        time.sleep(50)
        visual.take_screenshots(tag, UserInput.screens['home_screen'])
        self.driver.find_element(AppiumBy.XPATH, self.start_button).click()
        time.sleep(3)
        visual.take_screenshots(tag, UserInput.screens['app_screen'])
        self.driver.find_element(AppiumBy.XPATH, self.case_list).click()
        time.sleep(3)
        visual.take_screenshots(tag, UserInput.screens['form_screen'])
        self.driver.find_element(AppiumBy.XPATH, self.form).click()
        time.sleep(3)
        assert self.driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'Add Text')]").is_displayed()
        visual.take_screenshots(tag, UserInput.screens['before_input_screen'])
        self.driver.find_element(AppiumBy.XPATH, self.text_field).send_keys(random_text)
        visual.take_screenshots(tag, UserInput.screens['after_input_screen'])
        self.driver.find_element(AppiumBy.XPATH, self.submit_button).click()
        time.sleep(2)
        assert self.driver.find_element(AppiumBy.XPATH, "//android.widget.TextView[@text='1 form sent to server!']").is_displayed()
        self.driver.find_element(AppiumBy.XPATH, self.sync_button).click()
        visual.take_screenshots(tag, UserInput.screens['after_submission_screen'])
        time.sleep(3)

    def close_android_driver(self):
        self.driver.quit()
