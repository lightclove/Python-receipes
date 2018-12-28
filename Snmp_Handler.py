from configparser import ConfigParser
from time import asctime

from pysnmp.hlapi import *
import socket

from LogDB import psqlHandler
# try:
#################################################
configParser = ConfigParser()
configFilePath = r'Snmp_Handler.conf'
configParser.read(configFilePath)
##########################################
# Config parser parameters
host = configParser.get('db', 'host')
user = configParser.get('db', 'user')
password = configParser.get('db', 'password')
database = configParser.get('db', 'database')

###
communityData = configParser.get('snmp', 'CommunityData')
udpTransportTarget = configParser.get('snmp', 'UdpTransportTarget')
udpPort = configParser.get('snmp', 'udpPort')
version = configParser.get('snmp', 'version')
oid = configParser.get('snmp', 'oid')
uhost = configParser.get('net', 'uhost')
uport = configParser.get('net', 'uport')
uport2 = configParser.get('net', 'uport2')
uport3 = configParser.get('net', 'uport3')

messageON = configParser.get('net', 'messageON')
messageOFF = configParser.get('net', 'messageOFF')
#hostToSend1

# linking unified logging class and connected it to the database log writer (Db handler)
import Logger

logger = configParser.get('log', 'logger')
pathTolog = configParser.get('log', 'pathTolog')
myh = psqlHandler({''
                   'host': host,
                   'user': user,
                   'password': password,
                   'database': database})

logger = Logger.Logger.initLogging(

    logger,
    pathTolog
)
 #logger = logging.getLogger("TEST")
 #logger.setLevel(logging.DEBUG)

# link Db handler
logger.addHandler(myh)


########################################
def sendTCP(TCP_IP, TCP_PORT, MESSAGE):
    # TCP_IP = '127.0.0.1'
    # TCP_PORT = 555
    BUFFER_SIZE = 4096
    # MESSAGE = 'b\'' + MESSAGE

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE.encode())

    data = s.recv(BUFFER_SIZE)
    s.close()
    print("received data:", data)
    logger.info("received data:", data)


###
def sendUDP(messageToSend, serverAddress, serverPort):
    # messageToSend = b"Hello UDP Server"
    bytesToSend = str.encode(messageToSend)
    # serverAddressPort = ("127.0.0.1", 20001)
    serverAddressPort = (serverAddress, serverPort)
    bufferSize = 2048
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    # UDPClientSocket.sendto(bytesToSend, serverAddress, serverPort)
    # messageFromServer = UDPClientSocket.recvfrom(bufferSize)
    #     # messageFromServer = "Message from Server {}".format(messageFromServer[0])
    #     # print(messageFromServer)
    # Logging block

def sendFullAMR(switchState, IP, PORT):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    s.connect((IP, PORT))
    datasend = bytearray([8, 0x0A, 0, 0, 0, 0, 0, 0, 1])

    if(switchState == True):
        #datasend = bytearray([8, 0x0A, 0, 0, 0, 0, 0, 0, 1] )
        datasend[len(datasend) - 1] = 2
    else:
        #datasend = bytearray([8, 0x0A, 0, 0, 0, 0, 0, 0, 2] )
        datasend[len(datasend) - 1] = 1
    message = bytearray([0x1C, 0x60, 0x0A, 0x60, 0, 0x30, len(datasend)])
    #message = bytearray([ 0x1C, 0x60, 0x0A, 0x60, 0, 30, 9, 8, 0x0A, 0, 0, 0, 0, 0, 0, 1])
    s.send((message + datasend))

    print('message sent')

    print(str(message))
    s.close()

def initRipexInteraction():
    sendUDPON = False
    sendUDPOFF = False

    while 1:
        # Requesting...
        try:
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(communityData, mpModel=0),
                       UdpTransportTarget(("33.55.77.5", 161)),
                       ContextData(),
                       ObjectType(ObjectIdentity(version, oid, 0)))
            )
        except BaseException:
            if sendUDPOFF == False:
                print("Network connection error")
                print("Sended UDP-Datagram: "+messageOFF+udpTransportTarget)
                sendUDP(messageOFF, uhost, 20001)

                logger.info(messageOFF + udpTransportTarget)
                #break
                sendUDPON = False
                sendUDPOFF = True
            continue

        #
        if errorIndication:
            # print(errorIndication)
            logger.error(errorIndication)
            print(errorIndication)
            if sendUDPOFF == False:
                # print('SENDING UDP OFF TO DEN')
                # sendTCP('127.0.0.1', 555, 'SENDING UDP OFF TO DEN' )
                #sendUDP(messageOFF, uhost, 20001)
                sendFullAMR(False, uhost, int(uport2))
                print(messageOFF  + uhost)
                logger.info(messageOFF + uhost)
                sendUDPON = False
                sendUDPOFF = True
        #
        elif errorStatus:
            # print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            logger.info(
                '%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            if sendUDPOFF == False:
                #sendUDP(messageOFF , uhost, 20001)
                sendFullAMR(False, uhost, int(uport2))
                print(messageOFF + uhost)
                logger.info(messageOFF  + uhost)
                # sendUDP('SENDING UDP OFF TO DEN', '127.0.0.1', 20001)
                sendUDPOFF = True
                sendUDPON = False
        else:
            for varBind in varBinds:
                # print(' = '.join([x.prettyPrint() for x in varBind]))
                print(' = '.join([x.prettyPrint() for x in varBind]))
                logger.info(' = '.join([x.prettyPrint() for x in varBind]))

            if sendUDPON == False:
                #sendUDP(messageON, uhost, 20001)
                sendFullAMR(True, uhost, int(uport2))
                print(messageON + uhost)
                logger.info(messageON + uhost)
                sendUDP(messageON, uhost, 20001)
                sendUDPON = True
                sendUDPOFF = False

# import ConfigParser
# and then in you code:
# 
# configParser = ConfigParser.RawConfigParser()
# configFilePath = r'c:\abc.txt'
# configParser.read(configFilePath)
# Use case:
# 
# self.path = configParser.get('your-config', 'path1')

def main():
    """
    The main entry point of the application
    """
    # @TODO #to run in concurrent mode - each module in the separate thread, launched in main() and logging in a common console output.
    # app = "python"
    # file = ".UDP_Server.py"
    # pid = subprocess.Popen([app, file]).pid
    print("Program started...")
    logger.info("Program started...")
    print("Rypex radio modem interaction initialization....")
    logger.info("Rypex radio modem interaction initialization....")
    initRipexInteraction();


if __name__ == "__main__":
    main()

# except BaseException as BE:
#     print('Exception occured:' + str(BE))
#     #logger.error('Exception occured' + str(BE))`
#     print(str(BE))

