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

def calc_traj(s):
    tspan = np.linspace(0, 500, TIME_LEN)
    return odeint(sys, s, tspan).transpose()
    

def polar2z(r, theta):
    z = r * np.exp(1j * theta)
    return z.real, z.imag

def calc_trajectories():
    x = np.linspace(0.5, 1, 10)
    y = np.linspace(np.pi, 2*np.pi, 10)
    X, Y = np.meshgrid(x, y)
    X, Y = X.ravel(), Y.ravel()
    X, Y = polar2z(X, Y)
    sz = X.shape[0]
    res = np.zeros((sz*3, 6, TIME_LEN))
    for i, (xx, yy) in enumerate(zip(X, Y)):
        XX = np.array([xx, yy + 1, 1])
        XX /= np.linalg.norm(XX)
        res[i] = calc_traj([-0, XX[0] / 10, -1, XX[1] / 10, -1, XX[2] / 10])
        res[i+sz] = calc_traj([-0, XX[0] / 20, -1, XX[1] / 20, -1, XX[2] / 20])
        res[i+2*sz] = calc_traj([-0, XX[0] / 30, -1, XX[1] / 30, -1, XX[2] / 30])
    return res
    
def animate(i, res, lines):
    print(i)
    for j, line in enumerate(lines):
        line.set_data(res[j, :4:2, i*10:(i+1)*10])
        line.set_3d_properties(res[j, 5, i*10:(i+1)*10])
    # ~ ax.clear()
    # ~ ax.set_xlim3d([-1.1, 1.1])
    # ~ ax.set_ylim3d([-1.1, 1.1])
    # ~ ax.set_zlim3d([-1.1, 1.1])
    # ~ for tr in res:
        # ~ ax.plot(tr[i*10:(i+1)*10,0], tr[i*10:(i+1)*10,2], tr[i*10:(i+1)*10,4], alpha=0.75)
    return lines

def print_trajectories(res) -> None:
    # ~ plt.figure(0)
    # ~ plt.scatter(X, Y, 0.1)
    # ~ plt.figure(1)
    fig = plt.figure(0)
    ax = fig.add_subplot(projection='3d')
    ax.set_xlim3d([-1, 1])
    ax.set_ylim3d([-1, 1])
    ax.set_zlim3d([-1, 1])
    lines = [ax.plot(tr[0,:10], tr[2,:10], tr[4,:10], alpha=0.75)[0] for tr in res]
    # ~ plt.figure(0)
    # ~ plt.plot(tspan, tr[:,1])
    # ~ plt.plot(tspan, tr[:,3])
    # ~ plt.figure(1)
    # ~ plt.plot(tspan, tr[:,0])
    # ~ plt.plot(tspan, tr[:,2])
    # ~ plt.figure(2)
    # ~ plt.plot(tr[:,0], tr[:,2])
    # ~ plt.figure(3)
        
    ani = animation.FuncAnimation(
        fig, animate, fargs=(res, lines), interval=200, blit=True, save_count=100)
    
    ani.save('matplot003.mp4')
    
    plt.show()

def main():
    res = calc_trajectories()
    print_trajectories(res)

main()
