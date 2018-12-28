from pysnmp.hlapi.asyncore import *
import logging
try: # COMMON EXCEPTION CATCHING
    # START LOGGING SECTION
    # LOGGING SECTION #
    # linking unified logging class
    import Logger
    logger = Logger.Logger.initLogging(
        "Snmp_Sender",
        "Snmp_Sender.log"
    )
    ###
    def trapSender(community, ipaddress, port, OIDname):
        snmpEngine = SnmpEngine()
        sendNotification(
            snmpEngine,
            CommunityData(community),
            UdpTransportTarget((ipaddress, port)),
            ContextData(),
            'trap',
            NotificationType(ObjectIdentity('SNMPv2-MIB', OIDname)),
        )
        snmpEngine.transportDispatcher.runDispatcher()
        ###
        print("Snmp trap successfully sended on ip: " + str(ipaddress) + ' and port: ' + str(port))
        logger.info("Snmp trap successfully sended on ip: " + str(ipaddress) + ' and port: ' + str(port))
    ### Realization ###

    trapSender('public', '192.168.13.66', 162, 'coldStart' )

    ###             ###
except BaseException as BE: # COMMON EXCEPTION CATCHING END
    print(BE)