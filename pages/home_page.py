from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    URL = "https://useinsider.com"
    COMPANY_MENU_XPATH = "(//*[@id='navbarDropdownMenuLink'])[5]"
    CAREERS_LINK_XPATH = "//*[@id='navbarNavDropdown']/ul[1]/li[6]/div/div[2]/a[2]"
    COOKIE_BUTTON_XPATH = "//*[@id='wt-cli-accept-all-btn']"

    def open(self):
        """
        Opens the Insider homepage.

        """
        self.driver.get(self.URL)

    def is_accessible(self):
        """
        Checks whether the homepage is accessible by verifying the title.
        :return: True if title contains 'Insider', else False
        :rtype: bool

        """
        return "Insider" in self.driver.title

    def accept_cookies(self):
        """
        Accepts cookies using BasePage method.

        """
        try:
            cookie_button = self.wait_for_element_to_be_clickable(By.XPATH, self.COOKIE_BUTTON_XPATH)
            if cookie_button:
                cookie_button.click()
                print("✅ Cookies accepted.")
            else:
                print("⚠️ Cookie button not found or already accepted.")
        except NoSuchElementException:
            print("⚠️ Cookie button not visible, skipping.")

    def navigate_to_careers(self):
        """
        Navigates to the Careers page through the Company menu.

        """
        self.click_element(By.XPATH, self.COMPANY_MENU_XPATH)
        self.click_element(By.XPATH, self.CAREERS_LINK_XPATH)
