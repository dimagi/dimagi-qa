import time
import datetime
import logging
from functools import wraps

from dateutil.parser import parse
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException, ElementClickInterceptedException, UnexpectedAlertPresentException,
    StaleElementReferenceException, NoSuchElementException, JavascriptException,
    ElementNotInteractableException, WebDriverException
)

from common_utilities.path_settings import PathSettings

logger = logging.getLogger(__name__)


def retry_on_stale(retries=2, delay=0.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except StaleElementReferenceException:
                    time.sleep(delay)
            raise
        return wrapper
    return decorator


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.alert_button_accept = (By.ID, "hs-eu-confirmation-button")
        self.error_404 = (By.XPATH, "//h1[contains(text(),'404')]")
        self.error_403 = (By.XPATH, "//h1[text()='403 Forbidden']")

    def wait_until(self, condition, timeout=10, message=None):
        return WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(condition, message=message)

    def page_404(self):
        return self.is_displayed(self.error_404)

    def page_403(self):
        return self.is_displayed(self.error_403)

    def cookie_alert(self):
        return self.is_displayed(self.alert_button_accept)

    @retry_on_stale()
    def wait_to_click(self, locator, timeout=30):
        try:
            element = self.wait_until(ec.element_to_be_clickable(locator), timeout, f"Couldn't click: {locator}")
            element.click()
        except UnexpectedAlertPresentException:
            self.driver.switch_to.alert.accept()
            self.wait_until(ec.element_to_be_clickable(locator), timeout).click()
        except TimeoutException:
            self.wait_for_element(locator)
            if self.page_403() or self.page_404():
                self.driver.back()
                self.wait_until(ec.element_to_be_clickable(locator), timeout).click()
            else:
                raise
        except Exception:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", element)
        self.wait_after_interaction()

    def wait_for_element(self, locator, timeout=10):
        try:
            self.wait_until(ec.presence_of_element_located(locator), timeout, f"Couldn't find: {locator}")
        except (StaleElementReferenceException, TimeoutException):
            self.wait_after_interaction()
            self.wait_until(ec.presence_of_element_located(locator), timeout, f"Couldn't find: {locator}")
        self.wait_after_interaction()

    def wait_to_clear_and_send_keys(self, locator, user_input, timeout=10):
        try:
            element = self.wait_until(ec.visibility_of_element_located(locator), timeout, f"Couldn't find: {locator}")
            element.clear()
            element.send_keys(user_input)
        except Exception as e:
            logger.error(f"[wait_to_clear_and_send_keys] Failed on {locator}: {e}")
            raise

    def click(self, locator):
        try:
            self.driver.find_element(*locator).click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", self.driver.find_element(*locator))
        self.wait_after_interaction()
        time.sleep(1)

    def send_keys(self, locator, user_input, timeout=10):
        try:
            element = self.wait_until(ec.element_to_be_clickable(locator), timeout, f"Couldn't click: {locator}")
            element.clear()
            element.send_keys(user_input)
        except (ElementNotInteractableException, TimeoutException) as e:
            logger.warning(f"{type(e).__name__}: {e} — trying JS fallback")
            try:
                element = self.driver.find_element(*locator)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                self.driver.execute_script("arguments[0].value = arguments[1];", element, user_input)
            except JavascriptException as js_e:
                logger.error(f"JS fallback failed: {js_e}")
                raise
        except Exception as e:
            logger.error(f"send_keys failed: {e}")
            raise

    def is_displayed(self, locator):
        try:
            return self.driver.find_element(*locator).is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_after_interaction(self):
        if self.driver.find_elements(By.ID, "formplayer-progress") or \
           self.driver.find_elements(By.ID, "formplayer-progress-container") or \
           self.driver.find_elements(By.CSS_SELECTOR, ".spinner"):
            logger.info("Detected progress/spinner — waiting...")
            self.wait_until(lambda d: not d.find_elements(By.ID, "formplayer-progress"), timeout=60)
            self.wait_for_ajax_and_progress()
        else:
            logger.info("No progress detected — continuing.")

    def wait_for_ajax_and_progress(self, timeout=10):
        try:
            self.wait_until(lambda d: d.execute_script("return window.jQuery ? jQuery.active == 0 : true"), timeout)
            if self.driver.find_elements(By.ID, "formplayer-progress-container"):
                self.wait_until(lambda d: d.execute_script(
                    """
                    const el = document.querySelector('#formplayer-progress-container');
                    return el && el.children.length === 0;
                    """), timeout)
        except Exception as e:
            logger.warning(f"Exception while waiting for AJAX/progress: {e}")

    def wait_until_progress_removed(self, timeout=60):
        try:
            if self.driver.find_elements(By.ID, "formplayer-progress"):
                self.wait_until(lambda d: not d.find_elements(By.ID, "formplayer-progress"), timeout)
        except Exception as e:
            logger.warning(f"Exception while waiting for progress to disappear: {e}")

    def scroll_to_element(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def js_click(self, locator, timeout=10):
        try:
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            logger.warning(f"JS click failed: {e}, retrying...")
            element = self.wait_until(ec.element_to_be_clickable(locator), timeout)
            self.driver.execute_script("arguments[0].click();", element)

    def js_send_keys(self, locator, value, timeout=10):
        element = self.wait_until(ec.element_to_be_clickable(locator), timeout)
        self.driver.execute_script("arguments[0].value='" + value + "';", element)
        self.wait_after_interaction()

    def reload_page(self):
        self.driver.refresh()

    def back(self):
        try:
            self.driver.back()
        except WebDriverException as e:
            logger.warning(f"driver.back() failed: {e}, trying JS fallback")
            self.driver.execute_script("window.history.back();")
    def is_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def is_selected(self, locator):
        try:
            return self.driver.find_element(*locator).is_selected()
        except (NoSuchElementException, TimeoutException):
            return False

    def is_enabled(self, locator):
        try:
            return self.driver.find_element(*locator).is_enabled()
        except (NoSuchElementException, TimeoutException):
            return False

    def clear(self, locator):
        try:
            self.driver.find_element(*locator).clear()
        except Exception as e:
            logger.warning(f"[clear] Failed to clear {locator}: {e}")

    def get_text(self, locator):
        try:
            element_text = self.driver.find_element(*locator).text
            logger.info(f"[get_text] Found text: {element_text}")
            return element_text
        except Exception as e:
            logger.error(f"[get_text] Failed to get text from {locator}: {e}")
            raise

    def get_attribute(self, locator, attribute):
        try:
            attr = self.driver.find_element(*locator).get_attribute(attribute)
            logger.info(f"[get_attribute] {attribute}={attr}")
            return attr
        except Exception as e:
            logger.error(f"[get_attribute] Failed for {locator}: {e}")
            raise

    def find_element(self, locator):
        try:
            return self.driver.find_element(*locator)
        except NoSuchElementException:
            logger.warning(f"[find_element] Element not found: {locator}")
            return None

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def find_elements_texts(self, locator):
        return [el.text for el in self.driver.find_elements(*locator)]

    def select_by_text(self, locator, text):
        try:
            select = Select(self.driver.find_element(*locator))
            select.select_by_visible_text(text)
            logger.info(f"[select_by_text] Selected '{text}'")
        except Exception as e:
            logger.error(f"[select_by_text] Failed to select '{text}' from {locator}: {e}")
            raise

    def select_by_value(self, locator, value):
        try:
            select = Select(self.driver.find_element(*locator))
            select.select_by_value(value)
            logger.info(f"[select_by_value] Selected value '{value}'")
        except Exception as e:
            logger.error(f"[select_by_value] Failed to select value '{value}' from {locator}: {e}")
            raise

    def select_by_index(self, locator, index):
        try:
            select = Select(self.driver.find_element(*locator))
            select.select_by_index(index)
            logger.info(f"[select_by_index] Selected index '{index}'")
        except Exception as e:
            logger.error(f"[select_by_index] Failed to select index '{index}' from {locator}: {e}")
            raise

    def get_selected_text(self, locator):
        try:
            select = Select(self.driver.find_element(*locator))
            selected_text = select.first_selected_option.text
            logger.info(f"[get_selected_text] Selected option: {selected_text}")
            return selected_text
        except Exception as e:
            logger.error(f"[get_selected_text] Failed to get selected option from {locator}: {e}")
            raise

    def deselect_all(self, locator):
        try:
            select = Select(self.driver.find_element(*locator))
            select.deselect_all()
            logger.info(f"[deselect_all] Deselected all options for {locator}")
        except Exception as e:
            logger.error(f"[deselect_all] Failed to deselect all from {locator}: {e}")
            raise

    def switch_to_next_tab(self):
        try:
            win_handles = self.driver.window_handles
            self.driver.switch_to.window(win_handles[1])
            logger.info(f"[switch_to_next_tab] Switched to: {self.driver.title}")
        except Exception as e:
            logger.error(f"[switch_to_next_tab] Failed: {e}")
            raise

    def switch_back_to_prev_tab(self):
        try:
            win_handles = self.driver.window_handles
            self.driver.switch_to.window(win_handles[0])
            logger.info(f"[switch_back_to_prev_tab] Switched to: {self.driver.title}")
        except Exception as e:
            logger.error(f"[switch_back_to_prev_tab] Failed: {e}")
            raise

    def switch_to_new_tab(self):
        try:
            self.driver.switch_to.new_window('tab')
            logger.info("[switch_to_new_tab] New tab opened")
        except Exception as e:
            logger.error(f"[switch_to_new_tab] Failed: {e}")
            raise

    def switch_to_default_content(self):
        try:
            self.driver.switch_to.default_content()
            logger.info("[switch_to_default_content] Switched to default content")
        except Exception as e:
            logger.error(f"[switch_to_default_content] Failed: {e}")
            raise

    def switch_to_frame(self, frame_locator):
        try:
            frame = self.driver.find_element(*frame_locator)
            self.driver.switch_to.frame(frame)
            logger.info("[switch_to_frame] Switched to frame")
        except Exception as e:
            logger.error(f"[switch_to_frame] Failed: {e}")
            raise

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
        logger.info("[scroll_to_top] Scrolled to top")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        logger.info("[scroll_to_bottom] Scrolled to bottom")

    def hover_on_element(self, locator):
        try:
            element = self.wait_until(ec.visibility_of_element_located(locator), timeout=10)
            ActionChains(self.driver).move_to_element(element).pause(2).perform()
            logger.info("[hover_on_element] Hovered over element")
        except Exception as e:
            logger.error(f"[hover_on_element] Failed: {e}")
            raise

    def hover_and_click(self, locator1, locator2):
        try:
            action = ActionChains(self.driver)
            el1 = self.wait_until(ec.visibility_of_element_located(locator1), timeout=5)
            el2 = self.wait_until(ec.visibility_of_element_located(locator2), timeout=5)
            action.move_to_element(el1).move_to_element(el2).click().perform()
            logger.info("[hover_and_click] Performed hover and click")
        except Exception as e:
            logger.error(f"[hover_and_click] Failed: {e}")
            raise

    def accept_pop_up(self):
        try:
            WebDriverWait(self.driver, 3, poll_frequency=0.5).until(ec.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            logger.info("[accept_pop_up] Alert accepted")
        except TimeoutException:
            logger.info("[accept_pop_up] No alert found")

    def assert_downloaded_file(self, file_path, file_name):
        try:
            mod_time = file_path.stat().st_mtime
            file_time = datetime.datetime.fromtimestamp(mod_time)
            now = datetime.datetime.now()
            age = (now - file_time).total_seconds()
            assert file_name in file_path.name and age < 600, f"[assert_downloaded_file] Invalid or old file: {file_path.name}"
            logger.info(f"[assert_downloaded_file] Verified file: {file_path.name}")
        except Exception as e:
            logger.error(f"[assert_downloaded_file] Assertion failed: {e}")
            raise

    def page_source_contains(self, text):
        assert text in self.driver.page_source, f"[page_source_contains] Text '{text}' not in page source"
        logger.info(f"[page_source_contains] Verified text in page source: {text}")

    def get_url(self, link):
        self.driver.get(link)
        time.sleep(2)