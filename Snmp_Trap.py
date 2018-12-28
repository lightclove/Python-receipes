'''
Snmp Trap / UDP-packet Catcher
'''
import socket

from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp, udp6
from pyasn1.codec.ber import decoder
from pysnmp.proto import api

try:
    # LOGGING SECTION #
    # linking unified logging class
    import Logger
    logger = Logger.Logger.initLogging(
        "Snmp_Trap",
        "Snmp_Trap.log"
    )
    ######

    # noinspection PyUnusedLocal

    def cbFun(transportDispatcher, transportDomain, transportAddress, wholeMsg):

        while wholeMsg:
            msgVer = int(api.decodeMessageVersion(wholeMsg))
            if msgVer in api.protoModules:
                pMod = api.protoModules[msgVer]
            else:
                print('Unsupported SNMP version %s' % msgVer)
                logger.info('Unsupported SNMP version %s' % msgVer)
                return
            reqMsg, wholeMsg = decoder.decode(
                wholeMsg, asn1Spec=pMod.Message(),
            )
            print('Notification message from %s:%s: ' % (
                transportDomain, transportAddress
            )
                  )
            logger.info('Notification message from %s:%s: ' % (
                transportDomain, transportAddress
            )
                        )

            reqPDU = pMod.apiMessage.getPDU(reqMsg)
            if reqPDU.isSameTypeWith(pMod.TrapPDU()):
                if msgVer == api.protoVersion1:
                    print('Enterprise: %s' % (pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()))
                    logger.info('Enterprise: %s' % (pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()))
                    print('Agent Address: %s' % (pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()))
                    logger.info('Agent Address: %s' % (pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()))
                    print('Generic Trap: %s' % (pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()))
                    logger.info('Generic Trap: %s' % (pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()))
                    print('Specific Trap: %s' % (pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()))
                    logger.info('Specific Trap: %s' % (pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()))
                    print('Uptime: %s' % (pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()))
                    logger.info('Uptime: %s' % (pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()))
                    varBinds = pMod.apiTrapPDU.getVarBinds(reqPDU)
                else:
                    varBinds = pMod.apiPDU.getVarBinds(reqPDU)
                print('Var-binds:')
                logger.info('Var-binds:')
                for oid, val in varBinds:
                    print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
                    logger.info('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))

        return wholeMsg

    def testReceive(port):
        print('Test UDP packet receiver function.')
        logger.info('UDP packet receiver started')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", port))
        while 1:
            data, addr = s.recvfrom(4048)

            print('Received trap is: ' + str(data) + " " + str(addr))
            logger.info('Received trap is: ' + str(data) + " " + str(addr))
    ###
    def main():
        """
        The main entry point of the application
        """
        print("Starting trap catching...")
        logger.info("Starting trap catching...")
        print("trap catching in progress... Press Ctrl + C to stop...")
        logger.info("trap catching in progress... Press Ctrl + C to stop...")
        #testReceive(162)
        transportDispatcher = AsyncoreDispatcher()
        transportDispatcher.registerRecvCbFun(cbFun)

        # LOAD CONFIG

        # UDP/IPv4
        transportDispatcher.registerTransport(
            udp.domainName, udp.UdpSocketTransport().openServerMode(("", 20001))
        )
        # UDP/IPv6
        transportDispatcher.registerTransport(
            udp6.domainName, udp6.Udp6SocketTransport().openServerMode(('::1', 162))
        )
        ## Local domain socket
        # transportDispatcher.registerTransport(
        #    unix.domainName, unix.UnixSocketTransport().openServerMode('/tmp/snmp-manager')
        # )
        transportDispatcher.jobStarted(1)

        try:
            # Dispatcher will never finish as job#1 never reaches zero
            transportDispatcher.runDispatcher()
        except:
            transportDispatcher.closeDispatcher()
            print.info("Stop trap catching due to exception...")
            logger.info("Stop trap catching due to exception...")
            raise


    if __name__ == "__main__":

        main()


except BaseException as BE:
    print('Another exception occured' + str(BE))
    logger.error('Another exception occured' + str(BE))
    print(BE)

