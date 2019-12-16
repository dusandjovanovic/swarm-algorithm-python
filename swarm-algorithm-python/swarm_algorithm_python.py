from __future__ import division
from random import random
from random import uniform
from matplotlib import pyplot

w_inertia = 0.5    # tendency towards previous velocity
c_cognitive = 1    # cognitive constant
c_social = 2       # social constant

class Particle:
    def __init__(self, x0):
        self.velocity_i = []
        self.position_i = []
        self.position_i_best = []
        self.error_i = -1
        self.error_i_best = -1
 
        for i in range(0, num_dimensions):
            self.velocity_i.append(uniform(-1, 1))
            self.position_i.append(x0[i])

    def evaluate(self, costFunc):
        self.error_i = costFunc(self.position_i)
        if self.error_i < self.error_i_best or self.error_i_best == -1:
            self.position_i_best = self.position_i.copy()
            self.error_i_best = self.error_i

    def update_position(self, bounds):
        for i in range(0, num_dimensions):
            self.position_i[i] = self.position_i[i] + self.velocity_i[i]
            if self.position_i[i] > bounds[i][1]:
                self.position_i[i] = bounds[i][1]
            if self.position_i[i] < bounds[i][0]:
                self.position[i] = bounds[i][0]

    def update_velocity(self, position_g_best):
        for i in range(0, num_dimensions):
            r1, r2 = random(), random()
            vel_cognitive = c_cognitive * r1 * (self.position_i_best[i] - self.position_i[i])
            vel_social = c_social * r2 * (position_g_best[i] - self.position_i[i])
            self.velocity_i[i] = w_inertia * self.velocity_i[i] + vel_cognitive + vel_social

def sphere(x):
    total = 0
    for i in range(len(x)):
        total += x[i] ** 2
    return total

def minimize(costFunc, x0, bounds, num_particles, maxiter):
    global num_dimensions
    num_dimensions = len(x0)
    
    error_g_best = -1
    position_g_best = []

    swarm = []
    for i in range(0, num_particles):
        swarm.append(Particle(x0))

    pyplot.ion()
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)

    i = 0
    while i < maxiter:
        print(f'iter: {i:>4d}, best solution: {error_g_best:10.6f}')

        for j in range(0, num_particles):
            swarm[j].evaluate(costFunc)
            if swarm[j].error_i < error_g_best or error_g_best == -1:
                position_g_best = list(swarm[j].position_i)
                error_g_best = float(swarm[j].error_i)

        for j in range(0, num_particles):
            swarm[j].update_velocity(position_g_best)
            swarm[j].update_position(bounds)
            line1 = ax.plot(swarm[j].position_i[0], swarm[j].position_i[1], 'r+')
            line2 = ax.plot(position_g_best[0], position_g_best[1], 'g*')

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        fig.canvas.draw()
        ax.clear()
        ax.grid(True)

        i += 1

    print(f'\nBest-global position > {position_g_best}')
    print(f'Best-error > {error_g_best}\n')

def main():
    initial_location = [random() * 10, random() * 10]
    bounds = [(-10,10), (-10,10)]

    minimize(sphere, initial_location, bounds, num_particles=15, maxiter=30)
  
if __name__== "__main__":
    main()