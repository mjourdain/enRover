#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore

INFO = 1
DEBUG = 2

nb_handover = 0

class LogFile:
  __levels = (DEBUG, INFO)
  __mutex = QtCore.QMutex()

  level = INFO
  outFile = sys.stdout

  @classmethod
  def info(cls, message):
    cls.__mutex.lock()
    if cls.level >= INFO and cls.outFile:
      cls.outFile.write(message)
      cls.outFile.flush()
    cls.__mutex.unlock()

  @classmethod
  def debug(cls, message):
    cls.__mutex.lock()
    if cls.level >= DEBUG and cls.outFile:
      cls.outFile.write(message)
      cls.outFile.flush()
    cls.__mutex.unlock()

  @classmethod
  def printList(cls, messages):
    cls.__mutex.lock()
    if cls.outFile:
      cls.outFile.writelines([ m[1] for m in messages if cls.level >= m[0] ])
      cls.outFile.flush()
    cls.__mutex.unlock()

class AtomicLog:
  def __init__(self):
    self.__messages = []

  def info(self, *message):
    self.__messages.append((INFO, " ".join([ str(m) for m in message]) + "\n"))

  def debug(self, *message):
    self.__messages.append((DEBUG, " ".join([ str(m) for m in message]) + "\n"))

  def print_(self):
    LogFile.printList(self.__messages)
    self.__messages = []

  def __del__(self):
    self.print_()

