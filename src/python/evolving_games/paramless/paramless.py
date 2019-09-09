"""
Created on 2019-03-05 12:59
@summary: Paramless evolution on a 3D surface. Based on Julian Garcia's paramless - github.com/juliangarcia/paramless
@author: snpardy
"""
from dataclasses import replace    # standard library
import math
import random


import numpy as np   # 3rd party library

from .fitness_class import Exhaustive   # local source
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

    perturbation = _bivariate_normal_mutation(surface, mutation_epsilon, x_mean, y_mean,
                                              variance)
    # upwards
    if np.random.randint(2):
        mutant_utility_grid = surface.utility_grid + perturbation
    # downwards
    else:
        mutant_utility_grid = surface.utility_grid - perturbation

    return replace(surface, utility_grid=mutant_utility_grid)


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


# Fitness Functions for payoff-utility fitness
def _bayesian_nash_resident_vs_mutant(game: Game, population_epsilon: float):
    
    rowRes = game.payoff_matrices[0]
    colRes = np.transpose(game.payoff_matrices[0])
    colMut = game.payoff_matrices[1]


    mutant_share = population_epsilon
    resident_share = 1 - population_epsilon
    
    combined_resident = [[] for _ in range(len(game.payoff_matrices[0]))]
    combined_mutant = [[] for _ in range(len(game.payoff_matrices[0]))]

    for rowIndex, row in enumerate(combined_resident):
        for i in (0,1):
            for j in (0,1):
                row.append(resident_share*rowRes[index][i] + mutant_share*rowRes[index][j])
                combined_mutant[rowIndex].append(resident_share*colRes[index][i] + mutant_share*colMut[index][j])

    bayesian_game = Game(combined_resident, combined_mutant)
    
    return bayesian_game.vertex_enumeration()
    

def _expected_payoff(game: Game, equilibrium):
    """
    Given a game with payoff structure of :param payoff_matrices:
    and a strategy equilibrium of :param equilibrium:
    :param equilibrium: tuple of arrays of probability of playing each strategy.
    """
    row_strategy = equilibrium[0]
    column_strategy = equilibrium[1]
    row_payoff = 0
    column_payoff = 0
    for i, _ in enumerate(row_strategy):
        for j, _ in enumerate(column_strategy):
            row_payoff += row_strategy[i] * column_strategy[j] * game.payoff_matrices[0][i][j]
            column_payoff += row_strategy[i] * column_strategy[j] * game.payoff_matrices[1][i][
                j]

    return row_payoff, column_payoff


def _utility_transform(game: Game, row_utility: UtilitySurface, column_utility: UtilitySurface):
    """
    Returns a new Game with the pay-off altered by the given utility functions.
    Assumes that the utility 'functions' are grids that accept arguments in the form of utility_function[my_payoff, opponents_payoff]
    This could be bad?
    :param game: nashpy Game object
    :param row_utility: np mesh grid
    :param column_utility: np mesh grid
    :return: Game: nashpy Game object
    """
    row_payoff_matrix = game.payoff_matrices[0]
    column_payoff_matrix = game.payoff_matrices[1]
    # There should be a better way to do this but ?? :(
    # This section just sets up arrays of the correct shape
    row_player = [[None for _ in range(len(game.payoff_matrices[0][0]))]
                  for _ in range(len(game.payoff_matrices[0]))]
    column_player = [[None for _ in range(len(game.payoff_matrices[0][0]))]
                     for _ in range(len(game.payoff_matrices[0]))]

    for i, _ in enumerate(row_payoff_matrix):
        for j, _ in enumerate(row_payoff_matrix[i]):
            row_player[i][j] = row_utility.get_utility_by_payoff(row_payoff_matrix[i][j],
                                                                 column_payoff_matrix[i][j])
            column_player[i][j] = column_utility.get_utility_by_payoff(
                column_payoff_matrix[i][j], row_payoff_matrix[i][j])
    return Game(row_player, column_player)



def tournament_fitness_function(resident: UtilitySurface, mutant:
                                              UtilitySurface, population_epsilon: float,
                                              assortativity: float=0,
                                              rounds=100,
                                              max_payoff=5,
                                              **kwargs):
    """
    :param resident: np.meshgrid utility function
    :param mutant: np.meshgrid utility function
    :param rounds: number of rounds the tournament goes for.
    :param max_payoff: max payoff that can be generated in a game.
    :return: a tuple of (resident payoff, mutant payoff)
    """

    resident_fitness, mutant_fitness = 0, 0
    for _ in range(rounds):
        # Generating game for the round
        payoffs = np.reshape((max_payoff * np.random.random(4)), (-1, 2))
        game: Game = Game(payoffs, np.transpose(payoffs))

        # Converting to utility based game
        resident_mutant_utility_game = _utility_transform(game, resident, mutant)
        resident_resident_utility_game = _utility_transform(game, resident, resident)

        # Selecting equilibria
        resident_mutant_equilibria = random.choice(list(
            resident_mutant_utility_game.support_enumeration()))
        resident_resident_equilibria = random.choice(list(
            resident_resident_utility_game.support_enumeration()))

        resident_payoff = (1-population_epsilon) * (
                               _expected_payoff(game,resident_resident_equilibria)[0])\
                          + population_epsilon*_expected_payoff(game, resident_mutant_equilibria)[0]

        mutant_payoff = _expected_payoff(game, resident_mutant_equilibria)[1]

        resident_fitness += resident_payoff
        mutant_fitness += mutant_payoff
    #     do we need to divide by something here to get average?
    return resident_fitness, mutant_fitness


def localised_tournament_fitness_function(resident: UtilitySurface,
                                      mutant: UtilitySurface,
                                      mutation_info: tuple,
                                      population_epsilon: float,
                                      assortativity: float=0,
                                      rounds=100,
                                      max_payoff=5,
                                              **kwargs):

    """
    :param resident: np.meshgrid utility function
    :param mutant: np.meshgrid utility function
    :param rounds: number of rounds the tournament goes for.
    :param max_payoff: max payoff that can be generated in a game.
    :return: a tuple of (resident payoff, mutant payoff)
    """

    variance = mutation_info[0]
    resident_mean = mutation_info[1]
    mutant_mean = mutation_info[2]

    locality = variance*1.5

    resident_min = resident_mean-locality
    resident_max = resident_mean+locality
    mutant_min = mutant_mean-locality
    mutant_max = mutant_mean+locality

    if resident_min < 0:
        resident_min = 0
    if mutant_min < 0:
        mutant_min = 0
    if resident_max > max_payoff:
        resident_max = max_payoff
    if mutant_max > max_payoff:
        mutant_max = max_payoff

    resident_fitness, mutant_fitness = 0, 0
    for _ in range(rounds):
        # Generating game for the round
        payoffs = np.reshape((np.random.random(4)), (-1, 2))
        resident_payoffs = resident_min + payoffs*(resident_max-resident_min)
        mutant_payoffs = mutant_min + np.transpose(payoffs)*(mutant_max-mutant_min)
        game_resident_mutant: Game = Game(resident_payoffs, mutant_payoffs)
        game_resident_resident: Game = Game(resident_payoffs, np.transpose(resident_payoffs))

        # Converting to utility based game
        resident_mutant_utility_game = _utility_transform(game_resident_mutant, resident, mutant)
        resident_resident_utility_game = _utility_transform(game_resident_resident, resident, resident)

        # Selecting equilibria
        resident_mutant_equilibria = random.choice(list(
            resident_mutant_utility_game.support_enumeration()))
        resident_resident_equilibria = random.choice(list(
            resident_resident_utility_game.support_enumeration()))

        resident_payoff = (1-population_epsilon) * (
                               _expected_payoff(game_resident_resident, resident_resident_equilibria)[0])\
                          + population_epsilon*_expected_payoff(game_resident_mutant, resident_mutant_equilibria)[0]

        mutant_payoff = _expected_payoff(game_resident_mutant, resident_mutant_equilibria)[1]

        resident_fitness += resident_payoff
        mutant_fitness += mutant_payoff
    #     do we need to divide by something here to get average?
    return resident_fitness, mutant_fitness


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
    if time_series_data:
        return resident, time_series_array, invasion_count
    return resident
