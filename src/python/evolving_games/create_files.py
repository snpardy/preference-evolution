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

inital_shapes = ['selfless', 'random']
mutant_shares = [.2, .5]
mutationSizes = [.1, .3]
mutationRadius = [4]
maxPayoff = 5
steps = [.1, .5]


def create_filenames():
    ans = []
    blueprint = 'Evolution_initial_{}_popShare_{}_mutationEp_{}_mutationR_{}_payoff_{' \
                '}_step_{}_seed_{}'

    for shape in inital_shapes:
        for epsilon in mutant_shares:
            for mutationEp in mutationSizes:
                for radius in mutationRadius:
                    for step in steps:
                        for _ in range(10):
                            seed = np.random.randint(999999999)
                            ans.append(blueprint.format(
                                shape, epsilon, mutationEp, radius, maxPayoff, step, seed))
    return ans


# INFER VARIABLES


def from_file_name_create_dict(filename):
    # determine variables
    # update_rule + '_game_{}_inst_{}_pop_{}_rep_{}'
    initial = str(find_between(filename, '_initial_', '_popShare_'))
    popShare = float(find_between(filename, '_popShare_', '_mutationEp_'))
    mutationEp = float(find_between(filename, '_mutationEp_', '_mutationR_'))
    mutationR = float(find_between(filename, '_mutationR_', '_payoff_'))
    maxPayoff = int(find_between(filename, '_payoff_', '_step_'))
    step = float(find_between(filename, '_step_', '_seed_'))
    seed = int(find_between(filename, '_seed_'))

    print("Creating dict from file name \n")


    # now create dictionary
    a = dict()
    a["INITIALSHAPE"] = str(initial)
    a["EPSILON"] = popShare
    a["MUTATIONSIZE"] = mutationEp
    a["MUTATIONRADIUS"] = mutationR
    a["MAXPAYOFF"] = maxPayoff
    a["STEP"] = step
    a["OUTPUTFILE"] = str(filename + '.csv')
    a["SEED"] = seed
    a["JSON_FILENAME"] = str(filename + '.json')
    return a


SUB_FILE_NAME = 'LIST'
TEMPLATE_LINE = 'python run.py {}\n'


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