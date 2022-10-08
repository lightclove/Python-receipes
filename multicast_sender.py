import socket
import struct
import sys
from time import time, sleep

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    packetID = 1
    while packetID:
        sock.sendto('{}, {:.9f}'.format(packetID, time()), ('224.0.0.1', 41724))
        print 'Packet with ID {} sent.'.format(packetID)
        sleep(0.1)
        packetID += 1

if __name__ == '__main__':
    main()
