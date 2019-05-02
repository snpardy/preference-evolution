import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy as deepcopy
from mpl_toolkits.mplot3d import axes3d
import paramless as p
from nashpy import Game
import random
import time
import progressbar
import os
from collections import namedtuple

class Games:
    """
    A place to define pay off structures of games. Uses nashpy for Game class.
    """
    def __init__(self):
        self.prisoners_dilemma = Game(np.array([[3, 0], [5, 1]]), np.array([[3, 5], [0, 1]]))
        self.stag_hunt = Game(np.array([[5, 0], [3, 3]]), np.array([[5, 3], [0, 3]]))


class InitialUtility:
    """
    A place to define initial utility surfaces that could be used in the evolution.
    """
    def __init__(self, payoff):
        self.mx = np.max(payoff)
        # Dividing by 10 here is a bit hacky, just put in to have a look at the
        # plots with max Z axis of 1
        self.selfish = deepcopy(payoff/10)
        self.zeroes = np.zeros_like(payoff/10)
        self.random = np.zeros_like(payoff)
        self.randomize()

    def randomize(self):
        for i in range(len(self.selfish)):
            for j in range(len(self.selfish[i])):
                self.random[i, j] = random.random()


def expected_payoff(payoff_matrices, equilibrium):
    """
    Given a game with payoff structure of :param payoff_matrices:
    and a strategy equilibrium of :param equilibrium:
    :param payoff_matrices:
    :param equilibrium: tuple of arrays of probability of playing each strategy.
    """
    row_strategy = equilibrium[0]
    column_strategy = equilibrium[1]
    row_payoff = 0
    column_payoff = 0
    for i, _ in enumerate(row_strategy):
        for j, _ in enumerate(column_strategy):
            row_payoff += row_strategy[i] * column_strategy[j] * payoff_matrices[0][i][j]
            column_payoff += row_strategy[i] * column_strategy[j] * payoff_matrices[1][i][j]

    return row_payoff, column_payoff


def utility_transform(game, row_utility, column_utility):
    """
    Returns a new Game with the pay-off altered by the given utility functions.
    Assumes that the utility 'functions' are grids that accept arguments in the form of utility_function[my_payoff, opponents_payoff]
    This could be bad?
    :param game: nashpy Game object
    :param row_utility: np mesh grid
    :param column_utility: np mesh grid
    :return: Game: nashpy Game object
    """

    # There should be a better way to do this but ?? :(
    row_player = [[None for _ in range(len(game.payoff_matrices[0][0]))]
                  for _ in range(len(game.payoff_matrices[0]))]
    column_player = [[None for _ in range(len(game.payoff_matrices[0][0]))]
                     for _ in range(len(game.payoff_matrices[0]))]

    for i, _ in enumerate(game.payoff_matrices[0]):
        for j, _ in enumerate(game.payoff_matrices[0][i]):
            row_player[i][j] = row_utility[game.payoff_matrices[0][i][j], game.payoff_matrices[1][i][j]]
            column_player[i][j] = column_utility[game.payoff_matrices[1][i][j], game.payoff_matrices[0][i][j]]
    return Game(row_player, column_player)


def payoff_fitness(resident, mutant, payoff_game, r=0, **kwargs):
    """
    Given the resident utility functions of the resident and the mutant to calculate the equilibria.
    Then uses this equilibria to calculate the expected payoff of both players for the given game.
    :param resident: np meshgrid utility function
    :param mutant: np meshgrid utility function
    :param payoff_game: nashpy game object
    :return: a tuple of (resident payoff, mutant payoff)
    """
    utility_game = utility_transform(payoff_game, resident, mutant)
    equilibria = list(utility_game.support_enumeration())
    eq = equilibria[random.randrange(len(equilibria))]
    ep = expected_payoff(payoff_game.payoff_matrices, eq)
    return ep


def save_run(path, time_series, run_data):
    HEIGHT = 6
    now = time.localtime(time.time())
    run_id = str(now.tm_year) + "_"+str(now.tm_mon)+"_"+str(now.tm_mday)+"_"+str(now.tm_hour)+"_"+str(now.tm_min)+"_"+str(now.tm_sec)
    path = path + run_id +"\\"
    os.mkdir(path)

    initial = time_series[0][2]
    final = time_series[-1][2]

    # Make a 3D plot
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.set_zlim3d(-HEIGHT, HEIGHT)
    ax1.plot_surface(X, Y, initial, cmap='viridis', linewidth=0)
    ax1.set_title('Initial Surface')
    ax1.set_xlabel('My Payoff')
    ax1.set_ylabel("Opponent's Payoff")
    ax1.set_zlabel('My Utility')
    plt.savefig(path+'\\initial.png')
    plt.close(fig)

    fig = plt.figure()
    ax2 = fig.add_subplot(111, projection='3d')
    ax2.set_zlim3d(-HEIGHT, HEIGHT)
    ax2.plot_surface(X, Y, final, cmap='viridis', linewidth=0)
    ax2.set_title('Evolved Surface')
    ax2.set_xlabel('My Payoff')
    ax2.set_ylabel("Opponent's Payoff")
    ax2.set_zlabel('My Utility')
    plt.savefig(path+'final.png')
    plt.close(fig)

    p.create_gif(path,
                 time_series,
                 HEIGHT,
                 10)

    with open(path+"summary.txt", "w") as file:
        for k, v in run_data.items():
            if k == 'X' or k == 'Y':
                pass
            else:
                file.write(k + ": " + str(v)+"\n")


def evolve_helper(config):
    return p.evolve([config['X'], config['Y'], config['initial']], config['fitness'], config['mutation'],
                    config['iterations'],
                    mutation_epsilon=config['mutation_epsilon'],
                    payoff_game=config['game'],
                    radius=config['radius'],
                    r=config['r'],
                    time_series_data=True,
                    )


if __name__ == '__main__':
    games = Games()
    HIGHEST_PAYOFF = 5

    # setting up player's utility functions
    x = np.arange(0, HIGHEST_PAYOFF+1, .1, dtype=float)
    y = np.arange(0, HIGHEST_PAYOFF+1, .1, dtype=float)
    X, Y = np.meshgrid(x, y, indexing='ij')
    iu = InitialUtility(X)

    config_1 = {"title": "prisoners_dilemma",
                "game": games.prisoners_dilemma,
                "X": X,
                "Y": Y,
                "initial": iu.zeroes,
                "fitness": payoff_fitness,
                "mutation": p.gaussian_mutation,
                "mutation_epsilon": .1,
                "r": 0,
                "iterations": 1000000,
                "radius": .01,
                "sucessful_invasions": None
                }

    output, tsa, invasions = evolve_helper(config_1)

    config_1["sucessful_invasions"] = invasions
    save_run("C:\\Users\\snpar\\Honours\\preference-evolution\\data\\paramless_run\\", tsa, config_1)
