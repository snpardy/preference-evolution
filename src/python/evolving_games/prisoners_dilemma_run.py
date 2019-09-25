import random

import numpy as np
from nashpy import Game

from paramless import paramless as p
from paramless import utils

if __name__ == "__main__":

    # Setting seeds
    random.seed(86987048)
    np.random.seed(86987048)


    initial = p.UtilitySurface.selfless(10, 0.5)
    game = Game([[3, 0],[5,1]], [[3,5],[0,1]])

    _, time_series, _ = p.evolve(initial,
                                 p.exhaustive_payoff_fitness,
                                 p.gaussian_mutation_more_info, 100, 1,
                                 seed=86987048, time_series_data=True,
                                 mutation_epsilon=.1, radius=2,
                                 population_epsilon=.4,  # assortativity,
                                 payoff_game=None,
                                 lower_bound=0,
                                 upper_bound=5)
    
    utils.time_series_to_csv("prisoners_run", time_series)