#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from sympy import *
from IPython.display import display, Latex
init_printing(use_latex='mathjax')
pprint = display

calc_force = lambda x: 2*x**25/(x**50+1)

starts = [
    ([-1, 0.01, -1, 0.01, -1, 0.001], 10),
]

def sys(X, t=0) -> np.ndarray:
    x, xv, y, yv, z, zv = X
    return np.array([
        xv,
        -calc_force(x**2+y**2+z**2)*x*xv,
        yv,
        -calc_force(x**2+y**2+z**2)*y*xv,
        zv,
        -calc_force(x**2+y**2+z**2)*z*zv,
    ])
    
def print_trajectories(ax, starts: list) -> None:
    # Обчислюємо траєкторії задані у змінній `starts`
    for s, t in starts:
        # Задаємо діапазон часу [0, t] та ділить відрізок на 2000 частин.
        tspan = np.linspace(0, t, 2000)
        # Інтегрує систему до заданого часу `t` та початкових значень `s`
        tr = odeint(sys, s, tspan)
        # Друкуєму саму траєкторію
        ax.plot3D(tr[:, 0], tr[:, 2], tr[:, 4])
        # ~ ax.plot3D(tr[:, 1], tr[:, 3], tr[:, 5])
        # Друкуємо початок траєкторії у вигляді кружечка
        ax.plot3D([tr[0, 0]], [tr[0, 2]], [tr[0, 4]], 'o')
        # Друкуємо кінець траєкторії у вигляді квадратика
        ax.plot3D([tr[-1, 0]], [tr[-1, 2]], [tr[-1, 4]], 's')


fig = plt.figure()
ax = fig.gca(projection="3d")

print_trajectories(ax, starts)
plt.show()
