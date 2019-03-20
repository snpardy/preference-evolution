
'''
Created on 2019-03-05 12:59
@summary: Paramless evolution on a 3D surface. Based on Julian Garcia's paramless.py
@author: snpardy
'''

import numpy as np
import math
from collections import OrderedDict as OrderedDict
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

import paramless as p

# default tolerance for float comparisons
DEFAULT_ATOL = 1e-8

def surface_distance(u, v):
    """
    Calculates the sum of euclidian distance between respective points in two given surfaces.
    Used as a distance function.
    Assumes that the arrays representing the surfaces are the same shape.
    """
    total = 0
    for index, _ in enumerate(u[0]):
        total += math.sqrt(np.sum((u[:,index]-v[:,index])**2))
    return total

def distance_fitness_function(resident, mutant, target_surface, **kwargs):
    """
    Returns the fitness of surfaces of two paramaters.
    @param resident: the resident surface, of which the fitness will be returned
    @param mutant: the mutant surface, of which the fitness will be returned
    @param target_surface: the surface against which the fitness of the other two will be measured
    """
    fitness_resident = 1.0 / surface_distance(resident, target_surface)
    fitness_mutant = 1.0 / surface_distance(mutant, target_surface)
    return fitness_resident, fitness_mutant

def evolution_step(resident_surface, fitness_function, mutation_function, atol, axis_to_mutate=2, *args, **kwargs):
    """
    One generation iteration
    """
    invasion = False
    mutant = np.copy(resident_surface)
    mutant[axis_to_mutate] = mutation_function(resident_surface[axis_to_mutate], .1, **kwargs)
    [fitness_resident, fitness_mutant] = fitness_function(
        resident_surface, mutant, **kwargs)
    if fitness_resident < fitness_mutant and abs(fitness_resident - fitness_mutant) > atol:
        resident_surface = np.copy(mutant)
        invasion = True
    return resident_surface, invasion

def evolve(initial_surface, fitness_function, mutation_function, iterations, atol=DEFAULT_ATOL, return_time_series=False, seed=None, **kwargs):
    """
    Evolve 
    Returns last resident , plus time series data if required
    """
    np.random.seed(seed)
    time_series = None
    last_entry_time = 0
    resident = np.copy(initial_surface)
    seq = 0
    if return_time_series:
        time_series = OrderedDict()
    previous_resident = np.zeros_like(initial_surface)
    for step in range(1, iterations):
        if return_time_series:
            previous_resident = np.copy(resident)
        resident, invasion = evolution_step(
            resident, fitness_function, mutation_function, atol, **kwargs)
        if (return_time_series and invasion):
            time_series[seq] = {
                "alive": step - last_entry_time, "resident": previous_resident}
            last_entry_time = step
            seq += 1
    if return_time_series:
        return resident, time_series
    else:
        return resident