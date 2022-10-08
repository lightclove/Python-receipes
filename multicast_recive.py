import socket
import struct
from time import time
multicast_addr = '224.0.0.1'
bind_addr = '0.0.0.0'
port = 41724

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    membership = socket.inet_aton(multicast_addr) + socket.inet_aton(bind_addr)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((bind_addr, port))

    while True:
        message, address = sock.recvfrom(255)
        # print message , address
        localTime = '{:.9f}'.format(time())
        result = '{}, {}\n'.format(message, localTime)
        file.write(result)
        file.flush()
        print 'Packet with ID {} received.'.format(result.split(', ')[0])
if __name__ == '__main__':
    with open('result.csv', 'a') as file:
        main()
