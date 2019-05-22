"""
Created on 2019-03-05 12:59
@summary: Paramless evolution on a 3D surface. Based on Julian Garcia's paramless - github.com/juliangarcia/paramless
@author: snpardy
"""
from dataclasses import replace    # standard library
import math
import random

from nashpy import Game    # 3rd party packages
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from utilitySurface import UtilitySurface    # local source
import fitness

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
            math.e ** -(.5 * ((((x_grid - mean_x) ** 2) / variance ** 2) + (
                ((y_grid - mean_y) ** 2) / variance ** 2))))


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


def gaussian_mutation(surface: UtilitySurface, mutation_epsilon, radius,
                      max_iterations=1000000, lower_bound=None,
                      upper_bound=None, **kwargs):
    is_inside = False
    attempt = 0
    mutant = None
    while not is_inside:
        mutant = _attempt_gaussian_mutation(surface, mutation_epsilon, radius)
        is_inside = _within_bounds(mutant, lower_bound, upper_bound)
        attempt += 1
        if attempt > max_iterations:
            raise RuntimeError(
                "Attempted too many mutations without producing anything within bounds")
    return mutant


# Fitness Functions for payoff-utility fitness
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


def _utility_transform(game: Game, row_utility, column_utility):
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
            row_player[i][j] = row_utility[row_payoff_matrix[i][j], column_payoff_matrix[i][j]]
            column_player[i][j] = column_utility[
                column_payoff_matrix[i][j], row_payoff_matrix[i][j]]
    return Game(row_player, column_player)


def random_payoff_fitness(resident: np.meshgrid, mutant: np.meshgrid, **kwargs):
    payoff_game: Game = kwargs['payoff_game']

    utility_game = _utility_transform(payoff_game, resident, mutant)
    equilibria = list(utility_game.support_enumeration())
    equilibrium = random.choice(equilibria)

    return _expected_payoff(payoff_game, equilibrium)


def exhaustive_payoff_fitness(resident: np.meshgrid, mutant: np.meshgrid, **kwargs):
    """
    Given the resident utility functions of the resident and the mutant
    to calculate the equilibria.
    Then uses this equilibria to calculate the expected payoff of both
    players for the given game.

    :param resident: np.meshgrid utility function
    :param mutant: np.meshgrid utility function
    :param payoff_game: nashpy game object
    :return: a tuple of (resident payoff, mutant payoff)
    """
    payoff_game: Game = kwargs['payoff_game']

    utility_game = _utility_transform(payoff_game, resident, mutant)
    equilibria = utility_game.support_enumeration()

    resident_payoff_list = []
    mutant_payoff_list = []
    for eq in equilibria:
        # For each equilibrium, we unpack the
        # expected payoffs for both types for each
        resident_payoff_list[len(resident_payoff_list):], \
            mutant_payoff_list[len(mutant_payoff_list):] \
            = tuple(zip(_expected_payoff(payoff_game, eq)))

    return fitness.Exhaustive(resident_payoff_list), \
        fitness.Exhaustive(mutant_payoff_list)


# Evolution
def evolution_step(resident: UtilitySurface, fitness_function, mutation_function, atol,
                   **kwargs):
    """
    One generation iteration
    """

    invasion = False
    mutant = mutation_function(resident, **kwargs)

    fitness_resident, fitness_mutant = fitness_function(resident.utility_grid,
                                                        mutant.utility_grid, **kwargs)

    if fitness_resident < fitness_mutant and abs(fitness_resident - fitness_mutant) > atol:
        resident = mutant
        invasion = True
    return resident, invasion


def evolve(initial_surface: UtilitySurface, fitness_function, mutation_function, iterations,
           atol=DEFAULT_ATOL, seed=None, time_series_data=False, **kwargs):
    """
    Evolve
    """
    invasion_count = 0
    step_count = 0
    np.random.seed(seed)
    resident = initial_surface
    if time_series_data:
        # Only care about saving the utility grid at each mutation
        time_series_array = [resident]

    # with progressbar.ProgressBar(max_value=iterations) as bar:
    for step in range(1, iterations):
        step_count += 1
        # bar.update(step)
        resident, invasion = evolution_step(resident, fitness_function, mutation_function,
                                            atol, **kwargs)
        if invasion:
            invasion_count += 1
            if time_series_data:
                # Only care about saving the utility grid at each mutation
                time_series_array.append(resident)
    if time_series_data:
        return resident, time_series_array, invasion_count
    return resident


'''
Extra functions - not part of main evolution simulation.
'''


def create_animation(path, x, y, time_series_array, height, fps, mp4=True, gif=False):
    """

    """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.xlabel("My Payoff")
    plt.ylabel("Opponent's Payoff")

    def update_plot(frame_number, z, plot):
        plot[0].remove()
        plot[0] = ax.plot_surface(x, y, z[frame_number], cmap="viridis", linewidth=0)

    plot = [ax.plot_surface(x, y, time_series_array[0], cmap='viridis', linewidth=0)]

    ax.set_zlim(-height, height)

    ani = animation.FuncAnimation(fig, update_plot, len(time_series_array),
                                  fargs=(time_series_array, plot),
                                  interval=1000 / fps)

    fn = 'plot_surface_animation'
    if mp4:
        ani.save(path + fn + '.mp4', writer='ffmpeg', fps=fps)
    if gif:
        ani.save(path + fn + '.gif', writer='imagemagick', fps=fps)


# Unused and untested since recent changes
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
                one_point_dist += (u[axis][i, j] - v[axis][i, j]) ** 2
            total += math.sqrt(one_point_dist)

    return total


# Unused and untested since recent changes
def _distance_fitness_function(resident, mutant, target_surface, **kwargs):
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
