"""
Created on 2019-08-06 13:30
@summary: A place for functions that support paramless evolution (e.g saving run details,
creating animations)
@author: snpardy
"""

import os
import time
import glob
from collections import deque

import matplotlib.animation as animation      # 3rd party packages
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import numpy as np

from .utilitySurface import UtilitySurface  # local source


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

    ax.set_zlim(-1, height)

    ani = animation.FuncAnimation(fig, update_plot, len(time_series_array),
                                  fargs=(time_series_array, plot),
                                  interval=1000 / fps)

    fn = 'plot_surface_animation'
    if mp4:
        ani.save(path + fn + '.mp4', writer='ffmpeg', fps=fps)
    if gif:
        ani.save(path + fn + '.gif', writer='imagemagick', fps=fps)


def save_run(path, time_series, initial_surface: UtilitySurface, iterations,
             mutation_epsilon, mutation_radius, population_epsilon, assortitivity, \
                                               lower_bound=0,
             upper_bound=10,):

    now = time.localtime(time.time())
    run_id = str(now.tm_year) + "_"+str(now.tm_mon)+"_"+str(now.tm_mday)+"_"+str(now.tm_hour)+"_"+str(now.tm_min)+"_"+str(now.tm_sec)
    path = path + run_id +"\\"
    os.mkdir(path)

    f = open(path+"details.txt", "w+")
    f.write("Iterations: " + iterations + "\n")
    f.write("Mutation Epsilon: " + mutation_epsilon + "\n")
    f.write("Mutation Radius: " + mutation_radius + "\n")
    f.write("Population Structure: " + population_epsilon + "\n")
    f.write("Index of assortativity: " + assortitivity + "\n")

    X, Y = np.meshgrid(initial_surface.my_payoff, initial_surface.opponent_payoff, indexing='ij')
    initial_Z = initial_surface.utility_grid
    final_Z = time_series[-1]

    # Make a 3D plot
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.set_zlim3d(-1, upper_bound)
    ax1.plot_surface(X, Y, initial_Z, cmap='viridis', linewidth=0)
    ax1.set_title('Initial Surface')
    ax1.set_xlabel('My Payoff')
    ax1.set_ylabel("Opponent's Payoff")
    ax1.set_zlabel('My Utility')
    plt.savefig(path+'\\initial.png')
    plt.close(fig)

    fig = plt.figure()
    ax2 = fig.add_subplot(111, projection='3d')
    ax2.set_zlim3d(-1, upper_bound)
    ax2.plot_surface(X, Y, final_Z, cmap='viridis', linewidth=0)
    ax2.set_title('Evolved Surface')
    ax2.set_xlabel('My Payoff')
    ax2.set_ylabel("Opponent's Payoff")
    ax2.set_zlabel('My Utility')
    plt.savefig(path+'final.png')
    plt.close(fig)

    # seems to be that ~half of all mutations result in an invasion,
    # so we make a video that's ~60 seconds long
    fps = (iterations / 2) / 60

    create_animation(path,
                       X,
                       Y,
                       time_series,
                       upper_bound,
                       fps)


def time_series_to_csv(file_name: str, time_series_array: list):
    with open(file_name, 'a+') as f:
        for array in time_series_array:
            np.savetxt(f, array, delimiter=',')
            f.write("<break/>\n")


def append_matrix_to_csv(file_name: str, matrix):
    with open(file_name, 'a+') as f:
        np.savetxt(f, matrix, delimiter=',')
        f.write("<break/>\n")


def csv_to_time_series_array(file_name: str):
    out_arr = []
    with open(file_name, 'r') as f:
        curr_matrix = []
        for line in f:
            if (line == "<break/>\n") or (line == "<break/>"):
                 # reached the end of a matrix
                out_arr.append(np.array(curr_matrix))
                curr_matrix = []
            else:
                curr_matrix.append(np.array(line.strip().split(sep=','), dtype=float))
    return out_arr

def _readlines_reverse(filename):
    with open(filename) as qfile:
        qfile.seek(0, os.SEEK_END)
        position = qfile.tell()
        line = ''
        while position >= 0:
            qfile.seek(position)
            next_char = qfile.read(1)
            if next_char == "\n":
                yield line[::-1]
                line = ''
            else:
                line += next_char
            position -= 1
        yield line[::-1]

def average_surface(path:str):
    """
    Takes a parameter of a path to a directory containing csv files of time series
    arrays.
    Averages across the final matrix of each array and returns this average matrix.
    BEWARE matrices in csv time series array must be the same shape (i.e. arrays can be
    different lengths, but the matrices within the arrays need to be the same.
    :param path:
    :return: average_matrix
    """
    file_name_array = glob.glob(path + '/*.csv')

    matrix_array = []
    for file_name in file_name_array:
        curr_matrix = deque()
        breaks_seen = 0
        for line in _readlines_reverse(file_name):
            if line == '':
                # blank line is the last in file (first read)
                pass
            elif (line == '<break/>' or line == '<break/>\n'):
                if breaks_seen <1:
                    breaks_seen += 1
                else:
                    break
            else:
                curr_matrix.appendleft(np.array(line.strip().split(sep=','), dtype=float))
        matrix_array.append(np.array(curr_matrix))
    matrix_array = np.array(matrix_array)

    return np.average(matrix_array, axis=0)
