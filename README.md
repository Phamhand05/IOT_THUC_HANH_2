# Buoi thuc hanh: Lap trinh Python voi giao thuc AMQP

- Sinh viên:
  - Lê Huy Hải – B23DCCN272
  - Phạm Thu Hà – B23DCCN267
  - Nguyễn Thu Thảo – B23DCCN776

## 1. Broker su dung

- **RabbitMQ Server** cai truc tiep tren Windows (chay duoi dang service `RabbitMQ`).
- **Erlang/OTP 27.3.4.18** (cai bang winget). Khong dung Erlang 29 vi nhieu ban RabbitMQ chua ho tro.
- Ket noi: host `localhost`, cong AMQP `5672`, user/pass `guest/guest`.
- Giao dien quan tri: http://localhost:15672 (user/pass `guest/guest`).
- Co the doi broker bang bien moi truong (PowerShell):
  ```
  $env:AMQP_HOST="192.168.x.x"
  $env:AMQP_USER="ten_user"
  $env:AMQP_PASS="mat_khau"
  ```

## 2. Chuan bi moi truong

```
pip install pika
Get-Service RabbitMQ            # Status phai la Running
Start-Service RabbitMQ          # neu dang Stopped (PowerShell Admin)
Test-NetConnection localhost -Port 5672   # TcpTestSucceeded : True
```

Bat giao dien quan tri (tuy chon, PowerShell Admin):

```
rabbitmq-plugins enable rabbitmq_management
Restart-Service RabbitMQ
```

(Neu khong nhan lenh, dung "RabbitMQ Command Prompt (sbin dir)" trong Start Menu.)

## 3. Cach chay (moi chuong trinh mo o 1 terminal rieng)

### Bai 1

```
python consumer_bai1.py
python producer_bai1.py
```

### Bai 2

```
python monitor_consumer_bai2.py
python sensor_producer_bai2.py
python sensor_producer_bai2.py sensor01 sensor02 sensor03
```

### Bai 3 (chay 2 consumer truoc, producer sau)

```
python warning_consumer_bai3.py
python critical_consumer_bai3.py
python alert_producer_bai3.py
```

## 4. Ket qua dat duoc

- **Bai 1:** producer gui message vao `iot_lab_queue`; consumer nhan, in noi dung va thoi diem nhan.
- **Bai 2:** gui JSON (device_id, temperature, humidity, timestamp) moi 3 giay vao `sensor_data_queue`; consumer in thong so va canh bao khi nhiet do > 35 hoac do am < 40. Ho tro nhieu cam bien.
- **Bai 3:** direct exchange `iot_alert_exchange`; `info` khong queue nao nhan, `warning` chi vao `warning_queue`, `critical` chi vao `critical_queue`.

## 5. Loi gap phai va cach khac phuc

- `pika.exceptions.AMQPConnectionError`: RabbitMQ chua chay hoac chua khoi dong xong. Kiem tra `Get-Service RabbitMQ` va `Test-NetConnection localhost -Port 5672`, cho vai chuc giay sau khi khoi dong roi chay lai.
- Lenh `erl` khong nhan: chi la van de PATH, khong anh huong RabbitMQ.

## 6. Anh minh chung

- Bai 1:
  ![alt text](<Screenshot 2026-10-16 175854-1.png>)
  ![alt text](<Screenshot 2026-10-16 175901-1.png>)
- Bai 2:
  ![alt text](<Screenshot 2026-10-16 180018-1.png>)
  ![alt text](<Screenshot 2026-10-16 180025-1.png>)
- Bai 3:
  ![alt text](<Screenshot 2026-10-16 180237-1.png>)
  ![alt text](<Screenshot 2026-10-16 180244-1.png>)
  ![alt text](<Screenshot 2026-10-16 180251-1.png>)
