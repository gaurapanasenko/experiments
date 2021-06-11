#!/usr/bin/env python3

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

print("ready")
pts = np.fromfile("out.bin", dtype=np.float32).reshape((-1,3))
print("readed")
print(pts)

app = pg.mkQApp("GLScatterPlotItem Example")
w = gl.GLViewWidget()
w.opts['distance'] = 20
w.show()
w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
sp1 = gl.GLScatterPlotItem(pos=pts, size=2, color=(0.2, 0.8, 0.2, 0.8))
sp1.translate(0.930293062763, 0.902966360950, 0)
w.addItem(sp1)

QtGui.QApplication.instance().exec_()
