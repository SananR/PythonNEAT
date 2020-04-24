class Genome:

    def __init__(self):
        self.node_genes = []
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
