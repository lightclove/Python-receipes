# -*- coding: utf-8 -*-
#!/usr/bin/env python2
########################################################################################################################
# Имя модуля: INT_HEX_BYTES_CONVERTER.
# Назначение: конвертер значений. No external libraries are required, and it works natively with Python 2 and 3.
# Автор: http://opentechnotes.blogspot.com/2014/04/convert-values-to-from-integer-hex.html
# Создан: 15.04.2019
# Изменен:
# Лицензия: MIT www.opensource.org/licenses/mit-license.php
########################################################################################################################


def bytes2int(str):
 return int(str.encode('hex'), 16)

def bytes2hex(str):
 return '0x'+str.encode('hex')

def int2bytes(i):
 h = int2hex(i)
 return hex2bytes(h)

def int2hex(i):
 return hex(i)

def hex2int(h):
 if len(h) > 1 and h[0:2] == '0x':
  h = h[2:]

 if len(h) % 2:
  h = "0" + h

 return int(h, 16)

def hex2bytes(h):
 if len(h) > 1 and h[0:2] == '0x':
  h = h[2:]

 if len(h) % 2:
  h = "0" + h

 return h.decode('hex')

if __name__ == '__main__':
    print hex2bytes("0xC2")
