import pytest
import os

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    # Testin sonucunu al
    outcome = yield
    report = outcome.get_result()

    # 'call' aşamasında ve test başarısızsa ekran görüntüsü al
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            driver.save_screenshot(screenshot_path)
            print(f"🖼 Ekran görüntüsü alındı: {screenshot_path}")