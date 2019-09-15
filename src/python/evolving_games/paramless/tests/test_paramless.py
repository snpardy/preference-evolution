import numpy as np
from nashpy import Game
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


from paramless import utilitySurface as us
from paramless import paramless as p





# A few different strategies
# in the form of ([row strategy], [column strategy])
defect = ([0, 1], [0, 1])
cooperate = ([1, 0], [1, 0])
mixed = ([.5, .5], [.1, .9])

# setting up player's utility functions
x = np.arange(0, 6, 1, dtype=float)
y = np.arange(0, 6, 1, dtype=float)
selfish = np.meshgrid(x, y, indexing='ij')[0]
selfless = np.meshgrid(x, y, indexing='ij')[1]

selfish = us.UtilitySurface(x, y, selfish, 1)
selfless = us.UtilitySurface(x, y, selfless, 1)


def test_expected_payoff():
    # A prisoners dilemma game
    prisoners_dilemma = Game([[3, 0], [5, 1]], [[3, 5], [0, 1]])
    # different strategies that may be played
    assert p._expected_payoff(prisoners_dilemma, defect) == (1, 1)
    assert p._expected_payoff(prisoners_dilemma, cooperate) == (3, 3)
    # mixed strategy results in an expected payoff that is accurate with acceptable
    # rounding error, in this case, 15 decimal places
    assert tuple(np.round(p._expected_payoff(prisoners_dilemma, mixed), 15)) == (0.85, 2.85)


def test_utility_transform():
    # A prisoners dilemma game
    prisoners_dilemma = Game([[3, 0], [5, 1]], [[3, 5], [0, 1]])
    # x is the row player payoff
    x = np.arange(0, 6, dtype=float)
    # y is the column player payoff
    y = np.arange(0, 6, dtype=float)
    X, Y = np.meshgrid(x, y, indexing='ij')

    # Z is a utility function - the indices of which represent each players payoff
    # so the entry at Z[i, j] is the utility gained when respective payoffs of i and j are achieved.
    Z = np.zeros_like(X)
    for i in range(len(Z)):
        for j in range(len(Z)):
            # i and j are equally weighted so an agent with this utility function
            # prefers to maximise overall payoff (her own or her opponent's)
            Z[i][j] = 0.5 * i + 0.5 * j

    Z = us.UtilitySurface(x, y, Z, 1)
    # Given the prisoners_dilemma created above, if both players have the utility function Z,
    # we would expect the transformed utility game to have the equal payoffs for both players at each entry
    equal_payoff = Game(np.array([[3, 2.5], [2.5, 1]]),
                        np.array([[3, 2.5], [2.5, 1]])).payoff_matrices
    transformed_payoff = p._utility_transform(prisoners_dilemma, Z, Z).payoff_matrices
    assert np.array(equal_payoff).all() == np.array(transformed_payoff).all()

    selfish_vs_selfless = Game(np.array([[3, 5], [0, 1]]),
                               np.array([[3, 5], [0, 1]])).payoff_matrices
    transformed_payoff = p._utility_transform(prisoners_dilemma, selfish,
                                              selfless).payoff_matrices
    assert np.array(selfish_vs_selfless).all() == np.array(transformed_payoff).all()


def test_real_number_payoffs():
    x = np.arange(0, 10, .3, dtype=float)
    y = np.arange(0, 10, .3, dtype=float)
    selfish = np.meshgrid(x, y, indexing='ij')[0]


def test_gaussian_mutation():
    my_payoff = np.arange(0, 10, 1)
    opponent_payoff = np.arange(0, 10, 1)

    X, Y = np.meshgrid(my_payoff, opponent_payoff, indexing='ij')

    resident = np.meshgrid(np.zeros(10), np.zeros(10), indexing='ij')[0]
    resident = us.UtilitySurface(my_payoff, opponent_payoff, resident, 1)
    mutant, mutation_info = p.gaussian_mutation_more_info(resident, .2, 3)
    np.set_printoptions(precision=3)
    print("\n")
    print(resident.utility_grid)
    print("\n ############ \n")
    print(mutation_info)
    print("\n ##########\n")
    np.set_printoptions(precision=3)
    for line in mutant.utility_grid:

        print(line)


    # Make a 3D plot
    fig = plt.figure()
    ax1 = fig.add_subplot(121, projection='3d')
    ax1.set_zlim3d(-1, 10 + 1)
    ax1.plot_surface(X, Y, resident.utility_grid, cmap='viridis', linewidth=0)
    ax1.set_title('Initial Surface')
    ax1.set_xlabel('My Payoff')
    ax1.set_ylabel("Opponent's Payoff")
    ax1.set_zlabel('My Utility')

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_zlim3d(-1, 10 + 1)
    ax2.plot_surface(X, Y, mutant.utility_grid, cmap='viridis', linewidth=0)
    ax2.set_title('Evolved Surface')
    ax2.set_xlabel('My Payoff')
    ax2.set_ylabel("Opponent's Payoff")
    ax2.set_zlabel('My Utility')
    plt.show()

