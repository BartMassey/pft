#!/usr/bin/python3

# https://brushingupscience.com/2016/06/21/matplotlib-animations-the-easy-way/

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def render(sensors, states, dt):

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set(xlim=(0, 1), ylim=(0, 1))
    x = np.linspace(0, 1, 100)
    ax.plot(x, x, color='k', lw=2)[0]
    ax.plot([s.x for s in sensors], [s.y for s in sensors],
             'o', markersize=2)[0]
    vpos = ax.plot([states[0][0].x], [states[0][0].x], 'o', color='r', markersize=3)[0]
    cpos = ax.plot([states[0][2]], [states[0][2]], 'o', color='b', markersize=3)[0]

    def animate(i):
        vpos.set_xdata([states[i][0].x])
        vpos.set_ydata([states[i][0].x])
        cpos.set_xdata([states[i][2]])
        cpos.set_ydata([states[i][2]])

    anim = FuncAnimation(fig, animate, interval=int(dt * 1000),
                         frames=len(states))
    
    plt.draw()
    plt.show()
