#!/usr/bin/python
# -*- coding: utf-8 -*-

from station import Station
from PyQt4 import QtCore
import random
import operator
import math

speed_light = 3 * 100000000
nbsamples = 0

class MS(Station):

  """Represent a Mobile Station"""
  def __init__(self, station_id, x, y, network, p, pe, ge):
    Station.__init__(self, station_id, x, y)
    self.__bts_list = set()
    self.bts = None
    self.pref_network = network
    self.p = p
    self.pe = pe
    self.ge = ge

    self.__bts_mutex = QtCore.QMutex()

    self.__last_move = random.randint(0, 7)

    self.__handover_timer = QtCore.QTimer()
    self.__handover_timer.timeout.connect(self.measure)
    self.set_speed(1)
    self.__handover_timer.start()

  def set_speed(self, speed):
    """Set map speed"""
    self.__handover_timer.setInterval(480/pow(2, speed-1))

  def update_bts_list(self, bts_list):
    """Update known Base Transmiter Station list"""
    self.__bts_mutex.lock()

    self.__bts_list = bts_list

    # Initialize by choosing closest BTS, ins desired network if possible
    btss = [ b for b in self.__bts_list if b.network == self.pref_network ]
    if not btss:
      btss = self.__bts_list
    dists = [ (bts, self.distance_from(bts)) for bts in btss ]
    self.select_bts(min(dists, key=operator.itemgetter(1))[0])

    self.__bts_mutex.unlock()

  def select_bts(self, bts):
    """Select a BTS"""
    if self.bts:
      self.bts.unlink(self)
    self.bts = bts
    self.bts.link(self)


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

  def measure(self):
    self.__bts_mutex.lock()

    nbsamples + 1

    if self.bts is None:
      self.__bts_mutex.unlock()
      return

    #Distances
    distanceMsBts = {}
    for aBts in self.__bts_list:
      distanceMsBts[aBts] = self.distance_from(aBts)

    #rx_lev
    rxlev_dl = self.ge + self.bts.ge - self.pe + (20 * math.log10(speed_light)) - (20 * math.log10(self.bts.f * 1000000)) - (20 * math.log10(4 * math.pi * distanceMsBts[self.bts]))
    rxlev_up = self.ge + self.bts.ge - self.bts.pe + (20 * math.log10(speed_light)) - (20 * math.log10(self.bts.f * 1000000)) - (20 * math.log10(4 * math.pi * distanceMsBts[self.bts]))

    #rx_qual
    I = 0
    for aBts in self.__bts_list:
      if (aBts.f == self.bts.f):
        I += pow(10, aBts.pe/10.)
    cOverI = self.pe / (10 * math.log10(I))

    rxqual_dl = getRxQualFromCOverI(cOverI)

    I = 0
    for aMs in self.bts.ms_list:
      if (aMs.bts.f == self.bts.f):
        I += pow(10, aMs.pe)
    cOverI = self.pe / (10 * math.log10(I))

    rxqual_up = getRxQualFromCOverI(cOverI)

    #rx_lev on other cells
    rxlev_ncell = {}
    for aBts in self.__bts_list:
      rxlev_ncell[aBts] = self.ge + aBts.ge - self.pe + (20 * math.log10(speed_light)) - (20 * math.log10(aBts.f * 1000000)) - (20 * math.log10(4 * math.pi * self.distance_from(aBts)))

    
    if (nbsamples % 32 == 0):
      self.meanValues()

    self.__bts_mutex.unlock()

  def meanValues(self):
    return
  
def getRxQualFromCOverI(cOverI):
  if (cOverI < 1):
    return 7;
  elif (cOverI < 3):
    return 6
  elif (cOverI < 4.5):
    return 5
  elif (cOverI < 5):
    return 4
  elif (cOverI < 6.5):
    return 3
  elif (cOverI < 7.5):
    return 2
  elif (cOverI < 15):
    return 1
  return 0
