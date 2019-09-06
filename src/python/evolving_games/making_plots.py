import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


from paramless import utils


if __name__ == '__main__':
    time_series = utils.csv_to_time_series_array('C:\\Users\\snpar\\Honours\\preference-evolution\\data\\results_250k_iterations\\Evolution_initial_selfless_popShare_0.5_mutationEp_0.5_mutationR_4_payoff_5_step_0.5_seed_900269190.csv')



    payoff_size = 5
    X, Y = np.meshgrid(np.arange(0, 5, 0.5), np.arange(0, 5, 0.5), indexing='ij')

    # utils.create_animation('C:\\Users\\snpar\\Honours\\preference-evolution\\data\\results_250k_iterations\\', X, Y, time_series, 5, (len(time_series)/480))

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
    ax2.plot_surface(X, Y, time_series[len(time_series)//2], cmap='viridis', linewidth=0)
    ax2.set_title('Evolved Surface')
    ax2.set_xlabel('My Payoff')
    ax2.set_ylabel("Opponent's Payoff")
    ax2.set_zlabel('My Utility')
    plt.show()