from pythonneat.neat.Gene import NodeType
from sortedcontainers import SortedDict
import pythonneat.utils.Activations as Activations


class Neuron:

    def __init__(self, id, height):
        self.id = id
        self.value = 0
        self.in_connections = []
        self.height = height

    def activate(self):
        self.value = 0
        for c in self.in_connections:
            if not c.enabled:
                continue
            self.value += c.in_neuron.value * c.weight

        self.value = Activations.sigmoid(self.value)


class Connection:

    def __init__(self, in_neuron, out_neuron, weight, enabled):
        self.in_neuron = in_neuron
        self.out_neuron = out_neuron
        self.weight = weight
        self.enabled = enabled


class NEATNetwork:

    def __init__(self):
        # Height to neuron
        self.neurons = SortedDict({})
        self.inputs = {}
        self.outputs = {}

    def get_neuron(self, id):
        for l in self.neurons.items():
            for n in l[1]:
                if n.id == id:
                    return n
        return None

    def generate_network(self, genome):
        # Create Neurons
        for n in genome.node_genes:
            neuron = Neuron(n.id, n.height)
            if n.node_type == NodeType.INPUT_NODE:
                self.inputs[n.id] = neuron
                dict_list_add(self.neurons, 0, neuron)
            elif n.node_type == NodeType.HIDDEN_NODE:
                dict_list_add(self.neurons, neuron.height, neuron)
            else:
                self.outputs[n.id] = neuron
                dict_list_add(self.neurons, 1, neuron)

        # Create Synapses
        for con in genome.connection_genes.items():
            c = con[1]
            in_n = self.get_neuron(c.in_id)
            out_n = self.get_neuron(c.out_id)
            if in_n is not None and out_n is not None:
                con = Connection(in_n, out_n, c.weight, c.enabled)
                out_n.in_connections.append(con)

    def activate(self, inp):
        # Setup input neurons
        for i in range(len(self.neurons[0])):
            self.neurons[0][i].value = inp[i]

        for height in self.neurons:
            if height == 0:
                continue
            for n in self.neurons[height]:
                n.activate()


def dict_list_add(d, key, item):
    if key in d:
        d[key].append(item)
    else:
        d[key] = [item]

