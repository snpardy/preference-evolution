from nashpy import Game
from utilitySurface import UtilitySurface
import numpy as np
import paramless as p

# A prisoners dilemma game
prisoners_dilemma = Game([[3, 0], [5, 1]], [[3, 5], [0, 1]])
# A few different strategies
#  in the form of ([row strategy], [column strategy])
defect = ([0, 1], [0, 1])
cooperate = ([1, 0], [1, 0])
mixed = ([.5, .5], [.1, .9])

# setting up player's utility functions
x = np.arange(0, 6, 1, dtype=float)
y = np.arange(0, 6, 1, dtype=float)
selfless = np.meshgrid(x, y, indexing='ij')[0]
selfish = np.meshgrid(x, y, indexing='ij')[1]

selfish = UtilitySurface(x, y, selfish)
selfless = UtilitySurface(x, y, selfless)


def test_expected_payoff():
    # # A prisoners dilemma game
    # prisoners_dilemma = Game([[3, 5], [0, 1]], [[3, 0], [5, 1]])
    # different strategies that may be played
    assert p._expected_payoff(prisoners_dilemma, defect) == (1, 1)
    assert p._expected_payoff(prisoners_dilemma, cooperate) == (3, 3)
    # mixed strategy results in an expected payoff is accurate to 15 decimal places (in this case)
    assert tuple(np.round(p._expected_payoff(prisoners_dilemma, mixed), 15)) == (0.85, 2.85)


def test_utility_transform():
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
            Z[i, j] = 0.5*i + 0.5 *j
    # Given the prisoners_dilemma created above, if both players have the utility function Z,
    # we would expect the transformed utility game to have the equal payoffs for both players at each entry
    equal_payoff = Game(np.array([[3, 2.5], [2.5, 1]]), np.array([[3, 2.5], [2.5, 1]])).payoff_matrices
    transformed_payoff = p._utility_transform(prisoners_dilemma, Z, Z).payoff_matrices
    assert np.array(equal_payoff).all() == np.array(transformed_payoff).all()

    selfish_vs_selfless = Game(np.array([[3, 5], [0, 1]]), np.array([[3, 5], [0, 1]])).payoff_matrices
    transformed_payoff = p._utility_transform(prisoners_dilemma, selfish.utility_grid, selfless.utility_grid).payoff_matrices
    assert np.array(selfish_vs_selfless).all() == np.array(transformed_payoff).all()

    # assert(False and "this fails when the resulting game is not symmetric/identical for each player")


def test_payoff_fitness():
    # seflishness should be selected over selflessness
    fitness = p.payoff_fitness(selfish.utility_grid, selfless.utility_grid, payoff_game=prisoners_dilemma, atol=p.DEFAULT_ATOL)
    assert fitness[0] > fitness[1]
    # line 117 of paramless - swapped the indexing of the meshgrid
    # need to think more about whether this is correct
    assert False
