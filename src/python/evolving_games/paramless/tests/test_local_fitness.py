from pytest import approx

import numpy as np

from nashpy import Game
from paramless.utilitySurface import UtilitySurface as us

from paramless import paramless as p



def test_local_fitness_average_payoff():
    np.random.seed(1)

    # PARAMS FOR FUNCTION
    resident = us.selfless(5, 0.5)
    mutant, mutation_info = p.gaussian_mutation_more_info(resident, .2, 3)
    population_epsilon = 0.5


    actual_fitness = p.exhaustive_local_average_tournament_fitness_function(resident, mutant, mutation_info,
                                                           population_epsilon,
                                                      rounds=1)

    payoff_array = np.array([3.56782016, 4.01994434, 1.03029842, 1.28499477])
    resident_payoffs = np.reshape(payoff_array, (-1, 2))
    mutant_payoffs = np.reshape(np.transpose(resident_payoffs), (-1, 2))

    game = Game(resident_payoffs, mutant_payoffs)
    resident_resident_utilty_game = p._utility_transform(game, resident, resident)
    resident_mutant_utility_game = p._utility_transform(game, resident, mutant)
    resident_payoff = 0
    mutant_payoff = 0

    r_r_eqs = list(resident_resident_utilty_game.support_enumeration())
    r_m_eqs = list(resident_mutant_utility_game.support_enumeration())

    for e in r_r_eqs:
        resident_payoff += (1 - population_epsilon) * p._expected_payoff(game, e)[0]
    for e in r_m_eqs:
        resident_payoff += population_epsilon * p._expected_payoff(game, e)[0]
        mutant_payoff += p._expected_payoff(game, e)[1]


    resident_actual, mutant_actual = actual_fitness

    print(resident_actual)
    print(mutant_actual)

    assert approx(resident_payoff, abs=1e-6) == resident_actual
    assert approx(mutant_payoff, abs=1e-6) == mutant_actual