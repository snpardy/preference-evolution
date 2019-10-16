import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from paramless.utilitySurface import UtilitySurface
from paramless.paramless import gaussian_mutation_more_info, _bivariate_normal_mutation

if __name__ == '__main__':
    selfish = UtilitySurface.selfish(5, 0.1)

    mutation_epsilon = 0.3
    variance = 0.27243305619247093
    x_mean = 3
    y_mean = 3
    perturbation = _bivariate_normal_mutation(selfish, mutation_epsilon, x_mean,
                                            y_mean,
                                            variance)

    mutant_utility_grid = selfish.utility_grid + perturbation

    # mutant, replace(surface, utility_grid=np.around(mutant_utility_grid, 8))

    x = np.arange(0, 5, 0.1)
    X, Y = np.meshgrid(x, x, indexing='ij')

    fig = plt.figure()


    ax2 = fig.add_subplot(111, projection='3d')
    ax2.set_zlim3d(0, 5)
    ax2.plot_surface(X, Y, mutant_utility_grid, cmap='viridis', linewidth=0)
    ax2.set_title('Selfish Type After One Mutation')
    ax2.set_xlabel('My Payoff')
    ax2.set_ylabel("Opponent's Payoff")
    ax2.set_zlabel('Utility')
    ax2.view_init(elev=22, azim=-133)

    # a = -133, e = 23

    plt.savefig("one_mutation")
    # print(mutation_info)
    plt.show()