import numpy as np
from algorithm.parameters import params
from fitness.game import Game


def average(resident_function, mutant_function, sample_game, mutant_share, assortativity):

    resident_fitness, mutant_fitness = 0, 0

    for rounds in range(params["TOURNAMENT_ROUNDS"]):
        # Randomly sampling to create a game

        game = sample_game()

        # Transforming games based on individuals preferences
        r_r_utility_game = game.utility_transform(resident_function, resident_function)
        r_m_utility_game = game.utility_transform(resident_function, mutant_function)
        m_m_utility_game = game.utility_transform(mutant_function, mutant_function)

        r_r_eqs = list(r_r_utility_game.support_enumeration())
        r_m_eqs = list(r_m_utility_game.support_enumeration())
        m_m_eqs = list(m_m_utility_game.support_enumeration())

        # Calculates the fitness as specified in ALger & Weibull 2012,  pg. 44, equations 4,5

        curr_r_r_payoff = 0
        for eq in r_r_eqs:
            curr_r_r_payoff += game.expected_payoff(eq)[0]

        curr_r_r_payoff /= len(r_r_eqs)
        curr_r_r_payoff *= (assortativity+mutant_share*(1-assortativity))

        curr_r_m_payoff = 0
        curr_m_r_payoff = 0
        for eq in r_m_eqs:
            r, m = game.expected_payoff(eq)
            curr_r_m_payoff += r
            curr_m_r_payoff += m

        curr_r_m_payoff /= len(r_m_eqs)
        curr_r_m_payoff *= (mutant_share*(1-assortativity))

        curr_m_r_payoff /=len(r_m_eqs)
        curr_m_r_payoff *= ((1-mutant_share)*(1-assortativity))

        curr_m_m_payoff = 0
        for eq in m_m_eqs:
            curr_m_m_payoff += game.expected_payoff(eq)[1]

        curr_m_m_payoff /= len(m_m_eqs)
        curr_m_m_payoff *= (assortativity + mutant_share*(1-assortativity))

        resident_fitness += (curr_r_r_payoff + curr_r_m_payoff)
        mutant_fitness += (curr_m_m_payoff + curr_m_r_payoff)

    return resident_fitness, mutant_fitness


def exhaustive(resident_function, mutant_function, sample_game, mutant_share, assortativity):
    """
    ASSORTATIVITY NOT IMPLEMENTED!
    :param resident_function:
    :param mutant_function:
    :param sample_game:
    :param mutant_share:
    :param assortativity:
    :return:
    """

    for rounds in range(params["TOURNAMENT_ROUNDS"]):
        # Randomly sampling to create a game
        game = sample_game()
        # Transforming games based on individuals preferences
        r_r_utility_game = game.utility_transform(resident_function, resident_function)
        r_m_utility_game = game.utility_transform(resident_function, mutant_function)

        r_r_eqs = list(r_r_utility_game.support_enumeration())
        r_m_eqs = list(r_m_utility_game.support_enumeration())

        resident_payoffs = []
        mutant_payoffs = []
        for eq in r_r_eqs:
            resident_payoffs.append(game.expected_payoff(eq)[0])

        for eq in r_m_eqs:
            mutant_payoffs.append(game.expected_payoff(eq)[1])

        for r_payoff in resident_payoffs:
            for m_payoff in mutant_payoffs:
                if not m_payoff > r_payoff:
                    return 1, 0

    return 0 ,1