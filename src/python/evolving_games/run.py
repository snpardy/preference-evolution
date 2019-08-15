from numpy import *


from paramless import paramless as p


if __name__ == "__main__":

    payoff_size = 10

    # setting up player's utility functions
    x = arange(0, payoff_size, .5, dtype=float)
    y = arange(0, payoff_size, .5, dtype=float)
    X, Y = meshgrid(x, y, indexing='ij')
    selfless = meshgrid(x, y, indexing='ij')[1]
    selfless = p.UtilitySurface(x, y, selfless)

    resident, time_series, invasion_count = p.evolve(selfless, p.tournament_fitness_function,
                                                     p.gaussian_mutation, 1500,
                                                     mutation_epsilon=.2, radius=4,
                                                     payoff_game=None,
                                                     time_series_data=True,
                                                     lower_bound=0,
                                                     upper_bound=10)
    print(invasion_count)

    p.save_run(".", time_series, selfless, 11)
