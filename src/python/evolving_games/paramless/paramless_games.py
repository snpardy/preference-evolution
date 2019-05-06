from nashpy import Game
from mpl_toolkits.mplot3d import axes3d
from utilitySurface import UtilitySurface
import matplotlib.pyplot as plt
import numpy as np
import os
import paramless as p
import time
from matplotlib import cm


def save_run(path, time_series, run_data):
    HEIGHT = 6
    now = time.localtime(time.time())
    run_id = str(now.tm_year) + "_"+str(now.tm_mon)+"_"+str(now.tm_mday)+"_"+str(now.tm_hour)+"_"+str(now.tm_min)+"_"+str(now.tm_sec)
    path = path + run_id +"\\"
    os.mkdir(path)
    initial_surface: UtilitySurface = run_data['initial_surface']
    X = initial_surface.my_payoff
    Y = initial_surface.opponent_payoff
    initial_Z = initial_surface.utility_grid
    final_Z = time_series[-1]

    # Make a 3D plot
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.set_zlim3d(-HEIGHT, HEIGHT)
    ax1.plot_surface(X, Y, initial_Z, cmap='viridis', linewidth=0)
    ax1.set_title('Initial Surface')
    ax1.set_xlabel('My Payoff')
    ax1.set_ylabel("Opponent's Payoff")
    ax1.set_zlabel('My Utility')
    plt.savefig(path+'\\initial.png')
    plt.close(fig)

    fig = plt.figure()
    ax2 = fig.add_subplot(111, projection='3d')
    ax2.set_zlim3d(-HEIGHT, HEIGHT)
    ax2.plot_surface(X, Y, final_Z, cmap='viridis', linewidth=0)
    ax2.set_title('Evolved Surface')
    ax2.set_xlabel('My Payoff')
    ax2.set_ylabel("Opponent's Payoff")
    ax2.set_zlabel('My Utility')
    plt.savefig(path+'final.png')
    plt.close(fig)

    p.create_animation(path,
                       initial_surface.my_payoff,
                       initial_surface.opponent_payoff,
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
    return p.evolve(config["initial_surface"], config['fitness'], config['mutation'],
                    config['iterations'],
                    mutation_epsilon=config['mutation_epsilon'],
                    payoff_game=config['game'],
                    radius=config['radius'],
                    r=config['r'],
                    time_series_data=True,
                    )


if __name__ == '__main__':
    prisoners_dilemma = Game([[3, 5], [0, 1]], [[3, 0], [5, 1]])
    HIGHEST_PAYOFF = 5

    # setting up player's utility functions
    x = np.arange(0, HIGHEST_PAYOFF+1, 1, dtype=float)
    y = np.arange(0, HIGHEST_PAYOFF+1, 1, dtype=float)
    Z = np.meshgrid(x, y, indexing='ij')[0]

    selfless = UtilitySurface(x, y, Z)

    X, Y = np.meshgrid(x, y)
    # Make a 3D plot
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.plot_surface(X, Y, selfless.utility_grid, cmap=cm.coolwarm, linewidth=0)
    ax1.set_title('Initial Surface')
    ax1.set_xlabel('My Payoff')
    ax1.set_ylabel("Opponent's Payoff")
    ax1.set_zlabel('My Utility')
    plt.show()

    config_1 = {"title": "prisoners_dilemma",
                "game": prisoners_dilemma,
                "initial_surface": selfless,
                "fitness": p.payoff_fitness,
                "mutation": p.gaussian_mutation,
                "mutation_epsilon": .5,
                "r": 0,
                "iterations": 100,
                "radius": .1,
                "sucessful_invasions": None
                }

    output, tsa, invasions = evolve_helper(config_1)
    config_1["sucessful_invasions"] = invasions

    # Make a 3D plot
    # fig = plt.figure()
    # ax1 = fig.add_subplot(111, projection='3d')
    # ax1.set_zlim3d(-HIGHEST_PAYOFF+1, HIGHEST_PAYOFF+1)
    # ax1.plot_surface(selfless.my_payoff, selfless.opponent_payoff, tsa[-1], cmap='viridis', linewidth=0)
    # ax1.set_title('Initial Surface')
    # ax1.set_xlabel('My Payoff')
    # ax1.set_ylabel("Opponent's Payoff")
    # ax1.set_zlabel('My Utility')
    # plt.show()
