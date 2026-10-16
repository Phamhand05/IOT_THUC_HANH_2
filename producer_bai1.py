"""Bai 1 - Producer: gui message co ban vao queue iot_lab_queue."""
import os
import pika

HOST = os.getenv("AMQP_HOST", "localhost")
USER = os.getenv("AMQP_USER", "guest")
PASSWORD = os.getenv("AMQP_PASS", "guest")
QUEUE = "iot_lab_queue"


def main():
    ho_ten = input("Nhap ho ten sinh vien: ").strip() or "Nguyen Van A"
    ma_sv = input("Nhap ma sinh vien: ").strip() or "B21xxxx"

    credentials = pika.PlainCredentials(USER, PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)

    # Gui message dau tien
    message = f"Xin chao tu ung dung Python AMQP - {ma_sv} - {ho_ten}"
    channel.basic_publish(
        exchange="",                      # default exchange
        routing_key=QUEUE,                # default exchange route theo ten queue
        body=message.encode("utf-8"),
        properties=pika.BasicProperties(delivery_mode=2),  # persistent
    )
    print(f"[x] Da gui: {message}")

    # Mo rong: gui nhieu message lien tiep
    try:
        n = int(input("Gui them bao nhieu message nua? (0 de bo qua): ") or 0)
    except ValueError:
        n = 0
    for i in range(1, n + 1):
        msg = f"Message #{i} - {ma_sv} - {ho_ten}"
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE,
            body=msg.encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        print(f"[x] Da gui: {msg}")

    connection.close()


if __name__ == "__main__":
    main()