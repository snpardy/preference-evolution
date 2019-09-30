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
    # g = [11]
    # g = [49809, 98196, 37506, 96120, 58970, 23792, 44382, 78151, 2878, 66791, 15145, 10122, 80492, 3740, 78176, 57331, 31222, 61313, 41779]
    # selfish = Individual(g, None)

    resident = i.generate_PI_ind_tree(5)

    # resident = selfish

    print("Initial: " + resident.phenotype)
    initial_function = function_builder(resident.phenotype)
    time_series = search_loop(resident)
    print("Evolved: " + time_series[-1].phenotype)
    evolved_function = function_builder(time_series[-1].phenotype)

if __name__ == "__main__":

    path = "C:\\Users\\snpar\\Honours\\preference-evolution\\src\\python" \
           "\\symbolic_regression\\grammars\\utility.bnf"
    grammar = Grammar(path)
    params['BNF_GRAMMAR'] = grammar
    params['GRAMMAR'] = "utility"
    params['GENERATIONS'] = 1000
    params['MUTATION'] = m.int_flip_per_codon
    params["MAX_PAYOFF"] = 5
    params["GAME_PAYOFFS"] = 'symmetric'
    params["FITNESS_FUNCTION"] = 'average'
    params["MUTANT_SHARE"] = 0.1
    params["ASSORTATIVITY"] = 0
    params["TOURNAMENT_ROUNDS"] = 100


    main()