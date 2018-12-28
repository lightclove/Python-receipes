//
// Created by bless.grace on 07.12.2018.
//

#include <stdio.h>
#include <Winsnmp.h>

SNMPAPI_STATUS CALLBACK MySnmpCallback(
    HSNMP_SESSION hSession,
    HWND hWnd,
    UINT wMsg,
    WPARAM wParam,
    LPARAM lParam,
    LPVOID lpClientData
)
{
    printf("MySnmpCallback!\n");
    return SNMPAPI_SUCCESS;
}

void SnmpTest()
{
    smiUINT32 nMajorVersion;
    smiUINT32 nMinorVersion;
    smiUINT32 nLevel;
    smiUINT32 nTranslateMode;
    smiUINT32 nRetransmitMode;

    SNMPAPI_STATUS statusStartup = SnmpStartupEx(
        &nMajorVersion,
        &nMinorVersion,
        &nLevel,
        &nTranslateMode,
        &nRetransmitMode
    );

    if (SNMPAPI_SUCCESS == statusStartup)
    {
        printf("  MajorVersion = %u\n", nMajorVersion);
        printf("  MinorVersion = %u\n", nMinorVersion);
        printf("         Level = %u\n", nLevel);
        printf("RetransmitMode = %u\n", nRetransmitMode);
        SnmpSetTranslateMode(SNMPAPI_UNTRANSLATED_V2);
        SnmpGetTranslateMode(&nTranslateMode);
        printf(" TranslateMode = %u\n", nTranslateMode);
    }
    else
    {
        printf("SnmpStartup Failed. (%u)\n", SnmpGetLastError(NULL));
    }

    if (SNMPAPI_SUCCESS == statusStartup)
    {
        HSNMP_SESSION hSession = SnmpCreateSession(NULL, NULL, (SNMPAPI_CALLBACK)&MySnmpCallback, NULL);
        if (SNMPAPI_FAILURE != hSession)
        {
            HSNMP_ENTITY localEntity = SnmpStrToEntity(hSession, "0.0.0.0");
            SNMPAPI_STATUS regStatus = SnmpRegister(hSession, localEntity, NULL, NULL, NULL, SNMPAPI_ON);
            if (SNMPAPI_SUCCESS == regStatus)
            {
                while (TRUE)
                {
                    Sleep(100);
                    if (GetKeyState('A') && 0x8000)
                        break;
                }

                SnmpClose(hSession);
            }
            else
            {
                printf("SnmpRegister Failed. (%u)\n", SnmpGetLastError(hSession));
            }
        }
        else
        {
            printf("SnmpCreateSession Failed. (%u)\n", SnmpGetLastError(NULL));
        }
    }

    if (SNMPAPI_SUCCESS == statusStartup)
    {
        SnmpCleanup();
    }

}

int main(int argc, CHAR* argv[])
{
    SnmpTest();
    return 0;
}