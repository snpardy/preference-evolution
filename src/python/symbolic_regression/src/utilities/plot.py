import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from matplotlib import cm
import numpy as np

from utilities.algorithm.general import function_builder



def plot_initial_and_evolved(initial, evolved, min_payoff=0, max_payoff=5, step=0.1,
                             save_plot=False, path=None):

    axis = np.arange(min_payoff, max_payoff, step)

    x, y = np.meshgrid(axis, axis, indexing='ij')

    i = initial(x, y)
    e = evolved(x, y)


    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    # ax1.set_zlim3d(min_payoff, max_payoff)
    ax1.plot_surface(x, y, i, cmap='viridis', linewidth=0)
    ax1.set_title('Initial Surface')
    ax1.set_xlabel('My Payoff')
    ax1.set_ylabel("Opponent's Payoff")
    ax1.set_zlabel('My Utility')

    ax2 = fig.add_subplot(122, projection='3d')
    # ax2.set_zlim3d(min_payoff, max_payoff)
    ax2.plot_surface(x, y, e, cmap='viridis', linewidth=0)
    ax2.set_title('Evolved Surface')
    ax2.set_xlabel('My Payoff')
    ax2.set_ylabel("Opponent's Payoff")
    ax2.set_zlabel('My Utility')

    plt.show()

    if save_plot:
        plt.savefig(path)


def plot_phenotype_as_surface(phenotype, min_payoff=0, max_payoff=5, step=0.1, save_plot=False,
                              path=None):
    fig = plt.figure()

    axis = np.arange(min_payoff, max_payoff, step)

    x, y = np.meshgrid(axis, axis, indexing='ij')

    z = phenotype_to_matrix(phenotype, max_payoff, step, min_payoff)

    ax2 = fig.add_subplot(111, projection='3d')
    # ax2.set_zlim3d(min_payoff, max_payoff)
    ax2.plot_surface(x, y, z, cmap='viridis', linewidth=0)
    ax2.set_title('Evolved Surface')
    ax2.set_xlabel('My Payoff')
    ax2.set_ylabel("Opponent's Payoff")
    ax2.set_zlabel('My Utility')

    plt.show()

    if save_plot:
        plt.savefig(path)


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

    # ax.set_zlim(-1, height)

    ani = animation.FuncAnimation(fig, update_plot, len(time_series_array),
                                  fargs=(time_series_array, plot),
                                  interval=1000 / fps)

    fn = 'plot_surface_animation'
    if mp4:
        ani.save(path + fn + '.mp4', writer='ffmpeg', fps=fps)
    if gif:
        ani.save(path + fn + '.gif', writer='imagemagick', fps=fps)


def phenotype_to_matrix(phenotype: str, max:int, step:float, min:int =0):
    f = function_builder(phenotype)

    axis = np.arange(min, max, step)

    x, y = np.meshgrid(axis, axis, indexing='ij')

    return f(x, y)



def _selfish(x, y):
    return x

def _selfless(x, y):
    return y


if __name__ == '__main__':
    plot_initial_and_evolved(_selfless, _selfish)

