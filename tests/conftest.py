import pytest
import os
from datetime import datetime
from database_controller import insert_test_result_to_influxdb

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Pytest hook to handle test result reporting:
    - Inserts test result to InfluxDB
    - Captures screenshot on test failure

    :param item: pytest test item
    
    """
    # Testin sonucunu al
    outcome = yield
    report = outcome.get_result()

    # Sadece testin "call" (yürütme) aşamasında sonucu kaydet
    if report.when == "call":
        test_name = item.name
        status = "passed" if report.passed else "failed"
        duration = getattr(report, 'duration', 0)
        timestamp = datetime.utcnow()

        # Sonucu InfluxDB'ye yaz
        try:
            insert_test_result_to_influxdb(
                test_name=test_name,
                status=status,
                duration=duration,
                timestamp=timestamp
            )
        except Exception as e:
            print(f"❌ InfluxDB'ye yazma hatası: {e}")

        # Test başarısızsa ekran görüntüsü al
        if report.failed:
            driver = item.funcargs.get("driver", None)
            if driver:
                screenshot_dir = "screenshots"
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
                driver.save_screenshot(screenshot_path)
                print(f"🖼 Ekran görüntüsü alındı: {screenshot_path}")
                