import pythonneat.neat.utils.Parameters as Parameters
import pythonneat.neat.Genome.Genome as Genome
import pythonneat.neat.Gene.NodeType as NodeType
import pythonneat.neat.Population as Population
import pythonneat.neat.Speciation as Speciation
import random


def initialize_population(genome_inputs, genome_outputs):
    for _ in range(Parameters.POPULATION_SIZE):
        genome = Genome()
        for i in range(genome_inputs):
            input_node = genome.add_node_gene(NodeType.INPUT_NODE)
            for j in range(genome_outputs):
                output_node = genome.add_node_gene(NodeType.OUTPUT_NODE)
                genome.add_connection_gene(input_node.id, output_node.id, random.uniform(-1, 1), True)
        Population.current_genomes.append(genome)
        Speciation.add_genome(genome)


def start_evolution(network_inputs, network_outputs, fitness_function):
    # CREATE AND SPECIATE INITIAL POPULATION
    initialize_population(network_inputs, network_outputs)
    current_generation = 0

    while current_generation < Parameters.GENERATIONS:
        # EVALUATE POPULATION FITNESS
        print("Evaluating Generation", current_generation, "...")
        average_fitness = 0
        average_adjusted_fitness = 0
        for g in Population.current_genomes:
            # TODO: MAP TO NEURAL NETWORK
            fitness = fitness_function(g)
            adjusted_fitness = Genome.adjusted_fitness(g, fitness)
            g.fitness = adjusted_fitness
            average_fitness += fitness
            average_adjusted_fitness += adjusted_fitness
        average_fitness /= len(Population.current_genomes)
        average_adjusted_fitness /= len(Population.current_genomes)
        print("Generation", current_generation, "Evaluated:")
        print("Average Fitness:", average_fitness)
        print("Average Adjusted Fitness:", average_adjusted_fitness)
        print("Number of Species:", len(Speciation.species))
        current_generation += 1

        print("Generating new population...")
        # TODO: MUTATE/CROSSOVER POPULATION TO GENERATE NEW POPULATION
        new_population = []
        for g in new_population:
            Speciation.add_genome(g)
        print("New population generated.")
