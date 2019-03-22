
'''
Created on 2019-03-05 12:59
@summary: Paramless evolution on a 3D surface. Based on Julian Garcia's paramless.py
@author: snpardy
'''

import numpy as np
import math
from collections import OrderedDict as OrderedDict
import matplotlib.pyplot as plt
import matplotlib
import os
import imageio
# from mpl_toolkits.mplot3d import axes3d

# default tolerance for float comparisons
DEFAULT_ATOL = 1e-8

# maximum iterations
MAX_ITERATIONS = 1000000

def _within_bounds(vector, lower_bound, upper_bound):
    '''
    @summary: Determines if the values of vector are in the [lower_bound, upper_bound] interval
    @param vector: surface to test
    @param lower_bound: lower_bound
    @param upper_bound: upper_bound
    @result: True or False 
    @todo: Add tolerance!
    '''
    if lower_bound != None and np.min(vector) < lower_bound :
        return False
    if upper_bound != None and np.max(vector) > upper_bound:
        return False
    return True

def _bivariate_normal_mutation(x, y, mutation_epsilon, mean_x, mean_y, variance):
    # This function assumes that the pearson correlation coefficient is 0
    return mutation_epsilon * (math.e ** -((.5)*((((x-mean_x)**2)/variance**2) + (((y-mean_y)**2)/variance**2))))

def _attemp_gaussian_mutation(X,Y,Z, mutation_epsilon, radius, lower_bound=None, upper_bound=None):
    location = np.array([np.random.randint(0, len(X)), np.random.randint(0, len(Y))])
    mutant = np.copy(Z)
    variance = np.random.rand() * radius
    perturbation = _bivariate_normal_mutation(X, Y, mutation_epsilon, location[0], location[1], variance)
    # upwards
    if (np.random.randint(2)):
        mutant += perturbation
    # downwards
    else:
        mutant -= perturbation
    return mutant

def gaussian_mutation(X,Y,Z, mutation_epsilon, radius, lower_bound=None, upper_bound=None, **kwargs):
    is_inside = False
    attemp = 0
    while (not is_inside):
        mutant = _attemp_gaussian_mutation(X,Y,Z, mutation_epsilon, radius, lower_bound=lower_bound, upper_bound=upper_bound)
        is_inside=_within_bounds(mutant, lower_bound, upper_bound)
        attemp+=1
        if attemp > MAX_ITERATIONS:
            raise RuntimeError("Attempted too many mutations without producing anythin within bounds")
            pass
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
    Returns the fitness of surfaces of two paramaters.
    @returns fitness_resident, fitness_mutant
    @param resident: the resident surface, of which the fitness will be returned
    @param mutant: the mutant surface, of which the fitness will be returned
    @param target_surface: the surface against which the fitness of the other two will be measured
    """
    fitness_resident = 1.0 / _surface_distance(resident, target_surface)
    fitness_mutant = 1.0 / _surface_distance(mutant, target_surface)
    return fitness_resident, fitness_mutant

def evolution_step(resident_surface, fitness_function, mutation_function, atol, *args, **kwargs):
    """
    One generation iteration
    """
    invasion = False
    mutantVector = mutation_function(resident_surface[0], resident_surface[1], resident_surface[2], **kwargs)
    fitness_resident, fitness_mutant = fitness_function(resident_surface, [resident_surface[0], resident_surface[1], mutantVector], **kwargs)
    if fitness_resident < fitness_mutant and abs(fitness_resident - fitness_mutant) > atol:
        resident_surface = np.copy(resident_surface)
        resident_surface[2] = np.copy(mutantVector)
        invasion = True
    return resident_surface, invasion



def evolve(initial_surface, fitness_function, mutation_function, iterations, atol=DEFAULT_ATOL, seed=None, time_series_data=False, **kwargs):
    """
    Evolve
    """
    np.random.seed(seed)
    resident = np.copy(initial_surface)
    previous_resident = np.zeros_like(initial_surface)
    if time_series_data:
        time_series_array = [resident]
    for step in range(1, iterations):
        resident, invasion = evolution_step(resident, fitness_function, mutation_function, atol, **kwargs)
        if invasion and time_series_data:
            time_series_array.append(resident)
            
    if time_series_data:
        return resident, time_series_array
    return resident

def createGIF(path, time_series_array):
    os.mkdir(path + "\.plots")
    fig = plt.figure()
    images = []
    for i, item in enumerate(time_series_array):
        ax = fig.add_subplot(111, projection='3d')
        ax.set_zlim3d(0, 1.1)
        ax.set_title('Evolved Surface')
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        ax.plot_surface(item[0], item[1], item[2],cmap='viridis',linewidth=0)
        file_name = path + "\.plots\plot_" + str(i) + '.png'
        fig.savefig(file_name)


    for i in range(len(time_series_array)):
        fn = path + "\.plots\plot_" + str(i) + '.png'
        images.append(imageio.imread(fn))
        os.remove(fn)
    os.rmdir(path+"\.plots")
    imageio.mimsave(path +'\evolution.gif', images)