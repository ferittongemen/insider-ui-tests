import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .base_page import BasePage

class CareersPage(BasePage):
    def __init__(self, driver):
        """
        CareersPage constructor.

        :param driver: Selenium WebDriver instance

        """
        super().__init__(driver)
        self.LOCATIONS_XPATH = "//*[@id='career-our-location']/div/div/div/div[1]"
        self.TEAMS_PATH = "//*[@id='career-find-our-calling']/div/div/a"
        self.life_at_insider_xpath = "//h2[contains(text(), 'Life at Insider')]"
        self.see_all_teams_xpath = "//a[contains(text(), 'See all teams')]"
        self.qa_careers_xpath = "//h3[contains(text(), 'Quality Assurance')]"
        self.cookie_accept_id = "//*[@id='wt-cli-accept-all-btn']"
        self.qa_open_positions_xpath = "//h3[contains(text(), 'Quality Assurance')]/following-sibling::a[contains(text(), 'Open Positions')]"

    def is_accessible(self):
        """
        Verifies if the Careers page is accessible.

        :return: True if title or URL contains career-related keywords, else False
        :rtype: bool

        """
        try:
            print("🔍 QA sayfasının başlığı kontrol ediliyor...")
            self.wait_for_page_to_load()
            title = self.driver.title.lower()
            url = self.driver.current_url.lower()
            print(f"📄 QA Sayfa Başlığı: {title}")
            print(f"🌐 QA Sayfa URL: {url}")
            return "careers" in title or "quality assurance" in title or "/careers" in url
        except Exception as e:
            print(f"❌ QA sayfası erişim kontrolü sırasında hata: {e}")
            return False

    def verify_sections(self):
        """
        Verifies the presence of key sections: Locations, Teams, and Life at Insider.

        :return: True if all sections are found, else False
        :rtype: bool

        """
        try:
            print("🔄 Bekleniyor: Locations bölümü...")
            self.wait_for_element(By.XPATH, self.LOCATIONS_XPATH)
            print("✅ Locations bölümü bulundu!")

            print("🔄 Bekleniyor: Teams bölümü...")
            self.wait_for_element(By.XPATH, self.TEAMS_PATH)
            print("✅ Teams bölümü bulundu!")

            self.wait_for_element(By.XPATH, self.life_at_insider_xpath)
            print("✅ Life at Insider bölümü bulundu!")

            return True
        except Exception as e:
            print(f"❌ HATA: Element bulunamadı: {e}")
            return False

    def go_to_qa_careers(self):
        """
        Navigates to the QA Careers page, using fallback methods if necessary.

        :raises Exception: If navigation fails
        
        """
        try:
            print("🔄 'See All Teams' butonu bekleniyor ve kaydırılıyor...")
            see_all_teams_button = self.wait_for_element_to_be_clickable(By.XPATH, self.see_all_teams_xpath)

            self.scroll_to_element(By.XPATH, self.see_all_teams_xpath)
            time.sleep(1)
            self.scroll_to_element(By.XPATH, self.see_all_teams_xpath)
            time.sleep(1)

            see_all_teams_button.click()
            print("✅ 'See All Teams' butonuna tıklandı.")

            print("🔄 Sayfanın tamamen yüklenmesi bekleniyor...")
            self.wait_for_page_to_load()
            time.sleep(2)

            print("🔄 'QA Careers' butonu bekleniyor...")
            self.scroll_to_element(By.XPATH, self.qa_careers_xpath)
            time.sleep(1)

            qa_careers_section = self.wait_for_element(By.XPATH, self.qa_careers_xpath)

            qa_open_link = self.wait_for_element_to_be_clickable(By.XPATH, self.qa_open_positions_xpath)

            if qa_open_link:
                print("🖱 'Open Positions' linkine tıklanıyor (workaround)...")
                self.scroll_to_element(By.XPATH, self.qa_open_positions_xpath)
                time.sleep(1)
                qa_open_link.click()
                print("✅ 'QA Careers' sayfasına geçildi (link ile).")
            else:
                print("⚠️ Link bulunamadı, JavaScript ile başlığa tıklanıyor...")
                self.driver.execute_script("arguments[0].click();", qa_careers_section)
                print("✅ 'QA Careers' butonuna tıklandı (fallback).")

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'See all QA jobs')]"))
            )
        except Exception as e:
            print(f"❌ HATA: 'QA Careers' sayfasına geçerken hata oluştu: {e}")
