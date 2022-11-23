# -*- coding: UTF-8 -*-
# !/usr/bin/env python3
'''
Клиент должен знать, что файл для сокета существует,
поскольку сервер создает его путем привязки к адресу.
Отправка и получение данных в клиенте UDS работает так же, как и в TCP/IP .
Поскольку сокет UDS представлен файлом в файловой системе, нужны соответствующие разрешения на чтение и запись
'''
import socket
import sys
import json
import time


class UDS_Client:
    # Создаем UDP socket.
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    # Подключаемся сокет-файл
    server_address = './uds_socket'
    print('connecting to {}'.format(server_address))
    try:
        sock.connect(server_address)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    try:
        message = b'This is the message. It will be repeated.'
        print('sending {!r}'.format(message))
        # Отправка ответа: sendall отправляет весь передаваемый вами буфер или выдает исключение.
        while True:
            sock.sendall(message)
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                data = sock.recv(16)
                amount_received += len(data)
                print('received {!r}'.format(data))

            time.sleep(1)

    finally:
        # print('closing socket')
        sock.close()