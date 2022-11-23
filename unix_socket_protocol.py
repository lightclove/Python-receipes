# -*- coding: UTF-8 -*-
# !/usr/bin/env python
import os
import sys
import time
import socket
import struct
import threading
import traceback

"""
message format:
  4 bytes of unsigned int for length of string follows.
  utf-8 encoded string with length of which proviced by first 4 bytes(not including NULL, end of array)
"""

class USP_SERVER:
    """
    param:
      sock_addr: address of unix socket. ex) /tmp/sock_addr_0
      callback_func: callback function for receiving data from client
                     interface --> func(json_str)
    """

    def __init__(self, sock_addr, callback_func, worker_num=1):
        self.is_stop_mode = False
        self.sock_addr = sock_addr
        self.callback_func = callback_func
        self.worker_num = worker_num
        self.__unbind_sock()
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(sock_addr)
        self.sock.settimeout(1)
        self.sock.listen(worker_num * 2)

    def __unbind_sock(self):
        try:
            os.unlink(self.sock_addr)
        except OSError:
            if os.path.exists(self.sock_addr):
                raise

    def start_server(self):

        self.worker_thread = []
        for _ in range(self.worker_num):
            thread = threading.Thread(target=self.__thread_func, args=())
            thread.start()
            self.worker_thread.append(thread)

    def stop_server(self):

        self.is_stop_mode = True
        for thread in self.worker_thread:
            thread.join()
        self.__unbind_sock()

    def __thread_func(self):

        while not self.is_stop_mode:
            try:
                connection, client_address = self.sock.accept()
                data_len_buf = connection.recv(4)
                data_len = struct.unpack('>l', data_len_buf)[0]
                data_buf = connection.recv(data_len)
                data = struct.unpack('>{}s'.format(data_len), data_buf)[0]
                self.callback_func(data)
                connection.close()

            except socket.timeout:
                pass

            except:
                traceback.print_exc()

class USP_CLIENT:

    def __init__(self, sock_addr):
        self.sock_addr = sock_addr
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    def send(self, message):
        self.sock.connect(self.sock_addr)
        msg_len = len(message)
        data_len_buf = struct.pack(">l", msg_len)
        message_buf = struct.pack(">{}s".format(msg_len), message)
        send_buf = data_len_buf + message_buf
        self.sock.sendall(send_buf)