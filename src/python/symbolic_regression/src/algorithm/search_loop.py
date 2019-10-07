from algorithm.parameters import params
from fitness.evaluation import evaluate_fitness
from operators.initialisation import initialisation
from operators.mutation import mutate
from utilities.io import save


atol = params['TOLERANCE']


def search_loop(initial_resident):
    """
    This is a standard search process for an evolutionary algorithm. Loop over
    a given number of generations.
    
    :return: The final population after the evolutionary process has run for
    the specified number of generations.
    """

    resident = initial_resident
    time_series = [resident]
    file_name = params["OUTPUTFILE"]

    save_at_step = params["SAVESTEP"]

    save.save_phenotype_as_we_go(resident, file_name)

    # Traditional GE
    for generation in range(1, (params['GENERATIONS']+1)):

        resident, invasion = step(resident)
        if invasion:
            time_series.append(resident)
            if len(time_series)%save_at_step == 0:
                save.save_phenotype_as_we_go(resident, file_name)

    save.save_phenotype_as_we_go(time_series[-1], file_name)

    return time_series

def step(resident):
    mutant = mutate(resident)

    resident.fitness, mutant.fitness = evaluate_fitness(resident, mutant)

    if mutant.fitness > resident.fitness and abs(mutant.fitness - resident.fitness) > atol:
        return mutant, True

    return resident, False
