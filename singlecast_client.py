# -*- coding: utf-8 -*-

from socket import socket as Socket, AF_INET, SOCK_DGRAM
from time import time, sleep

def main():
    print 'Starting...'
    socket = Socket(AF_INET, SOCK_DGRAM)
    packetID = 1
    while packetID:
        socket.sendto('{}, {:.9f}'.format(packetID, time()), ('insert_your_ipaddr_here', 41724))
        print 'Packet with ID {} sent.'.format(packetID)
        sleep(1)
        packetID += 1

if __name__ == '__main__':
    main()
