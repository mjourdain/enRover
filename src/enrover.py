#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import os
import time
from PyQt4 import QtGui, QtCore
from carte import Carte
from ms import MS
from bts import BTS
import log

LOG_DIR = "log"

app = QtGui.QApplication(sys.argv)
args = QtCore.QCoreApplication.arguments()

carte = Carte(800, 600)

if (len(args) >= 2):
  carte.load_file(args[1])

if (len(args) >= 3):
  carte.set_speed(int(args[2]))


if not os.path.exists(LOG_DIR):
  os.makedirs(LOG_DIR)

log.LogFile.outFile = file(LOG_DIR + time.strftime("/%F_%T.log"), "w")

carte.start_moving_ms()

app.exec_()

