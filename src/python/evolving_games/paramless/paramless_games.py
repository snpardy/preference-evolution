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


def expected_payoff(payoff_matrices, equilibria):
    row_strategy = equilibria[0]
    column_strategy = equilibria[1]
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
    :param row_utility:
    :param column_utility:
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
    if random.random() >= r:
        utility_game = utility_transform(payoff_game, resident, mutant)
    else:
        utility_game = utility_transform(payoff_game, resident, resident)
    equilibria = list(utility_game.support_enumeration())
    eq = equilibria[random.randrange(len(equilibria))]
    ep = expected_payoff(payoff_game.payoff_matrices, eq)
    return ep


def save_run(path, time_series, run_data):
    HEIGHT = 1.1
    now = time.localtime(time.time())
    run_id = str(now.tm_year) + "_"+str(now.tm_mon)+"_"+str(now.tm_mday)+"_"+str(now.tm_hour)+"_"+str(now.tm_min)+"_"+str(now.tm_sec)
    path = path + run_id +"\\"
    os.mkdir(path)

    initial = time_series[0][2]
    final = time_series[-1][2]

    # Make a 3D plot
    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_zlim3d(-HEIGHT, HEIGHT)
    ax1.plot_surface(X, Y, initial, cmap='viridis', linewidth=0)
    ax1.set_title('Initial Surface')
    ax1.set_xlabel('X axis')
    ax1.set_ylabel('Y axis')
    ax1.set_zlabel('Z axis')
    plt.savefig(path+'\\initial.png', bbox_inches='tight')
    plt.close(fig)

    fig = plt.figure()
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_zlim3d(-HEIGHT, HEIGHT)
    ax2.plot_surface(X, Y, final, cmap='viridis', linewidth=0)
    ax2.set_title('Evolved Surface')
    ax2.set_xlabel('X axis')
    ax2.set_ylabel('Y axis')
    ax2.set_zlabel('Z axis')
    plt.savefig(path+'final.png', bbox_inches='tight')
    plt.close(fig)

    p.create_gif(path,
                 time_series,
                 HEIGHT)

    with open(path+"summary.txt", "w") as file:
        for k, v in run_data.items():
            file.write(k + ": " + str(v)+"\n")


if __name__ == '__main__':
    games = Games()
    HIGHEST_PAYOFF = 5

    # setting up player's utility functions
    x = np.arange(0, HIGHEST_PAYOFF+1, dtype=float)
    y = np.arange(0, HIGHEST_PAYOFF+1, dtype=float)
    X, Y = np.meshgrid(x, y, indexing='ij')
    iu = InitialUtility(X)

    r1 = {"game": "prisoners_dilemma", "mutation_epsilon": .05, "r": .8, "iterations": 1000000, "sucessful_invasions": None}

    output, tsa, invasions = p.evolve([X, Y, iu.zeroes], payoff_fitness, p.gaussian_mutation, 1000000,
                                      mutation_epsilon=.05,
                                      payoff_game=games.prisoners_dilemma,
                                      radius=4,
                                      r=0.8,
                                      time_series_data=True)

    r1["sucessful_invasions"] = invasions
    save_run("C:\\Users\\snpar\\Honours\\preference-evolution\\data\\paramless_run\\", tsa, r1)
