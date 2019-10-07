import numpy as np
from .game import Game
import random
from .utilitySurface import UtilitySurface


def nonsymmetric_tournament_fitness_function(resident: UtilitySurface,
                                                  mutant: UtilitySurface,
                                                  mutation_info: tuple,
                                                  population_epsilon: float,
                                                  assortativity: float=0,
                                                  rounds=1000,
                                                  max_payoff=5,
                                                  **kwargs):
    """
    :param resident: np.meshgrid utility function
    :param mutant: np.meshgrid utility function
    :param rounds: number of rounds the tournament goes for.
    :param max_payoff: max payoff that can be generated in a game.
    :return: a tuple of (resident payoff, mutant payoff)
    """

    resident_fitness, mutant_fitness = 0, 0
    for _ in range(rounds):
        # Generating game for the round
        row_payoffs = np.reshape((max_payoff * np.random.random(4)), (-1, 2))
        col_payoffs = np.reshape((max_payoff * np.random.random(4)), (-1, 2))
        game: Game = Game(row_payoffs, col_payoffs)

    #     # Converting to utility based game
    #     resident_mutant_utility_game = game.utility_transform(resident, mutant)
    #     resident_resident_utility_game = game.utility_transform(resident, resident)

    #     # Iterating through all equilibria
    #     resident_mutant_equilibria = list(resident_mutant_utility_game.support_enumeration())
    #     resident_resident_equilibria = list(resident_resident_utility_game.support_enumeration())
    #     resident_payoff = 0
    #     mutant_payoff = 0

    #     resident_v_resident_payoff = 0
    #     resident_v_mutant_payoff = 0

    #     resident_equilibria_faced = len(resident_resident_equilibria) + len(resident_mutant_equilibria)

    #     for r_r_eq in resident_resident_equilibria:
    #         resident_v_resident_payoff += (1 - population_epsilon) * (game.expected_payoff(r_r_eq)[0])

    #     for r_m_eq in resident_mutant_equilibria:
    #         resident_v_mutant_payoff += population_epsilon * (game.expected_payoff(r_m_eq)[0])
    #         mutant_payoff += game.expected_payoff(r_m_eq)[1]

        
    #     resident_payoff = (resident_v_resident_payoff + resident_v_mutant_payoff)/resident_equilibria_faced
    #     mutant_payoff = mutant_payoff/len(resident_mutant_equilibria)

    #     resident_fitness += resident_payoff
    #     mutant_fitness += mutant_payoff

    # return resident_fitness, mutant_fitness
    # Converting to utility based game
        resident_mutant_utility_game = game.utility_transform(resident, mutant)
        resident_resident_utility_game = game.utility_transform(resident, resident)

        # Iterating through all equilibria
        resident_mutant_equilibria = list(resident_mutant_utility_game.support_enumeration())
        resident_resident_equilibria = list(resident_resident_utility_game.support_enumeration())
        resident_payoff = 0
        mutant_payoff = 0

        resident_v_resident_payoff = 0
        resident_v_mutant_payoff = 0

        resident_equilibria_faced = len(resident_resident_equilibria) + len(resident_mutant_equilibria)

        for r_r_eq in resident_resident_equilibria:
            resident_v_resident_payoff += (1 - population_epsilon) * (game.expected_payoff(r_r_eq)[0])

        for r_m_eq in resident_mutant_equilibria:
            resident_v_mutant_payoff += population_epsilon * (game.expected_payoff(r_m_eq)[0])
            mutant_payoff += game.expected_payoff(r_m_eq)[1]

        
        resident_payoff = (resident_v_resident_payoff + resident_v_mutant_payoff)/resident_equilibria_faced
        mutant_payoff = mutant_payoff/len(resident_mutant_equilibria)

        resident_fitness += resident_payoff
        mutant_fitness += mutant_payoff

    return resident_fitness, mutant_fitness


def localised_tournament_fitness_function(resident: UtilitySurface,
                                                  mutant: UtilitySurface,
                                                  mutation_info: tuple,
                                                  population_epsilon: float,
                                                  assortativity: float=0,
                                                  rounds=100,
                                                  max_payoff=5,
                                                  **kwargs):

    """
    :param resident: np.meshgrid utility function
    :param mutant: np.meshgrid utility function
    :param rounds: number of rounds the tournament goes for.
    :param max_payoff: max payoff that can be generated in a game.
    :return: a tuple of (resident payoff, mutant payoff)
    """

    variance = mutation_info[0]
    resident_mean = mutation_info[1]
    mutant_mean = mutation_info[2]

    locality = variance*1.5

    resident_min = resident_mean-locality
    resident_max = resident_mean+locality
    mutant_min = mutant_mean-locality
    mutant_max = mutant_mean+locality

    if resident_min < 0:
        resident_min = 0
    if mutant_min < 0:
        mutant_min = 0
    if resident_max > max_payoff:
        resident_max = max_payoff
    if mutant_max > max_payoff:
        mutant_max = max_payoff

    resident_fitness, mutant_fitness = 0, 0
    for _ in range(rounds):
        # Generating game for the round
        payoff_array = np.zeros(4)
        # A
        payoff_array[0] = np.random.random(1) * 5
        # D
        payoff_array[3] = np.random.random(1) * 5
        # B
        payoff_array[1] = resident_min + np.random.random(1) * (resident_max - resident_min)
        # C
        payoff_array[2] = mutant_min + np.random.random(1) * (mutant_max - mutant_min)

        resident_payoffs = np.reshape(payoff_array, (-1, 2))
        mutant_payoffs = np.reshape(np.transpose(resident_payoffs), (-1, 2))

        game: Game = Game(resident_payoffs, mutant_payoffs)

        # Converting to utility based game
        resident_mutant_utility_game = game.utility_transform(resident, mutant)
        resident_resident_utility_game = game.utility_transform(resident, resident)

        # Selecting equilibria
        resident_mutant_equilibria = random.choice(list(
            resident_mutant_utility_game.support_enumeration()))
        resident_resident_equilibria = random.choice(list(
            resident_resident_utility_game.support_enumeration()))

        resident_payoff = (1-population_epsilon) * (
                               game.expected_payoff(resident_resident_equilibria)[0])\
                          + population_epsilon*game.expected_payoff(resident_mutant_equilibria)[0]

        mutant_payoff = game.expected_payoff(resident_mutant_equilibria)[1]

        resident_fitness += resident_payoff
        mutant_fitness += mutant_payoff
    #     do we need to divide by something here to get average?
    return resident_fitness, mutant_fitness


def exhaustive_localised_tournament_stringent_fitness_function(resident: UtilitySurface,
                                                  mutant: UtilitySurface,
                                                  mutation_info: tuple,
                                                  population_epsilon: float,
                                                  assortativity: float=0,
                                                  rounds=100,
                                                  max_payoff=5,
                                                  **kwargs):

    """
    :param resident: np.meshgrid utility function
    :param mutant: np.meshgrid utility function
    :param rounds: number of rounds the tournament goes for.
    :param max_payoff: max payoff that can be generated in a game.
    :return: a tuple of (resident payoff, mutant payoff)
    """


    variance = mutation_info[0]
    resident_mean = mutation_info[1]
    mutant_mean = mutation_info[2]

    locality = variance

    resident_min = resident_mean-locality
    resident_max = resident_mean+locality
    mutant_min = mutant_mean-locality
    mutant_max = mutant_mean+locality

    if resident_min < 0:
        resident_min = 0
    if mutant_min < 0:
        mutant_min = 0
    if resident_max > max_payoff:
        resident_max = max_payoff
    if mutant_max > max_payoff:
        mutant_max = max_payoff

    resident_fitness, mutant_fitness = 0, 0
    for _ in range(rounds):
        # Generating game for the round
        payoff_array = np.zeros(4)
        # A
        payoff_array[0] = np.random.random(1) * 5
        # D
        payoff_array[3] = np.random.random(1) * 5
        # B
        payoff_array[1] = resident_min + np.random.random(1) * (resident_max - resident_min)
        # C
        payoff_array[2] = mutant_min + np.random.random(1) * (mutant_max - mutant_min)

        resident_payoffs = np.reshape(payoff_array, (-1, 2))
        mutant_payoffs = np.reshape(np.transpose(resident_payoffs), (-1, 2))

        game: Game = Game(resident_payoffs, mutant_payoffs)

        # Converting to utility based game
        resident_mutant_utility_game = game.utility_transform(resident, mutant)
        resident_resident_utility_game = game.utility_transform(resident, resident)

        # Iterating through all equilibria
        resident_mutant_equilibria = list(resident_mutant_utility_game.support_enumeration())
        resident_resident_equilibria = list(resident_resident_utility_game.support_enumeration())
        resident_payoff = 0
        mutant_payoff = 0

        resident_v_resident_payoff = []

        # Calculate all payoffs that the resident achieved playing against itself
        for r_r_eq in resident_resident_equilibria:
            resident_v_resident_payoff.append(game.expected_payoff(r_r_eq)[0])

        for r_m_eq in resident_mutant_equilibria:
            curr_mutant_payoff = game.expected_payoff(r_m_eq)[1]
            for resident_payoff in resident_v_resident_payoff:
                # All mutant payoffs must be greater than all resident payoffs
                if not curr_mutant_payoff > resident_payoff:
                    # No invasion
                    return 1, 0
    # If we've made it to here, then the mutant invades
    return 0, 1


def exhaustive_local_average_tournament_fitness_function(resident: UtilitySurface,
                                      mutant: UtilitySurface,
                                      mutation_info: tuple,
                                      population_epsilon: float,
                                      assortativity: float=0,
                                      rounds=100,
                                      max_payoff=5,
                                              **kwargs):

    """
    :param resident: np.meshgrid utility function
    :param mutant: np.meshgrid utility function
    :param rounds: number of rounds the tournament goes for.
    :param max_payoff: max payoff that can be generated in a game.
    :return: a tuple of (resident payoff, mutant payoff)
    """

    variance = mutation_info[0]
    resident_mean = mutation_info[1]
    mutant_mean = mutation_info[2]

    locality = variance

    resident_min = resident_mean-locality
    resident_max = resident_mean+locality
    mutant_min = mutant_mean-locality
    mutant_max = mutant_mean+locality

    if resident_min < 0:
        resident_min = 0
    if mutant_min < 0:
        mutant_min = 0
    if resident_max > max_payoff:
        resident_max = max_payoff
    if mutant_max > max_payoff:
        mutant_max = max_payoff

    resident_fitness, mutant_fitness = 0, 0
    for _ in range(rounds):
        # Generating game for the round
        payoff_array = np.zeros(4)
        # A
        payoff_array[0] = np.random.random(1) * 5
        # D
        payoff_array[3] = np.random.random(1) * 5
        # B
        payoff_array[1] = resident_min + np.random.random(1) * (resident_max - resident_min)
        # C
        payoff_array[2] = mutant_min + np.random.random(1) * (mutant_max - mutant_min)

        resident_payoffs = np.reshape(payoff_array, (-1, 2))
        mutant_payoffs = np.reshape(np.transpose(resident_payoffs), (-1, 2))

        game: Game = Game(resident_payoffs, mutant_payoffs)

        # Converting to utility based game
        resident_mutant_utility_game = game.utility_transform(resident, mutant)
        resident_resident_utility_game = game.utility_transform(resident, resident)

        # Iterating through all equilibria
        resident_mutant_equilibria = list(resident_mutant_utility_game.support_enumeration())
        resident_resident_equilibria = list(resident_resident_utility_game.support_enumeration())
        resident_payoff = 0
        mutant_payoff = 0

        resident_v_resident_payoff = 0
        resident_v_mutant_payoff = 0

        resident_equilibria_faced = len(resident_resident_equilibria) + len(resident_mutant_equilibria)

        for r_r_eq in resident_resident_equilibria:
            resident_v_resident_payoff += (1 - population_epsilon) * (game.expected_payoff(r_r_eq)[0])

        for r_m_eq in resident_mutant_equilibria:
            resident_v_mutant_payoff += population_epsilon * (game.expected_payoff(r_m_eq)[0])
            mutant_payoff += game.expected_payoff(r_m_eq)[1]

        
        resident_payoff = (resident_v_resident_payoff + resident_v_mutant_payoff)/resident_equilibria_faced
        mutant_payoff = mutant_payoff/len(resident_mutant_equilibria)

        resident_fitness += resident_payoff
        mutant_fitness += mutant_payoff

    return resident_fitness, mutant_fitness


def symmetric_average(resident: UtilitySurface,
                                                  mutant: UtilitySurface,
                                                  mutation_info: tuple,
                                                  population_epsilon: float,
                                                  assortativity: float,
                                                  rounds=3000,
                                                  max_payoff=5,
                                                  **kwargs):
    mutant_share = population_epsilon
    variance = mutation_info[0]
    resident_mean = mutation_info[1]
    mutant_mean = mutation_info[2]

    locality = variance*1.5

    resident_min = resident_mean-locality
    resident_max = resident_mean+locality
    mutant_min = mutant_mean-locality
    mutant_max = mutant_mean+locality

    if resident_min < 0:
        resident_min = 0
    if mutant_min < 0:
        mutant_min = 0
    if resident_max > max_payoff:
        resident_max = max_payoff
    if mutant_max > max_payoff:
        mutant_max = max_payoff

    resident_fitness, mutant_fitness = 0, 0
    for _ in range(rounds):
        # Generating game for the round
        payoff_array = np.zeros(4)
        # A
        payoff_array[0] = np.random.random(1) * 5
        # D
        payoff_array[3] = np.random.random(1) * 5
        # B
        payoff_array[1] = resident_min + np.random.random(1) * (resident_max - resident_min)
        # C
        payoff_array[2] = mutant_min + np.random.random(1) * (mutant_max - mutant_min)

        resident_payoffs = np.reshape(payoff_array, (-1, 2))
        mutant_payoffs = np.reshape(np.transpose(resident_payoffs), (-1, 2))

        game: Game = Game(resident_payoffs, mutant_payoffs)

        # Converting to utility based game
        r_r_utility_game = game.utility_transform(resident, resident)
        r_m_utility_game = game.utility_transform(resident, mutant)
        m_m_utility_game = game.utility_transform(mutant, mutant)

        # List of equilibrias
        r_r_eqs = list(r_r_utility_game.support_enumeration())
        r_m_eqs = list(r_m_utility_game.support_enumeration())
        m_m_eqs = list(m_m_utility_game.support_enumeration())

        # Calculates the fitness as specified in ALger & Weibull 2012,  pg. 44, equations 4,5
        curr_r_r_payoff = 0
        for eq in r_r_eqs:
            curr_r_r_payoff += game.expected_payoff(eq)[0]

        curr_r_r_payoff /= len(r_r_eqs)
        curr_r_r_payoff *= (assortativity + (1-mutant_share)*(1-assortativity))

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
        curr_m_m_payoff *= (assortativity + (mutant_share)*(1-assortativity))

        resident_fitness += (curr_r_r_payoff + curr_r_m_payoff)
        mutant_fitness += (curr_m_m_payoff + curr_m_r_payoff)

    return resident_fitness, mutant_fitness