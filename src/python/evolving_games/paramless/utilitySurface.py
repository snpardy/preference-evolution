from dataclasses import dataclass
from dpcontracts import require
import math
import numpy as np


@dataclass
class UtilitySurface:
    """
    A data class to represent the utility function of an agent that consider their own and their opponent's payoff.
    Done so with two 1d np.ndarrays: my_payoff, opponent_payoff
    And one np.meshgrid utility_grid.
    """
    # A lot of the time the payoff arrays will just be equal to the indexes of the utility_grid
    # but this will not always be the case. This is why they're stored separately to the utility_grid.
    # We store the payoff arrays
    my_payoff: np.ndarray
    opponent_payoff: np.ndarray
    utility_grid: np.meshgrid

    @require("`my_payoff` must be the same shape as `opponent_payoff`",
             lambda args: args.self.my_payoff.shape == args.self.opponent_payoff.shape )
    @require("`utility_grid` must have the dimensions `len(my_payoff) by len(opponent_payoff)`",
             lambda args: len(args.self.my_payoff) == len(args.self.utility_grid)
             and len(args.self.opponent_payoff) == len(args.self.utility_grid[0]))
    def __post_init__(self, ):
        """
        @dataclass calls post_init at the end of init. It is being used to
        force arguments to meet the assumptions made in mutation methods.
        """
        pass

    def __getitem__(self, args):
        """
        Can access the utility_grid by index by applying square brackets directly to UtilitySurface object.
        :param args: must contain [my_payoff, opponent_payoff]
        :return: self.utility_grid[args[0], args[1]]
        """
        return self.utility_grid[args[0], args[1]]
