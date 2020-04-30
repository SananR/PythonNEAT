import pythonneat.neat.utils.Parameters as Parameters
from pythonneat.neat.Genome import Genome
from pythonneat.neat.Gene import NodeType
import pythonneat.neat.Population as Population
import pythonneat.neat.Speciation as Speciation
from pythonneat.nn.NEATNetwork import NEATNetwork
from sortedcontainers import SortedDict
from pythonneat.neat.Species import Species
import  pythonneat.nn.NEATNetwork as neat
import pythonneat
import random
import math

sorted_pop = SortedDict({})


def initialize_population(genome_inputs, genome_outputs):
    for _ in range(Parameters.POPULATION_SIZE):
        genome = Genome()
        for i in range(genome_inputs):
            genome.add_node_gene(NodeType.INPUT_NODE, 0)
        for j in range(genome_outputs):
            genome.add_node_gene(NodeType.OUTPUT_NODE, 1)

        for one in genome.node_genes:
            for two in genome.node_genes:
                if one.height == 0 and two.height == 1:
                    genome.create_connection_gene(one.id, two.id, random.uniform(-1, 1), True)
        Population.add_genome(genome)


def start_evolution(network_inputs, network_outputs, fitness_function):
    # CREATE AND SPECIATE INITIAL POPULATION
    initialize_population(network_inputs, network_outputs)
    current_generation = 0

    while current_generation < Parameters.GENERATIONS:
        # EVALUATE POPULATION FITNESS
        print(" -------------- Evaluating Generation", current_generation, "... --------------")
        average_fitness = 0
        average_adjusted_fitness = 0
        networks = []
        for specie in Population.current_genomes:
            for g in specie.genomes:
                g_network = NEATNetwork()
                g_network.generate_network(g)
                networks.append(g_network)

        fitness = fitness_function(networks)

        i = 0
        for specie in Population.current_genomes:
            for g in specie.genomes:
                average_fitness += fitness[i]
                fitness[i] = pythonneat.neat.Genome.adjusted_fitness(g, fitness[i])
                g.fitness = fitness[i]
                average_adjusted_fitness += fitness[i]
                i += 1

        average_fitness /= len(Population.current_genomes)
        average_adjusted_fitness /= len(Population.current_genomes)
        print("Generation", current_generation, "Evaluated:")
        print("Population Size:", Population.population_size())
        print("Average Fitness:", average_fitness)
        print("Average Adjusted Fitness:", average_adjusted_fitness)
        print("Number of Species:", len(Population.current_genomes))
        print("Number of Unique Genes:", len(Speciation.genes))
        current_generation += 1

        print("Generating new population...")
        new_population = []

        # Add species champions
        for specie in Population.current_genomes:
            champ = specie.get_champion()
            new_population.append(champ)
            Population.remove_genome(champ)

        # TODO: SORT REMAINING POPULATION BY FITNESS AND REMOVE BOTTOM 50%
        sorted_pop.clear()
        for specie in Population.current_genomes:
            for g in specie.genomes:
                pythonneat.nn.NEATNetwork.dict_list_add(sorted_pop, g.fitness, g)

        temp = []
        for f in sorted_pop.values():
            for g in f:
                temp.append(g)

        for i in range(math.ceil(len(temp) / 2)):
            new_population.append(temp[i])

        # TODO: FILL POPULATION BY CROSS OVER
        for i in range(49):
            new_population.append(pythonneat.neat.Genome.cross_over(random.choice(new_population), random.choice(new_population)))

        print("New population generated.")
        print("-------------- End of Generation --------------")
        # MUTATE NEW POPULATION

        for g in new_population:
            mutate_node = random.random()
            if mutate_node <= Parameters.ADD_NODE_MUTATE_PROBABILITY:
                pythonneat.neat.Genome.mutate_add_node(g)
            mutate_connection = random.random()
            if mutate_connection <= Parameters.ADD_CONNECTION_MUTATE_PROBABILITY:
                pythonneat.neat.Genome.mutate_add_connection(g)
            mutate_weights = random.random()
            if mutate_weights <= Parameters.CONNECTION_MUTATE_PROBABILITY:
                pythonneat.neat.Genome.mutate_weights(g)

        # for i in range(25):
        #   new_population.append(pythonneat.neat.Genome.cross_over(random.choice(new_population), random.choice(new_population)))

        # CLEAR OLD POPULATION
        Population.current_genomes.clear()
        # Speciation.species.clear()

        # SPECIATE NEW POPULATION
        for g in new_population:
            Population.add_genome(g)


def print_genome(g):
    connections = []
    nodes = []

    for c in g.connection_genes:
        s = str(g.connection_genes[c].in_id) + " -> " + str(g.connection_genes[c].out_id)
        x = (c, s, g.connection_genes[c].enabled)
        connections.append(x)
    for n in g.node_genes:
        x = (n.id, n.height)
        nodes.append(x)

    print(connections)
    print(nodes)


def test_func():
    genome = Genome()
    genome2 = Genome()
    s = Species()
    s.add_genome(genome)
    s.add_genome(genome2)
    genome2.fitness = 500
    s.remove_all_but_champ()
    print(len(s.genomes))

    for i in range(6):
        genome.add_node_gene(NodeType.INPUT_NODE, 0)
        genome2.add_node_gene(NodeType.INPUT_NODE, 0)
    for j in range(1):
        genome.add_node_gene(NodeType.OUTPUT_NODE, 1)
        genome2.add_node_gene(NodeType.OUTPUT_NODE, 1)

    for one in genome.node_genes:
        for two in genome.node_genes:
            if one.height == 0 and two.height == 1:
                genome.create_connection_gene(one.id, two.id, random.uniform(-1, 1), True)
                genome2.create_connection_gene(one.id, two.id, random.uniform(-1, 1), True)

    pythonneat.neat.Genome.mutate_add_node(genome)

    genome2.fitness = -5

    print_genome(genome)
    print_genome(genome2)

    off1 = pythonneat.neat.Genome.cross_over(genome, genome2)
    print_genome(off1)

test_func()