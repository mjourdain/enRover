#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ms import MS
from bts import BTS
from display import Display

class Carte:
  def __init__(self, width=800, height=600):
    (self.__width, self.__height) = (width, height)
    self.__display = Display(width, height)
    self.__bts = {}
    self.__ms = set()
    self.__color_index = 0
    self.__filename = None

    self.__display.action_load.triggered.connect(self.load_file)
    self.__display.action_reload.triggered.connect(self.reload_file)
    self.__display.action_play.triggered.connect(self.toggle_moving_ms)

    self.__move_timer = QtCore.QTimer()
    self.__move_timer.timeout.connect(self.movems)
    self.__move_timer.setInterval(50)

    self.__display.show()

  def add(self, elem):
    # Add a BTS and update all MS
    if isinstance(elem, BTS):
      idx_color = sum([ e.network == elem.network for e in self.__bts ])
      color = get_color(idx_color, elem.network == "GSM")
      self.__bts[elem] = QtGui.QColor(*color)
      bts_set = set(self.__bts.keys())
      for ms in self.__ms:
        ms.update_bts_set(bts_set)

    # Add a MS and update it with BTS list
    elif isinstance(elem, MS):
      self.__ms.add(elem)
      elem.update_bts_list(set(self.__bts.keys()))

    else:
      return

    self.__update_display()

  def __update_display(self):
    self.__display.clean()

    for (bts, color) in self.__bts.iteritems():
      self.__display.draw(bts, color)
    for ms in self.__ms:
      self.__display.draw(ms, self.__bts[ms.bts])

    self.__display.update()

  def refresh(self):
    self.__update_display()

  def movems(self):
    for ms in self.__ms:
      ms.random_move(self.__width-1, self.__height-1)
    self.__update_display()

  def start_moving_ms(self):
    self.__move_timer.start()

  def toggle_moving_ms(self):
    if self.__move_timer.isActive():
      self.__move_timer.stop()
    else:
      self.__move_timer.start()

  def load_file(self, filename=None):
    if not filename:
      filename = QtGui.QFileDialog.getOpenFileName()

    self.__filename = filename
    self.__load_file()

  def reload_file(self):
    self.__load_file()

  def __load_file(self):
    if not self.__filename:
      return

    print self.__filename



def get_color(idx, low_value = False):
  if not low_value:
    saturation = 1
    value = 1
  else:
    saturation = 0.9
    value = 0.7

  hue = (idx % 6) * 60

  if (idx % 12) >= 6:
    hue += 30

  return hsv2rgb(hue%360, saturation, value)


def hsv2rgb(hue, saturation, value):
  if (hue < 0) or (hue > 360):
    return (0, 0, 0)
  if (saturation < 0) or (saturation > 1):
    return (0, 0, 0)
  if (value < 0) or (saturation > 1):
    return (0, 0, 0)

  chroma = value * saturation
  hue_60 = hue / 60.
  x = chroma * (1 - abs(hue_60 % 2 - 1))
  m = value - chroma
  chroma = int((chroma + m) * 255)
  x = int((x + m) * 255)
  m = int(m * 255)

  if (hue_60 < 1):
    rgb = (chroma, x, m)
  elif (hue_60 < 2):
    rgb = (x, chroma, m)
  elif (hue_60 < 3):
    rgb = (m, chroma, x)
  elif (hue_60 < 4):
    rgb = (m, x, chroma)
  elif (hue_60 < 5):
    rgb = (x, m, chroma)
  elif (hue_60 < 6):
    rgb = (chroma, m, x)

  return rgb

