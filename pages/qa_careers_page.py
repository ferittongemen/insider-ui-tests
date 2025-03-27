import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class QACareersPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.department_container_id = "select2-filter-by-department-container"
        self.location_container_id = "select2-filter-by-location-container"
        self.location_istanbul_xpath = "//li[contains(@class, 'select2-results__option') and normalize-space(text())='Istanbul, Turkiye']"
        self.location_dropdown_xpath = "//select[@id='location']"
        self.department_dropdown_xpath = "//select[@id='department']"
        self.view_role_button_xpath = "//a[contains(text(), 'View Role')]"
        self.see_all_qa_jobs_xpath = "//a[contains(text(), 'See all QA jobs')]"
        self.job_card_xpath = "//div[contains(@class, 'position-list-item')]"
        self.job_list_xpath = "//div[@id='jobs-list']//div[contains(@class, 'position-list-item')]"

    def is_accessible(self):
        try:
            print("🔍 QA sayfasının başlığı kontrol ediliyor...")
            self.wait_for_page_to_load()
            self.wait_for_element(By.XPATH, self.view_role_button_xpath)
            current_url = self.driver.current_url
            print("🌐 QA Sayfa URL:", current_url)
            return "quality-assurance" in current_url or "qa" in current_url
        except Exception as e:
            print(f"❌ QA sayfası erişim kontrolü sırasında hata: {e}")
            return False

    def filter_jobs(self, location, department):
        location_dropdown = self.wait_for_element_to_be_clickable(By.XPATH, self.location_dropdown_xpath)
        if location_dropdown:
            location_dropdown.send_keys(location)

        department_dropdown = self.wait_for_element_to_be_clickable(By.XPATH, self.department_dropdown_xpath)
        if department_dropdown:
            department_dropdown.send_keys(department)

    def select_location_if_department_is_qa(self):
        print("⏳ Department filtresinin 'Quality Assurance' olmasını bekliyoruz...")

        for attempt in range(3):
            self.scroll_to_element(By.ID, self.department_container_id)
            success = self.wait_for_element_text_to_be(By.ID, self.department_container_id, "Quality Assurance", timeout=5)

            if success:
                print("✅ Department doğru, lokasyon dropdown'a tıklanıyor...")
                self.wait_for_job_cards_to_be_replaced()
                self.click_element(By.ID, self.location_container_id)
                print("⏳ 'Istanbul, Turkiye' seçeneği yükleniyor...")
                self.click_element(By.XPATH, self.location_istanbul_xpath)
                print("✅ 'Istanbul, Turkiye' seçeneği seçildi.")
                print("⏳ Job-listing’lerin yüklenmesi bekleniyor...")
                self.wait_for_element(By.XPATH, self.job_card_xpath)
                return
            else:
                print(f"⚠️ {attempt + 1}. denemede 'Quality Assurance' değeri gelmedi. Tekrar denenecek...")
                time.sleep(2)

        print("❌ HATA: Department değeri 'Quality Assurance' olarak ayarlanamadı.")

    def wait_for_job_cards_to_load(self, timeout=15):
        print("⏳ Job kartlarının yüklenmesi bekleniyor...")
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, self.job_list_xpath))
        )
        print("✅ Job kartları yüklendi.")

    def wait_for_job_cards_to_be_replaced(self):
        try:
            print("⏳ Eski job kartlarının görünmez olmasını bekliyoruz...")
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, self.job_card_xpath)))
            print("✅ Eski job kartları kayboldu.")
        except:
            print("⚠️ Eski job kartları görünmeye devam ediyor olabilir. Yine de devam ediyoruz...")

        self.wait.until(lambda d: len(d.find_elements(By.XPATH, self.job_card_xpath)) > 0)
        print("✅ Yeni job kartları DOM’da yüklendi.")

    def verify_job_listings(self):
        print("🧪 Sayfada QA + Istanbul job'ları var mı JS ile kontrol ediliyor...")

        job_texts = self.driver.execute_script("""
            return Array.from(document.querySelectorAll(".position-list-item")).map(el => el.innerText);
        """)

        valid_jobs = 0
        for i, text in enumerate(job_texts, 1):
            print(f"📋 JS Job {i}:\n{text}\n")
            lower_text = text.lower()
            if "quality assurance" in lower_text and "istanbul" in lower_text:
                print(f"✅ Job {i} UYUMLU: QA + Istanbul")
                valid_jobs += 1
            else:
                print(f"⚠️ Job {i} UYUMLU DEĞİL")

        print(f"🎯 Toplam geçerli iş ilanı: {valid_jobs}")
        return valid_jobs > 0

    def verify_view_role_redirects(self):
        print("🔍 View Role butonu aranıyor...")
        try:
            self.wait_for_element(By.XPATH, self.job_card_xpath, timeout=15)
            print("✅ Pozisyon kartları yüklendi.")

            for attempt in range(3):
                try:
                    view_role_buttons = self.driver.find_elements(By.XPATH, self.view_role_button_xpath)
                    if view_role_buttons:
                        view_role_button = view_role_buttons[0]
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_role_button)
                        time.sleep(0.5)

                        try:
                            view_role_button.click()
                            print("✅ Normal tıklama başarılı.")
                        except Exception as e:
                            print(f"⚠️ Normal tıklama başarısız: {e}, JS fallback devrede.")
                            self.driver.execute_script("arguments[0].click();", view_role_button)

                        break
                    else:
                        print("❌ View Role butonu bulunamadı.")
                        return False

                except Exception as e:
                    print(f"⚠️ {attempt + 1}. denemede hata: {e}")
                    time.sleep(1)

            windows = self.driver.window_handles
            if len(windows) > 1:
                self.driver.switch_to.window(windows[1])
                print("🔄 Yeni sekmeye geçildi:", self.driver.current_url)

            self.wait_for_page_to_load()
            return "lever.co" in self.driver.current_url

        except Exception as e:
            print(f"❌ View Role genel hata: {e}")
            return False

    def click_see_all_qa_jobs(self):
        print("🔍 'See all QA jobs' butonu bekleniyor...")
        button = self.wait_for_element_to_be_clickable(By.XPATH, self.see_all_qa_jobs_xpath)
        if button:
            self.scroll_to_element(By.XPATH, self.see_all_qa_jobs_xpath)
            button.click()
            print("✅ 'See all QA jobs' butonuna tıklandı.")
        else:
            print("❌ HATA: 'See all QA jobs' butonu bulunamadı.")
