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
   
    if "INITIAL" in params and params["INITIAL"] == "selfless":
            g = [49809, 79659, 6091, 80039, 45779, 29889, 42762, 70970, 65154, 78405, 63170, 16630, 40867, 53183, 95355]
            resident = Individual(g, None)    
    else:
        resident = i.generate_PI_ind_tree(10)

    time_series = search_loop(resident)

if __name__ == "__main__":



    path = "../grammars/"
    bnf = ".bnf"

    with open(sys.argv[1]) as read_file:

        given_params = json.loads(read_file.read())

    for k, v in given_params.items():
        params[k] = v

    params["MUTATION"] = eval(params["MUTATION"])
    path = path + params["GRAMMAR"] + bnf
    params["BNF_GRAMMAR"] = Grammar(path)

    np.random.seed(params["RANDOM_SEED"])
    random.seed(params["RANDOM_SEED"])

    main()