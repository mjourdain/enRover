#!/usr/bin/python
# -*- coding: utf-8 -*-

from station import Station
from PyQt4 import QtCore
import random
import operator
import math
import log

speed_light = 3 * 100000000


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
    self.dtx = random.choice((True, False))

    self.__rxlev_dl = []
    self.__rxlev_up = []
    self.__rxqual_up = []
    self.__rxqual_dl = []

    self.__nb_means_rxlev_up = 0
    self.__nb_means_rxlev_dl = 0
    self.__nb_means_rxqual_up = 0
    self.__nb_means_rxqual_dl = 0
    self.__nb_means_distance = 0

    self.__rxlev_up_mean = []
    self.__rxlev_dl_mean = []
    self.__rxqual_up_mean = []
    self.__rxqual_dl_mean = []
    self.__distanceMsBts_mean = {}
    self.__rxlev_ncell_mean = {}

    self.__nbsamples = -1
    self.__nb_means = -1
    self.__distanceMsBts = {}
    self.__rxlev_ncell = {}
    for aBts in self.__bts_list:
      self.__distanceMsBts[aBts] = []
      self.__rxlev_ncell[aBts] = []


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

    # Dtx ?
    if random.randint(0, 99) is 0:
      self.dtx = not self.dtx

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

    if self.bts is None:
      self.__bts_mutex.unlock()
      return

    self.__nbsamples += 1

    if (self.__nbsamples ==  12):
      self.__nbsamples = 0
      #print self.__distanceMsBts
      #print self.__rxlev_dl
      #print self.__rxlev_up
      #print self.__rxqual_dl
      #print self.__rxqual_up
      #print  self.__rxlev_ncell

      self.meanValues()
    if (self.__nbsamples == 0):
      for aBts in self.__bts_list:
        self.__distanceMsBts[aBts] = []
        self.__rxlev_ncell[aBts] = []


    #Distances
    for aBts in self.__bts_list:
      self.__distanceMsBts[aBts].append(self.distance_from(aBts))

    #rxlev
    self.__rxlev_dl.append(self.ge + self.bts.ge - self.pe + (20 *
math.log10(speed_light)) - (20 * math.log10(self.bts.f * 1000000)) - (20 *
math.log10(4 * math.pi * max(1, self.__distanceMsBts[self.bts][self.__nbsamples]))))
    self.__rxlev_up.append(self.ge + self.bts.ge - self.bts.pe + (20 *
math.log10(speed_light)) - (20 * math.log10(self.bts.f * 1000000)) - (20 *
math.log10(4 * math.pi * max(1, 3 * self.__distanceMsBts[self.bts][self.__nbsamples]))))

    #rxqual
    I = 0
    for aBts in self.__bts_list:
      if (aBts.f == self.bts.f):
        I += pow(10, aBts.pe/10.)
    cOverI = self.pe / (10 * math.log10(I))

    self.__rxqual_dl.append(getRxQualFromCOverI(cOverI))

    I = 0
    for aMs in self.bts.ms_list:
      if (aMs.bts.f == self.bts.f):
        I += pow(10, aMs.pe)
    if(I != 0):
      cOverI = self.pe / (10 * math.log10(I))
      self.__rxqual_up.append(getRxQualFromCOverI(cOverI))
    else:
      self.__rxqual_up.append(0)

    #rxlev on other cells
    for aBts in self.__bts_list:
      toto = (20 * math.log10(speed_light))
      tata = (20 * math.log10(aBts.f * 1000000))
      tutu = (20 * math.log10(4 * math.pi * 3 * max(1, self.distance_from(aBts))))

      self.__rxlev_ncell[aBts].append(self.ge + aBts.ge - self.pe + toto - tata
- tutu)


    self.__bts_mutex.unlock()

  def meanValues(self):
    lg = log.AtomicLog()
    lg.info("==============================" )
    lg.info("MS " , self.id , ", measure phase")

    nb_values_rxlev_up = 12
    nb_values_rxlev_dl = 12
    nb_values_rxqual_up = 7
    nb_values_rxqual_dl = 7
    nb_values_distance = 10

    self.__nb_means_rxlev_up += 1
    self.__nb_means_rxlev_dl += 1
    self.__nb_means_rxqual_up += 1
    self.__nb_means_rxqual_dl += 1
    self.__nb_means_distance += 1

    if (self.__nb_means_rxlev_up == 0):
      self.__rxlev_up_mean = []
    if (self.__nb_means_rxlev_dl == 0):
      self.__rxlev_dl_mean = []
    if (self.__nb_means_rxqual_up == 0):
      self.__rxqual_up_mean = []
    if (self.__nb_means_rxqual_dl == 0):
      self.__rxqual_dl_mean = []
    if (self.__nb_means_distance == 0):
      self.__distanceMsBts_mean = {}
      for aBts in self.__bts_list:
        self.__distanceMsBts_mean[aBts] = []



    if (self.__nb_means_rxlev_up > nb_values_rxlev_up -1):
      self.__nb_means_rxlev_up = 0
      self.__rxlev_up_mean = []
    if (self.__nb_means_rxlev_dl > nb_values_rxlev_dl -1):
      self.__nb_means_rxlev_dl = 0
      self.__rxlev_dl_mean = []
    if (self.__nb_means_rxqual_up > nb_values_rxqual_dl -1):
      self.__nb_means_rxlev_up = 0
      self.__rxqual_up_mean = []
    if (self.__nb_means_rxqual_dl > nb_values_rxqual_up -1):
      self.__nb_means_rxqual_dl = 0
      self.__rxqual_dl_mean = []
    if (self.__nb_means_distance > nb_values_distance -1):
      self.__nb_means_distance = 0
      self.__distanceMsBts_mean = {}
      for aBts in self.__bts_list:
        self.__distanceMsBts_mean[aBts] = []



    for val in self.__rxlev_dl:
      try:
        self.__rxlev_dl_mean[self.__nb_means_rxlev_dl] += val
      except IndexError:
        self.__rxlev_dl_mean.append(val)
    self.__rxlev_dl_mean[self.__nb_means_rxlev_dl] /= 12
    lg.info("rxlev_dl_mean : " , self.__rxlev_dl_mean[self.__nb_means_rxlev_dl])

    for val in self.__rxlev_up:
      try:
        self.__rxlev_up_mean[self.__nb_means_rxlev_up] += val
      except IndexError:
        self.__rxlev_up_mean.append(val)
    self.__rxlev_up_mean[self.__nb_means_rxlev_up] /= 12
    lg.info("rxlev_up_mean : " , self.__rxlev_up_mean[self.__nb_means_rxlev_up])

    for val in self.__rxqual_dl:
      try:
        self.__rxqual_dl_mean[self.__nb_means_rxqual_dl] += val
      except IndexError:
        self.__rxqual_dl_mean.append(val)
    self.__rxqual_dl_mean[self.__nb_means_rxqual_dl] /= 12
    lg.info("rxqual_dl_mean : " , self.__rxqual_dl_mean[self.__nb_means_rxqual_dl])

    for val in self.__rxqual_up:
      try:
        self.__rxqual_up_mean[self.__nb_means_rxqual_up] += val
      except IndexError:
        self.__rxqual_up_mean.append(val)
    self.__rxqual_up_mean[self.__nb_means_rxqual_up] /= 12
    lg.info("rxqual_up_mean : " , self.__rxqual_up_mean[self.__nb_means_rxqual_up])

    for aBts in self.__bts_list:
      for val in self.__distanceMsBts[aBts]:
        try:
          self.__distanceMsBts_mean[aBts][self.__nb_means_distance] += val
        except IndexError:
          self.__distanceMsBts_mean[aBts].append(val)
        except KeyError:
          self.__distanceMsBts_mean[aBts] = [val]
      self.__distanceMsBts_mean[aBts][self.__nb_means_distance] /= 12
      lg.info("distanceMsBts_mean[" , aBts.id , "] : " , self.__distanceMsBts_mean[aBts][self.__nb_means_distance])


    for aBts in self.__bts_list:
      self.__rxlev_ncell_mean[aBts] = 0
      for val in self.__rxlev_ncell[aBts]:
        self.__rxlev_ncell_mean[aBts] += val
      self.__rxlev_ncell_mean[aBts] /= 12
      lg.info("rxlev_ncell_mean[" , aBts.id , "] : " , self.__rxlev_ncell_mean[aBts])

    pwr_c_d = self.bts.bts_txpwr_max - self.bts.pe
    pgbt = {}
    for aBts in self.__bts_list:
      pgbt[aBts] = (min(self.bts.ms_txpwr_max, self.p) -
self.__rxlev_dl_mean[self.__nb_means_rxlev_dl] -
pwr_c_d) - (min(aBts.ms_txpwr_max, self.p) - self.__rxlev_ncell_mean[aBts])

    neighbour_list = []
    for aBts in self.__bts_list:
      pa = aBts.ms_txpwr_max - self.p
      if (self.__rxlev_ncell_mean[aBts] > (aBts.rxlev_min + max(self.p, pa))):
        val_neighbour_list = pgbt[aBts] - self.bts.ho_margin
        if (val_neighbour_list > 0):
          neighbour_list.append((aBts, val_neighbour_list))
    neighbour_list.sort(key = operator.itemgetter(1))

    lg.info("neighbour_list : [" , ", ".join(
                  [ str(e[0].id) + ": " + str(e[1]) for e in neighbour_list]),
                  "]")

    nb_values_rxlev_up = 12
    nb_values_rxlev_dl = 12
    nb_values_rxqual_up = 7
    nb_values_rxqual_dl = 7
    nb_values_distance = 10


    if(len(self.__rxlev_up_mean) == nb_values_rxlev_up and
len(self.__rxlev_dl_mean) == nb_values_rxlev_dl and len(self.__rxqual_up_mean)
== nb_values_rxqual_up and len(self.__rxqual_dl_mean) == nb_values_rxqual_dl and
len(self.__distanceMsBts_mean) == nb_values_distance):
      print("bleh")

      for btsTuple in neighbour_list:
        if (self.__rxlev_up_mean[self.__nb_means_rxlev_up] < self.bts.l_rxlev_up_h
and self.__rxlev_dl_mean[self.__nb_means_rxlev_dl] < self.bts.l_rxlev_dl_h
and self.__rxqual_up_mean[self.__nb_means_rxqual_up] > self.bts.l_rxqual_h and
self.__rxqual_dl_mean[self.__nb_means_rxqual_dl] > self.bts.l_rxqual_h and
self.__distanceMsBts_mean[btsTuple[0]] > self.bts.max_ms_range and pgbt[btsTuple[0]] >
self.bts.ho_margin and pgbt[btsTuple[0]] > 0):
          if(btsTuple[0] != self.bts):
            print ("MS", self.id, " handover from BTS", self.bts.id, " to BTS", btsTuple[0].id)
            self.bts = btsTuple[0]

    lg.info("==============================" )
    lg.info("" )







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
