#!/usr/bin/python
# -*- coding: utf-8 -*-

class Station:
  """Represent a station"""
  def __init__(self, x, y):
    self.pos_x = x
    self.pos_y = y

  def distance_from(self, elem):
    """Get distance from another station"""
    if isinstance(elem, Station):
      return (self.pos_x - elem.pos_x)**2 + (self.pos_y - elem.pos_y)**2

