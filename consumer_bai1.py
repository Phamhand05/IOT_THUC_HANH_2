"""Bai 1 - Consumer: nhan message tu queue iot_lab_queue."""
import os
from datetime import datetime
import pika

HOST = os.getenv("AMQP_HOST", "localhost")
USER = os.getenv("AMQP_USER", "guest")
PASSWORD = os.getenv("AMQP_PASS", "guest")
QUEUE = "iot_lab_queue"


def on_message(ch, method, properties, body):
    print(f"Da nhan message: {body.decode('utf-8')}")
    print(f"Thoi gian nhan: {datetime.now().strftime('%H:%M:%S')}")
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

    print(f"[*] Dang cho message tu queue '{QUEUE}'. Nhan Ctrl+C de dung.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nDa dung consumer.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()