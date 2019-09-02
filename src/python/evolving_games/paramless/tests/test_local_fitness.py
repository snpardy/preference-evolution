import numpy as np

from nashpy import Game
from paramless.utilitySurface import UtilitySurface as us

from paramless import paramless as p


def test_local_fitness():
    results =[]
    print("\n")
    print(("whole", "local"))
    for _ in range(20):
        initial = us.random(5, .5)
        mutant, mutation_info = p.gaussian_mutation_more_info(initial, .5, .5)
        norm_resident_f, norm_mutant_f = p.tournament_deterministic_fitness_function(initial,
                                                                                mutant,
                                                                           .2)
        local_resident_f, local_mutant_f = p.tournament_local_fitness_function(initial,
                                                                                     mutant,
                                                                                     .2, mutation_info)
        # TESTED BY LOOKING AT OUTPUT - NOT SURE HOW TO TEST FOR CORRECTNESS
        # print((norm_resident_f-norm_mutant_f, local_resident_f-local_mutant_f))
