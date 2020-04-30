from pythonneat.neat.Species import Species
import pythonneat.neat.Speciation as Speciation
import pythonneat.neat.utils.Parameters as Parameters

current_genomes = []


def add_genome(genome):
    """Adds genome to the species list based on its
    compatability distance to already existing species

    Inputs:
    genome: The genome to add. type: Genome
    """
    for specie in current_genomes:
        first = specie.get_champion()
        if Speciation.compatibility_distance(genome, first) < Parameters.COMPATABILITY_THRESHOLD:
            specie.add_genome(genome)
            return
    s = Species()
    s.add_genome(genome)
    current_genomes.append(s)
    return


def remove_genome(genome):
    for specie in current_genomes:
        if genome in specie.genomes:
            specie.remove_genome(genome)


def cleanup_species():
    for specie in current_genomes:
        if specie.get_average_fitness() - specie.prev_fitness >= Parameters.SPECIES_STAGNATE_MIN_IMPROVEMENT:
            specie.consec_stagnate = 0
            specie.prev_fitness = specie.get_average_fitness()
        else:
            # Stagnate
            specie.consec_stagnate += 1
            if specie.consec_stagnate >= Parameters.SPECIES_STAGNATE_GEN_COUNT:
                specie.reproduce = False


def population_size():
    pop = 0
    for specie in current_genomes:
        for _ in specie.genomes:
            pop += 1
    return pop
