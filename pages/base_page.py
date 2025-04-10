from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element(self, by, locator, timeout=None):
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            print(f"❌ ERROR: Element not found: {locator}")
            return False

    def wait_for_element_to_be_clickable(self, by, locator, timeout=None):
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.element_to_be_clickable((by, locator)))
        except TimeoutException:
            print(f"❌ ERROR: Element not clickable: {locator}")
            return False

    def click_element(self, by, locator):
        element = self.wait_for_element_to_be_clickable(by, locator)
        if element:
            try:
                element.click()
                print(f"✅ Click successful: {locator}")
            except Exception:
                print(f"⚠️ Selenium click failed, using JavaScript click: {locator}")
                self.driver.execute_script("arguments[0].click();", element)
        else:
            print(f"⚠️ WARNING: Could not click element: {locator}")

    def scroll_to_element(self, by, locator):
        element = self.wait_for_element(by, locator)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            print(f"🔽 Scrolled to element: {locator}")
        else:
            print(f"⚠️ WARNING: Element not found for scrolling: {locator}")

    def get_element_text(self, by, locator):
        element = self.wait_for_element(by, locator)
        if element:
            return element.text.strip()
        return ""

    def find_element(self, by, locator):
        try:
            return self.driver.find_element(by, locator)
        except NoSuchElementException:
            print(f"❌ ERROR: Element not found via find_element: {locator}")
            return False

    def find_elements(self, by, locator):
        try:
            return self.driver.find_elements(by, locator)
        except NoSuchElementException:
            print(f"❌ ERROR: Elements not found via find_elements: {locator}")
            return []

    def execute_js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    def click_with_fallback(self, by, locator):
        element = self.wait_for_element_to_be_clickable(by, locator)
        if element:
            try:
                element.click()
            except Exception:
                print(f"⚠️ Regular click failed for {locator}, using JS fallback")
                self.execute_js_click(element)

    def wait_for_page_to_load(self):
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            print("✅ Page fully loaded.")
        except TimeoutException:
            print("⚠️ Page load timeout.")

    def wait_for_element_text_to_be(self, by, locator, expected_text, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((by, locator), expected_text)
            )
            print(f"✅ Element text is '{expected_text}'")
            return True
        except TimeoutException:
            actual_text = self.get_element_text(by, locator)
            print(f"❌ ERROR: Expected text '{expected_text}', but found '{actual_text}'")
            return False
