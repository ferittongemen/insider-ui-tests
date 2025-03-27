from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    def __init__(self, driver, timeout=15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_element(self, by, locator, timeout=None):
        """Belirtilen elementin varlığını bekler ve döndürür."""
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            print(f"❌ HATA: {locator} elementi bulunamadı.")
            return None

    def wait_for_element_to_be_clickable(self, by, locator, timeout=None):
        """Belirtilen elementin tıklanabilir olmasını bekler ve döndürür."""
        try:
            wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
            return wait.until(EC.element_to_be_clickable((by, locator)))
        except TimeoutException:
            print(f"❌ HATA: {locator} elementi tıklanabilir değil.")
            return None

    def click_element(self, by, locator):
        """Elementin tıklanmasını bekler ve tıklar."""
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
        """Elemente kaydırma yapar."""
        element = self.wait_for_element(by, locator)
        if element:
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            print(f"🔽 Sayfa kaydırıldı: {locator}")
        else:
            print(f"⚠️ Uyarı: {locator} kaydırılamadı, element bulunamadı.")

    def accept_cookies(self, cookie_xpath):
        """Çerezleri kabul etme butonu tıklanabilir ise kabul eder."""
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
        """Sayfanın tamamen yüklenmesini bekler."""
        try:
            self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
            print("✅ Sayfa tamamen yüklendi.")
        except TimeoutException:
            print("⚠️ Sayfa yüklenme süresi aşıldı.")

    def get_element_text(self, by, locator):
        """Elementin metnini döndürür."""
        element = self.wait_for_element(by, locator)
        if element:
            return element.text.strip()
        return ""

    def wait_for_element_text_to_be(self, by, locator, expected_text, timeout=10):
        """
        Elementin text'inin belirli bir değere eşit olmasını bekler.
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