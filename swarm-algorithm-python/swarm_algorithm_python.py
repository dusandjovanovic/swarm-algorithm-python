from __future__ import division
import numpy
from random import random
from random import uniform
import matplotlib.pyplot as plot
import matplotlib.colors as plot_colors

w_inertia = 0.5    # tendency towards previous velocity
c_cognitive = 1    # cognitive constant
c_social = 2       # social constant

num_particles = 40
num_iterations = 25

plot_config_toolbar = "None"
plot_config_font = {'family': 'DejaVu Sans', 'weight': 'bold', 'size': 7}

triangle_a = [-8, -2]
triangle_b = [3, -1]
triangle_c = [0, 3]
triangle_centroid = [0, 0]

class Particle:
    def __init__(self, x0):
        self.velocity_i = []
        self.position_i = []
        self.position_i_best = []
        self.error_i = -1
        self.error_i_best = -1
 
        for i in range(0, num_dimensions):
            self.velocity_i.append(uniform(-1, 1))
            self.position_i.append(x0[i] + random())

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

def cost_function(x):
    distance_to_goal = numpy.sqrt((triangle_centroid[0] - x[0]) ** 2 + (triangle_centroid[1] - x[1]) ** 2)
    return distance_to_goal

def minimize(costFunc, x0, bounds, num_particles, maxiter):
    global num_dimensions
    num_dimensions = len(x0)
    
    error_g_best = -1
    position_g_best = []

    swarm = []
    for i in range(0, num_particles):
        swarm.append(Particle(x0))

    plot.ion()
    plot.rcParams['toolbar'] = plot_config_toolbar
    plot.rc('font', **plot_config_font)
    figure = plot.figure()
    figure.canvas.set_window_title('Swarm particle algorithm 2D-View')
    ax = figure.add_subplot(111)
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
            line1 = ax.plot(swarm[j].position_i[0], swarm[j].position_i[1], 'r+', c=(plot_colors.to_rgba("grey", alpha=0.75)))
            line2 = ax.plot(position_g_best[0], position_g_best[1], 'g*', c=(plot_colors.to_rgba("orange", alpha=1.0)))

        ax.plot([triangle_a[0], triangle_b[0]], [triangle_a[1], triangle_b[1]], c=(plot_colors.to_rgba("blue", alpha=0.35)))
        ax.plot([triangle_b[0], triangle_c[0]], [triangle_b[1], triangle_c[1]], c=(plot_colors.to_rgba("blue", alpha=0.35)))
        ax.plot([triangle_c[0], triangle_a[0]], [triangle_c[1], triangle_a[1]], c=(plot_colors.to_rgba("blue", alpha=0.35)))
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        figure.canvas.draw()
        ax.clear()
        ax.grid(True)

        i += 1

    print(f'\nBest-global position > {position_g_best}')
    print(f'Best-error > {error_g_best}\n')

def main():
    global triangle_centroid, triangle_a, triangle_b, triangle_c
    triangle_centroid = [(triangle_a[0] + triangle_b[0] + triangle_c[0]) / 3, (triangle_a[1] + triangle_b[1] + triangle_c[1]) / 3]
    initial_location = [random() * 10, random() * 10]
    bounds = [(-20,20), (-20,20)]

    minimize(cost_function, initial_location, bounds, num_particles, num_iterations)
  
if __name__== "__main__":
    main()