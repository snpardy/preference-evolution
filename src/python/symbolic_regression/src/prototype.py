from representation.grammar import Grammar
from algorithm.parameters import params
from algorithm.search_loop import search_loop
from operators import initialisation as i
from operators.mutation import int_flip_per_codon

def main():
    """
    Run evolution.
    """
    path = "C:\\Users\\snpar\\Honours\\preference-evolution\\src\\python" \
           "\\symbolic_regression\\grammars\\utility.bnf"
    grammar = Grammar(path)
    params['BNF_GRAMMAR'] = grammar
    params['GENERATIONS'] = 50
    params['MUTATION'] = int_flip_per_codon
    params["MAX_PAYOFF"] = 5
    params["GAME_PAYOFFS"] = 'symmetric'
    params["FITNESS_CALCULATION"] = 'average'
    params["TOURNAMENT_ROUNDS"] = 100

    resident = i.generate_PI_ind_tree(5)
    print("Initial: " + resident.phenotype)
    resident = search_loop(resident)
    print("Evolved: " + resident.phenotype)

if __name__ == "__main__":
    main()