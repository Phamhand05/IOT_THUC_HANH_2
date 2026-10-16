"""Bai 2 - Sensor Producer: mo phong cam bien gui telemetry moi 3 giay."""
import json
import os
import random
import sys
import time
from datetime import datetime
import pika

HOST = os.getenv("AMQP_HOST", "localhost")
USER = os.getenv("AMQP_USER", "guest")
PASSWORD = os.getenv("AMQP_PASS", "guest")
QUEUE = "sensor_data_queue"
INTERVAL = 3  # giay

# Mo rong: mo phong nhieu cam bien. Chay: python sensor_producer_bai2.py sensor01 sensor02 ...
DEVICES = sys.argv[1:] or ["sensor01"]


def main():
    credentials = pika.PlainCredentials(USER, PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)

    print(f"[*] Cam bien {DEVICES} dang gui du lieu moi {INTERVAL}s. Ctrl+C de dung.")
    try:
        while True:
            for device_id in DEVICES:
                payload = {
                    "device_id": device_id,
                    "temperature": round(random.uniform(20.0, 40.0), 1),
                    "humidity": round(random.uniform(30.0, 90.0), 1),
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                }
                channel.basic_publish(
                    exchange="",
                    routing_key=QUEUE,
                    body=json.dumps(payload),
                    properties=pika.BasicProperties(
                        content_type="application/json", delivery_mode=2
                    ),
                )
                print(f"[x] Da gui: {payload}")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nDa dung sensor producer.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()