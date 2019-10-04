

def save_phenotype_as_we_go(ind, file_name):
    with open(file_name, 'a+') as f:
        f.write(ind.phenotype)
        f.write("\n")