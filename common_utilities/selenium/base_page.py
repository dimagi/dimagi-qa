import time
import datetime

from dateutil.parser import parse
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    UnexpectedAlertPresentException, StaleElementReferenceException, NoSuchElementException, JavascriptException, \
    ElementNotInteractableException, WebDriverException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from common_utilities.path_settings import PathSettings

"""This class contains all the generic methods and utilities for all pages"""

from functools import wraps

def retry_on_exception(exceptions, retries=1, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt < retries - 1:
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

class BasePage:
    ENABLE_WAIT_AFTER_INTERACTION = False
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

    @retry_on_exception((StaleElementReferenceException, TimeoutException), retries=2, delay=2)
    def wait_to_click(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout, poll_frequency=1).until(
            ec.element_to_be_clickable(locator),
            message=f"Couldn't find locator: {locator}"
            )
        try:
            element.click()
        except UnexpectedAlertPresentException:
            self.driver.switch_to.alert.accept()
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
        self.wait_after_interaction()

    @retry_on_exception((ElementNotInteractableException, StaleElementReferenceException, TimeoutException))
    def wait_to_clear_and_send_keys(self, locator, user_input, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(locator),
            message=f"Couldn't find locator: {locator}"
            )
        element.clear()
        element.send_keys(user_input)
        # self.wait_after_interaction()

    def wait_to_get_text(self, locator, timeout=10):
        clickable = ec.visibility_of_element_located(locator)
        element_text = WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(clickable).text
        return element_text

    def wait_to_get_value(self, locator, timeout=10):
        clickable = ec.visibility_of_element_located(locator)
        element_text = WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(clickable).get_attribute("value")
        return element_text

    @retry_on_exception((StaleElementReferenceException, TimeoutException))
    def wait_for_element(self, locator, timeout=10):
        clickable = ec.presence_of_element_located(locator)
        WebDriverWait(self.driver, timeout, poll_frequency=1).until(clickable,
                                                                        message="Couldn't find locator: " + str(locator)
                                                                        )
            # self.wait_after_interaction()


    @retry_on_exception((StaleElementReferenceException, TimeoutException))
    def wait_and_sleep_to_click(self, locator, timeout=20):
        time.sleep(2)  # Optional initial sleep
        element = WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(
            ec.element_to_be_clickable(locator),
            message=f"Couldn't find locator: {locator}"
            )
        try:
            element.click()
        except ElementClickInterceptedException:
            if self.cookie_alert():
                self.click(self.alert_button_accept)
                element.click()
        except UnexpectedAlertPresentException:
            self.driver.switch_to.alert.accept()
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
        # self.wait_after_interaction()

    def find_elements(self, locator):
        # self.wait_after_interaction()
        elements = self.driver.find_elements(*locator)
        return elements
        # return [WrappedWebElement(e, self.driver, base_page=self) for e in elements]

    def find_elements_texts(self, locator):
        # self.wait_after_interaction()
        elements = self.driver.find_elements(*locator)
        value_list = []
        for element in elements:
            value_list.append(element.text)
        return value_list

    def find_element(self, locator):
        # self.wait_after_interaction()
        element = self.driver.find_element(*locator)
        return element
        # return WrappedWebElement(element, self.driver, base_page=self)

    @retry_on_exception((StaleElementReferenceException, ElementClickInterceptedException, TimeoutException))
    def click(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(
            ec.element_to_be_clickable(locator),
            message=f"Couldn't find or click locator: {locator}"
            )
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)
        # self.wait_after_interaction()

    def select_by_partial_text(self, locator, partial_text):
        select_element = self.driver.find_element(*locator)
        options = select_element.find_elements(By.TAG_NAME, "option")
        for option in options:
            text = option.text.strip().replace('\u200e', '')  # Remove LRM or other hidden chars
            if partial_text in text:
                option.click()
                print(f"[INFO] Selected: '{text}'")
                return
        raise Exception(f"[ERROR] Option with partial text '{partial_text}' not found.")

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
        element = WebDriverWait(self.driver, 20, poll_frequency=0.5).until(ec.visibility_of_element_located(locator))
        ActionChains(self.driver).move_to_element(element).pause(2).perform()

    def clear(self, locator):
        element = self.driver.find_element(*locator)
        element.clear()

    @retry_on_exception((ElementNotInteractableException, StaleElementReferenceException, TimeoutException))
    def send_keys(self, locator, user_input, timeout=10):
        element = WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(
            ec.element_to_be_clickable(locator),
            message=f"Couldn't find or click locator: {locator}"
            )
        try:
            element.clear()
            element.send_keys(user_input)
        except ElementNotInteractableException:
            print("[WARNING] Element not interactable. Trying JavaScript fallback...")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.driver.execute_script("arguments[0].value = arguments[1];", element, user_input)
        except Exception as e:
            print(f"[ERROR] send_keys failed: {e}")
            self.driver.execute_script("arguments[0].value = arguments[1];", element, user_input)
        # self.wait_after_interaction()

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

    def is_visible_and_displayed(self, locator, timeout=30):
        try:
            visible = ec.visibility_of_element_located(locator)
            element = WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(visible,
                                                                                   message="Element" + str(
                                                                                       locator
                                                                                       ) + "not displayed"
                                                                                   )
            is_displayed = element.is_displayed()
        except TimeoutException:
            is_displayed = False
        return bool(is_displayed)

    def is_present_and_displayed(self, locator, timeout=30):
        try:
            visible = ec.presence_of_element_located(locator)
            element = WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(visible,
                                                                                  message="Element" + str(
                                                                                      locator
                                                                                      ) + "not displayed"
                                                                                  )
            is_displayed = element.is_displayed()
        except TimeoutException:
            is_displayed = False
        except StaleElementReferenceException:
            self.driver.refresh()
            time.sleep(0.5)
            visible = ec.presence_of_element_located(locator)
            element = WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(visible,
                                                                                  message="Element" + str(locator
                                                                                                          ) + "not displayed"
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
        assert file_name in newest_file and diff_seconds in range(0, 600), f"Export not completed, {file_name} not in {newest_file}"

    def accept_pop_up(self):
        try:
            WebDriverWait(self.driver, 3, poll_frequency=0.5).until(ec.alert_is_present(), 'Waiting for popup to appear.')
            alert = self.driver.switch_to.alert
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")

    def page_source_contains(self, text):
        assert text in self.driver.page_source

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0)")

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
        element = WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(clickable,
                                                                              message="Couldn't find locator: "
                                                                                      + str(locator)
                                                                              )
        # action chain object
        action = ActionChains(self.driver)
        # double click operation
        action.double_click(element)

    @retry_on_exception((TimeoutException,StaleElementReferenceException))
    def js_click(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout, poll_frequency=0.25).until(
            ec.presence_of_element_located(locator),
            message=f"Couldn't find locator: {locator}"
            )
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
        self.wait_after_interaction()

    def scroll_to_element(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def wait_and_find_elements(self, locator, cols, timeout=50):
        elements = WebDriverWait(self.driver, timeout, poll_frequency=2).until(
            lambda driver: len(driver.find_elements(*locator)) >= int(cols)
            )
        return elements

    def wait_till_progress_completes(self, type="export"):
        if type == "export":
            if self.is_present((By.XPATH, "//div[contains(@class,'progress-bar')]")):
                WebDriverWait(self.driver, 200, poll_frequency=0.5).until(
                    ec.visibility_of_element_located((By.XPATH,
                                                      "//div[contains(@class,'progress-bar bg-success')]")
                                                     )
                    )
        elif type == "integration":
            WebDriverWait(self.driver, 200, poll_frequency=0.5).until(
                ec.invisibility_of_element_located((By.XPATH, "//div[contains(@class,'progress-bar')]"))
                )

    def is_clickable(self, locator, timeout=20):
        try:
            clickable = ec.element_to_be_clickable(locator)
            element = WebDriverWait(self.driver, timeout, poll_frequency=2).until(clickable,
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
        time.sleep(3)

    def get_url(self, link):
        self.driver.get(link)
        time.sleep(3)

    def switch_to_frame(self, frame_name):
        frame = self.driver.find_element(*frame_name)
        self.driver.switch_to.frame(frame)
        print("Switched to frame.")

    def js_send_keys(self, locator, value, timeout=10):
        clickable = ec.element_to_be_clickable(locator)
        element = WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(clickable,
                                                                              message="Couldn't find locator: "
                                                                                      + str(locator)
                                                                              )
        self.driver.execute_script("arguments[0].value='" + value + "';", element)
        time.sleep(1)
        self.wait_after_interaction()

    def wait_for_loading_spinner(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout, poll_frequency=0.5).until_not(
                ec.presence_of_element_located(("css selector", ".spinner"))
                )
        except Exception:
            pass

    def wait_for_ajax_and_progress(self, timeout=6):  # lower default timeout
        try:
            jquery_present = self._is_jquery_present()
            progress_container_present = self._is_element_present(By.ID, "formplayer-progress-container")

            if not jquery_present and not progress_container_present:
                return  # no need to wait

            end_time = time.time() + timeout
            while time.time() < end_time:
                ajax_done = (
                        not jquery_present or
                        self.driver.execute_script("return jQuery.active == 0")
                )
                progress_done = (
                        not progress_container_present or
                        self.driver.execute_script("""
                        const el = document.querySelector('#formplayer-progress-container');
                        return el && el.children.length === 0;
                    """
                                                   )
                )
                if ajax_done and progress_done:
                    return  # done early
                time.sleep(0.25)
        except Exception as e:
            print(f"[wait_for_ajax_and_progress] skipped or failed: {e}")


    def wait_until_progress_removed(self, timeout=20):
        if not self._is_element_present(By.ID, "formplayer-progress"):
            return
        try:
            WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(
                lambda d: not d.find_elements(By.ID, "formplayer-progress")
                )
        except Exception as e:
            print(f"[wait_until_progress_removed] Timeout or error: {e}")

    def wait_after_interaction(self, timeout=6):
        if not BasePage.ENABLE_WAIT_AFTER_INTERACTION:
            return

        if self._is_element_present(By.ID, "formplayer-progress"):
            self.wait_until_progress_removed()

        self.wait_for_ajax_and_progress(timeout=timeout)

    def _is_element_present(self, by, value):
        return bool(self.driver.find_elements(by, value))

    def _is_jquery_present(self):
        try:
            return self.driver.execute_script("return !!window.jQuery")
        except JavascriptException:
            return False

    def back(self):
        try:
            self.driver.back()
            print("[INFO] Navigated back using driver.back()")
        except WebDriverException as e:
            print(f"[WARNING] driver.back() failed: {e}. Trying JavaScript fallback...")
            try:
                self.driver.execute_script("window.history.back();")
                print("[INFO] Navigated back using JavaScript")
            except Exception as js_e:
                print(f"[ERROR] JavaScript fallback also failed: {js_e}")
                raise