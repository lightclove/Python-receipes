#!/usr/bin/env python3

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 555
BUFFER_SIZE = 2048
MESSAGE = b'Message from Dimi: Hello, SuperDen 2018!'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)

data = s.recv(BUFFER_SIZE)
s.close()
print ("received data:", data)