import random
import nashpy as nash
import numpy as np


class Game(nash.Game):

    def shift_game(self, lower_bound, upper_bound):
        """
        Returns a new Game shifted randomly
        :param lower_bound:
        :param upper_bound:
        :return: None
        """
        
        new_payoffs = self.payoff_matrices

        # kinda gross
        # uses list comp to generate a list of mins/maxs of row and column payoffs
        # then selects min/max from that list
        new_min = np.min([np.min(item) for item in new_payoffs])
        new_max = np.max([np.max(item) for item in new_payoffs])

        payoff_shift = random.randint(0, upper_bound)

        while new_max+payoff_shift > upper_bound and new_min-payoff_shift < lower_bound:
            payoff_shift = random.randint(0, upper_bound)

        if new_max+payoff_shift < upper_bound:
            if new_min-payoff_shift > lower_bound:
                # can move either direction
                if random.randint(0,1):
                    for payoffs in new_payoffs:
                        payoffs += payoff_shift
                else:
                    for payoffs in new_payoffs:
                        payoffs -= payoff_shift
            else:
                # must move upwards
                for payoffs in new_payoffs:
                    payoffs += payoff_shift
        else:
            # must move downwards
            for payoffs in new_payoffs:
                payoffs -= payoff_shift

        return Game(*new_payoffs)
