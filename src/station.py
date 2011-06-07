#!/usr/bin/python
# -*- coding: utf-8 -*-

import math

class Station:
  """Represent a station"""
  def __init__(self, x, y):
    self.pos_x = x
    self.pos_y = y

  def squared_distance_from(self, elem):
    """Get squared distance from another station"""
    if isinstance(elem, Station):
      return (self.pos_x - elem.pos_x)**2 + (self.pos_y - elem.pos_y)**2

  def distance_from(self, elem):
    """Get distance from another station"""
    if isinstance(elem, Station):
      return math.sqrt(self.squared_distance_from(elem))

