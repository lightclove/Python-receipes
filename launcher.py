import subprocess

import Snmp_Handler
import sys
import psycopg2
def main():
    """
    The main entry point of the application
    """

    subprocess.call("python Snmp_Handler.py ")
    #subprocess.call("python Snmp_Trap.py ")


    #UDP_Server.init();
if __name__ == "__main__":

    main()
    sys.exit()