from math import floor
from os import path, getcwd, listdir
from random import shuffle, randint

from representation import individual
from representation.derivation import generate_tree, pi_grow
from representation.tree import Tree


def generate_PI_ind_tree(max_depth, grammar, codon_size):
    """
    Generate an individual using a given Position Independent subtree
    initialisation method.

    :param max_depth: The maximum depth for the initialised subtree.
    :return: A fully built individual.
    """

    # Initialise an instance of the tree class
    ind_tree = Tree(str(grammar.start_rule["symbol"]), None)

    # Generate a tree
    genome, output, nodes, depth = pi_grow(ind_tree, max_depth)

    # Get remaining individual information
    phenotype, invalid, used_cod = "".join(output), False, len(genome)


    # Initialise individual
    ind = individual.Individual(genome, ind_tree, map_ind=False)

    # Set individual parameters
    ind.phenotype, ind.nodes = phenotype, nodes
    ind.depth, ind.used_codons, ind.invalid = depth, used_cod, invalid

    # Generate random tail for genome.
    ind.genome = genome + [randint(0, codon_size) for
                           _ in range(int(ind.used_codons / 2))]

    return ind
