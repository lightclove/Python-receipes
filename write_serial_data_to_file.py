# -*- coding: UTF-8 -*-
# !/usr/bin/env python2
 
import time, serial
 
#ser = serial.Serial("/dev/ttyUSB0")
#ser = serial.Serial("/dev/ttyS0")
ser = serial.Serial("COM8")
#ser.baudrate = 9600
#ser.baudrate = 115200
ser.baudrate = 57600
 
filename = 'DATA-%4d-%02d-%02d-%02d-%02d-%02d.csv' % time.localtime()[0:6]
 
f = open(filename, 'w')
while True :
  line = ser.readline()
  f.write(line)
  print line, # Запятая нужна!