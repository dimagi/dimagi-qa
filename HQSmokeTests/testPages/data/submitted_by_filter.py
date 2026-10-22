from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By

""""Shared helpers for the Submitted By / Users (select2) filter on Manage Forms and Export pages"""


class SubmittedByFilterMixin:
    submitted_by_field = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]")
    # Exact match, so e.g. "[Deactivated Web Users]" is never picked instead of "[Active Web Users]"
    submitted_by_option_exact = "//ul[@role='listbox']/li[normalize-space(.)='{}']"
    submitted_by_chips = (By.XPATH, "(//textarea[@class='select2-search__field'])[1]/ancestor::span[contains(@class,'select2-selection--multiple')]//li[contains(@class,'select2-selection__choice')]")

    def get_selected_users(self):
        # The chip's title holds the label; its text also includes the "×" remove button
        return [(chip.get_attribute("title") or chip.text).replace("×", "").strip()
                for chip in self.find_elements(self.submitted_by_chips)]

    def select_submitted_by_option(self, label, clear_existing=True):
        """Select `label` in the filter. With clear_existing, it must end up the only selection;
        otherwise it is added to whatever is already selected."""
        selected = self.get_selected_users()
        if not clear_existing and label in selected:
            return
        for attempt in range(2):
            if clear_existing:
                self.remove_default_users()
            self.send_keys(self.submitted_by_field, label.strip("[]"))
            try:
                self.wait_to_click((By.XPATH, self.submitted_by_option_exact.format(label)), 30)
            except TimeoutException:
                print(f"Option {label} not offered on attempt {attempt + 1}")
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            selected = self.get_selected_users()
            if (selected == [label]) if clear_existing else (label in selected):
                return
            print(f"Submitted By filter is {selected} after attempt {attempt + 1}")
        assert False, f"Submitted By filter should {'be only' if clear_existing else 'include'} {label}, got {selected}"
