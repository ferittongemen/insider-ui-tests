from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    def __init__(self, driver):
        """
        HomePage constructor.

        :param driver: Selenium WebDriver instance

        """
        super().__init__(driver)
        self.url = "https://useinsider.com"
        self.company_menu_xpath = "(//*[@id='navbarDropdownMenuLink'])[5]"
        self.careers_link_xpath = "//*[@id='navbarNavDropdown']/ul[1]/li[6]/div/div[2]/a[2]"
        self.cookie_button_xpath = "//*[@id='wt-cli-accept-all-btn']"

    def open(self):
        """
        Opens the Insider homepage.

        """
        self.driver.get(self.url)

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
        super().accept_cookies(self.cookie_button_xpath)

    def navigate_to_careers(self):
        """
        Navigates to the Careers page through the Company menu.

        """
        self.click_element(By.XPATH, self.company_menu_xpath)
        self.click_element(By.XPATH, self.careers_link_xpath)