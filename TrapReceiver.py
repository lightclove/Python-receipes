import socket
import sys

port = 162
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("192.168.169.169", port))
while 1:
        data, addr = s.recvfrom(4048)
        print(data)