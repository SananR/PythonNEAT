import pythonneat.neat.utils.Parameters as Parameters
import pythonneat.neat.Population as Population
import pythonneat.neat.Speciation as Speciation
from pythonneat.neat.Gene import NodeGene
from pythonneat.neat.Gene import ConnectionGene
from pythonneat.neat.Gene import NodeType
import random


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
            if cg >= mv:
                mv = cg
        return mv

    def add_node_gene(self, node_type, height):
        """Adds and returns a new node gene with type node_type

        Inputs:
        node_type: The type of node. type: NodeType
        """
        node = NodeGene(len(self.node_genes) + 1, node_type, height)
        self.node_genes.append(node)
        return node

    def add_connection_gene(self, connection_gene):
        self.connection_genes[connection_gene.innovation] = connection_gene

    def create_connection_gene(self, in_id, out_id, weight, enabled):
        """Adds and returns a new connection gene

        Inputs:
        in_id
        out_id
        weight
        enabled
        """
        connection = ConnectionGene(in_id, out_id, weight, enabled, 0)
        connection.innovation = Speciation.get_innovation(connection)

        self.connection_genes[connection.innovation] = connection
        return connection

    def get_node_height(self, node_id):
        """Returns the height of the node associated with the id node_id

        Inputs:
        node_id: The id of the node. type: int
        """
        for n in self.node_genes:
            if n.id == node_id:
                return n.height
        return None

    def has_connection(self, in_id, out_id):
        for g in self.connection_genes.items():
            if g[1].in_id == in_id and g[1].out_id == out_id:
                return True
        return False

    def get_connection(self, in_id, out_id):
        for g in self.connection_genes.items():
            if g[1].in_id == in_id and g[1].out_id == out_id:
                return g[1]
        return None

    def has_node(self, id):
        for n in self.node_genes:
            if n.id == id:
                return True
        return False

    def get_node(self, id):
        for n in self.node_genes:
            if n.id == id:
                return n
        return None


def match_genes(i, j):
    """Returns a list of lists containing the excess, disjoint and,
    matching genes, respectively, between organisms i and j.

    Inputs:
    i: First organism. type: Genome
    j: Second organism. type: Genome
    """
    rtrn = []
    excess = []
    disjoint = []
    matching = []

    max_innov = max(i.innovation_range(), j.innovation_range())
    for k in range(1, max_innov + 1):
        if k > j.innovation_range() or k > i.innovation_range():
            excess.append(k)
        elif k not in j.connection_genes or k not in i.connection_genes:
            disjoint.append(k)
        else:
            matching.append(k)
    rtrn.append(excess)
    rtrn.append(disjoint)
    rtrn.append(matching)
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
    divide = 0
    for specie in Population.current_genomes:
        for genome in specie.genomes:
            divide += share_function(Speciation.compatibility_distance(i, genome))
    if divide == 0:
        divide = 1
    return original_fitness / divide


def cross_over(i, j):
    """Returns the offspring of organism i and j
    """
    matched_genes = match_genes(i, j)

    # Create offspring
    offspring = Genome()

    # Random matching genes
    for match in matched_genes[2]:
        r = random.random()
        enabled = True
        if not i.connection_genes[match].enabled or not j.connection_genes[match].enabled:
            d = random.random()
            if d <= Parameters.PARENT_GENE_DISABLE:
                enabled = False
        if r <= 0.5:
            offspring.add_connection_gene(i.connection_genes[match])
        else:
            offspring.add_connection_gene(j.connection_genes[match])
        offspring.connection_genes[match].enabled = enabled

    # Excess and Disjoint genes from more fit parent
    fit_parent = i
    if j.fitness > i.fitness:
        fit_parent = j

    for excess in matched_genes[0]:
        if excess in fit_parent.connection_genes:
            offspring.add_connection_gene(fit_parent.connection_genes[excess])
    for disjoint in matched_genes[1]:
        if disjoint in fit_parent.connection_genes:
            offspring.add_connection_gene(fit_parent.connection_genes[disjoint])

    for c in offspring.connection_genes.values():
        if i.has_node(c.in_id) and not offspring.has_node(c.in_id):
            offspring.node_genes.append(i.get_node(c.in_id))
        elif j.has_node(c.in_id) and not offspring.has_node(c.in_id):
            offspring.node_genes.append(j.get_node(c.in_id))
        if i.has_node(c.out_id) and not offspring.has_node(c.out_id):
            offspring.node_genes.append(i.get_node(c.out_id))
        elif j.has_node(c.out_id) and not offspring.has_node(c.out_id):
            offspring.node_genes.append(j.get_node(c.out_id))

    return offspring


def mutate_weights(i):
    """Randomly mutate the weights of genome i
    based off of mutate probabilities in Parameters

    Inputs:
    i: Genome to be mutated. type: Genome
    """
    for g in i.connection_genes.values():
        mp = random.random()
        if mp <= Parameters.WEIGHT_PERTURB_PROBABILITY:
            r = random.uniform(-Parameters.WEIGHT_PURTURB_RANGE, Parameters.WEIGHT_PURTURB_RANGE)
            g.weight += r
        else:
            g.weight = random.uniform(-1, 1)


def mutate_add_node(i):
    """Add a new random node to genome i
    """
    random_connection = i.connection_genes[random.choice(list(i.connection_genes.keys()))]
    if not random_connection.enabled:
        return
    random_connection.enabled = False

    in_height = i.get_node_height(random_connection.in_id)
    out_height = i.get_node_height(random_connection.out_id)
    n = i.add_node_gene(NodeType.HIDDEN_NODE, (in_height + out_height) / 2)

    i.create_connection_gene(random_connection.in_id, n.id, random.uniform(-1, 1), True)
    i.create_connection_gene(n.id, random_connection.out_id, random.uniform(-1, 1), True)


def mutate_add_connection(i):
    """Add a new random connection to genome i
    """
    start_neuron = random.choice(i.node_genes)
    end_neuron = random.choice(i.node_genes)
    while start_neuron.height == 1:
        start_neuron = random.choice(i.node_genes)
    while start_neuron.height >= end_neuron.height:
        end_neuron = random.choice(i.node_genes)

    if i.has_connection(start_neuron.id, end_neuron.id):
        return

    c = ConnectionGene(start_neuron.id, end_neuron.id, random.uniform(-1, 1), True, 0)
    c.innovation = Speciation.get_innovation(c)
    i.connection_genes[c.innovation] = c

