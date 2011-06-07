#!/usr/bin/python
# -*- coding: utf-8 -*-

from station import Station
from PyQt4 import QtCore
import random
import operator

class MS(Station):
  """Represent a Mobile Station"""
  def __init__(self, x, y, network, p):
    Station.__init__(self, x, y)
    self.__bts_list = set()
    self.bts = None
    self.pref_network = network
    self.p = p

    self.__bts_mutex = QtCore.QMutex()

    self.__last_move = random.randint(0, 7)

    self.__handover_timer = QtCore.QTimer()
    self.__handover_timer.timeout.connect(self.handover)
    self.__handover_timer.setInterval(480)
    self.__handover_timer.start()

  def update_bts_list(self, bts_list):
    """Update known Base Transmiter Station list"""
    self.__bts_mutex.lock()

    self.__bts_list = bts_list

    # Initialize by choosing closest BTS, ins desired network if possible
    btss = [ b for b in self.__bts_list if b.network == self.pref_network ]
    if not btss:
      btss = self.__bts_list
    dists = [ (bts, self.distance_from(bts)) for bts in btss ]
    self.bts = min(dists, key=operator.itemgetter(1))[0]

    self.__bts_mutex.unlock()

  def random_move(self, max_x, max_y):
    """Move Mobile Station randomly"""
    dir_change = random.randint(0, 300)

    # Change direction ?
    if dir_change in range(5):
      self.__last_move = (self.__last_move + 7) % 8
    elif dir_change in range(5, 10):
      self.__last_move = (self.__last_move + 1) % 8
    elif dir_change in range(10, 12):
      self.__last_move = (self.__last_move + 6) % 8
    elif dir_change in range(12, 14):
      self.__last_move = (self.__last_move + 2) % 8
    elif dir_change in range(14, 80):
      return

    # Move
    if self.__last_move in (7, 0, 1):
      self.pos_x += 1
    if self.__last_move in (1, 2, 3):
      self.pos_y += 1
    if self.__last_move in (3, 4, 5):
      self.pos_x -= 1
    if self.__last_move in (5, 6, 7):
      self.pos_y -= 1

    # MS on border of the map : go back !
    if self.pos_x < 0:
      self.pos_x = 0
      self.__last_move = (self.__last_move + 4) % 8
    elif self.pos_x > max_x:
      self.pos_x = max_x
      self.__last_move = (self.__last_move + 4) % 8
    elif self.pos_y < 0:
      self.pos_y = 0
      self.__last_move = (self.__last_move + 4) % 8
    elif self.pos_y > max_y:
      self.pos_y = max_y
      self.__last_move = (self.__last_move + 4) % 8

  def handover(self):
    """Check if we need do do an handover"""
    self.__bts_mutex.lock()

    if self.bts is None:
      return

    self.__bts_mutex.unlock()

