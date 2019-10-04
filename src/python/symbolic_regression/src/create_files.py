#!/usr/bin/python

import re
import numpy as np


# UTILS


def find_between(s, pre, post=''):
    result = re.search(pre + '(.*)' + post, s)
    return result.group(1)


def remplazar(diccionario, nombre_template):
    f = open(nombre_template)
    template = f.read()
    for key, value in diccionario.items():
        template = template.replace(str(key), str(value))
    return template


# SPECIFICS

TEMPLATE_NAME = 'template.json'

inital_shapes = ['random']
grammars = ["utility", "assortative_known"]
mutant_share = 0.001
mutation = ["m.int_flip_per_codon", "m.int_flip_per_ind", "m.subtree"]
assortativity = [0.2, 0.5]
maxPayoff = 5


def create_filenames():
    ans = []
    blueprint = 'SymReg_grammar_{}_mutation_{}_r_{}_seed_{}'

    for grammar in grammars:
        for m in mutation:
            for r in assortativity:
                for _ in range(10):
                    seed = np.random.randint(999999999)
                    ans.append(blueprint.format(
                        grammar, m, r, seed))
    return ans


# INFER VARIABLES


def from_file_name_create_dict(filename):
    # determine variables
    # update_rule + '_game_{}_inst_{}_pop_{}_rep_{}'
    grammar = str(find_between(filename, '_grammar_', '_mutation_'))
    mutation = str(find_between(filename, '_mutation_', '_r_'))
    r = float(find_between(filename, '_r_', '_seed_'))
    seed = int(find_between(filename, '_seed_'))

    print("Creating dict from file name \n")


    # now create dictionary
    a = dict()
    a["grammar"] = str(grammar)
    a["mutation_function"] = mutation
    a["__r__"] = r
    a["max_payoff"] = maxPayoff
    a["output_file"] = str(filename + '.txt')
    a["RANDOM_SEED"] = seed
    a["JSON_FILENAME"] = str(filename + '.json')
    return a


SUB_FILE_NAME = 'LIST'
TEMPLATE_LINE = 'python -W ignore symbolic_regression.py {}\n'


def create_sub(list_of_files):
    for filename in list_of_files:
        open(SUB_FILE_NAME, "a").write(
            TEMPLATE_LINE.format(filename + ".json"))


def main():
    list_of_files = create_filenames()
    for filename in list_of_files:
        diccionario = from_file_name_create_dict(filename)
        json_name = filename + '.json'
        json_file = open(json_name, 'w+')
        json_file.write(remplazar(diccionario, TEMPLATE_NAME))
        print('Created ' + json_name)
        json_file.close()
    create_sub(list_of_files)


if __name__ == '__main__':
    main()