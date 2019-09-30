"""
Created on 2019-03-05 12:59
@summary: Paramless evolution on a 3D surface. Based on Julian Garcia's paramless - github.com/juliangarcia/paramless
@author: snpardy
"""
import math   # standard library
import random
from dataclasses import replace  

import numpy as np   # 3rd party library

from .fitness_functions import *   # local source
from .game import Game  
from .utilitySurface import UtilitySurface
from .utils import append_matrix_to_csv


# default tolerance for float comparisons
DEFAULT_ATOL = 1e-8

# maximum iterations
MAX_ITERATIONS = 1000000


def _within_bounds(vector, lower_bound, upper_bound):
    """
    @summary: Determines if the values of vector are in the [lower_bound, upper_bound] interval
    @:param vector: surface to test
    @:param lower_bound: lower_bound
    @:param upper_bound: upper_bound
    @:return: True or False
    @todo: Add tolerance!
    """
    if lower_bound is not None and np.min(vector) < lower_bound:
        return False
    if upper_bound is not None and np.max(vector) > upper_bound:
        return False
    return True


# Functions for Gaussian Mutation
def _bivariate_normal_mutation(surface: UtilitySurface, mutation_epsilon, mean_x, mean_y,
                               variance):
    # This function assumes that the pearson correlation coefficient is 0
    # It creates grids of the payoff arrays so that output is in shape of grid.
    x_grid, y_grid = np.meshgrid(surface.my_payoff, surface.opponent_payoff)
    return mutation_epsilon * (
            math.e ** 
            -(.5 * (
                (((x_grid - mean_x) ** 2) / variance ** 2) + 
                (((y_grid - mean_y) ** 2) / variance ** 2)
                )
            )
        )


def _attempt_gaussian_mutation(surface: UtilitySurface, mutation_epsilon, radius):
    """
    :param surface:
    :param mutation_epsilon:
    :param radius:
    :return :param surface mutated by a randomly generate bivariate normal distribution
    """
    x_mean = np.random.choice(surface.my_payoff)
    y_mean = np.random.choice(surface.opponent_payoff)

    variance = np.random.rand() * radius

    perturbation = _bivariate_normal_mutation(surface, mutation_epsilon, x_mean,
                                                      y_mean,
                                              variance)
    # upwards
    if np.random.randint(2):
        mutant_utility_grid = surface.utility_grid + perturbation
    # downwards
    else:
        mutant_utility_grid = surface.utility_grid - perturbation

    return replace(surface, utility_grid=np.around(mutant_utility_grid, 8))


def _attempt_gaussian_mutation_more_info(surface: UtilitySurface, mutation_epsilon, radius):
    """
    :param surface:
    :param mutation_epsilon:
    :param radius:
    :return :param surface mutated by a randomly generate bivariate normal distribution
    """
    x_mean = np.random.choice(surface.my_payoff)
    y_mean = np.random.choice(surface.opponent_payoff)

    variance = np.random.rand() * radius

    perturbation = _bivariate_normal_mutation(surface, mutation_epsilon, x_mean, y_mean,
                                              variance)
    # upwards
    if np.random.randint(2):
        mutant_utility_grid = surface.utility_grid + perturbation
    # downwards
    else:
        mutant_utility_grid = surface.utility_grid - perturbation

    return replace(surface, utility_grid=mutant_utility_grid), (variance, x_mean, y_mean)


def gaussian_mutation_more_info(surface: UtilitySurface, mutation_epsilon, radius,
                      max_iterations=1000000, lower_bound=None,
                      upper_bound=None, **kwargs):
    is_inside = False
    attempt = 0
    mutant = None
    while not is_inside:
        mutant, mutation_info = _attempt_gaussian_mutation_more_info(surface,
                                                                     mutation_epsilon, radius)
        is_inside = _within_bounds(mutant.utility_grid, lower_bound, upper_bound)
        attempt += 1
        if attempt > max_iterations:
            raise RuntimeError(
                "Attempted too many mutations without producing anything within bounds")
    return mutant, mutation_info


def gaussian_mutation(surface: UtilitySurface, mutation_epsilon, radius,
                      max_iterations=1000000, lower_bound=None,
                      upper_bound=None, **kwargs):
    is_inside = False
    attempt = 0
    mutant = None
    while not is_inside:
        mutant = _attempt_gaussian_mutation(surface, mutation_epsilon, radius)
        is_inside = _within_bounds(mutant.utility_grid, lower_bound, upper_bound)
        attempt += 1
        if attempt > max_iterations:
            raise RuntimeError(
                "Attempted too many mutations without producing anything within bounds")
    return mutant
  

# Evolution
def evolution_step(resident: UtilitySurface, fitness_function, mutation_function, atol,
                   **kwargs):
    """
    One generation iteration
    """

    invasion = False
    mutant, mutation_info = mutation_function(resident, **kwargs)
    fitness_resident, fitness_mutant = fitness_function(resident,
                                                        mutant,
                                                        mutation_info,
                                                        **kwargs)

    if fitness_resident < fitness_mutant and abs(fitness_resident-fitness_mutant) > atol:
        # if fitness_resident <= fitness_mutant:
        resident = mutant
        invasion = True
    return resident, invasion, (fitness_mutant-fitness_resident)


def evolve(initial_surface: UtilitySurface, fitness_function, mutation_function, iterations,
           record_invasion_each_step: int, atol=DEFAULT_ATOL, seed=None,
           time_series_data=False, save_as_we_go=False, file_name: str=None, **kwargs):
    """
    Evolve
    """

    # No point starting the run if no file_name given
    if save_as_we_go:
        if file_name is None:
            raise ValueError("file_name paramater cannot be None if save_as_we_go is True")
        else:
            append_matrix_to_csv(file_name, initial_surface.utility_grid)
    invasion_count = 0
    rejected_mutant_count = 0
    step_count = 0
    np.random.seed(seed)
    resident = initial_surface
    if time_series_data:
        # Only care about saving the utility grid at each mutation
        time_series_array = [resident.utility_grid]

    for step in range(1, iterations):
        step_count += 1
        resident, invasion, fitness_diff = evolution_step(resident, fitness_function,
                                            mutation_function,
                                            atol, **kwargs)
        if invasion:
            # Only care about saving the utility grid when an invasion occurs
            invasion_count += 1
            if time_series_data and (invasion_count % record_invasion_each_step == 0):
                time_series_array.append(resident.utility_grid)
            if save_as_we_go and (invasion_count % record_invasion_each_step == 0):
                append_matrix_to_csv(file_name, resident.utility_grid)
        else:
            rejected_mutant_count += 1
    if time_series_data:
        return resident, time_series_array, invasion_count
    return resident
