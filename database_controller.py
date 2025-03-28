from influxdb import InfluxDBClient


# InfluxDB'ye test sonucu yazan fonksiyon
def insert_test_result_to_influxdb(test_name, status, duration, timestamp):
    """
    Inserts a test result into the InfluxDB database.

    :param test_name: Name of the test case
    :type test_name: str
    :param status: Status of the test ('passed' or 'failed')
    :type status: str
    :param duration: Duration of the test execution in seconds
    :type duration: float
    :param timestamp: Timestamp of the test execution (UTC)
    :type timestamp: datetime.datetime
    
    """
    try:
        client = InfluxDBClient(host='localhost', port=8086)
        client.switch_database('test_results')

        json_body = [
            {
                "measurement": "ui_test_results",
                "tags": {
                    "test_name": test_name,
                    "status": status,
                },
                "time": timestamp.isoformat(),  # Artık dışarıdan gelen timestamp kullanılıyor
                "fields": {
                    "duration": float(duration)
                }
            }
        ]

        client.write_points(json_body)
        client.close()
        print(f"✅ InfluxDB'ye veri yazıldı: {test_name} | {status} | {duration:.2f}s")

    except Exception as e:
        print(f"❌ InfluxDB yazım hatası: {e}")

