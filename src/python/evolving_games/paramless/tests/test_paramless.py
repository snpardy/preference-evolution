import numpy as np

from nashpy import Game
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


def test_exhaustive_payoff_fitness():
    """
    Tests the exhaustive_payoff_fitness function in paramless.
    By extension, the magic methods of fitness.Exhaustive are tested.
    """
    # selfishness should be selected over selflessness
    # given the payoffs of the prisoner's dilemma above,
    # the fitnesses should be selfish=5 and selfless=0

    # A prisoners dilemma game
    prisoners_dilemma = Game([[3, 0], [5, 1]], [[3, 5], [0, 1]])

    selfish_fitness, selfless_fitness = p.exhaustive_payoff_fitness(selfish, selfless,
                                                                    payoff_game=prisoners_dilemma)
    assert selfish_fitness[0] == 5
    assert selfless_fitness[0] == 0
    # comparison is done with a less than because that is how it is done in the
    # evolution_step function
    # negating the expression indicates no invasion
    assert not (selfish_fitness < selfless_fitness)

    # When both players are purely selfish, they both achieve a payoff of 1
    # when payoffs are equal, resident is considered to have greater fitness
    resident_fitness, mutant_fitness = p.exhaustive_payoff_fitness(selfish, selfish,
                                                                   payoff_game=prisoners_dilemma)
    assert resident_fitness[0] == 1
    assert mutant_fitness[0] == 1
    # comparison is done with a less than because that is how it is done
    # in the evolution_step function
    # negating the expression indicates no invasion
    assert not (resident_fitness < mutant_fitness)




