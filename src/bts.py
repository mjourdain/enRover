#!/usr/bin/python
# -*- coding: utf-8 -*-

class BTS:
  def __init__(self, x, y, network, ho_margin, ms_txpwr_max, bts_txpwr_max,
  rxlev_min, max_ms_range, l_rxqual_h, l_rxlev_dl_h, l_rxlev_up_h):
    self.pos_x = x
    self.pos_y = y
    self.network = network
    self.ho_margin = ho_margin
    self.ms_txpwr_max = ms_txpwr_max
    self.bts_txpwr_max = bts_txpwr_max
    self.rxlev_min = rxlev_min
    self.max_ms_range = max_ms_range
    self.l_rxqual_h = l_rxqual_h
    self.l_rxlev_dl_h = l_rxlev_dl_h
    self.l_rxlev_up_h = l_rxlev_up_h

