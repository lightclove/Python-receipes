import json
import socket
import struct
from socketserver import BaseRequestHandler, UDPServer
from time import time
# linking unified logging class and connected it to the database log writer (Db handler)
import Logger
from LogDB import configParser, psqlHandler

logger = configParser.get('log', 'logger')
pathTolog = configParser.get('log', 'pathTolog')
# Config parser parameters
host = configParser.get('db', 'host')
user = configParser.get('db', 'user')
password = configParser.get('db', 'password')
database = configParser.get('db', 'database')
uport = configParser.get('net', 'uport')

hostToSend = configParser.get('amr', 'hostToSend')
portToSend = configParser.get('amr', 'portToSend')
datasend = configParser.get('amr', 'datasend')
message = configParser.get('amr', 'message')

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

# datasend = bytearray(datasend, encoding="utf-8")
# message = bytearray(message, encoding="utf-8")
#datasend = bytearray([8, 0x0A, 0, 0, 0, 0, 0, 0, 1])

class UDP_Divisor(BaseRequestHandler):
    def handle(self):
        localTime = '{:.9f}'.format(time())
        result = '{}, {}\n'.format(self.request[0], localTime)
        file.write(result)
        file.flush()
        print('Packet with ID {} received.'.format(result.split(', ')[0]))
        logger.info('Packet with ID: {} received.'.format(result.split(', ')[0]))
        return True

    @staticmethod
    def sendFullAMR(switchState, IP, PORT):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        s.connect((IP, PORT))
        datasend = bytearray([8, 0x0A, 0, 0, 0, 0, 0, 0, 2])
        message = bytearray([0x1C, 60, 0x0A, 0x60, 0, 0x30, 9, len(datasend)])

        if(switchState == True):
            #datasend = bytearray([8, 0x0A, 0, 0, 0, 0, 0, 0, 1] )
            datasend[len(datasend) - 1] = 2
        else:
            #datasend = bytearray([8, 0x0A, 0, 0, 0, 0, 0, 0, 2] )
            datasend[len(datasend) - 1] = 1
        message = bytearray([0x1C, 60, 0x0A, 0x60, 0, 0x30, 9, len(datasend)])
        data = str(datasend + datasend)
        #data = json.dumps({"a": message, "b": datasend })
        s.send(bytes(data, encoding='utf-8'))

        #message = bytearray([0x1C, 60, 0x0A, 0x60, 0, 0x30, 9, len(datasend)])
        #message = bytearray([8, 0x0A, 0, 0, 0, 0, 0, 0, 1, 0x1C, 60, 0x0A, 0x60, 0, 0x30, 9, 9])
        print('message sent')

        print(str(message))
        s.close()

    # def sendArray(host, port):
    #
    #     s = socket.socket()
    #     s.connect((host, port))
    #     datasend = bytearray([8, 0x0A, 0, 0, 0, 0, 0, 0, 2])
    #     message = bytearray([0x1C, 60, 0x0A, 0x60, 0, 0x30, 9, len(datasend)])
    #
    #     arr = datasend + message
    #
    #     for elmt in arr:
    #         send_str = "%s," % str(elmt)
    #
    #     while send_str:
    #         chars_sent = s.send(send_str)
    #         send_str = send_str[chars_sent:]
    #
    #     s.close()

def main():

    UDP_Divisor.sendFullAMR(True, "33.55.77.208", 33002)
    # server = UDPServer(('0.0.0.0', int(uport)), UDPRequestHandler)
    # print('Server accepting UDP connections {}...'.format(server.server_address))
    # logger.info('Server accepting UDP connections {}...'.format(server.server_address))
    # server.serve_forever()


if __name__ == '__main__':
    with open('result.csv', 'a') as file:
        main()
