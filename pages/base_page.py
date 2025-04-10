from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """
    Initialize BasePage with driver and default timeout.
    :param driver: Selenium WebDriver instance
    :param int timeout: Maximum wait time for element actions

    """

    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element(self, by, locator, timeout=None):
        """
         Waits until the presence of an element is located.
         :param by: Selenium By strategy (e.g., By.ID, By.XPATH)
         :param locator: The locator string to find the element
         :param int timeout: Optional timeout override
         :return: WebElement or None
         :rtype: WebElement

         """
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            print(f"❌ ERROR: Element not found: {locator}")
            return False

    def wait_for_element_to_be_clickable(self, by, locator, timeout=None):
        """
        Waits until the element is clickable.
        :param by: Selenium By strategy
        :param locator: The locator string
        :param int timeout: Optional timeout override
        :return: WebElement or None
        :rtype: WebElement

        """
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.element_to_be_clickable((by, locator)))
        except TimeoutException:
            print(f"❌ ERROR: Element not clickable: {locator}")
            return False

    def click_element(self, by, locator):
        """
        Waits for the element to be clickable and clicks it. Falls back to JS click.
        :param by: Selenium By strategy
        :param locator: The locator string

        """
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
        """
        Scrolls to the specified element on the page.
        :param by: Selenium By strategy
        :param locator: The locator string

        """
        element = self.wait_for_element(by, locator)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            print(f"🔽 Scrolled to element: {locator}")
        else:
            print(f"⚠️ WARNING: Element not found for scrolling: {locator}")

    def get_element_text(self, by, locator):
        """
        Retrieves the text of the specified element.
        :param by: Selenium By strategy
        :param locator: The locator string
        :return: Cleaned string or empty string if not found

        """
        element = self.wait_for_element(by, locator)
        if element:
            return element.text.strip()
        return ""

    def find_element(self, by, locator):
        """
        Finds a single element without waiting.
        :param by: Selenium By strategy
        :param locator: The locator string
        :return: WebElement or False

        """
        try:
            return self.driver.find_element(by, locator)
        except NoSuchElementException:
            print(f"❌ ERROR: Element not found via find_element: {locator}")
            return False

    def find_elements(self, by, locator):
        """
        Finds multiple elements without waiting.
        :param by: Selenium By strategy
        :param locator: The locator string
        :return: List of WebElements or empty list

        """
        try:
            return self.driver.find_elements(by, locator)
        except NoSuchElementException:
            print(f"❌ ERROR: Elements not found via find_elements: {locator}")
            return []

    def execute_js_click(self, element):
        """
        Performs JavaScript-based click on a given element.
        :param element: WebElement to click

        """
        self.driver.execute_script("arguments[0].click();", element)

    def click_with_fallback(self, by, locator):
        """
        Clicks an element using standard click. If it fails, uses JavaScript as fallback.
        :param by: Selenium By strategy
        :param locator: The locator string

        """
        element = self.wait_for_element_to_be_clickable(by, locator)
        if element:
            try:
                element.click()
            except Exception:
                print(f"⚠️ Regular click failed for {locator}, using JS fallback")
                self.execute_js_click(element)

    def wait_for_page_to_load(self):
        """
        Waits until the page is fully loaded (document.readyState = complete).

        """
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            print("✅ Page fully loaded.")
        except TimeoutException:
            print("⚠️ Page load timeout.")

    def wait_for_element_text_to_be(self, by, locator, expected_text, timeout=10):
        """
        Waits until the specified element contains the expected text.
        :param by: Selenium By strategy
        :param locator: The locator string
        :param expected_text: Text to match
        :param timeout: Max wait time
        :return: True if matched, else False

        """
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
