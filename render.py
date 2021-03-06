#!/usr/bin/python3

# https://brushingupscience.com/2016/06/21/matplotlib-animations-the-easy-way/

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ms = 9

def cscale(w):
    if w < 1e-5:
        return 0
    return 1
    # return (5.0 + math.log10(w)) / 5.0

def render(sensors, states, dt):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set(xlim=(0, 1), ylim=(0, 1))
    x = np.linspace(0, 1, 100)
    ax.plot(x, x, marker=None, color='#000000', lw=0.1, ls='-')
    ax.plot([s.x for s in sensors], [s.y for s in sensors],
             'o', color='#ff8800', markersize=ms)[0]
    vpos = ax.plot([states[0][0].x], [states[0][0].x], 'o', color='r', markersize=ms*3//2)[0]
    px = np.array([p.x for p in states[0][1]], dtype=np.float32)
    pc = np.array([(0, cscale(p.weight), cscale(p.weight))
                   for p in states[0][1]], dtype=np.float32)
    ppos = ax.scatter(px, px, s=0.1, c=pc)
    cpos = ax.plot([states[0][2]], [states[0][2]], 'o', color='#0000ff', markersize=ms)[0]

    def animate(i):
        px = np.array([(p.x, p.x) for p in states[i][1]], dtype=np.float32)
        ppos.set_offsets(px)
        pc = np.array([(0, cscale(p.weight), cscale(p.weight))
                       for p in states[i][1]], dtype=np.float32)
        ppos.set_color(pc)
        vpos.set_xdata([states[i][0].x])
        vpos.set_ydata([states[i][0].x])
        cpos.set_xdata([states[i][2]])
        cpos.set_ydata([states[i][2]])

    anim = FuncAnimation(fig, animate, interval=int(dt * 1000),
                         frames=len(states))
    
    plt.draw()
    plt.show()
