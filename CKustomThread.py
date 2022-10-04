
"""
    Потомок threading.Thread, выполнение которого можно завершать извне (Hacked):
    https://www.linux.org.ru/forum/development/5632316?cid=5632368
"""
import sys
import threading
from threading import Thread


class CKustomThread(Thread):

  def __init__(self, *args, **keywords):
    Thread.__init__(self, *args, **keywords)
    self.killed = False
########################################################################################################################

  def start(self):
    """ Start the thread. """
    self.__run_backup = self.run
    self.run = self.__run # Force the Thread to install our trace.
    Thread.start(self)
    print ('Thread with name ' + threading.currentThread().getName() + ' started')
########################################################################################################################

  def __run(self):
    """ Hacked run function, which installs the trace. """
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup
########################################################################################################################

  def globaltrace(self, frame, why, arg):
    if why == 'call':
      return self.localtrace
    else:
      return None
#######################################################################################################################

  def localtrace(self, frame, why, arg):
    if self.killed:
      if why == 'line':
        raise SystemExit()
    return self.localtrace
########################################################################################################################

  def kill(self):
    self.killed = True
    print("Thread with name " + threading.currentThread().getName() + " killed")
    print()
########################################################################################################################
class CKustomThreadTester(CKustomThread):
  def __init__ (self, i, time):
    CKustomThread.__init__ (self, name ="Custom thread")

  def run (self):
    i = 0
    while True:
      #Н екие вычислительные действия:
      i = i + 1
if __name__ == '__main__':
  print()
  print(u"Program started...")
  import time

  a = CKustomThreadTester (1, time.perf_counter())
  b = CKustomThreadTester (1, time.perf_counter())

  a.start()
  a.setName("A")
  b.start()
  b.setName("B")
  time.sleep(1)

  a.kill()
  b.kill()