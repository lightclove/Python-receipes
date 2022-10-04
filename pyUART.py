"""
https://github.com/nhivp/Serial-Raspberry-Pi-3

Using UART Serial with Raspberry Pi 3
Default serial is configured for Raspberry Pi 3
/dev/ttyS0: Serial for Pinout
/dev/ttyAMA0: Serial for Bluetooth
Refer to the following step in usage:
Connect the UART to pinout on Raspberry Pi 3 (Pin 14, 15)
Open serial /dev/ttyS0 for using
Some useful command
dmesg | grep tty
ls -l /dev/ | grep tty
______________________________________________________________________
testSrial.py
"""
import serial
import struct

def main():
    port = serial.Serial("/dev/ttyACM0", baudrate=115200, timeout=3.0)
    port.write(struct.pack('>B', 1))
    print('Send OK')
    port.close()

if __name__ == '__main__':
    main()
