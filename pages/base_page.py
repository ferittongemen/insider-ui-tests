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
            print(f"❌ HATA: {locator} elementi bulunamadı.")
            return None

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
            print(f"❌ HATA: {locator} elementi tıklanabilir değil.")
            return None

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
                print(f"✅ Tıklama başarılı: {locator}")
            except Exception:
                print(f"⚠️ Selenium tıklayamadı, JavaScript ile tıklanıyor: {locator}")
                self.driver.execute_script("arguments[0].click();", element)
        else:
            print(f"⚠️ Uyarı: {locator} elementi tıklanamadı.")

    def scroll_to_element(self, by, locator):
        """
        Scrolls to the specified element on the page.

        :param by: Selenium By strategy
        :param locator: The locator string

        """
        element = self.wait_for_element(by, locator)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            print(f"🔽 Sayfa kaydırıldı: {locator}")
        else:
            print(f"⚠️ Uyarı: {locator} kaydırılamadı, element bulunamadı.")

    def accept_cookies(self, cookie_xpath):
        """
        Clicks the cookie accept button if it's visible and clickable.

        :param cookie_xpath: XPath locator for the cookie accept button

        """
        try:
            print("🔄 Çerezleri kabul etme butonu aranıyor...")
            cookie_button = self.wait_for_element_to_be_clickable(By.XPATH, cookie_xpath)
            if cookie_button:
                cookie_button.click()
                print("✅ Çerezler kabul edildi!")
            else:
                print("⚠️ Çerez kabul butonu bulunamadı, zaten kabul edilmiş olabilir.")
        except NoSuchElementException:
            print("⚠️ Çerez butonu görünmüyor, atlanıyor.")

    def wait_for_page_to_load(self):
        """
        Waits until the page's document.readyState is 'complete'.

        """
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            print("✅ Sayfa tamamen yüklendi.")
        except TimeoutException:
            print("⚠️ Sayfa yüklenme süresi aşıldı.")

    def get_element_text(self, by, locator):
        """
        Returns the trimmed text content of the specified element.

        :param by: Selenium By strategy
        :param locator: The locator string
        :return: Text of the element or empty string
        :rtype: str

        """
        element = self.wait_for_element(by, locator)
        if element:
            return element.text.strip()
        return ""

    def wait_for_element_text_to_be(self, by, locator, expected_text, timeout=10):
        """
        Waits until the element's text matches the expected value.

        :param by: Selenium By strategy
        :param locator: The locator string
        :param expected_text: Text expected to be present
        :param int timeout: Maximum wait time
        :return: True if match, else False
        :rtype: bool
        
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element((by, locator), expected_text)
            )
            print(f"✅ Elementin text'i '{expected_text}' olarak ayarlandı.")
            return True
        except TimeoutException:
            actual_text = self.get_element_text(by, locator)
            print(f"❌ HATA: Elementin text'i '{expected_text}' olmadı. Son durum: '{actual_text}'")
            return False
