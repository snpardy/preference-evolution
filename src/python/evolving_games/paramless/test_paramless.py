import paramless as p
from paramless_games import *
import unittest
import numpy as np


class TestMethods(unittest.TestCase):

    def test_expected_payoff(self):
        pd = Games().prisoners_dilemma
        defect = ([0, 1], [0, 1])
        cooperate = ([1, 0], [1, 0])
        mixed = ([.5, .5], [.1, .9])
        self.assertEqual(expected_payoff(pd.payoff_matrices, defect), (1, 1))
        self.assertEqual(expected_payoff(pd.payoff_matrices, cooperate), (3, 3))
        self.assertAlmostEqual(expected_payoff(pd.payoff_matrices, mixed)[0], 0.85, 5)
        self.assertAlmostEqual(expected_payoff(pd.payoff_matrices, mixed)[1], 2.85, 5)

    def test_utility_transform(self):
        pd = Games().prisoners_dilemma
        y = np.arange(0, 6, dtype=float)
        x = np.arange(0, 6, dtype=float)
        X, Y = np.meshgrid(x, y, indexing='ij')
        Z = np.zeros_like(X)
        for i in range(len(Z)):
            for j in range(len(Z)):
                Z[i, j] = 0.5*i + 0.5 *j
        # this is a bit hacky - payoff matrices are tuples of numpy arrays so makes it a little difficult
        equal_payoff = Game(np.array([[3, 2.5], [2.5, 1]]), np.array([[3, 2.5], [2.5, 1]])).payoff_matrices
        po = utility_transform(pd, Z, Z).payoff_matrices
        for i, item in enumerate(po):
            self.assertEqual(item.tolist(), equal_payoff[i].tolist())


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
