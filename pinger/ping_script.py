import os
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pythonping

INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")

PING_TARGETS_STR = os.getenv("PING_TARGETS", "google.de")
PING_TARGETS = [target.strip() for target in PING_TARGETS_STR.split(',')]
PING_INTERVAL = int(os.getenv("PING_INTERVAL", 10))

print("--- Pinger wird gestartet ---")
print(f"Ziele: {PING_TARGETS}")
print(f"Intervall pro Ziel: {PING_INTERVAL} Sekunden")
print(f"InfluxDB URL: {INFLUXDB_URL}")
print("----------------------------")


try:
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    print("Verbindung zu InfluxDB erfolgreich hergestellt.")
except Exception as e:
    print(f"Fehler bei der Verbindung zu InfluxDB: {e}")
    exit(1)


while True:
    for target in PING_TARGETS:
        try:
            response = pythonping.ping(target, count=1, timeout=5)

            if response.success:
                latency_ms = response.rtt_avg_ms
                print(f"Ping an {target} erfolgreich: {latency_ms:.2f} ms")

                point = (
                    Point("latency_measurement")
                    .tag("target", target)
                    .field("response_ms", float(latency_ms))
                )

                write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            else:
                print(f"Ping an {target} fehlgeschlagen. Keine Daten gesendet.")

        except Exception as e:
            print(f"Ein Fehler ist beim Pingen von {target} aufgetreten: {e}")

    time.sleep(PING_INTERVAL)