# usage: python USP_server_example.py <host> <port>

import sys
import os
import time
from unix_socket_protocol import USP_SERVER

def callback_func(json_str):
    print(json_str)

if __name__ == "__main__":
    server = USP_SERVER(sys.argv[1], callback_func, 10)
    server.start_server()
    print ("server started")
    time.sleep(10)
    print ("after 10s")
    server.stop_server()
    print ("server stopped")