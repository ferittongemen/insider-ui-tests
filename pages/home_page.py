from selenium.webdriver.common.by import By
from .base_page import BasePage

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://useinsider.com"
        self.company_menu_xpath = "(//*[@id='navbarDropdownMenuLink'])[5]"
        self.careers_link_xpath = "//*[@id='navbarNavDropdown']/ul[1]/li[6]/div/div[2]/a[2]"
        self.cookie_button_xpath = "//*[@id='wt-cli-accept-all-btn']"

    def open(self):
        self.driver.get(self.url)

    def is_accessible(self):
        return "Insider" in self.driver.title

    def accept_cookies(self):
        """BasePage metodunu kullanarak çerezleri kabul et"""
        super().accept_cookies(self.cookie_button_xpath)

    def navigate_to_careers(self):
        """Kariyer sayfasına git"""
        self.click_element(By.XPATH, self.company_menu_xpath)
        self.click_element(By.XPATH, self.careers_link_xpath)