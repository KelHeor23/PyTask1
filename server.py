import socket

import globals

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
                        break;
                    print(data)                    
            except Exception as e:
                print(f"Что-то пошло не так: {e}")
        
        print(f"Клиент ушел {addr}")

if __name__ == '__main__':
    server()