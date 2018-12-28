
from socketserver import BaseRequestHandler, UDPServer
from time import time
# linking unified logging class and connected it to the database log writer (Db handler)
import Logger
from LogDB import configParser, psqlHandler
from UDP_Server import UDPServerSocket

logger = configParser.get('log', 'logger')
pathTolog = configParser.get('log', 'pathTolog')
# Config parser parameters
host = configParser.get('db', 'host')
user = configParser.get('db', 'user')
password = configParser.get('db', 'password')
database = configParser.get('db', 'database')
uport2 = configParser.get('net', 'uport2')
uhost3 = configParser.get('net', 'uhost3')

myh = psqlHandler({''
                   'host': host,
                   'user': user,
                   'password': password,
                   'database': database})

logger = Logger.Logger.initLogging(

    logger,
    pathTolog
)
# logger = logging.getLogger("TEST")
# logger.setLevel(logging.DEBUG)

# link Db handler
logger.addHandler(myh)


class UDPRequestHandler(BaseRequestHandler):
    def handle(self):
        localTime = '{:.9f}'.format(time())
        #result = '{}, {}\n'.format(self.request[0], localTime)
        result = self.request[0]

        # file.write(result)
        # file.flush()
        # print('Packet with ID {} received.'.format(result.split(', ')[0]))
        # logger.info('Packet with ID: {} received: '.format(result.split(', ')[0]))
        print(str(result))
        bytesToSend = str.encode(result )
        # Sending a reply to client
        UDPServerSocket.sendto(bytesToSend, uhost3)

    UDPServerSocket.close()

def main():

    server = UDPServer(('0.0.0.0', int(uport2)), UDPRequestHandler)
    print('Server accepting UDP connections {}...'.format(server.server_address))
    logger.info('Server accepting UDP connections {}...'.format(server.server_address))
    server.serve_forever()


if __name__ == '__main__':
    #with open('result.csv', 'a') as file:
    main()
