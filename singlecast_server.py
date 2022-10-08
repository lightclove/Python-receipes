# -*- coding: utf-8 -*-

from SocketServer import UDPServer, BaseRequestHandler
from time import time

class UDPRequestHandler(BaseRequestHandler):
    def handle(self):
        localTime = '{:.9f}'.format(time())
        result = '{}, {}\n'.format(self.request[0], localTime)
        file.write(result)
        file.flush()
        print 'Packet with ID {} received.'.format(result.split(', ')[0])

def main():
    server = UDPServer(('0.0.0.0', 41724), UDPRequestHandler)
    print 'Server accepting UDP connections {}...'.format(server.server_address)
    server.serve_forever()

if __name__ == '__main__':
    with open('result.csv', 'a') as file:
        main()
