"""Bai 3 - Alert Producer: gui canh bao len direct exchange iot_alert_exchange."""
import os
import time
import pika

HOST = os.getenv("AMQP_HOST", "localhost")
USER = os.getenv("AMQP_USER", "guest")
PASSWORD = os.getenv("AMQP_PASS", "guest")
EXCHANGE = "iot_alert_exchange"

ALERTS = [
    ("info", "Cam bien phong server hoat dong binh thuong - info"),
    ("warning", "Nhiet do phong may chuot vuot nguong warning"),
    ("critical", "Cam bien kho lanh mat ket noi critical"),
]


def main():
    credentials = pika.PlainCredentials(USER, PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, credentials=credentials)
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct", durable=True)

    for routing_key, message in ALERTS:
        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=routing_key,
            body=message.encode("utf-8"),
        )
        print(f"[x] Da gui [{routing_key}]: {message}")
        time.sleep(1)

    connection.close()


if __name__ == "__main__":
    main()