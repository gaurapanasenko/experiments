import numpy as np
import math
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

SMALL_COEF = 0.4
EXP_COEF = 0

GREEN_COLOR = np.array([0.2,0.8,0.2,1])
BROWN_COLOR = np.array([0.588,0.294,0,1])

AXIOM = "F++F++F"
NEW = {"F": "F-F++F-F"}
THETA = 180 / 3
DATA_START = np.array([450, 50, 90], dtype="float")
LENGTH = 2
ITERATIONS = 5

AXIOM = "FB"
NEW = {"F": "F&&-------[F]+[F]+[F]++[F]+[F]+[F]+[F]^^-------[F]+[F]+[F]++[F]+[F]+[F]+[F]"}
THETA = np.pi * 360 / 8 / 180
DATA_START = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype="float")
LENGTH = 700
ITERATIONS = 4


AXIOM = "FB"
NEW = {"B": "FFF[&+B][&&+B][&&&+B][&&&&+B][&&&&&+B][&&&&&&+B][&&&&&&&+B][&&&&&&&&+B]B"}
THETA = np.pi * 360 / 8 / 180
DATA_START = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype="float")
LENGTH = 60
ITERATIONS = 5


AXIOM = "FB"
NEW = {
    "B": "FF[&+FBE][&&+FBE][&&&+FBE][&&&&+FBE][&&&&&+FBE][&&&&&&+FBE][&&&&&&&+FBE][&&&&&&&&+FBE][FFBE]",
    "EEEE": "[&+F][&&+F][&&&+F][&&&&+F][&&&&&+F][&&&&&&+F][&&&&&&&+F][&&&&&&&&+F]"
}
THETA = np.pi * 360 / 8 / 180
DATA_START = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype="float")
LENGTH = 200
ITERATIONS = 4
SMALL_COEF = 0.4


AXIOM = "FB"
NEW = {
    "B": "FB[&+FBE][&&+FBE][&&&+FBE][&&&&+FBE][&&&&&+FBE][&&&&&&+FBE][&&&&&&&+FBE][&&&&&&&&+FBE][FBE]",
    "EEEE": "[&+F][&&+F][&&&+F][&&&&+F][&&&&&+F][&&&&&&+F][&&&&&&&+F][&&&&&&&&+F]"
}
THETA = np.pi * 360 / 8 / 180
DATA_START = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype="float")
LENGTH = 200
ITERATIONS = 4
SMALL_COEF = 0.4

STATES = []
DATA = DATA_START.copy()

POINTS = None
POINT_LAST = 0


def rot_x(theta):
    return np.array([[1,0,0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])


def rot_y(theta):
    return np.array([[np.cos(theta), 0, -np.sin(theta)], [0,1,0], [np.sin(theta), 0, np.cos(theta)]])


def rot_z(theta):
    return np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0,0,1]])


def easeOutElastic(x):
    c4 = (2 * np.pi) / 3
    if math.isclose(x, 0):
        return 0
    if math.isclose(x, 1):
        return 1
    return pow(2, -10 * x) * np.sin((x * 10 - 0.75) * c4) + 1


def easeOutExpo(x):
    if math.isclose(x, 1):
        return 1
    return 1 - pow(2, -10 * x)


def easeOutBack(x):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(x - 1, 3) + c1 * pow(x - 1, 2);


def calc_dest(data):
    length = LENGTH * SMALL_COEF**(len(STATES)+1)
    new_data = data.copy()
    new_data[:3,3] += new_data[:3,:3].dot([1,0,0]) * length
    return new_data


def draw_line(data):
    level = ITERATIONS - len(STATES) - 1
    # ~ level = 1
    end_data = calc_dest(data)
    global POINT_LAST
    POINTS[level,POINT_LAST[level]] = data[:3,3]
    POINTS[level,POINT_LAST[level]+1] = end_data[:3,3]
    POINT_LAST[level] += 2
    #cv2.line(img, data[:2].astype("int"), end_data[:2].astype("int"), 0, level, lineType=cv2.LINE_AA)
    return end_data


def exp_angle(x, coef):
    return (np.exp(x/180*coef)-1)/(np.exp(coef)-1)*180

def exp_angle_abs(x, coef):
    return exp_angle(abs(x), coef) * np.sign(x)

def log_angle(x):
    x, s = abs(x), np.sign(x)
    return np.log(x+1)/np.log(180+1)*180 * s
    
def F():
    # ~ a = DATA[2] % 360
    # ~ if a > 180:
        # ~ a -= 360
    # ~ new_data = DATA.copy()
    # ~ new_data[2] = exp_angle_abs(a, EXP_COEF)
    # ~ DATA[:2] = draw_line(img, new_data)[:2]
    DATA[:3,3] = draw_line(DATA)[:3,3]
    
def b():
    DATA[:3,3] = calc_dest(DATA)[:3,3]
    
def ob():
    STATES.append(DATA.copy())
    
def cb():
    DATA[:] = STATES.pop()

def pax():
    DATA[:3,:3] = DATA[:3,:3].dot(rot_x(THETA))

def maxx():
    DATA[:3,:3] = DATA[:3,:3].dot(rot_x(-THETA))

def pay():
    DATA[:3,:3] = DATA[:3,:3].dot(rot_y(THETA))

def may():
    DATA[:3,:3] = DATA[:3,:3].dot(rot_y(-THETA))

def paz():
    DATA[:3,:3] = DATA[:3,:3].dot(rot_z(THETA))

def maz():
    DATA[:3,:3] = DATA[:3,:3].dot(rot_z(-THETA))
    
def none():
    pass

RULES_DICT = {"F": F, "b": b, "[": ob, "]": cb, "+": paz, "-": maz, "|": pay, "/": may, "&": pax, "^": maxx}
    
def draw_it():
    for i in AXIOM:
        RULES_DICT.get(i, none)()

def main():
    global AXIOM, ALPHA, POS, EXP_COEF, POINTS, POINT_LAST
    for _ in range(ITERATIONS):
        for k, v in NEW.items():
            AXIOM = AXIOM.replace(k, v)
    POINTS = np.zeros((ITERATIONS, AXIOM.count("F")*2, 3))
    x = 0
    app = pg.mkQApp("3D L-system")
    w = gl.GLViewWidget()
    w.opts['distance'] = 600
    w.opts['elevation'] = 0
    w.opts['azimuth'] = 0
    w.opts['center'] = pg.Vector(0,0,0)
    w.show()
    w.setWindowTitle('3D L-system')
    while(x < 160):
        x += 1

        DATA[:] = DATA_START
        POINT_LAST = np.zeros(ITERATIONS, dtype=int)
        xx = (x/40)%4
        if xx < 1:
            EXP_COEF = easeOutExpo(xx%1)
        elif xx < 2:
            EXP_COEF = 1-easeOutBack(xx%1)
        elif xx < 3:
            EXP_COEF = -easeOutExpo(xx%1)
        else:
            EXP_COEF = -1+easeOutBack(xx%1)
        if math.isclose(EXP_COEF, 0, abs_tol=0.01):
            EXP_COEF = 0.01
        print(xx, "%f" % EXP_COEF)
        draw_it()
        print(POINTS)
        for i in range(ITERATIONS):
            # ~ coef = i**(1/4)/(ITERATIONS-1)**(1/4)
            # ~ print(coef)
            # ~ color = (GREEN_COLOR*(1-coef)+(coef)*BROWN_COLOR).tolist()
            if i == 0:
                color = GREEN_COLOR.tolist()
            else:
                color = BROWN_COLOR.tolist()
            sp1 = gl.GLLinePlotItem(pos=POINTS[i,:POINT_LAST[i]], width=i*2+1, color=color, mode="lines")
            sp1.translate(-250, 0, 0)
            sp1.rotate(90, 1, 0, 0)
            sp1.rotate(-90, 0, 1, 0)
            sp1.rotate(90, 0, 0, 1)
            w.addItem(sp1)
        break

    QtGui.QApplication.instance().exec_()


if __name__ == "__main__":
    main()
