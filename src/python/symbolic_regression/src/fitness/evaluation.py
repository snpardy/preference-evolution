import numpy as np

from algorithm.parameters import params
from fitness.game import Game


def _function_builder(string: str):
    def function(my_payoff, opponent_payoff):
        res = eval(string)
        return res

    return function


def evaluate_fitness(resident, mutant):
    if mutant.phenotype is None:
        # Mutant is invalid, resident wins.
        return 1, 0

    MAX_PAYOFF = params["MAX_PAYOFF"]
    if params["GAME_PAYOFFS"] == 'symmetric':
        sample_game = _symmetric_game
    elif params["GAME_PAYOFFS"] == 'non-symmetric':
        sample_game = _non_symmetric_game
    else:
        raise ValueError("Param 'GAME_PAYOFFS' must be either 'symmetric' or 'non-symmetric'.")

    if params["FITNESS_CALCULATION"] == 'average':
        fitness_calculation = _average_payoff
        exhaustive = False
    elif params["FITNESS_CALCULATION"] == 'exhaustive':
        fitness_calculation = _exhaustive_payoff
        exhaustive = True
    else:
        raise ValueError("Param 'FITNESS_CALCULATION' must be either 'average' or "
                         "'exhaustive'.")
    resident_fitness, mutant_fitness = 0, 0
    # Creating utility conversion functions from individual phenotypes
    resident_function = _function_builder(resident.phenotype)
    mutant_function = _function_builder(mutant.phenotype)

    for rounds in range(params["TOURNAMENT_ROUNDS"]):

        # Randomly sampling to create a game
        game = sample_game()

        # Transforming games based on individuals preferences
        r_r_utility_game = game.utility_transform(resident_function, resident_function)
        r_m_utility_game = game.utility_transform(resident_function, mutant_function)

        resident_fitness_one_round, mutant_fitness_one_round = fitness_calculation(r_r_utility_game,
                                                               r_m_utility_game,
                                                               game)
        if exhaustive:
            if mutant_fitness_one_round > 0:
                return 1, 0
        else:
            resident_fitness += resident_fitness_one_round
            mutant_fitness += mutant_fitness_one_round

    if exhaustive:
        return 0, 1
    else:
        return resident_fitness, mutant_fitness


def _exhaustive_payoff(r_r_utility_game: Game, r_m_utility_game: Game, payoff_game: Game):

    r_r_eqs = list(r_r_utility_game.support_enumeration())
    r_m_eqs = list(r_m_utility_game.support_enumeration())

    resident_payoffs = []
    mutant_payoffs = []
    for eq in r_r_eqs:
        resident_payoffs.append(payoff_game.expected_payoff(eq)[0])

    for eq in r_m_eqs:
        mutant_payoffs.append(payoff_game.expected_payoff(eq)[1])

    for r_payoff in resident_payoffs:
        for m_payoff in mutant_payoffs:
            if not m_payoff > r_payoff:
                return 1, 0

    return 0, 1


def _average_payoff(r_r_utility_game: Game, r_m_utility_game: Game, payoff_game: Game):
    resident_fitness, mutant_fitness = 0, 0

    r_r_eqs = list(r_r_utility_game.support_enumeration())

    for eq in r_r_eqs:
        resident_fitness += payoff_game.expected_payoff(eq)[0]
    resident_fitness = resident_fitness/len(r_r_eqs)

    r_m_eqs = list(r_m_utility_game.support_enumeration())

    for eq in r_m_eqs:
        mutant_fitness += payoff_game.expected_payoff(eq)[1]
    mutant_fitness = mutant_fitness/len(r_m_eqs)

    return resident_fitness, mutant_fitness


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