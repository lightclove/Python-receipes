#!/usr/bin/python
import ctypes
import sys
import os

def is_admin_win():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def is_admin_linux(): # Не реализован механизм получения root-прав
    if not os.geteuid() == 0:
        print("\nOnly root can run this script\n")
        return False
    return True
