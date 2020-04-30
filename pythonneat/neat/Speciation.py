import pythonneat.neat.Genome as Genome
import pythonneat.neat.utils.Parameters as Parameters

genes = {}


def get_innovation(connection_gene):
    for g in genes.items():
        if g[1].in_id == connection_gene.in_id and g[1].out_id == connection_gene.out_id:
            return g[0]
    innov = len(genes) + 1
    genes[innov] = connection_gene
    return innov


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
    E = len(genes[0])
    D = len(genes[1])
    W = 0
    # Calculate weight difference
    for g in genes[2]:
        W += abs(i.connection_genes[g].weight - j.connection_genes[g].weight)
    W /= max(len(genes[2]), 1)

    delta = ((Parameters.EXCESS_IMPORTANCE*E)/N) + ((Parameters.DISJOINT_IMPORTANCE*D)/N) + (Parameters.WEIGHT_DIFFERENCE_IMPORTANCE*W)
    return delta
