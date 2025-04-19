import time
import datetime

from dateutil.parser import parse
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    UnexpectedAlertPresentException, StaleElementReferenceException, NoSuchElementException, JavascriptException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from common_utilities.path_settings import PathSettings

"""This class contains all the generic methods and utilities for all pages"""


class BasePage:
    def __init__(self, driver):
        self.driver = driver

        self.alert_button_accept = (By.ID, "hs-eu-confirmation-button")
        self.error_404 = (By.XPATH, "//h1[contains(text(),'404')]")
        self.error_403 = (By.XPATH, "//h1[text()='403 Forbidden']")

    def page_404(self):
        try:
            self.page_404_displayed = self.is_displayed(self.error_404)
        except NoSuchElementException:
            self.page_404_displayed = False
        return self.page_404_displayed

    def page_403(self):
        try:
            self.page_403_displayed = self.is_displayed(self.error_403)
        except NoSuchElementException:
            self.page_403_displayed = False
        return self.page_403_displayed

    def cookie_alert(self):
        try:
            self.cookie_alert_displayed = self.is_displayed(self.alert_button_accept)
        except NoSuchElementException:
            self.cookie_alert_displayed = False
        return self.cookie_alert_displayed

    def wait_to_click(self, locator, timeout=30):
        # element = None
        clickable = ec.element_to_be_clickable(locator)
        element = WebDriverWait(self.driver, timeout, poll_frequency=1).until(clickable, message="Couldn't find locator: "
                                                                               + str(locator)
                                                            )
        try:
            element.click()
        except UnexpectedAlertPresentException:
            alert = self.driver.switch_to.alert
            alert.accept()
            element.click()
        except StaleElementReferenceException:
            time.sleep(2)
            self.wait_to_click(locator)
            self.wait_after_interaction()
        except TimeoutException:
            self.wait_for_element(locator)
            self.wait_to_click(locator)
            self.wait_after_interaction()
            if self.page_403():
                self.driver.back()
                element.click()
            elif self.page_404():
                self.driver.back()
                element.click()
            else:
                raise TimeoutException()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
            self.wait_after_interaction()
        # try:
        #     clickable = ec.element_to_be_clickable(locator)
        #     element = WebDriverWait(self.driver, timeout).until(clickable,
        #                                                         message="Couldn't find locator: "
        #                                                                 + str(locator))
        #     element.click()
        # except ElementClickInterceptedException:
        #     if self.cookie_alert():
        #         self.click(self.alert_button_accept)
        #         element.click()


    def wait_to_clear_and_send_keys(self, locator, user_input):
        clickable = ec.visibility_of_element_located(locator)
        element = WebDriverWait(self.driver, timeout=5, poll_frequency=1).until(clickable, message="Couldn't find locator: " + str(locator))
        element.clear()
        element.send_keys(user_input)

    def wait_to_get_text(self, locator, timeout=10):
        clickable = ec.visibility_of_element_located(locator)
        element_text = WebDriverWait(self.driver, timeout, poll_frequency=1).until(clickable).text
        return element_text

    def wait_to_get_value(self, locator, timeout=10):
        clickable = ec.visibility_of_element_located(locator)
        element_text = WebDriverWait(self.driver, timeout, poll_frequency=1).until(clickable).get_attribute("value")
        return element_text

    def wait_for_element(self, locator, timeout=10):
        try:
            clickable = ec.presence_of_element_located(locator)
            WebDriverWait(self.driver, timeout, poll_frequency=1).until(clickable,
                                                                        message="Couldn't find locator: " + str(locator)
                                                                        )
            self.wait_after_interaction()
        except (StaleElementReferenceException, TimeoutException):
            self.wait_after_interaction()
            clickable = ec.presence_of_element_located(locator)
            WebDriverWait(self.driver, timeout, poll_frequency=1).until(clickable,
                                                                        message="Couldn't find locator: " + str(locator)
                                                                        )
            self.wait_after_interaction()


    def wait_and_sleep_to_click(self, locator, timeout=40):
        element = None
        try:
            time.sleep(2)
            clickable = ec.element_to_be_clickable(locator)
            element = WebDriverWait(self.driver, timeout, poll_frequency=1).until(clickable,
                                                                message="Couldn't find locator: "
                                                                        + str(locator)
                                                                )
            element.click()
        except ElementClickInterceptedException:
            if self.cookie_alert():
                self.click(self.alert_button_accept)
                element.click()
        except UnexpectedAlertPresentException:
            alert = self.driver.switch_to.alert
            alert.accept()
            element.click()
        except StaleElementReferenceException:
            time.sleep(2)
            self.wait_to_click(locator)
        except TimeoutException:
            if self.page_403():
                self.driver.back()
                element.click()
            elif self.page_404():
                self.driver.back()
                element.click()

    def find_elements(self, locator):
        self.wait_after_interaction()
        elements = self.driver.find_elements(*locator)
        return elements
        # return [WrappedWebElement(e, self.driver, base_page=self) for e in elements]

    def find_elements_texts(self, locator):
        self.wait_after_interaction()
        elements = self.driver.find_elements(*locator)
        value_list = []
        for element in elements:
            value_list.append(element.text)
        return value_list

    def find_element(self, locator):
        self.wait_after_interaction()
        element = self.driver.find_element(*locator)
        return element
        # return WrappedWebElement(element, self.driver, base_page=self)

    def click(self, locator):
        element = self.driver.find_element(*locator)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
        self.wait_after_interaction()
        time.sleep(1)

    def select_by_text(self, source_locator, value):
        select_source = Select(self.driver.find_element(*source_locator))
        select_source.select_by_visible_text(value)

    def select_by_value(self, source_locator, value):
        select_source = Select(self.driver.find_element(*source_locator))
        select_source.select_by_value(value)

    def select_by_index(self, source_locator, value):
        select_source = Select(self.driver.find_element(*source_locator))
        select_source.select_by_index(value)

    def get_selected_text(self, source_locator):
        select_source = Select(self.driver.find_element(*source_locator))
        return select_source.first_selected_option.text

    def deselect_all(self, source_locator):
        select_source = Select(self.driver.find_element(*source_locator))
        select_source.deselect_all()

    def move_to_element_and_click(self, locator):
        element = self.driver.find_element(*locator)
        ActionChains(self.driver).move_to_element(element).click(element).perform()

    def hover_on_element(self, locator):
        element = WebDriverWait(self.driver, 20, poll_frequency=1).until(ec.visibility_of_element_located(locator))
        ActionChains(self.driver).move_to_element(element).pause(2).perform()

    def clear(self, locator):
        element = self.driver.find_element(*locator)
        element.clear()

    def send_keys(self, locator, user_input, timeout=10):
        # Wait until the element is clickable
        element = WebDriverWait(self.driver, timeout, poll_frequency=1).until(
            ec.element_to_be_clickable(locator),
            message=f"Couldn't find or click locator: {locator}"
            )
        try:
            # Clear the field before typing
            element.clear()
            element.send_keys(user_input)
        except Exception as e:
            print(f"[Fallback] send_keys failed using normal method. Reason: {e}")
            try:
                self.driver.execute_script(
                    "arguments[0].value = arguments[1];", element, user_input
                    )
            except Exception as js_err:
                print(f"[ERROR] JS fallback also failed: {js_err}")
                raise

    def get_text(self, locator):
        element = self.driver.find_element(*locator)
        element_text = element.text
        print(element_text)
        return element_text

    def get_attribute(self, locator, attribute):
        element = self.driver.find_element(*locator)
        element_attribute = element.get_attribute(attribute)
        print(element_attribute)
        return element_attribute

    def is_selected(self, locator):
        try:
            element = self.driver.find_element(*locator)
            is_selected = element.is_selected()
        except TimeoutException:
            is_selected = False
        return bool(is_selected)

    def is_enabled(self, locator):
        try:
            element = self.driver.find_element(*locator)
            is_enabled = element.is_enabled()
        except TimeoutException:
            is_enabled = False
        return bool(is_enabled)

    def is_displayed(self, locator):
        try:
            element = self.driver.find_element(*locator)
            is_displayed = element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            is_displayed = False
        return bool(is_displayed)

    def is_present(self, locator):
        try:
            element = self.driver.find_element(*locator)
            is_displayed = True
        except NoSuchElementException:
            is_displayed = False
        return bool(is_displayed)

    def is_visible_and_displayed(self, locator, timeout=50):
        try:
            visible = ec.visibility_of_element_located(locator)
            element = WebDriverWait(self.driver, timeout, poll_frequency=10).until(visible,
                                                                                   message="Element" + str(
                                                                                       locator
                                                                                       ) + "not displayed"
                                                                                   )
            is_displayed = element.is_displayed()
        except TimeoutException:
            is_displayed = False
        return bool(is_displayed)

    def is_present_and_displayed(self, locator, timeout=50):
        try:
            visible = ec.presence_of_element_located(locator)
            element = WebDriverWait(self.driver, timeout, poll_frequency=2).until(visible,
                                                                                   message="Element" + str(
                                                                                       locator
                                                                                       ) + "not displayed"
                                                                                   )
            is_displayed = element.is_displayed()
        except TimeoutException:
            is_displayed = False
        except StaleElementReferenceException:
            self.driver.refresh()
            time.sleep(2)
            visible = ec.presence_of_element_located(locator)
            element = WebDriverWait(self.driver, timeout, poll_frequency=1).until(visible,
                                                                message="Element" + str(locator) + "not displayed"
                                                                )
            is_displayed = element.is_displayed()
        return bool(is_displayed)

    def switch_to_next_tab(self):
        winHandles = self.driver.window_handles
        window_after = winHandles[1]
        self.driver.switch_to.window(window_after)
        print(self.driver.title)
        print(self.driver.current_window_handle)

    def switch_to_new_tab(self):
        self.driver.switch_to.new_window('tab')

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def switch_back_to_prev_tab(self):
        winHandles = self.driver.window_handles
        window_before = winHandles[0]
        self.driver.switch_to.window(window_before)
        print(self.driver.title)
        print(self.driver.current_window_handle)

    def get_current_url(self):
        get_url = self.driver.current_url
        print("Current URL : " + get_url)
        return get_url

    def get_environment(self):
        get_env = self.driver.current_url
        env_name = get_env.split("/")[2]
        print("server : " + env_name)
        return env_name

    def get_domain(self):
        get_url = self.driver.current_url
        domain_name = get_url.split("/")[4]
        print("domain: " + domain_name)
        return domain_name

    def assert_downloaded_file(self, newest_file, file_name):
        modTimesinceEpoc = (PathSettings.DOWNLOAD_PATH / newest_file).stat().st_mtime
        modificationTime = datetime.datetime.fromtimestamp(modTimesinceEpoc)
        timeNow = datetime.datetime.now()
        diff_seconds = round((timeNow - modificationTime).total_seconds())
        print("Last Modified Time : ", str(modificationTime) + 'Current Time : ', str(timeNow),
              "Diff: " + str(diff_seconds)
              )
        assert file_name in newest_file and diff_seconds in range(0, 600), "Export not completed"

    def accept_pop_up(self):
        try:
            WebDriverWait(self.driver, 3, poll_frequency=1).until(ec.alert_is_present(), 'Waiting for popup to appear.')
            alert = self.driver.switch_to.alert
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")

    def page_source_contains(self, text):
        assert text in self.driver.page_source

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def hover_and_click(self, locator1, locator2):
        action = ActionChains(self.driver)
        element_1 = WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located(locator1))
        action.move_to_element(element_1).perform()
        # identify sub menu element
        element_2 = WebDriverWait(self.driver, 5).until(ec.visibility_of_element_located(locator2))
        # hover over element and click
        action.move_to_element(element_2).click().perform()

    def double_click(self, locator, timeout=10):
        clickable = ec.element_to_be_clickable(locator)
        element = WebDriverWait(self.driver, timeout, poll_frequency=1).until(clickable,
                                                            message="Couldn't find locator: "
                                                                    + str(locator)
                                                            )
        # action chain object
        action = ActionChains(self.driver)
        # double click operation
        action.double_click(element)

    # def js_click(self, locator, timeout=10):
    #     clickable = ec.element_to_be_clickable(locator)
    #     element = WebDriverWait(self.driver, timeout).until(clickable,
    #                                                         message="Couldn't find locator: "
    #                                                                 + str(locator)
    #                                                         )
    #     self.driver.execute_script("arguments[0].click();", element)
    #     time.sleep(3)

    def scroll_to_element(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def wait_and_find_elements(self, locator, cols, timeout=100):
        elements = WebDriverWait(self.driver, timeout, poll_frequency=2).until(
            lambda driver: len(driver.find_elements(*locator)) >= int(cols)
            )
        return elements

    def wait_till_progress_completes(self, type="export"):
        if type == "export":
            if self.is_present((By.XPATH, "//div[contains(@class,'progress-bar')]")):
                WebDriverWait(self.driver, 200, poll_frequency=2).until(
                    ec.visibility_of_element_located((By.XPATH,
                                                      "//div[contains(@class,'progress-bar')][.//span[@data-bind='text: progress'][.='100']]")
                                                     )
                    )
        elif type == "integration":
            WebDriverWait(self.driver, 200, poll_frequency=10).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[contains(@class,'progress-bar')]"))
                )

    def is_clickable(self, locator, timeout=50):
        try:
            clickable = ec.element_to_be_clickable(locator)
            element = WebDriverWait(self.driver, timeout, poll_frequency=1).until(clickable,
                                                                                   message="Element" + str(
                                                                                       locator
                                                                                       ) + "not displayed"
                                                                                   )
            is_clickable = element.is_enabled()
        except TimeoutException:
            is_clickable = False
        return bool(is_clickable)

    def get_element(self, xpath_format, insert_value):
        element = (By.XPATH, xpath_format.format(insert_value))
        return element

    def wait_for_ajax(self, timeout=10):
        """
        Waits for jQuery AJAX calls to complete.
        Automatically detects jQuery even if it's namespaced or suffixed.
        Skips wait if jQuery is not used or no AJAX is active.
        """
        try:
            # Find the actual jQuery object (handles cases like jQuery1234567890)
            jquery_object = self.driver.execute_script("""
                for (var key in window) {
                    if (key.startsWith("jQuery") && window[key] && window[key].active !== undefined) {
                        return key;
                    }
                }
                return null;
            """
                                                       )

            if jquery_object:
                # Check if AJAX is active
                is_ajax_active = self.driver.execute_script(f"return window['{jquery_object}'].active != 0;")
                if is_ajax_active:
                    print(f"Waiting for AJAX (using {jquery_object}) to complete...")
                    WebDriverWait(self.driver, timeout).until(
                        lambda driver: driver.execute_script(f"return window['{jquery_object}'].active") == 0
                        )
                else:
                    print("No active jQuery AJAX requests — skipping wait.")
            else:
                # Fallback: wait for document readyState
                print("No jQuery object detected — waiting for document.readyState == 'complete'")
                ready_state = self.driver.execute_script("return document.readyState")
                if ready_state != "complete":
                    WebDriverWait(self.driver, timeout).until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                        )

        except (JavascriptException, TimeoutException) as e:
            print(f"[wait_for_ajax] Skipped or timed out: {e}")

    def is_date(self, string, fuzzy=False):
        """
        Return whether the string can be interpreted as a date.

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try:
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False

    def get_all_dropdown_options(self, source_locator):
        select_source = Select(self.driver.find_element(*source_locator))
        list_opt = []
        for opt in select_source.options:
            print(opt.text)
            list_opt.append(opt.text)
        print("Option list", list_opt)
        return list_opt

    def select_multiple_by_text(self, source_locator, value_list):
        select_source = Select(self.driver.find_element(*source_locator))
        ActionChains(self.driver).key_down(Keys.CONTROL).perform()
        for value in value_list:
            select_source.select_by_visible_text(value)
        ActionChains(self.driver).key_up(Keys.CONTROL).perform()

    def reload_page(self):
        self.driver.refresh()
        time.sleep(2)

    def get_url(self, link):
        self.driver.get(link)
        time.sleep(2)

    def switch_to_frame(self, frame_name):
        frame = self.driver.find_element(*frame_name)
        self.driver.switch_to.frame(frame)
        print("Switched to frame.")

    def js_send_keys(self, locator, value, timeout=10):
        clickable = ec.element_to_be_clickable(locator)
        element = WebDriverWait(self.driver, timeout, poll_frequency=1).until(clickable,
                                                            message="Couldn't find locator: "
                                                                    + str(locator)
                                                            )
        self.driver.execute_script("arguments[0].value='" + value + "';", element)
        self.wait_after_interaction()

    def wait_for_loading_spinner(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout, poll_frequency=1).until_not(
                ec.presence_of_element_located(("css selector", ".spinner"))
                )
        except Exception:
            pass

    def wait_for_ajax_and_progress(self, timeout=10):
        try:
            # Wait until there are no active jQuery AJAX calls
            WebDriverWait(self.driver, timeout, poll_frequency=1).until(
                lambda d: d.execute_script("return window.jQuery ? jQuery.active == 0 : true")
                )

            # Check if the progress container exists before waiting for it to be empty
            if self.driver.find_elements(By.ID, "formplayer-progress-container"):
                WebDriverWait(self.driver, timeout, poll_frequency=1).until(
                    lambda d: d.execute_script("""
                        const el = document.querySelector('#formplayer-progress-container');
                        return el && el.children.length === 0;
                    """
                                               )
                    )

        except Exception as e:
            print(f"Exception while waiting for AJAX and progress: {e}")

    def wait_until_progress_removed(self, timeout=60):
        try:
            # Check if the progress element is present at all
            if self.driver.find_elements(By.ID, "formplayer-progress"):
                WebDriverWait(self.driver, timeout, poll_frequency=1).until(
                    lambda d: not d.find_elements(By.ID, "formplayer-progress")
                    )
        except Exception as e:
            print(f"Exception while waiting for progress to disappear: {e}")

    def wait_after_interaction(self):
        self.wait_until_progress_removed()
        self.wait_for_ajax_and_progress()

