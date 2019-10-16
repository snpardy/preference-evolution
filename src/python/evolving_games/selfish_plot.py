import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

from paramless.utilitySurface import UtilitySurface

if __name__ == '__main__':
    selfish = UtilitySurface.selfish(5, 0.1)
    print(selfish.utility_grid)
    x = np.arange(0, 5, 0.1)
    X, Y = np.meshgrid(x, x, indexing='ij')

    fig = plt.figure()


    ax2 = fig.add_subplot(111, projection='3d')
    ax2.set_zlim3d(0, 5)
    ax2.plot_surface(X, Y, selfish.utility_grid, cmap='viridis', linewidth=0)
    ax2.set_title('Selfish Type')
    ax2.set_xlabel('My Payoff')
    ax2.set_ylabel("Opponent's Payoff")
    ax2.set_zlabel('Utility')
    ax2.view_init(elev=22, azim=-133)

    # a = -133, e = 23

    plt.savefig("selfish")
    plt.show()