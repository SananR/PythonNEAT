import pythonneat.neat.Genome as Genome
import pythonneat.neat.utils.Parameters as Parameters

current_innovation = 0

# List of lists of genomes
species = [[]]


def add_genome(genome):
    """Adds genome to the species list based on its
    compatability distance to already existing species

    Inputs:
    genome: The genome to add. type: Genome
    """
    for i in range(len(species)):
        first = species[i][0]
        if compatibility_distance(genome, first) < Parameters.COMPATABILITY_THRESHOLD:
            species[i].append(genome)
    species.append([genome])
    return


def compatibility_distance(i, j):
    """Returns the compatibility distance between
    organism i and organism j

    Inputs:
    i - First organism. type: Genome
    j - Second organism. type: Genome
    """
    # As described in the paper published in 2002 by Stanley O. Brian
    N = max(len(i.connection_genes), len(j.connection_genes))
    if N < Parameters.DELTA_NORMALIZATION_THRESHOLD:
        N = 1

    genes = Genome.match_genes(i, j)
    E = genes[0]
    D = genes[1]
    W = genes[2]
    delta = (Parameters.EXCESS_IMPORTANCE*E)/N + (Parameters.DISJOINT_IMPORTANCE*D)/N + Parameters.WEIGHT_DIFFERENCE_IMPORTANCE*W
    return delta
