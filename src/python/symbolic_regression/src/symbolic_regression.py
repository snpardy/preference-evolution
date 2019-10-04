import sys
import json
import random

import numpy as np

from representation.grammar import Grammar
from representation.individual import Individual
from algorithm.parameters import params
from algorithm.search_loop import search_loop
from operators import initialisation as i
from operators import mutation as m
from algorithm.mapper import map_tree_from_genome
from utilities import plot as p
from utilities.algorithm.general import function_builder
import numpy as np


def main():
    """
    Run evolution.
    """

    # g = [49809, 98196, 37506, 96120, 58970, 23792, 44382, 78151, 2878, 66791, 15145, 10122, 80492, 3740, 78176, 57331, 31222, 61313, 41779]
    # selfless = Individual(g, None)


    resident = i.generate_PI_ind_tree(10)

    # resident = selfish

    print("Initial: " + resident.phenotype)
    time_series = search_loop(resident)
    print("Evolved: " + time_series[-1].phenotype)

if __name__ == "__main__":



    path = "../grammars/"
    bnf = ".bnf"

    with open(sys.argv[1]) as read_file:

        given_params = json.loads(read_file.read())

    for k, v in given_params.items():
        params[k] = v

    print("GENERATIONS: " + str(params["GENERATIONS"]))

    params["MUTATION"] = eval(params["MUTATION"])
    path = path + params["GRAMMAR"] + bnf
    params["BNF_GRAMMAR"] = Grammar(path)

    np.random.seed(params["RANDOM_SEED"])
    random.seed(params["RANDOM_SEED"])

    main()