# -*- coding: UTF-8 -*-
# !/usr/bin/env python3
'''
Cуществует два существенных различия между использованием сокета домена Unix и сокета TCP/IP c точки зрения программиста,
Во-первых, адрес сокета - это путь в файловой системе, а не кортеж, содержащий имя сервера и порт.
Во-вторых, узел, созданный в системе файл для представления сокета, сохраняется после закрытия сокета,
поэтому его необходимо удалять(os.unlink() ) при каждом запуске сервера.
Сокет UDS должен быть создан с адресным семейством AF_UNIX.
Привязка к сокету и управление входящими соединениями работает так же, как и для сокетов TCP/IP.

'''
import socket
import sys
import os
server_address = './uds_socket'

try:
    # Удаляем файл
    os.unlink(server_address)

except OSError:
    # Убедимся, что файл-сокет существует
    if os.path.exists(server_address):
        raise
# Создаем UDS-сокет
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the UDS-socket to the address.
print('starting up on {}'.format(server_address))
sock.bind(server_address)

# Слушаем входящие соединения:
sock.listen(1)
while True:
    # Ожидаем соединений
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        while True:
            # Получать данные небольшими порциями и повторно передаем их
            data = connection.recv(25)
            print('received {!r}'.format(data))
            if data:
                print('sending data back to the client')
                # Socket.sendall - это высокоуровневый метод Python-only, (в отличии от низкоуровнего С-метода send() )
                # который отправляет весь передаваемый вами буфер или выдает исключение.
                connection.sendall(data)
            else:
                print('no data from ', client_address)
                break
    finally:
        # Очищаем соединение
        print("Closing connection")
        connection.close()
