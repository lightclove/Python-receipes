from pysnmp.hlapi import *
i = 1

stateOFF = False
while i+1:
    # Request.
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget(('192.168.2.4', 161)),
               ContextData(),
               ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)))
            #sysUpTime
        # #sysName
        # #ipAdEntAddr
        # #ipAdEntNetMask
        # #ipForwarding forwarding(1) #
        #ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)))
        # #sysUpTime
        # #sysName
        # #ipAdEntAddr
        # #ipAdEntNetMask
        #ipForwarding forwarding(1)
        #sysUpTime
        # #sysName
        # #ipAdEntAddr
        # #ipAdEntNetMask
        # #ipForwarding forwarding(1) #
    )
    changeState = False
    if errorIndication:
        # Send udp to den
        print(errorIndication)

    elif errorStatus:
        changeState = False
        # Send udp to den
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

    else:
        for varBind in varBinds:
            changeState = True

            print(' = '.join([x.prettyPrint() for x in varBind]))
    changeState = True

'''         
1: enterprises.2021.10.1.5.1.0 28
2: enterprises.2021.10.1.5.2.0 81
3: enterprises.2021.10.1.5.3.0 55
4: enterprises.33555.2.1.1.1.0 R4
5: enterprises.33555.2.1.1.2.0 RipEX-160
6: enterprises.33555.2.1.1.3.0 RipEX-135S
7: enterprises.33555.2.1.1.4.0 11550803
8: enterprises.33555.2.1.1.5.0 1
9: enterprises.33555.2.1.1.6.1.0 1.0.41.5
10: enterprises.33555.2.1.1.6.2.0 1.2.70.4
11: enterprises.33555.2.1.1.7.1.0 1.6.7.0
12: enterprises.33555.2.1.1.7.2.0 0.24.0.57
13: enterprises.33555.2.1.1.7.3.0 0.5.19.0
14: enterprises.33555.2.1.1.7.4.0 3.0.2.18
105: enterprises.33555.2.3.1.3.1.2.1 192.168.2.255
106: enterprises.33555.2.3.1.3.1.2.2 224.0.0.251
107: enterprises.33555.2.3.1.3.1.2.3 224.0.0.252
108: enterprises.33555.2.3.1.3.1.2.4 239.255.255.250
109: enterprises.33555.2.3.1.3.1.2.5 UNKNOWN
110: enterprises.33555.2.3.1.3.1.2.6 RADIO BROADCAST
'''
