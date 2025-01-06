import socket
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

import globals
import msg_pb2

token = "bJiwAUAcziGUXcMPiwwDvKm5Dni847YspdXETTuT1CVVvmbLgKvdQ1anOcBURIjAilFF1flpiCBMHhM0ubbF2g=="
org = "temp"
url = "http://localhost:8086"
bucket="Sensors"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

# Функция чтения данных, заодно выводим в терминал
def readData(protobufData):
    msg = msg_pb2.SensorData()
    msg.ParseFromString(protobufData)

    print(f"ID устройства {msg.device_id}:")
    print(f"ID сообщения: {msg.event_id}")
    print(f"Влажность: {msg.humidity:.2f}%")
    print(f"Температура: {msg.temperature:.2f}°C")
    print()
    return msg

# Запись в БД
def writeMsgToDB(msg):
    try:
        point = Point("SensorData") \
            .tag("device_id", msg.device_id) \
            .field("event_id", msg.event_id) \
            .field("humidity", msg.humidity) \
            .field("temperature", msg.temperature)
    
        write_api.write(bucket=bucket, org="temp", record=point)
        print("Данные записаны")
    except Exception as e:
        print(f"В момент записи в БД что-то пошло не так: {e}")

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(globals.SERVER_ADDRESS)  # Привязываем сервер к адресу
    server_socket.listen(1)

    print("Сервер запущен")

    while True:
        conn, addr = server_socket.accept()  # Принимаем входящее соединение
        print(f"Подключился клиент {addr}")

        with conn:
            try:
                while True:
                    data = conn.recv(1024)  # Принимаем входящее сообщение. Размер буффера 1 КБ
                    if not data:
                        break
                    msg = readData(data) # Парсим пришедшее сообщение
                    writeMsgToDB(msg)    # Записываем сообщдение БД   
            except Exception as e:
                print(f"Что-то пошло не так: {e}")
        
        print(f"Клиент ушел {addr}")

if __name__ == '__main__':
    server()