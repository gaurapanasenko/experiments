#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from sympy import *
from IPython.display import display, Latex
import matplotlib.animation as animation
init_printing(use_latex='mathjax')
pprint = display

calc_force = lambda x: (0.6*x**4+0.4)/(1.2*x**16-1.4*x**12+1.2)

starts = [
    ([-0, 0.01, -1, 0.1, -1, 0], 500),
    ([-0, 0, -1, 0.1, -1, 0], 500),
]

TIME_LEN = 2000

def sys(X, t=0) -> np.ndarray:
    x, xv, y, yv, z, zv = X
    return np.array([
        xv,
        -0.1*calc_force(x**2+y**2+z**2)*x-0.01*xv,
        yv,
        -0.1*calc_force(x**2+y**2+z**2)*y-0.01*yv,
        zv,
        -0.1*calc_force(x**2+y**2+z**2)*z-0.01*zv,
    ])

t = symbols("t")
x, y, z = symbols("x, y, z", cls=Function)
x, y, z = x(t), y(t), z(t)

xv, yv, zv = diff(x, t), diff(y, t), diff(z, t)

s = sys([x, xv, y, yv, z, zv])

pprint(Matrix([Eq(x, s[0]), Eq(xv, s[1]), Eq(y, s[2]), Eq(xv, s[3]), Eq(z, s[4]), Eq(xv, s[5])]))
