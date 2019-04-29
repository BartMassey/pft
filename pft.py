# Copyright © 2019 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Bayesian Particle Filter demo.

import particle, sensor, resample, render

# Number of particles.
nparticles = 10000

# Number of sensors. Must be at least two for
# unambiguous estimation.
nsensors = 2

# Time step in secs.
dt = 0.1

# Resampling interval in secs.
rst = 0.5

def gen_particles():
    return [particle.gen() for _ in range(nparticles)]

# Set up simulation.
particles = gen_particles()
vehicle = particle.gen()
if vehicle.v > 0:
    vehicle.x = 0
    vehicle.v = max(vehicle.v, 0.05)
else:
    vehicle.x = 1
    vehicle.v = min(vehicle.v, -0.05)
vehicle.advance(dt)
sensors = [sensor.Sensor(x, y) for x, y in [(0.25, 0.5), (0.75, 0.6)]]

# Run sensing loop.
t = 0
states = list()
while vehicle.x > 0 and vehicle.x < 1 and t < 50 * dt:

    # Replace dead particles if needed.
    particle.freshen(particles)

    # Make measurements.
    for s in sensors:
        s.measure(vehicle.x)
        for p in particles:
            p.measure(s)
    if not particle.normalize(particles):
        print("lost")
        particles = gen_particles()
        continue

    # Report centroid.
    print("actual:", vehicle.x, "  imputed:", particle.centroid(particles))
    states.append((vehicle.clone(), [p.clone() for p in particles
                                   if p.weight != None]))

    # Resample as needed.
    if t > rst:
        print("resampling")
        particles = resample.resample(particles, nparticles)
        t = 0

    # Advance the state.
    vehicle.advance(dt)
    for p in particles:
        p.advance(dt)
    t += dt

render.render(sensors, states, dt)
