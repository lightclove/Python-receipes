#!/usr/bin/env python
import os
import signal
import time

def sigint_handler(signum, frame):
    print(os.getpid())
    print 'CTRL + C/Z Pressed App is now killed!'
    os.abort()
    #os.kill(os.getpid(),9)
signal.signal(signal.SIGINT, sigint_handler)

########################################################################################################################

# def sigterm_handler(signum, frame):
#     print(os.getpid())
#     print('Signal handler called with signal', signum)
#     raise SystemExit(1)
# signal.signal(signal.SIGTERM, sigterm_handler)
########################################################################################################################

# def sigtstp_handler(signum, frame):
#     print(os.getpid())
#     print('Signal handler called with signal', signum)
#     #raise SystemExit(1)
# signal.signal(signal.SIGTSTP, sigtstp_handler)
########################################################################################################################

# def main():
#     while True:
#         print '.'
#         time.sleep(1)
#
# ##########
#
# if __name__ == "__main__":
#     main()