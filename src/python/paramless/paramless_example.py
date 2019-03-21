import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D
from copy import deepcopy as deepcopy
import math
import paramless_two_args as p

def my_multivariate_normal(x, y, mutation_epsilon, mean_x, mean_y, variance):
    # This function assumes that the pearson correlation coefficient is 0
    return mutation_epsilon * (math.e ** -((.5)*((((x-mean_x)**2)/variance**2) + (((y-mean_y)**2)/variance**2))))
    
def example_evolution():
    # the x and y axes
    x = np.arange(0, 10, dtype=float)
    y = np.arange(0, 10, dtype=float)
    
    #Create grid and multivariate normal
    X, Y = np.meshgrid(x,y)
    Z = my_multivariate_normal(X, Y, 1, 5, 5, 3)


    target_surface = [X,Y,Z]
    initial_surface = [X,Y,np.zeros_like(X, dtype=float)]
    result_surface = p.evolve(initial_surface, p.distance_fitness_function, p.gaussian_mutation, 10000, target_surface=target_surface,
    mutation_epsilon=.05, radius=2)
   
   
    #Make a 3D plot
    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.plot_surface(X, Y, Z,cmap='viridis',linewidth=0)
    ax1.set_title('Target Surface')
    ax1.set_xlabel('X axis')
    ax1.set_ylabel('Y axis')
    ax1.set_zlabel('Z axis')
    
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.plot_surface(X, Y, result_surface[2],cmap='viridis',linewidth=0)
    ax2.set_title('Evolved Surface')
    ax2.set_xlabel('X axis')
    ax2.set_ylabel('Y axis')
    ax2.set_zlabel('Z axis')
    plt.show()

if __name__ == '__main__':
    example_evolution()