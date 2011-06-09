#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
from PyQt4 import QtGui, QtCore
from carte import Carte
from ms import MS
from bts import BTS

app = QtGui.QApplication(sys.argv)
args = QtCore.QCoreApplication.arguments()

carte = Carte(800, 600)

if (len(args) >= 2):
  carte.load_file(args[1])

if (len(args) >= 3):
  carte.set_speed(args[2])

carte.start_moving_ms()

app.exec_()

