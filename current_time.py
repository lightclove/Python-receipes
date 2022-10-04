# import datetime
# class current_time():
#     def __init__(self):
#         print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
import time
def current_time():
    print time.strftime("%Y-%m-%d %H:%M:%S")
    return time.strftime("%Y-%m-%d %H:%M:%S")
#current_time()