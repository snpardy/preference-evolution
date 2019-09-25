import random
import nashpy as nash
import numpy as np


class Game(nash.Game):

    def __init__(self, *args):
        super().__init__(*args)

    def expected_payoff(self, equilibrium):
        """
        Given a game with payoff structure of :param payoff_matrices:
        and a strategy equilibrium of :param equilibrium:
        :param equilibrium: tuple of arrays of probability of playing each strategy.
        """
        row_strategy = equilibrium[0]
        column_strategy = equilibrium[1]
        row_payoff = 0
        column_payoff = 0
        for i, _ in enumerate(row_strategy):
            for j, _ in enumerate(column_strategy):
                row_payoff += row_strategy[i] * column_strategy[j] * self.payoff_matrices[0][i][j]
                column_payoff += row_strategy[i] * column_strategy[j] * self.payoff_matrices[1][i][
                    j]

        return row_payoff, column_payoff

    def utility_transform(self, row_utility, column_utility):
        """
        Returns a new Game with the pay-off altered by the given utility functions.
        Assumes that the utility 'functions' are grids that accept arguments in the form of utility_function[my_payoff, opponents_payoff]
        This could be bad?
        :param game: nashpy Game object
        :param row_utility: np mesh grid
        :param column_utility: np mesh grid
        :return: Game: nashpy Game object
        """
        row_payoff_matrix = self.payoff_matrices[0]
        column_payoff_matrix = self.payoff_matrices[1]
        # There should be a better way to do this but ?? :(
        # This section just sets up arrays of the correct shape
        row_player = [[None for _ in range(len(self.payoff_matrices[0][0]))]
                    for _ in range(len(self.payoff_matrices[0]))]
        column_player = [[None for _ in range(len(self.payoff_matrices[0][0]))]
                        for _ in range(len(self.payoff_matrices[0]))]

        for i, _ in enumerate(row_payoff_matrix):
            for j, _ in enumerate(row_payoff_matrix[i]):

                my_payoff = row_payoff_matrix[i][j]
                opponent_payoff = column_payoff_matrix[i][j]

                row_player[i][j] = row_utility(row_payoff_matrix[i][j], column_payoff_matrix[i][j])
                column_player[i][j] = column_utility(column_payoff_matrix[i][j], row_payoff_matrix[i][j])

        return Game(row_player, column_player)


    def _bayesian_nash_resident_vs_mutant(self, population_epsilon: float):
        rowRes = self.payoff_matrices[0]
        colRes = np.transpose(self.payoff_matrices[0])
        colMut = self.payoff_matrices[1]

        mutant_share = population_epsilon
        resident_share = 1 - population_epsilon

        combined_resident = [[] for _ in range(len(self.payoff_matrices[0]))]
        combined_mutant = [[] for _ in range(len(self.payoff_matrices[0]))]

        for rowIndex, row in enumerate(combined_resident):
            for i in (0, 1):
                for j in (0, 1):
                    row.append(resident_share * rowRes[rowIndex][j] + mutant_share * rowRes[
                        rowIndex][i])
                    combined_mutant[rowIndex].append(
                        resident_share * colRes[rowIndex][j] + mutant_share * colMut[rowIndex][i])

        bayesian_game = Game(combined_resident, combined_mutant)

        return bayesian_game.vertex_enumeration()

