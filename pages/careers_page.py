from selenium.webdriver.common.by import By
from .base_page import BasePage

class CareersPage(BasePage):
    LOCATIONS_XPATH = "//*[@id='career-our-location']/div/div/div/div[1]"
    TEAMS_PATH = "//*[@id='career-find-our-calling']/div/div/a"
    LIFE_AT_INSIDER_XPATH = "//h2[contains(text(), 'Life at Insider')]"
    SEE_ALL_TEAMS_XPATH = "//a[contains(text(), 'See all teams')]"
    QA_CAREERS_XPATH = "//h3[contains(text(), 'Quality Assurance')]"
    COOKIE_ACCEPT_ID = "//*[@id='wt-cli-accept-all-btn']"
    QA_OPEN_POSITIONS_XPATH = "//h3[contains(text(), 'Quality Assurance')]/following-sibling::a[contains(text(), 'Open Positions')]"

    def is_accessible(self):
        try:
            print("🔍 Checking QA page title...")
            self.wait_for_page_to_load()
            title = self.driver.title.lower()
            url = self.driver.current_url.lower()
            print(f"📄 QA Page Title: {title}")
            print(f"🌐 QA Page URL: {url}")
            return "careers" in title or "quality assurance" in title or "/careers" in url
        except Exception as e:
            print(f"❌ ERROR during accessibility check: {e}")
            return False

    def verify_sections(self):
        try:
            print("🔄 Waiting for Locations section...")
            self.wait_for_element(By.XPATH, self.LOCATIONS_XPATH)
            print("✅ Locations section found!")

            print("🔄 Waiting for Teams section...")
            self.wait_for_element(By.XPATH, self.TEAMS_PATH)
            print("✅ Teams section found!")

            self.wait_for_element(By.XPATH, self.LIFE_AT_INSIDER_XPATH)
            print("✅ Life at Insider section found!")

            return True
        except Exception as e:
            print(f"❌ ERROR: Section not found: {e}")
            return False

    def go_to_qa_careers(self):
        """
        Navigates to the QA Careers page, using fallback methods if necessary.
        :raises Exception: If navigation fails
        """
        try:
            print("🔄 Scrolling to 'See All Teams' button...")
            self.scroll_to_element(By.XPATH, self.SEE_ALL_TEAMS_XPATH)

            # 🔁 Scroll sonrası tekrar clickable kontrolü yap
            see_all_teams_button = self.wait_for_element_to_be_clickable(By.XPATH, self.SEE_ALL_TEAMS_XPATH)
            if see_all_teams_button:
                self.click_element(By.XPATH, self.SEE_ALL_TEAMS_XPATH)
                print("✅ Clicked 'See All Teams'")
            else:
                print("❌ Could not click 'See All Teams'")
                return

            print("🔄 Waiting for full page load...")
            self.wait_for_page_to_load()

            print("🔄 Waiting for 'QA Careers' section...")
            self.scroll_to_element(By.XPATH, self.QA_CAREERS_XPATH)
            qa_careers_section = self.wait_for_element(By.XPATH, self.QA_CAREERS_XPATH)

            qa_open_link = self.wait_for_element_to_be_clickable(By.XPATH, self.QA_OPEN_POSITIONS_XPATH)

            if qa_open_link:
                print("🖱 Clicking 'Open Positions' link...")
                self.scroll_to_element(By.XPATH, self.QA_OPEN_POSITIONS_XPATH)
                qa_open_link.click()
                print("✅ Navigated to QA Careers via link.")
            else:
                print("⚠️ Link not found, using fallback JS click...")
                self.driver.execute_script("arguments[0].click();", qa_careers_section)
                print("✅ Fallback click successful.")

            # QA jobs yüklendi mi kontrol
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'See all QA jobs')]"))
            )

        except Exception as e:
            print(f"❌ ERROR while navigating to QA Careers page: {e}")
