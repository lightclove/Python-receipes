import socket
import sys
from pysnmp.hlapi.asyncore import *
port = 162
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))
while 1:
        data, addr = s.recvfrom(4048)
        print(data)
from pysnmp.hlapi.asyncore import *

snmpEngine = SnmpEngine()
sendNotification(
    snmpEngine,
    CommunityData('404040'),
    UdpTransportTarget(('192.168.169.169', 162)),
    ContextData(),
    'trap',
    NotificationType(ObjectIdentity('SNMPv2-MIB', 'coldStart')),
)
snmpEngine.transportDispatcher.runDispatcher()