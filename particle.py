# Copyright © 2019 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Particles for BPF demo.

import random

# Random fraction of v to update v by.
uv = 0.1

# Minimum / maximum v value.
vclamp = 0.2

class Particle(object):
    """A 'particle' represents a simulation state."""

    def __init__(self, x, v, w):
        """Create an uninitialized particle at position x
        with velocity v and weight w."""

        self.x = x
        self.v = v
        self.weight = w

    def clone(self):
        """Create a clone."""

        return Particle(self.x, self.v, self.weight)

    def advance(self, dt):
        """Propagate the particle forward by dt."""

        # Update model.
        self.v += uv * (0.5 - random.random())
        self.x += self.v * dt

        # Check bounds.
        if self.x < 0:
            self.weight = None
            self.x = 0
        if self.x > 1:
            self.weight = None
            self.x = 1

    def measure(self, sensor):
        """Update the weight via the sensor reading."""

        psense = sensor.prob(self.x)
        if self.weight == None:
            self.weight = psense
        else:
            self.weight *= psense
        
def gen():
    """Create a random particle."""

    x = random.random()
    v = (random.random() - 0.5) * 2 * vclamp
    return Particle(x, v, None)

def normalize(particles):
    """Adjust the weights of the particles to sum to 1."""

    w = sum([p.weight for p in particles if p != None])
    for i in range(len(particles)):
        if particles[i].weight != None:
            particles[i].weight /= w

def freshen(particles):
    """Replace dead particles."""

    for i in range(len(particles)):
        w = particles[i].weight
        if w == None or w < 1e-10:
            particles[i] = gen()

def centroid(particles):
    return sum(p.x * p.weight for p in particles if p.weight != None)
