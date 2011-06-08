#!/usr/bin/python
# -*- coding: utf-8 -*-

speed_light = 3 * 100000000

import math
from station import Station
import math

speed_light = 300000000

class BTS(Station):
  """Represent a Base Transmiter Station"""
  def __init__(self, x, y, network, ho_margin, ms_txpwr_max, bts_txpwr_max,
  rxlev_min, max_ms_range, l_rxqual_h, l_rxlev_dl_h, l_rxlev_up_h, pe, ge, f):
    Station.__init__(self, x, y)
    self.ms_list = set()
    self.network = network
    self.ho_margin = ho_margin
    self.ms_txpwr_max = ms_txpwr_max
    self.bts_txpwr_max = bts_txpwr_max
    self.rxlev_min = rxlev_min
    self.max_ms_range = max_ms_range
    self.l_rxqual_h = l_rxqual_h
    self.l_rxlev_dl_h = l_rxlev_dl_h
    self.l_rxlev_up_h = l_rxlev_up_h
    self.pe = pe
    self.ge = ge
    self.f = f

    squared_range = ge * pow(speed_light / f / 4 / math.pi, 2) / -120 * pe

    self.nominal_range = 42
    print self.nominal_range

  def link(self, ms):
    """Link a MS"""
    self.ms_list.add(ms)

  def unlink(self, ms):
    """Unlink a MS"""
    self.ms_list.remove(ms)

