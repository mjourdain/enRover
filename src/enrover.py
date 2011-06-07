#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
from PyQt4 import QtGui
from carte import Carte
from ms import MS
from bts import BTS

app = QtGui.QApplication(sys.argv)

carte = Carte(800, 600)

#carte.load_file("conf.xml")

#carte.add(BTS(20, 400, "GSM"))
#carte.add(BTS(130, 210, "GSM"))
#carte.add(BTS(80, 45, "UMTS"))
#carte.add(BTS(400, 300, "UMTS"))

#carte.add(MS(random.randint(0, 799), random.randint(0, 599), "GSM"))
#carte.add(MS(random.randint(0, 799), random.randint(0, 599), "GSM"))
#carte.add(MS(random.randint(0, 799), random.randint(0, 599), "GSM"))
#carte.add(MS(random.randint(0, 799), random.randint(0, 599), "UMTS"))
#carte.add(MS(random.randint(0, 799), random.randint(0, 599), "UMTS"))
#carte.add(MS(random.randint(0, 799), random.randint(0, 599), "UMTS"))

carte.start_moving_ms()

app.exec_()

