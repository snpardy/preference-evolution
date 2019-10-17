"""
A script used for making plots of outputs - not properly part of the 'evolving_games' codebase.
"""


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


from paramless import utils
from paramless.utilitySurface import UtilitySurface
from paramless.game import Game


def _surface_distance(u, v):
    """
    Calculates the sum of euclidian distance between respective points in two given surfaces.
    Used as a distance function.
    Assumes that the arrays representing the surfaces are the same shape.
    """
    total = 0
    for i in range(len(u)):
        for j in range(len(u[i])):
            one_point_dist = (u[i][j] - v[i][j]) ** 2
            total += np.sqrt(one_point_dist)

    return total


def test_fitness_symmetric(target: UtilitySurface, evolved: UtilitySurface, rounds=200, max_payoff=5, **kwargs):
    target_fitness, evolved_fitness = 0, 0
    for _ in range(rounds):
        # Generating game for the round
        payoff_array = np.zeros(4)
        # A
        payoff_array[0] = np.random.random(1) * 5
        # D
        payoff_array[3] = np.random.random(1) * 5
        # B
        payoff_array[1] = np.random.random(1) * 5
        # C
        payoff_array[2] = np.random.random(1) * 5

        resident_payoffs = np.reshape(payoff_array, (-1, 2))
        mutant_payoffs = np.reshape(np.transpose(resident_payoffs), (-1, 2))

        game: Game = Game(resident_payoffs, mutant_payoffs)

        # Converting to utility based game
        t_e_utility_game = game.utility_transform(target, evolved)

        # List of equilibrias
        t_e_eqs = list(t_e_utility_game.support_enumeration())

        # Calculates the fitness as specified in ALger & Weibull 2012,  pg. 44, equations 4,5
        curr_t_e_payoff = 0
        curr_e_t_payoff = 0
        for eq in t_e_eqs:
            t, e = game.expected_payoff(eq)
            curr_t_e_payoff += t
            curr_e_t_payoff += e

        curr_t_e_payoff /= len(t_e_eqs)


        curr_e_t_payoff /=len(t_e_eqs)
 

        target_fitness += curr_t_e_payoff
        evolved_fitness += curr_e_t_payoff

    return target_fitness/rounds, evolved_fitness/rounds



if __name__ == '__main__':
    selfish = UtilitySurface.selfish(5, 0.1)
    x = np.arange(0, 5, 0.1)


    path_to_plot_csv = 'C:\\Users\\snpar\\Honours\\preference-evolution\\data\\last_try\\symmetric\\csv_files\\initial_selfless\\r_0.0\\average_surface.csv'
    path_to_dir = 'C:\\Users\\snpar\\Honours\\preference-evolution\\data\\last_try\\symmetric\\csv_files\\initial_selfless\\r_0.0\\'

    time_series = np.array(utils.csv_to_time_series_array(path_to_plot_csv))

    # curr = UtilitySurface(x, x, time_series[-1], 0.1)

    # surface_array = utils.array_final_matrices_in_dir(path_to_dir)
    distances = []
    fitnesses_against_target = []
    fitness_against_self = []
    fitnesses_target_target = []

    # for surface in surface_array:
    #     distances.append(_surface_distance(selfish.utility_grid, surface))
    #     # curr = UtilitySurface(x, x, surface, 0.1)
    #     fitnesses_against_target.append(test_fitness_symmetric(selfish, curr)[1])
    #     fitness_against_self.append(test_fitness_symmetric(curr, curr)[1])
    #     fitnesses_target_target.append(test_fitness_symmetric(selfish, selfish)[0])


    # # fig, ax = plt.subplots()
    # # ax.set_title("Distance between evolved surfaces and Target Surface")
    # # ax.boxplot(distances)
    # # plt.show()

    # fitness_of_target = test_fitness_symmetric(selfish, selfish)
    # print("Fitness of target: {}".format(fitness_of_target))

    # fig, ax = plt.subplots()
    # ax.set_title("Fitness earned by Evolved surfaces against Target Surface")
    # data = [fitnesses_against_target, fitness_against_self, fitnesses_against_target]
    # l = ["Evolved vs. Target", "Evolved vs. self", "Target vs. self"]
    # ax.set_xticklabels(l, fontsize=10)
    # ax.boxplot(data)

    # plt.xticks([1,2,3], l)


    # plt.show()


    payoff_size = 5
    x = np.arange(0, 5, 0.1)
    X, Y = np.meshgrid(x, x, indexing='ij')

    # Make a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, time_series[-1], cmap='viridis', linewidth=0)
    ax.set_title('Evolved Surface')
    ax.set_xlabel('My Payoff')
    ax.set_ylabel("Opponent's Payoff")
    ax.set_zlabel('My Utility')
    ax.view_init(elev=25, azim=-161)

    plt.savefig("average_r_0_symmetric_evolved.png")
    plt.show()