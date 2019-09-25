from algorithm.parameters import params
from fitness.evaluation import evaluate_fitness
from stats.stats import stats, get_stats
from utilities.stats import trackers
from operators.initialisation import initialisation
from operators.mutation import mutate

def search_loop(initial_resident):
    """
    This is a standard search process for an evolutionary algorithm. Loop over
    a given number of generations.
    
    :return: The final population after the evolutionary process has run for
    the specified number of generations.
    """

    resident = initial_resident
    # Traditional GE
    for generation in range(1, (params['GENERATIONS']+1)):

        resident = step(resident)

    return resident


def search_loop_from_state():
    """
    Run the evolutionary search process from a loaded state. Pick up where
    it left off previously.

    :return: The final population after the evolutionary process has run for
    the specified number of generations.
    """
    
    individuals = trackers.state_individuals
    

    # Traditional GE
    for generation in range(stats['gen'] + 1, (params['GENERATIONS'] + 1)):
        stats['gen'] = generation
        
        # New generation
        individuals = params['STEP'](individuals)
    

    return individuals


def step(resident):
    mutant = mutate(resident)

    resident.fitness, mutant.fitness = evaluate_fitness(resident, mutant)

    if mutant.fitness > resident.fitness:
        resident = mutant

    return resident
