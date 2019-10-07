"""
A script used for making plots of outputs - not properly part of the 'evolving_games' codebase.
"""


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


from paramless import utils


if __name__ == '__main__':

    path_to_csv_dir = 'C:\\Users\\snpar\\Honours\\preference-evolution\\data\\last_try' \
                       '\\csv_files\\initial_selfless\\r_0.0\\'
    average_path = 'C:\\Users\\snpar\\Honours\\preference-evolution\\data\\last_try' \
                       '\\csv_files\\initial_random\\r_0.0\\average_surface.csv'

    # If you need to create the average surface:
    # average_surface = utils.average_surface(path_to_csv_dir)
    # utils.append_matrix_to_csv(average_path, average_surface)

    # If you have the average surface:
    average_surface = utils.csv_to_time_series_array(average_path)[0]



    payoff_size = 5
    x = np.arange(0, 5, 0.1)
    X, Y = np.meshgrid(x, x, indexing='ij')


    # Line graph of cross-section of surface
    opp_pay = 40
    print(opp_pay)
    col = average_surface[:, opp_pay]
    # col = np.mean(average_surface, axis=1)
    print(col)
    
    
    
    fig, ax = plt.subplots()
    ax.plot(x, col)
    
    ax.set(xlabel='my payoff', ylabel='utility')
    ax.grid()



    # Make a 3D plot
    fig = plt.figure()
    # ax1 = fig.add_subplot(121, projection='3d')
    # ax1.set_zlim3d(-1, 5)
    # ax1.plot_surface(X, Y, time_series[0], cmap='viridis', linewidth=0)
    # ax1.set_title('Initial Surface')
    # ax1.set_xlabel('My Payoff')
    # ax1.set_ylabel("Opponent's Payoff")
    # ax1.set_zlabel('My Utility')

    ax2 = fig.add_subplot(111, projection='3d')
    ax2.set_zlim3d(-1, 5)
    ax2.plot_surface(X, Y, average_surface, cmap='viridis', linewidth=0)
    ax2.set_title('Evolved Surface')
    ax2.set_xlabel('My Payoff')
    ax2.set_ylabel("Opponent's Payoff")
    ax2.set_zlabel('My Utility')

    plt.show()