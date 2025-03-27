from influxdb import InfluxDBClient

# InfluxDB'ye test sonucu yazan fonksiyon
def insert_test_result_to_influxdb(test_name, status, duration, timestamp):
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