D_ON = 1
D_OFF=0
CARD_POSITION_UNIVERSAL_MAX=14
Define = {
# "LicenseKeyPosition": {
    "RadioCapacity":{
        "Invalid": 0,
        "Mbps10": 10,
        "Mbps20": 20,
        "Mbps50": 50,
        "Mbps100": 100,
        "Mbps150": 150,
        "Mbps200": 200,
        "Mbps300": 300,
        "Mbps400": 400,
        "Mbps500": 500,
    },
    "RadioBitrate": {
        "AMR": 2,
        "Fixed": 0,
        "Free": 1,
    },
#},
"Rj45PortUsage": {"Invalid": 0, "FE2": 1, "GbE": 2},
"HighModulation": {"NotAvailable": 0, "QAM512": 1, "QAM1024": 2, "QAM2048": 3, "QAM4096": 4},
"AddPweE1": {"E1x16": 16, "E1x32": 32, "E1x48": 48, "E1x64": 64, "E1x128": 128},
"AddPweE1Data": [16, 16, 16, 32, 48, 64, 128],
"E1Rst1Index": {
    "Invalid": 0,
    "Mbps10": 7,
    "Mbps20": 8,
    "Mbps50": 9,
    "Mbps100": 10,
    "Mbps150": 11,
    "Mbps200": 12,
    "Mbps300": 13,
    "Mbps400": 14,
    "Mbps500": 14
}
}
LicenseKey={
"ADD_PWE_E1": 18,
"ADD_VLAN_TABLE": 17,
"ADV_HEADER_COMPRESS": 26,
"CWDM": 25,
"DHCP_SERVER_RELAY": 27,
"E1_SNCP": 6,
"END": 29,
"ETH_LAGLACPLINE": 21,
"ETH_MSTP": 23,
"ETH_OAM": 8,
"ETH_OAM_LINK": 28,
"ETH_OAM_LMDM": 14,
"ETH_RING_PROTECTION": 22,
"HIGH_CAPACITY_XC": 24,
"HIGH_MODULATION": 10,
"MAIN_CARD_REDUNDANCY": 19,
"NEO_C_IDU_COMPABILITY": 11,
"NEO_ODU_COMPABILITY": 9,
"QOS_CLASSIFY": 15,
"RADIO_BITRATE": 1,
"RADIO_CAPACITY": 2,
"RADIO_REDUNDANCY": 0,
"RADIO_TRAFFIC_AGGREGATION": 20,
"RJ45_PORTUSAGE": 4,
"SFP_PORTUSAGE": 5,
"SFP_PORTUSAGE_OPTION": 13,
"STM1_APS_PROTECTION": 16,
"STM1_MUX_DEMUX": 7,
"SYNC_ETH_CLOCK": 12,
"XPIC_FUNC": 3
}
LicenseKeyInv={
18:"ADD_PWE_E1",
17:"ADD_VLAN_TABLE",
26:"ADV_HEADER_COMPRESS",
25:"CWDM",
27:"DHCP_SERVER_RELAY",
6:"E1_SNCP",
29:"END",
21:"ETH_LAGLACPLINE",
23:"ETH_MSTP",
8:"ETH_OAM",
28:"ETH_OAM_LINK",
14:"ETH_OAM_LMDM" ,
22:"ETH_RING_PROTECTION",
24:"HIGH_CAPACITY_XC",
10:"HIGH_MODULATION",
19:"MAIN_CARD_REDUNDANCY",
11:"NEO_C_IDU_COMPABILITY",
9:"NEO_ODU_COMPABILITY",
15:"QOS_CLASSIFY",
1:"RADIO_BITRATE",
2:"RADIO_CAPACITY",
0:"RADIO_REDUNDANCY",
20:"RADIO_TRAFFIC_AGGREGATION",
4:"RJ45_PORTUSAGE",
5:"SFP_PORTUSAGE",
13:"SFP_PORTUSAGE_OPTION",
16:"STM1_APS_PROTECTION",
7:"STM1_MUX_DEMUX",
12:"SYNC_ETH_CLOCK",
3:"XPIC_FUNC"
}
LicenseKeyPosition  = {
"AdditionalPwe128E1": {"Byte": 30, "Bit": 4},
"AdditionalPweE1": {"Byte": 29, "Bit": {"Min": 2, "Max": 5}},
"AdditionalVlanTable": {"Byte": 25, "Bit": 0},
"AdvHeaderCompress": {"Byte": 23, "Bit": 0},
"CWDM": {"Byte": 31, "Bit": 2},
"DHCPServerRelay": {"Byte": 30, "Bit": 3},
"E1Sncp": {"Byte": 24, "Bit": 6},
"EthMstp": {"Byte": 25, "Bit": 7},
"EthOamLink": {"Byte": 26, "Bit": 0},
"EthRingProtection": {"Byte": 25, "Bit": 4},
"EthTrafficAggregation": {"Byte": 22, "Bit": 0},
"EthernetOam": {"Byte": 24, "Bit": 5},
"EthernetOamLMDM": {"Byte": 25, "Bit": 3},
"HighCapacityXC": {"Byte": 26, "Bit": 1},
"HighModulation": {"Byte": 23, "Bit": {"Min": 1, "Max": 4}},
"LagLacp": {"Byte": 24, "Bit": 4},
"MainCardRedundancy": {"Byte": 31, "Bit": 0},
"NEOcIDUCompatibility": {"Byte": 22, "Bit": 5},
"NeoOduCompatibility": {"Byte": 22, "Bit": 2},
"QoSClassify": {"Byte": 25, "Bit": 2},
"RadioBitrate": {"Byte": 22, "Bit": 1},
"RadioBitrateFix": {"Byte": 22, "Bit": 6},
"RadioBitrateFree": {"Byte": 22, "Bit": 7},
"RadioCapacity": {},
"RadioRedundancy": {"Byte": 20, "Bit": {"Min": 0, "Max": 1, "Skip": 2}},
"RadioRedundancy1000": {"Byte": 20, "Bit": {"Min": 0, "Max": 7, "Skip": 5}},
"Rj45PortUsage": {"Byte": 25, "FE2": 5, "GbE": 6},
"SfpPortUsage": {"Byte": 24, "Bit": 3},
"SfpPortUsageOption": {
    "Bit": [{"Min": 0, "Max": 7},{"Min": 0, "Max": 5}],
    "Byte": [27, 28]
    },
"Stm1ApsProtection": {"Byte": 25, "Bit": 1},
"Stm1MuxDemux": {"Byte": 24, "Bit": 7},
"SyncETHClock": {"Byte": 29, "Bit": 0},
"XpicFunction": {"Byte": 21, "Bit": 0},
"XpicFunction1000": {"Byte": 21, "Bit": {"Min": 0, "Max": 7, "Skip": 5}}
}

def convertToInt(hex_string):
    return int(hex_string,16)

def getBitValueFromHex (data, indexByte, indexBit):
    
    retValue = -1

    if (indexByte is None or indexBit is None ):
        return retValue
    
    bitArray = []

    bitcode  = [ 1, 2, 4, 8, 16, 32, 64, 128 ]

    end = 0
    
    for i in range(len(data)):
        start = i * 2
        end   += 2
        if (end > len(data)):
            break
        
        temp = data[start: end]

        try:
            temp = convertToInt(temp)
        except:
            return retValue

        bitArray.append( temp )

    if(len(bitArray) <= indexByte):
        return retValue

    hexcode = bitArray[ indexByte ]

    if ( (hexcode & bitcode[ indexBit ]) == bitcode[ indexBit ] ):
        retValue = 1

    else:
        retValue = 0

    return retValue

def getAvailabilityData(supportabilityInfo):
        str_licenseInfo = ''
    
        licenseInfo  = list(range(LicenseKey["END"]))
        orgdata = supportabilityInfo


        # Radio Capacity
        wkarr = list(range(CARD_POSITION_UNIVERSAL_MAX))

        position = LicenseKeyPosition

        bitrate = D_OFF
        for cnt in range(CARD_POSITION_UNIVERSAL_MAX):
            bitnum = 0
            wkarr[cnt] = 17

            bitcnt = 0
            if( cnt < 10 ):
                if( getBitValueFromHex(orgdata, cnt*2 + 1, bitcnt) == D_ON ):
                    if( wkarr[cnt] == 17 ):
                        wkarr[cnt] = bitcnt + 8                    
                    bitnum = bitnum+1
                
            else:
                if( getBitValueFromHex(orgdata, cnt*2 + 13, bitcnt) == D_ON ):
                    if( wkarr[cnt] == 17 ):
                        wkarr[cnt] = bitcnt + 8
                    
                    bitnum = bitnum+1

            for bitcnt in range(7, -1, -1):
                if( cnt < 10 ):
                    if( getBitValueFromHex(orgdata, cnt*2, bitcnt) == D_ON ):
                        if( wkarr[cnt] == 17 ):
                            wkarr[cnt] = bitcnt
                        bitnum = bitnum+1
                else:
                    if( getBitValueFromHex(orgdata, cnt*2 + 12, bitcnt) == D_ON ):
                        if( wkarr[cnt] == 17 ):
                            wkarr[cnt] = bitcnt
                        bitnum = bitnum+1

            if( bitnum > 1 ):
                bitrate = D_ON

            if wkarr[cnt] == 0:
                wkarr[cnt] = Define["RadioCapacity"]["Mbps10"]
                #break
            elif wkarr[cnt] == 1:
                wkarr[cnt] = Define["RadioCapacity"]["Mbps20"]
                #break
            elif wkarr[cnt] == 2:
                wkarr[cnt] = Define["RadioCapacity"]["Mbps50"]
                #break
            elif wkarr[cnt] == 3:
                wkarr[cnt] = Define["RadioCapacity"]["Mbps100"]
                #break
            elif wkarr[cnt] == 4:
                wkarr[cnt] = Define["RadioCapacity"]["Mbps150"]
                #break
            elif wkarr[cnt] == 5:
                wkarr[cnt] = Define["RadioCapacity"]["Mbps200"]
                #break
            elif wkarr[cnt] == 6:
                wkarr[cnt] = Define["RadioCapacity"]["Mbps300"]
                #break
            elif wkarr[cnt] == 7:
                wkarr[cnt] = Define["RadioCapacity"]["Mbps400"]
                #break
            elif wkarr[cnt] == 8:
                wkarr[cnt] = Define["RadioCapacity"]["Mbps500"]
                #break
            else:
                wkarr[cnt] = Define["RadioCapacity"]["Invalid"]
                #break
        licenseInfo[LicenseKey["RADIO_CAPACITY"]] = wkarr

        # Radio Bitrate
        if ( getBitValueFromHex(orgdata, position["RadioBitrate"]["Byte"], position["RadioBitrate"]["Bit"]) == D_ON ):
            licenseInfo[LicenseKey["RADIO_BITRATE"]] = Define["RadioBitrate"]["AMR"]
        elif( getBitValueFromHex(orgdata, position["RadioBitrateFree"]["Byte"], position["RadioBitrateFree"]["Bit"]) == D_ON ):
            licenseInfo[LicenseKey["RADIO_BITRATE"]] = Define["RadioBitrate"]["Free"]
        else:
            licenseInfo[LicenseKey["RADIO_BITRATE"]] = Define["RadioBitrate"]["Fixed"]
        # Radio Redundancy
        licenseInfo[LicenseKey["RADIO_REDUNDANCY"]] = 0

        # if( Lct.common.SystemManager.getSystem() == SYSTEM.ADVANCED10 ){
        radioredposi = position["RadioRedundancy1000"]
        # }else{
        #radioredposi = position.RadioRedundancy
        # }

        for cnt in range(radioredposi["Bit"]["Max"], radioredposi["Bit"]["Min"] , -1):
            if( cnt == radioredposi["Bit"]["Skip"] ):
                continue
            
            if( getBitValueFromHex( orgdata, radioredposi["Byte"], cnt ) == 1 ):
                if( cnt > radioredposi["Bit"]["Skip"] ):
                    licenseInfo[LicenseKey["RADIO_REDUNDANCY"]] = cnt
                else:
                    licenseInfo[LicenseKey["RADIO_REDUNDANCY"]] = cnt + 1
                break

        # XPIC Function
        # licenseInfo[LicenseKey.XPIC_FUNC] = 0;
        # var xpicFuncPosi = position.XpicFunction1000;

        # for( var cnt = xpicFuncPosi["Bit"].Max; cnt >= xpicFuncPosi["Bit"].Min; cnt-- ){
        #     if( cnt == xpicFuncPosi["Bit"].Skip ){
        #         continue;
        #     }
        #     if( getBitValueFromHex( orgdata, xpicFuncPosi["Byte"], cnt ) == 1 ){
        #         if( cnt > xpicFuncPosi["Bit"].Skip ){
        #             licenseInfo[LicenseKey.XPIC_FUNC] = cnt;
        #         }else{
        #             licenseInfo[LicenseKey.XPIC_FUNC] = cnt + 1;
        #         }
        #         break;
        licenseInfo[LicenseKey["XPIC_FUNC"]] = getBitValueFromHex( orgdata, position["XpicFunction"]["Byte"], position["XpicFunction"]["Bit"])

        # NEO ODU Compatibility
        licenseInfo[LicenseKey["NEO_ODU_COMPABILITY"]] = getBitValueFromHex( orgdata, position["NeoOduCompatibility"]["Byte"], position["NeoOduCompatibility"]["Bit"])

        # Radio Traffic Aggregation
        licenseInfo[LicenseKey["RADIO_TRAFFIC_AGGREGATION"]] = getBitValueFromHex( orgdata, position["EthTrafficAggregation"]["Byte"], position["EthTrafficAggregation"]["Bit"])

        # LAG / LACP (Line)
        licenseInfo[LicenseKey["ETH_LAGLACPLINE"]] = getBitValueFromHex( orgdata, position["LagLacp"]["Byte"], position["LagLacp"]["Bit"])

        # RJ-45 Port Usage
        if( D_ON == getBitValueFromHex( orgdata, position["Rj45PortUsage"]["Byte"], position["Rj45PortUsage"]["GbE"])):
            licenseInfo[LicenseKey["RJ45_PORTUSAGE"]] = Define["Rj45PortUsage"]["GbE"]
        elif( D_ON == getBitValueFromHex( orgdata, position["Rj45PortUsage"]["Byte"], position["Rj45PortUsage"]["FE2"]) ):
            licenseInfo[LicenseKey["RJ45_PORTUSAGE"]] = Define["Rj45PortUsage"]["FE2"]
        else:
            licenseInfo[LicenseKey["RJ45_PORTUSAGE"]] = Define["Rj45PortUsage"]["Invalid"]
        

        # SFP Port Usage
        licenseInfo[LicenseKey["SFP_PORTUSAGE"]] = getBitValueFromHex( orgdata, position["SfpPortUsage"]["Byte"], position["SfpPortUsage"]["Bit"])

        # SFP Port Usage (Option 1-14)
        sfpport = []

        for cnt in range(len(position["SfpPortUsageOption"]["Byte"])):
            for cnt2 in range(position["SfpPortUsageOption"]["Bit"][cnt]["Min"],position["SfpPortUsageOption"]["Bit"][cnt]["Max"]+1):
                sfpport.append(getBitValueFromHex( orgdata, position["SfpPortUsageOption"]["Byte"][cnt], cnt2))
                
        licenseInfo[LicenseKey["SFP_PORTUSAGE_OPTION"]] = sfpport

        # E1 SNCP
        licenseInfo[LicenseKey["E1_SNCP"]] = getBitValueFromHex( orgdata, position["E1Sncp"]["Byte"], position["E1Sncp"]["Bit"])
        # STM-1 MUX/DEMUX
        licenseInfo[LicenseKey["STM1_MUX_DEMUX"]] = getBitValueFromHex( orgdata, position["Stm1MuxDemux"]["Byte"], position["Stm1MuxDemux"]["Bit"])
        # High Capacity XC
        licenseInfo[LicenseKey["HIGH_CAPACITY_XC"]] = getBitValueFromHex( orgdata, position["HighCapacityXC"]["Byte"], position["HighCapacityXC"]["Bit"])
        # Ethernet OAM(CC/LT/LB)
        licenseInfo[LicenseKey["ETH_OAM"]] = getBitValueFromHex( orgdata, position["EthernetOam"]["Byte"], position["EthernetOam"]["Bit"])

        # High Modulation
        modulation = Define["HighModulation"]["QAM2048"]

        for cnt in range(position["HighModulation"]["Bit"]["Max"], position["HighModulation"]["Bit"]["Min"],-1 ):
            if( getBitValueFromHex( orgdata, position["HighModulation"]["Byte"], cnt ) != 1 ):
                modulation = modulation-1
                continue
            else:
                break
        if(modulation < Define["HighModulation"]["NotAvailable"]):
            modulation = Define["HighModulation"]["NotAvailable"]
        licenseInfo[LicenseKey["HIGH_MODULATION"]] = modulation

        # NEO/c IDU Compatibility
        licenseInfo[LicenseKey["NEO_C_IDU_COMPABILITY"]] = getBitValueFromHex( orgdata, position["NEOcIDUCompatibility"]["Byte"], position["NEOcIDUCompatibility"]["Bit"])
        # Sync. ETH Clock
        licenseInfo[LicenseKey["SYNC_ETH_CLOCK"]] = getBitValueFromHex( orgdata, position["SyncETHClock"]["Byte"], position["SyncETHClock"]["Bit"])
        # Ethernet OAM (LM/DM)
        licenseInfo[LicenseKey["ETH_OAM_LMDM"]] = getBitValueFromHex( orgdata, position["EthernetOamLMDM"]["Byte"], position["EthernetOamLMDM"]["Bit"])
        # QoS Classify
        licenseInfo[LicenseKey["QOS_CLASSIFY"]] = getBitValueFromHex( orgdata, position["QoSClassify"]["Byte"], position["QoSClassify"]["Bit"])
        # ETH-Ring Protection
        licenseInfo[LicenseKey["ETH_RING_PROTECTION"]] = getBitValueFromHex( orgdata, position["EthRingProtection"]["Byte"], position["EthRingProtection"]["Bit"])
        # STM-1 APS Protection
        licenseInfo[LicenseKey["STM1_APS_PROTECTION"]] = getBitValueFromHex( orgdata, position["Stm1ApsProtection"]["Byte"], position["Stm1ApsProtection"]["Bit"])
        # Additional VLAN Table
        licenseInfo[LicenseKey["ADD_VLAN_TABLE"]] = getBitValueFromHex( orgdata, position["AdditionalVlanTable"]["Byte"], position["AdditionalVlanTable"]["Bit"])
        # ETH SMTP
        licenseInfo[LicenseKey["ETH_MSTP"]] = getBitValueFromHex( orgdata, position["EthMstp"]["Byte"], position["EthMstp"]["Bit"])

        # Additional PWE E1
        licenseInfo[LicenseKey["ADD_PWE_E1"]] = Define["AddPweE1"]["E1x16"]
        for cnt in range(position["AdditionalPweE1"]["Bit"]["Max"],position["AdditionalPweE1"]["Bit"]["Min"],-1):
            if( getBitValueFromHex( orgdata, position["AdditionalPweE1"]["Byte"], cnt ) == 1 ):
                licenseInfo[LicenseKey["ADD_PWE_E1"]] = Define["AddPweE1Data"][cnt]
                break
            
        

        # Additional PWE 128E1
        if (getBitValueFromHex( orgdata, position["AdditionalPwe128E1"]["Byte"], position["AdditionalPwe128E1"]["Bit"]) == 1):
            licenseInfo[LicenseKey["ADD_PWE_E1"]] = Define["AddPweE1"]["E1x128"]
        

        # Main Card Redundancy
        licenseInfo[LicenseKey["MAIN_CARD_REDUNDANCY"]] = getBitValueFromHex( orgdata, position["MainCardRedundancy"]["Byte"], position["MainCardRedundancy"]["Bit"])
        # CWDM
        licenseInfo[LicenseKey["CWDM"]] = getBitValueFromHex( orgdata, position["CWDM"]["Byte"], position["CWDM"]["Bit"])
        # Advanced Header Compression
        licenseInfo[LicenseKey["ADV_HEADER_COMPRESS"]] = getBitValueFromHex( orgdata, position["AdvHeaderCompress"]["Byte"], position["AdvHeaderCompress"]["Bit"])
        # DHCP Server / Relay
        licenseInfo[LicenseKey["DHCP_SERVER_RELAY"]] = getBitValueFromHex( orgdata, position["DHCPServerRelay"]["Byte"], position["DHCPServerRelay"]["Bit"])
        # ETH OAM Link
        licenseInfo[LicenseKey["ETH_OAM_LINK"]] = getBitValueFromHex( orgdata, position["EthOamLink"]["Byte"], position["EthOamLink"]["Bit"])

        for i in range(len(licenseInfo)):
            val=''
            if LicenseKeyInv[i]=='RADIO_CAPACITY':
                slot=0
                for el in licenseInfo[i]:
                    slot+=1
                    val+=str(el)+'%'
                    print(LicenseKeyInv[i]+'_S'+str(slot), el, sep=" : ")
            elif LicenseKeyInv[i]=='SFP_PORTUSAGE_OPTION':
                slot=0
                for el in licenseInfo[i]:
                    slot+=1
                    val += str(el)+'%'
                    print(LicenseKeyInv[i]+'_S'+str(slot), el, sep=" : ")
            else:
                val += str(licenseInfo[i]) + '%'
                print(LicenseKeyInv[i],licenseInfo[i],sep=" : " )
            str_licenseInfo += val
        #for i in range(len(licenseInfo)):
        #    print(LicenseKeyInv[i],licenseInfo[i],sep=" : " )
        #for i in range(len(licenseInfo)):
        #    print(i,licenseInfo[i],sep=" : " )
        #return licenseInfo

        return str_licenseInfo


licenseAbility = '0xFF 01 FF 01 FF 01 FF 01 FF 01 FF 01 FF 01 FF 01 01 00 01 00 40 40 0F 1D F8 DF 03 00 03 21 08 05 FF 01 FF 01 FF 01 FF 01'
abils = licenseAbility[2:].replace(" ", "")
abils = 'ff00ff00ff00ff00ff00010001000100010001000802030208410000000400000100010001000100'
print(getAvailabilityData(abils))
