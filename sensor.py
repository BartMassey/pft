import math, random

# Assumed minimum distance between sensor and target.
mindist = 0.001

# Assumed positive white noise amplitude. XXX
# This should be gaussian, but who wants to play with
# errinv()?
us = 1

class Sensor(object):
    """A sensor model."""

    def __init__(self, x, y):
        """Create a new sensor at the given position."""

        self.x = x
        self.y = y
        self.strength = None

    def true_measure(self, x):
        """Return the true signal value given
        a coordinate x."""
        dist2 = (self.x - x)**2 + (self.y - x)**2
        return 1 / max(math.sqrt(dist2), mindist)

    def measure(self, x):
        """Synthesize a noisy signal strength measurement
        given a true coordinate x."""

        s = self.true_measure(x)
        s += us * random.random() / s
        self.strength = s

    def prob(self, x):
        """Return a likelihood of the true position
        given the measured position."""

        s0 = self.true_measure(x)
        ds = s0 * (self.strength - s0) / us
        if ds < 0 or ds > 1:
            return 0
        return 1 / us

def gen():
    """Randomly place a sensor."""
    return Sensor(random.random(), random.random())
