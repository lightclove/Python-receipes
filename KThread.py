# -*- coding: utf-8 -*-
#!/usr/bin/env python2
import sys
from threading import Thread

# Потомок threading.Thread, выполнение которого
# можно завершать извне (Hacked).
class KThread(Thread):
  def __init__(self, *args, **keywords):
    Thread.__init__(self, *args, **keywords)
    self.killed = False

  def start(self):
    """Start the thread."""
    self.__run_backup = self.run
    self.run = self.__run # Force the Thread to install our trace.
    Thread.start(self)

  def __run(self):
    """Hacked run function, which installs the
    trace."""
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup

  def globaltrace(self, frame, why, arg):
    if why == 'call':
      return self.localtrace
    else:
      return None

  def localtrace(self, frame, why, arg):
    if self.killed:
      if why == 'line':
        raise SystemExit()
    return self.localtrace

  def kill(self):
    self.killed = True

class SimpleThread (KThread):
  def __init__ (self, i, time):
    KThread.__init__ (self, name = "Simple")

  def run (self):
    i = 0
    while True:
      # Некие вычислительные действия.
      i = i + 1

import time
A = []
N = 25

while True:
  for i in xrange(N):
    A = A + [SimpleThread (i, time.clock())]
    A[i].start()
    time.sleep(0.5)
    A[i].kill()
    time.sleep(0.5)