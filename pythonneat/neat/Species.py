class Species:

    def __init__(self):
        self.genomes = []
        self.prev_average_fitness = 0
        self.consec_stagnate = 0
        self.reproduce = True

    def add_genome(self, genome):
        self.genomes.append(genome)

    def remove_genome(self, genome):
        if genome in self.genomes:
            self.genomes.remove(genome)

    def get_average_fitness(self):
        average = 0
        for g in self.genomes:
            average += g.fitness
        return average / len(self.genomes)

    def get_champion(self):
        top = 0
        champ = self.genomes[0]
        for g in self.genomes:
            if g.fitness >= top:
                top = g.fitness
                champ = g
        return champ

    def remove_all_but_champ(self):
        champ = self.get_champion()
        to_remove = []
        for g in self.genomes:
            if g != champ:
                to_remove.append(g)
        for r in to_remove:
            self.remove_genome(r)