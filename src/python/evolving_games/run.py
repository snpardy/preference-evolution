import json    # standard library
import sys
import random

import numpy as np   # 3rd party library


from paramless import paramless as p   # local source
from paramless import utils

if __name__ == "__main__":

    with open(sys.argv[1]) as read_file:

        params = json.loads(read_file.read())

    seed = params["seed"]
    iterations = params["iterations"]
    payoff_size = params["maxPayoff"]
    step = params["step"]
    initial_shape = params["initialShape"]
    population_epsilon = params["mutantShareOfPopulation"]
    assortativity = params["assortativity"]
    save_data_at_step = params["reportEveryTimeSteps"]
    output_file_name = params["outputFileName"]
    mutation_epsilon = params["mutationEpsilon"]
    radius = params["mutationRadius"]
    fitness_function_name = params["fitnessFunction"]

    # Setting seeds
    random.seed(seed)
    np.random.seed(seed)

    # Setting initzenial utility surface
    if initial_shape == "restart_run":
      path_to_csv = params["path_to_csv"]
      raise ValueError("Functionality incomplete")
    elif hasattr(p.UtilitySurface, initial_shape):
        initial = getattr(p.UtilitySurface, initial_shape)(payoff_size, step)
    else:
        raise ValueError("Please provide one of the built in initial shapes: selfish, \
                         selfless or random")

    if hasattr(p, fitness_function_name):
        fitness_function = getattr(p, fitness_function_name)
    else:
        raise ValueError("Fitness Function provided is not defined in paramless")

    _, time_series, _ = p.evolve(initial,
                                 fitness_function,
                                 p.gaussian_mutation_more_info, iterations, save_data_at_step,
                                 seed=seed, time_series_data=True, save_as_we_go=True,
                                 file_name=output_file_name,
                                 mutation_epsilon=mutation_epsilon, radius=radius,
                                 population_epsilon=population_epsilon,  # assortativity,
                                 payoff_game=None,
                                 lower_bound=0,
                                 upper_bound=5)

