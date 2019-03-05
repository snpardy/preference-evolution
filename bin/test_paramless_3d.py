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
    x = np.linspace(-3,3, 20)
    y = np.array([i**2 for i in x])
    z = np.copy(y)

    target_surface = np.array([x,y,z])
    initial_z = randrange(len(x), 0, 9)
    initial_surface = np.array([x, y, initial_z])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(target_surface[0], target_surface[1], np.array([target_surface[2], target_surface[2]-2*target_surface[2]]), rstride=10, cstride=10)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()

    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(initial_surface[0], initial_surface[1], np.array([initial_surface[2], initial_surface[2]-2*initial_surface[2]]), rstride=10, cstride=10)

    plt.show()

    Result = evolve(initial_surface, distance_fitness_function, p.point_mutation, 10000, target_surface=target_surface, domain=initial_surface[0], width=18)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(Result[0], Result[1], np.array([Result[2], Result[2]-2*Result[2]]), rstride=10, cstride=10)

    plt.show()

if __name__ == '__main__':
    example()