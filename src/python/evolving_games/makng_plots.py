import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# from .paramless.utils import csv_to_time_series_array

from paramless import utils

if __name__ == '__main__':
    time_series = utils.csv_to_time_series_array('test_result.csv')
    payoff_size = 5

    X, Y = np.meshgrid(np.arange(0, 5, 0.5), np.arange(0, 5, 0.5), indexing='ij')

    # Make a 3D plot
    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_zlim3d(-1, payoff_size + 1)
    ax1.plot_surface(X, Y, time_series[0], cmap='viridis', linewidth=0)
    ax1.set_title('Initial Surface')
    ax1.set_xlabel('My Payoff')
    ax1.set_ylabel("Opponent's Payoff")
    ax1.set_zlabel('My Utility')

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_zlim3d(-1, payoff_size + 1)
    ax2.plot_surface(X, Y, time_series[-1], cmap='viridis', linewidth=0)
    ax2.set_title('Evolved Surface')
    ax2.set_xlabel('My Payoff')
    ax2.set_ylabel("Opponent's Payoff")
    ax2.set_zlabel('My Utility')
    plt.show()