import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

import paramless as p
import paramless_3d as ps

def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

def test_surface_distance():
    u = np.array([[2,1],[3,-2],[4,1],[2,3]])
    v = np.array([[1,2],[-2,3],[1,4],[3,2]])
    assert ps.surface_distance(u,v) == 12.0
    return True

def example():
    """

    """
    x = np.linspace(-3,3, 20)
    y = np.array([i**2 for i in x])
    z = np.copy(y)

    target_surface = np.array([x,y,z])
    initial_z = randrange(len(x), 0, 9)
    initial_surface = np.array([x, y, initial_z])

    fig = plt.figure()

    # Plotting the Target Surface
    ax1 = fig.add_subplot(221, projection='3d')
    ax1.plot_wireframe(target_surface[0], target_surface[1], np.array([target_surface[2], target_surface[2]-2*target_surface[2]]), rstride=10, cstride=10)
    
    ax1.set_title('Target Surface')
    ax1.set_xlabel('X Label')
    ax1.set_ylabel('Y Label')
    ax1.set_zlabel('Z Label')
   
    # Plotting the Initial Surface
    ax2 = fig.add_subplot(223, projection='3d')
    ax2.plot_wireframe(initial_surface[0], initial_surface[1], np.array([initial_surface[2], initial_surface[2]-2*initial_surface[2]]), rstride=10, cstride=10)
    ax2.set_title('Initial Surface')
    ax2.set_xlabel('X Label')
    ax2.set_ylabel('Y Label')
    ax2.set_zlabel('Z Label')


    # using paramless_3d to evolve the initial surface towards the target
    Result = ps.evolve(initial_surface, ps.distance_fitness_function, p.point_mutation, 10000, target_surface=target_surface, domain=initial_surface[0], width=18)

    # Plotting the Evolved surface
    ax3 = fig.add_subplot(224, projection='3d')
    ax3.plot_wireframe(Result[0], Result[1], np.array([Result[2], Result[2]-2*Result[2]]), rstride=10, cstride=10)
    ax3.set_title('Evolved Surface')    
    ax3.set_xlabel('X Label')
    ax3.set_ylabel('Y Label')
    ax3.set_zlabel('Z Label')
   

    plt.show()

if __name__ == '__main__':
    example()