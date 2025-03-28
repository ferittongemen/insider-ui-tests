import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from pages.home_page import HomePage
from pages.careers_page import CareersPage
from pages.qa_careers_page import QACareersPage
from selenium.webdriver.chrome.options import Options as ChromeOptions

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    """Tarayıcı başlatma ve test sonrası kapatma"""
    if request.param == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # Manuel belirttiğin driver path
        service = ChromeService(executable_path="/Users/ferit.tongemen/Documents/Drivers/chromedriver-mac-arm64/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)

    elif request.param == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)

    driver.maximize_window()
    yield driver
    driver.quit()

def test_insider_career_page(driver):
    """Insider kariyer sayfası test akışı"""

    print("🚀 Test başlıyor: Insider anasayfası açılıyor...")
    home_page = HomePage(driver)
    home_page.open()
    assert home_page.is_accessible(), "❌ Hata: Insider anasayfası erişilemez!"

    print("✅ Çerezler kabul ediliyor...")
    home_page.accept_cookies()

    print("✅ Kariyer sayfasına gidiliyor...")
    home_page.navigate_to_careers()
    careers_page = CareersPage(driver)
    assert careers_page.is_accessible(), "❌ Hata: Careers sayfası yüklenemedi!"

    print("✅ Sayfa bölümleri kontrol ediliyor...")
    assert careers_page.verify_sections(), "❌ Hata: Careers sayfasındaki bölümler eksik!"

    print("✅ QA Careers sayfasına geçiliyor...")
    careers_page.go_to_qa_careers()
    qa_careers_page = QACareersPage(driver)

    print("🔍 QA Careers sayfası erişilebilir mi kontrol ediliyor...")
    assert qa_careers_page.is_accessible(), "❌ Hata: QA Careers sayfasına erişilemedi!"

    print("✅ 'See all QA jobs' butonuna tıklanıyor...")
    qa_careers_page.click_see_all_qa_jobs()

    print("✅ Department'ın 'Quality Assurance' olması bekleniyor ve lokasyon seçimi yapılıyor...")
    qa_careers_page.select_location_if_department_is_qa()
    qa_careers_page.wait_for_job_cards_to_be_replaced()

    qa_careers_page.wait_for_job_cards_to_load()
    print("✅ İş ilanları doğrulanıyor...")
    assert qa_careers_page.verify_job_listings(), "❌ Hata: İş ilanları kriterlere uymuyor!"

    print("✅ View Role butonu kontrol ediliyor...")
    assert qa_careers_page.verify_view_role_redirects(), "❌ Hata: View Role butonu yönlendirmiyor!"

    print("🎉 Tüm testler başarıyla tamamlandı!")
    print("🌐 Son URL:", driver.current_url)