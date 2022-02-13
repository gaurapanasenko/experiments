#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
from sympy import *
from IPython.display import display, Latex
init_printing(use_latex='mathjax')
pprint = display

calc_force = lambda x: 2*x**25/(x**50+1)

def sys(X, t=0) -> np.ndarray:
    x, y, z = X
    return np.array([
        -calc_force(x**2+y**2+z**2)*x,
        -calc_force(x**2+y**2+z**2)*y,
        -calc_force(x**2+y**2+z**2)*z,
    ])


def polar2z(r, theta):
    z = r * np.exp(1j * theta)
    return z.real, z.imag


def main():
    x = np.linspace(0.0, 1.2, 12)
    y = np.linspace(0, 2*np.pi, 12)
    z = np.linspace(0, 2*np.pi, 12)

    fig = plt.figure()
    ax = fig.gca(projection="3d")

    X, Y, Z = np.meshgrid(x, y, z)
    X, Y = polar2z(X, Y)
    X, Z = polar2z(X, Z)
    u, v, w = sys([X, Y, Z])
    ax.quiver(X, Y, Z, u, v, w, color='r', length=0.3, alpha=0.5)
    plt.show()

main()
