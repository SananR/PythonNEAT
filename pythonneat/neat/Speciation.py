import pythonneat.neat.Genome as Genome

current_innovation = 0

# List of lists of genomes
species = [[]]


def add_genome(genome):
    return


def compatability_distance(i, j):
    """Returns the compatability distance between
    organism i and organism j

    Inputs:
    i - First organism. type: Genome
    j - Second organism. type: Genome
    """
    # As described in the paper published in 2002 by Stanley O. Brian
    # TODO: Make hyperparameters dynamic
    c1 = 1
    c2 = 1
    c3 = 0.4
    N = 1 # TODO: Calculate N
    genes = Genome.match_genes(i, j)
    E = genes[0]
    D = genes[1]
    W = genes[2]
    delta = (c1*E)/N + (c2*D)/N + c3*W
    return delta