"""Bai 2 - Monitoring Consumer: nhan du lieu cam bien, phat hien canh bao."""
import json
import os
import pika

HOST = os.getenv("AMQP_HOST", "localhost")
USER = os.getenv("AMQP_USER", "guest")
PASSWORD = os.getenv("AMQP_PASS", "guest")
QUEUE = "sensor_data_queue"

TEMP_MAX = 35
HUMIDITY_MIN = 40


def on_message(ch, method, properties, body):
    try:
        data = json.loads(body.decode("utf-8"))
        device = data["device_id"]
        temp = float(data["temperature"])
        hum = float(data["humidity"])
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"[!] Payload khong hop le: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    print(f"Device: {device}")
    print(f"Temperature: {temp}")
    print(f"Humidity: {hum}")
    if "timestamp" in data:
        print(f"Timestamp: {data['timestamp']}")
    if temp > TEMP_MAX:
        print("CANH BAO: Nhiet do cao")
    if hum < HUMIDITY_MIN:
        print("CANH BAO: Do am thap")
    print("-" * 40)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    credentials = pika.PlainCredentials(USER, PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_consume(queue=QUEUE, on_message_callback=on_message)

    print(f"[*] Dang giam sat queue '{QUEUE}'. Ctrl+C de dung.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nDa dung monitor.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()