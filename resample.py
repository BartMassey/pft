# Copyright © 2019 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Resampling for BPF demo.

import random

def resample(particles, m):
    """Produce an array of m particles from an array of n
    particles by weighted resampling, using the shuffled
    regular sampling method. Weights are assumed to be
    normalized."""

    n = len(particles)
    random.shuffle(particles)
    si = 1 / m
    result = list()
    wt = 0
    i = 0
    for j in range(1, m + 1):
        while i < n - 1 and wt < j * si:
            if particles[i].weight != None:
                wt += particles[i].weight
            i += 1
        result.append(particles[i].clone())
    
    return result
