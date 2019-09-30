import numpy as np

from algorithm.parameters import params
from fitness import functions as f
from fitness.game import Game
from utilities.algorithm.general import function_builder




def evaluate_fitness(resident, mutant):
    if mutant.phenotype is None:
        # Mutant is invalid, resident wins.
        return 1, 0


    # What kind of games do we sample?
    if params["GAME_PAYOFFS"] == 'symmetric':
        sample_game = _symmetric_game
    elif params["GAME_PAYOFFS"] == 'non-symmetric':
        sample_game = _non_symmetric_game
    else:
        raise ValueError("Param 'GAME_PAYOFFS' must be either 'symmetric' or 'non-symmetric'.")

    # How are we comparing the payoffs of our players?
    if hasattr(f, params["FITNESS_FUNCTION"]):
        fitness_function = getattr(f, params["FITNESS_FUNCTION"])
    else:
        raise ValueError("Param 'FITNESS_CALCULATION' must be either 'average' or "
                         "'exhaustive'.")

    # What is our population structure?
    if "MUTANT_SHARE" in params:
        mutant_share = params["MUTANT_SHARE"]
    else:
        mutant_share = 0

    if "ASSORTATIVITY" in params:
        assortativity = params["ASSORTATIVITY"]
    else:
        assortativity = 1

    # Creating utility functions from individual phenotypes
    resident_function = function_builder(resident.phenotype)
    mutant_function = function_builder(mutant.phenotype)

    return fitness_function(resident_function, mutant_function, sample_game, mutant_share, assortativity)




def _non_symmetric_game():
    MAX_PAYOFF = params["MAX_PAYOFF"]
    row_payoffs = np.reshape((MAX_PAYOFF * np.random.random(4)), (-1, 2))
    col_payoffs = np.reshape((MAX_PAYOFF * np.random.random(4)), (-1, 2))

    return Game(row_payoffs, col_payoffs)


def _symmetric_game():
    MAX_PAYOFF = params["MAX_PAYOFF"]
    row_payoffs = np.reshape((MAX_PAYOFF * np.random.random(4)), (-1, 2))
    col_payoffs = np.reshape(np.transpose(row_payoffs), (-1, 2))

    return Game(row_payoffs, col_payoffs)