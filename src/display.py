#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ms import MS
from bts import BTS

class Display(QtGui.QMainWindow):
  """Map display class"""

  def __init__(self, width, height):
    QtGui.QMainWindow.__init__(self)

    self.__pix = QtGui.QPixmap(width, height)
    self.__paint = QtGui.QPainter(self.__pix)

    self.__label = QtGui.QLabel()
    self.__label.resize(width, height)

    self.setCentralWidget(self.__label)
    self.adjustSize()

    self.__bts_pen = QtGui.QPen()
    self.__bts_pen.setWidth(3)
    self.__ms_pen1 = QtGui.QPen()
    self.__ms_pen1.setWidth(7)
    self.__ms_pen2 = QtGui.QPen()
    self.__ms_pen2.setWidth(1)
    self.__ms_pen2.setColor(QtGui.QColor((0, 0, 0)))
    paintFont = QtGui.QFont()
    paintFont.setPointSizeF(7.0)
    self.__paint.setFont(paintFont);

    self.__toolbar = QtGui.QToolBar()
    self.addToolBar(self.__toolbar)

    style =  self.style()
    loadIcon = style.standardIcon(QtGui.QStyle.SP_DirOpenIcon)
    self.action_load = self.__toolbar.addAction(loadIcon, "load file")
    reloadIcon = style.standardIcon(QtGui.QStyle.SP_BrowserReload)
    self.action_reload = self.__toolbar.addAction(reloadIcon, "reload file")
    self.__toolbar.addSeparator()

    pauseIcon = style.standardIcon(QtGui.QStyle.SP_MediaPause)
    self.action_play = self.__toolbar.addAction(pauseIcon, "play / pause")

    self.clean()
    self.update()

  def clean(self):
    """Clean BTS painter"""
    self.__pix.fill(QtGui.QColor(191, 191, 191))

  def draw(self, elem, color):
    """Draw an element"""
    if isinstance(elem, BTS):
      self.__draw_bts(elem, color)
    elif isinstance(elem, MS):
      self.__draw_ms(elem, color)

  def __draw_bts(self, bts, color):
    """Draw a BTS"""
    self.__bts_pen.setColor(color)
    self.__paint.setPen(self.__bts_pen)
    self.__paint.drawLine(bts.pos_x, bts.pos_y, bts.pos_x, bts.pos_y - 6)
    self.__paint.drawLine(bts.pos_x, bts.pos_y - 6, bts.pos_x - 3, bts.pos_y - 8)
    self.__paint.drawLine(bts.pos_x, bts.pos_y - 6, bts.pos_x + 3, bts.pos_y - 8)
    if bts.network == "GSM":
      self.__paint.drawText(bts.pos_x+5, bts.pos_y+5, "G")
    else:
      self.__paint.drawText(bts.pos_x+5, bts.pos_y+5, "U")

  def __draw_ms(self, ms, color):
    """Draw a MS"""
    self.__ms_pen1.setColor(color)
    self.__paint.setPen(self.__ms_pen1)
    self.__paint.drawEllipse(ms.pos_x-2, ms.pos_y-2, 5, 5)

    if ms.pref_network != "GSM":
      self.__paint.setPen(self.__ms_pen2)
      self.__paint.drawEllipse(ms.pos_x-5, ms.pos_y-5, 11, 11)

  def update(self):
    """Update display from current map"""
    self.__label.setPixmap(self.__pix)

  def resize_(self, width, height):
    """Resize display size"""
    self.__paint = None
    self.__pix = QtGui.QPixmap(width, height)
    self.__paint = QtGui.QPainter(self.__pix)

    self.__label = QtGui.QLabel()
    self.__label.resize(width, height)

    self.setCentralWidget(self.__label)
    self.adjustSize()

