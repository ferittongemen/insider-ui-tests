from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class QACareersPage(BasePage):
    DEPARTMENT_CONTAINER_ID = "select2-filter-by-department-container"
    LOCATION_CONTAINER_ID = "select2-filter-by-location-container"
    LOCATION_ISTANBUL_XPATH = "//li[contains(@class, 'select2-results__option') and normalize-space(text())='Istanbul, Turkiye']"
    LOCATION_DROPDOWN_XPATH = "//select[@id='location']"
    DEPARTMENT_DROPDOWN_XPATH = "//select[@id='department']"
    VIEW_ROLE_BUTTON_XPATH = "//a[contains(text(), 'View Role')]"
    SEE_ALL_QA_JOBS_XPATH = "//a[contains(text(), 'See all QA jobs')]"
    JOB_CARD_XPATH = "//div[contains(@class, 'position-list-item')]"
    JOB_LIST_XPATH = "//div[@id='jobs-list']//div[contains(@class, 'position-list-item')]"

    def is_accessible(self):
        try:
            print("🔍 Checking QA careers page accessibility...")
            self.wait_for_page_to_load()
            self.wait_for_element(By.XPATH, self.VIEW_ROLE_BUTTON_XPATH)
            current_url = self.driver.current_url
            print("🌐 QA Page URL:", current_url)
            return "quality-assurance" in current_url or "qa" in current_url
        except Exception as e:
            print(f"❌ ERROR while checking accessibility: {e}")
            return False

    def filter_jobs(self, location, department):
        location_dropdown = self.wait_for_element_to_be_clickable(By.XPATH, self.LOCATION_DROPDOWN_XPATH)
        if location_dropdown:
            location_dropdown.send_keys(location)

        department_dropdown = self.wait_for_element_to_be_clickable(By.XPATH, self.DEPARTMENT_DROPDOWN_XPATH)
        if department_dropdown:
            department_dropdown.send_keys(department)

    def select_location_if_department_is_qa(self):
        print("⏳ Waiting for department to be 'Quality Assurance'...")

        for attempt in range(3):
            self.scroll_to_element(By.ID, self.DEPARTMENT_CONTAINER_ID)
            success = self.wait_for_element_text_to_be(By.ID, self.DEPARTMENT_CONTAINER_ID, "Quality Assurance", timeout=5)

            if success:
                print("✅ Department is correct, selecting location...")
                self.wait_for_job_cards_to_be_replaced()
                self.click_element(By.ID, self.LOCATION_CONTAINER_ID)
                print("⏳ Waiting for 'Istanbul, Turkiye' option...")
                self.click_element(By.XPATH, self.LOCATION_ISTANBUL_XPATH)
                print("✅ 'Istanbul, Turkiye' selected.")
                print("⏳ Waiting for job listings to load...")
                self.wait_for_element(By.XPATH, self.JOB_CARD_XPATH)
                return
            else:
                print(f"⚠️ Attempt {attempt + 1}: 'Quality Assurance' not visible yet. Retrying...")

        print("❌ ERROR: Failed to set department to 'Quality Assurance'.")

    def wait_for_job_cards_to_load(self, timeout=15):
        print("⏳ Waiting for job cards to load...")
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, self.JOB_LIST_XPATH))
        )
        print("✅ Job cards loaded.")

    def wait_for_job_cards_to_be_replaced(self):
        try:
            print("⏳ Waiting for old job cards to disappear...")
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, self.JOB_CARD_XPATH)))
            print("✅ Old job cards disappeared.")
        except:
            print("⚠️ Old job cards may still be visible. Continuing anyway...")

        self.wait.until(lambda d: len(d.find_elements(By.XPATH, self.JOB_CARD_XPATH)) > 0)
        print("✅ New job cards loaded in the DOM.")

    def verify_job_listings(self):
        print("🧪 Verifying that job listings match QA + Istanbul criteria using JS...")

        job_texts = self.driver.execute_script("""
            return Array.from(document.querySelectorAll(".position-list-item")).map(el => el.innerText);
        """)

        valid_jobs = 0
        for i, text in enumerate(job_texts, 1):
            print(f"📋 JS Job {i}:{text}\n")
            lower_text = text.lower()
            if "quality assurance" in lower_text and "istanbul" in lower_text:
                print(f"✅ Job {i} VALID: QA + Istanbul")
                valid_jobs += 1
            else:
                print(f"⚠️ Job {i} INVALID")

        print(f"🎯 Total valid jobs: {valid_jobs}")
        return valid_jobs > 0

    def verify_view_role_redirects(self):
        print("🔍 Looking for 'View Role' button...")
        try:
            self.wait_for_element(By.XPATH, self.JOB_CARD_XPATH, timeout=15)
            print("✅ Job cards loaded.")

            for attempt in range(3):
                view_role_buttons = self.find_elements(By.XPATH, self.VIEW_ROLE_BUTTON_XPATH)
                if view_role_buttons:
                    view_role_button = view_role_buttons[0]
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_role_button)
                    time.sleep(0.5)

                    self.click_with_fallback(By.XPATH, self.VIEW_ROLE_BUTTON_XPATH)
                    break
                else:
                    print("❌ 'View Role' button not found.")
                    return False

            windows = self.driver.window_handles
            if len(windows) > 1:
                self.driver.switch_to.window(windows[1])
                print("🔄 Switched to new tab:", self.driver.current_url)

            self.wait_for_page_to_load()
            return "lever.co" in self.driver.current_url

        except Exception as e:
            print(f"❌ ERROR: View Role redirection failed: {e}")
            return False

    def click_see_all_qa_jobs(self):
        print("🔍 Waiting for 'See all QA jobs' button...")
        button = self.wait_for_element_to_be_clickable(By.XPATH, self.SEE_ALL_QA_JOBS_XPATH)
        if button:
            self.scroll_to_element(By.XPATH, self.SEE_ALL_QA_JOBS_XPATH)
            button.click()
            print("✅ Clicked 'See all QA jobs' button.")
        else:
            print("❌ ERROR: 'See all QA jobs' button not found.")
