import socket
import time
import random

import globals
import msg_pb2

countMsg = 0

def createMsg():
    global countMsg
    msg = msg_pb2.SensorData()

    msg.device_id   = 0
    msg.event_id    = countMsg
    msg.humidity    = random.uniform(10.0, 30.0)
    msg.temperature = random.uniform(60.0, 80.0)

    countMsg += 1
    return msg

def client():
    while True:
        try:
            print("Подключение к серверу...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
                soc.connect(globals.SERVER_ADDRESS)
                print("Подключение успешно!")
                while True:
                    soc.send(createMsg().SerializeToString())
                    time.sleep(1)  # Ждем 1 секунду

        except Exception as e:
            print(f"Ошибка подключения: {e}")
            time.sleep(1)

if __name__ == '__main__':
    client()