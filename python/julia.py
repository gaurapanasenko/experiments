#!/usr/bin/env python3
#import matplotlib.pyplot as plt
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
#from scipy.integrate import odeint

minIters = 150
maxIters = 200
sz = np.array([400,400])
pts = np.zeros(((maxIters-minIters)*sz[0]*sz[1], 3))
pts_i = 0
minV = np.array([-3,-1])
maxV = np.array([1,1])
#minV = np.array([-0.150724643046,-0.930293062763])
#maxV = np.array([-0.069501700630,-0.902966360950])
inf = 4

def prop(x):
    return (maxV-minV)*x/sz+minV


for i in range(sz[0]):
    for j in range(sz[1]):
        cords = prop(np.array([i, j], dtype="float"))
        z = complex(0, 0)
        c = complex(cords[0], cords[1])
        for k in range(maxIters):
            last_z = z
            z = z*z + c
            try:
                cur_abs = abs(z)
                if cur_abs > inf:
                    raise ValueError
            except:
                #if k <= 10:
                #    continue
                #pts[pts_i] = np.array([c.imag, c.real, k])
                #pts_i+=1
                break
            if k > minIters:
                pts[pts_i] = np.array([c.imag, c.real, abs(z)])
                pts_i+=1

print("builded")

#fig = plt.figure()
#ax = plt.axes(projection='3d')
#ax.scatter3D(pts[:pts_i,0], pts[:pts_i,1], pts[:pts_i,2], s=1, alpha=0.75)
#plt.show()

app = pg.mkQApp("GLScatterPlotItem Example")
w = gl.GLViewWidget()
w.opts['distance'] = 20
w.show()
w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
sp1 = gl.GLScatterPlotItem(pos=pts[:pts_i], size=1, color=(0.2, 0.8, 0.2, 0.8))
sp1.translate(0.930293062763, 0.902966360950, 0)
w.addItem(sp1)

QtGui.QApplication.instance().exec_()

