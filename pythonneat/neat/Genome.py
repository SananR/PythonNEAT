import pythonneat.neat.utils.Parameters as Parameters
import pythonneat.neat.Population as Population
import pythonneat.neat.Speciation as Speciation
import pythonneat.neat.Gene.NodeGene as NodeGene
import pythonneat.neat.Gene.ConnectionGene as ConnectionGene


class Genome:

    def __init__(self):
        self.current_node_id = 1
        self.node_genes = []
        self.fitness = 0
        # Dictionary mapping innovation numbers to genes
        self.connection_genes = {}

    def innovation_range(self):
        """Returns the maximum innovation number of
        the genome
        """
        # O(G), G = # of genes
        mv = 0
        for cg in self.connection_genes:
            if cg.innovation >= max:
                mv = cg.innovation
        return mv

    def add_node_gene(self, node_type):
        """Adds and returns a new node gene with type node_type

        Inputs:
        node_type: The type of node. type: NodeType
        """
        node = NodeGene(node_type)
        self.node_genes.append(node)
        return node

    def add_connection_gene(self, in_id, out_id, weight, enabled):
        """Adds and returns a new connection gene

        Inputs:
        in_id
        out_id
        weight
        enabled
        """
        Speciation.current_innovation += 1
        connection = ConnectionGene(in_id, out_id, weight, enabled, Speciation.current_innovation)
        self.connection_genes[Speciation.current_innovation] = connection
        return connection


def match_genes(i, j):
    """Returns a tuple containing the number of excess and disjoint genes,
    and the average weight difference of matching genes, respectively,
    between organisms i and j.

    Inputs:
    i: First organism. type: Genome
    j: Second organism. type: Genome
    """
    # O(1) - Best case constant complexity
    # O(n) - Average case LINEAR complexity!
    wd = 0
    wdd = 0
    rtrn = [0, 0, 0.0]
    if i.innovation_range >= j.innovation_range:
        for k in range(1, i.innovation_range + 1):
            if k > j.innovation_range:
                rtrn[0] += 1
            elif k not in j.connection_nodes:
                rtrn[1] += 1
            else:
                wd += abs(i.connection_nodes[k].weight - j.connection_nodes[k].weight)
                wdd += 1
    else:
        for k in range(1, j.innovation_range + 1):
            if k > j.innovation_range:
                rtrn[0] += 1
            elif k not in j.connection_nodes:
                rtrn[1] += 1
            else:
                wd += abs(j.connection_nodes[k].weight - i.connection_nodes[k].weight)
                wdd += 1
    if wdd != 0:
        rtrn[2] = wd/wdd
    else:
        rtrn[2] = 0
    return rtrn


def share_function(delta):
    """Returns 0 when delta is above COMPATABILITY_THRESHOLD,
    returns 1 otherwise. When j is all organisms in the population
    this function represents number of organisms in that genome's
    species

    Inputs:
    delta: compatibility_distance(i, j). type: float
    """
    if delta > Parameters.COMPATABILITY_THRESHOLD:
        return 0
    else:
        return 1


def adjusted_fitness(i, original_fitness):
    """Returns the adjusted fitness of organism i, based on
    the current population

    Inputs:
    i: The organism corresponding to original_fitness. type: Genome
    original_fitness: The fitness of genome i. type: float
    """
    sum = 0
    for genome in Population.current_genomes:
        sum += share_function(Speciation.compatibility_distance(i, genome))
    # sum is assumed to non-zero because i is included in current_genomes
    return original_fitness / sum
