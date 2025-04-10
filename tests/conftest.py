import pytest
import os
from datetime import datetime, timezone
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.firefox import GeckoDriverManager
from database_controller import insert_test_result_to_influxdb

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    """
    Pytest fixture to initialize and return a Selenium WebDriver instance.

    This fixture supports both Chrome and Firefox browsers. It:
    - Configures browser-specific options
    - Launches the driver
    - Maximizes the window for consistency
    - Tears down the driver after test execution

    """
    if request.param == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # ✅ Using local chromedriver path
        service = ChromeService(
            executable_path="/Users/ferit.tongemen/Documents/Drivers/chromedriver-mac-arm64/chromedriver"
        )
        driver = webdriver.Chrome(service=service, options=chrome_options)

    elif request.param == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)

    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Pytest hook that runs after each test case.

    Responsibilities:
    - Logs test results to InfluxDB (name, status, duration, UTC timestamp)
    - Captures and saves a screenshot when a test fails
    - Outputs the result clearly in console for visibility

    This hook helps with:
    - Monitoring test stability in Grafana
    - Debugging UI failures with screenshots

    Trigger: Runs after the 'call' phase of every test function.

    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        test_name = item.name
        status = "passed" if report.passed else "failed"
        duration = getattr(report, 'duration', 0)
        timestamp = datetime.now(timezone.utc)

        try:
            insert_test_result_to_influxdb(
                test_name=test_name,
                status=status,
                duration=duration,
                timestamp=timestamp
            )
            print(f"✅ InfluxDB write: {test_name} | {status} | {duration}s")
        except Exception as e:
            print(f"❌ InfluxDB error: {e}")

        if status == "failed":
            driver = item.funcargs.get("driver", None)
            if driver:
                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
                driver.save_screenshot(screenshot_path)
                print(f"🖼 Screenshot saved: {screenshot_path}")
