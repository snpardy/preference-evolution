
"""
Created on 2019-03-05 12:59
@summary: Paramless evolution on a 3D surface. Based on Julian Garcia's paramless.py
@author: snpardy
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import os
import imageio
import time
import progressbar
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D 
from collections import namedtuple

# default tolerance for float comparisons
DEFAULT_ATOL = 1e-8

# maximum iterations
MAX_ITERATIONS = 1000000


def _within_bounds(vector, lower_bound, upper_bound):
    """
    @summary: Determines if the values of vector are in the [lower_bound, upper_bound] interval
    @param vector: surface to test
    @param lower_bound: lower_bound
    @param upper_bound: upper_bound
    @result: True or False 
    @todo: Add tolerance!
    """
    if lower_bound is not None and np.min(vector) < lower_bound:
        return False
    if upper_bound is not None and np.max(vector) > upper_bound:
        return False
    return True


def _bivariate_normal_mutation(x, y, mutation_epsilon, mean_x, mean_y, variance):
    # This function assumes that the pearson correlation coefficient is 0
    return mutation_epsilon * (math.e ** -(.5*((((x-mean_x)**2)/variance**2) + (((y-mean_y)**2)/variance**2))))


def _attempt_gaussian_mutation(X, Y, Z, mutation_epsilon, radius, lower_bound=None, upper_bound=None):
    location = np.array([np.random.randint(0, len(X)), np.random.randint(0, len(Y))])

    # This creates an implicit dependency that X and Y are meshgrids with indexing='ij'
    x_mean = X[location[0], 0]
    y_mean = Y[0, location[1]]
    mutant = np.copy(Z)
    variance = np.random.rand() * radius
    perturbation = _bivariate_normal_mutation(X, Y, mutation_epsilon, x_mean, y_mean, variance)
    # upwards
    if np.random.randint(2):
        mutant += perturbation
    # downwards
    else:
        mutant -= perturbation
    return mutant


def gaussian_mutation(X,Y,Z, mutation_epsilon, radius, lower_bound=None, upper_bound=None, **kwargs):
    is_inside = False
    attempt = 0
    mutant = None
    while not is_inside:
        mutant = _attempt_gaussian_mutation(X, Y, Z, mutation_epsilon, radius, lower_bound=lower_bound, upper_bound=upper_bound)
        is_inside = _within_bounds(mutant, lower_bound, upper_bound)
        attempt += 1
        if attempt > MAX_ITERATIONS:
            raise RuntimeError("Attempted too many mutations without producing anythin within bounds")
    return mutant


def _surface_distance(u, v):
    """
    Calculates the sum of euclidian distance between respective points in two given surfaces.
    Used as a distance function.
    Assumes that the arrays representing the surfaces are the same shape.
    """
    total = 0
    for i, _ in enumerate(u[0]):
        for j, _ in enumerate(u[0][i]):
            one_point_dist = 0
            for axis, _ in enumerate(u):
                one_point_dist += (u[axis][i,j]-v[axis][i,j])**2
            total += math.sqrt(one_point_dist)

    return total


def distance_fitness_function(resident, mutant, target_surface, **kwargs):
    """
    Returns the fitness of surfaces of two parameters.
    @returns fitness_resident, fitness_mutant
    @param resident: the resident surface, of which the fitness will be returned
    @param mutant: the mutant surface, of which the fitness will be returned
    @param target_surface: the surface against which the fitness of the other two will be measured
    """
    fitness_resident = 1.0 / _surface_distance(resident, target_surface)
    fitness_mutant = 1.0 / _surface_distance(mutant, target_surface)
    return fitness_resident, fitness_mutant


def evolution_step(resident_surface, fitness_function, mutation_function, atol, step, **kwargs):
    """
    One generation iteration
    """
    invasion = False
    mutant = np.copy(resident_surface)
    mutant_vector = mutation_function(mutant[0], mutant[1], mutant[2], **kwargs)
    fitness_resident, fitness_mutant = fitness_function(resident_surface[2],
                                                        mutant_vector, **kwargs)
    if fitness_resident < fitness_mutant and abs(fitness_resident - fitness_mutant) > atol:
        resident_surface = np.copy(resident_surface)
        resident_surface[2] = np.copy(mutant_vector)
        invasion = True
    return resident_surface, invasion


def evolve(initial_surface, fitness_function, mutation_function, iterations,
           atol=DEFAULT_ATOL, seed=None, time_series_data=False, **kwargs):
    """
    Evolve
    """
    invasion_count = 0
    step_count = 0
    np.random.seed(seed)
    resident = np.copy(initial_surface)
    if time_series_data:
        time_series_array = [resident]
    with progressbar.ProgressBar(max_value=iterations) as bar:
        for step in range(1, iterations):
            step_count += 1
            bar.update(step)
            resident, invasion = evolution_step(resident, fitness_function, mutation_function, atol, step, **kwargs)
            if invasion:
                invasion_count += 1
                if time_series_data:
                    time_series_array.append(resident)
    if time_series_data:
        return resident, time_series_array, invasion_count
    return resident


def create_gif(path, time_series_array, height, fps, mp4=True, gif=False):
    """

    """
    
    x = time_series_array[0][0]
    y = time_series_array[0][1]
    z = []

    for item in time_series_array:
        z.append(item[2])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.xlabel("My Payoff")
    plt.ylabel("Opponent's Payoff")

    def update_plot(frame_number, z, plot):
        plot[0].remove()
        plot[0] = ax.plot_surface(x, y, z[frame_number], cmap="viridis", linewidth=0)
        
    plot = [ax.plot_surface(x, y, z[0], cmap='viridis', linewidth=0)]

    ax.set_zlim(-height, height)

    ani = animation.FuncAnimation(fig, update_plot, len(time_series_array), fargs=(z, plot), interval=1000/fps)

    fn = 'plot_surface_animation'
    if mp4:
        ani.save(path+fn+'.mp4',writer='ffmpeg',fps=fps)
    if gif:
        ani.save(path+fn+'.gif',writer='imagemagick',fps=fps)
