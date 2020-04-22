import numpy as np
from neatflapper.utils import Activations


class Layer:
    def __init__(self,  num_nodes_in, num_nodes, act_func=None):
        """Creates a layer with num_nodes nodes, connecting to a layer
        (possibly input) with num_nodes_in nodes, activation function act_func
        (by default sigmoid)

        Input:
        num_nodes_in: # of nodes in the previous layer. type: int
        num_nodes: # of nodes in the layer type: int
        act_func: activation function of the layer type: function (lambda)
        """
        if act_func is None:
            act_func = Activations.sigmoid

        self.size = num_nodes
        self.act_func = act_func
        self.weighted_sum = np.zeros(num_nodes)
        self.biases = np.zeros(num_nodes)
        self.output = np.zeros(num_nodes)
        self.weights = np.random.rand(num_nodes, num_nodes_in)

    def activate(self, inp):
        """Returns output of layer given input

        Input:
        inp: the input vector. type: ndarray

        Output:
        wighted_sum with act_func applied. type: ndarray
        """
        self.weighted_sum = self.weights.dot(inp) + self.biases
        self.output = self.act_func(self.weighted_sum)
        return self.output


class FeedForwardNetwork:
    def __init__(self, num_in, network_structure):
        """Creates a Neural Network that takes num_in inputs, has
        len(network_structure) layers (not including input), and where the nth
        layer, has network_structure[n] nodes

        Input:
        num_in: # of inputs the network takes. type: int
        network_structure: an array representing the # of nodes in each layer,
        includes output layer. type: int[# of layers]
        """
        self.num_layers = len(network_structure)
        self.num_in = num_in
        self.num_out = network_structure[self.num_layers - 1]
        self.layer_sizes = network_structure
        self.layers = []

        self.layers += [Layer(num_in, self.layer_sizes[0])]
        for i in range(1, self.num_layers):
            self.layers += [Layer(self.layer_sizes[i-1], self.layer_sizes[i])]

    def layer(self, num_in, num_nodes, act_func=None):
        if act_func is None:
            act_func = Activations.sigmoid
        self.layers += [Layer(num_in, num_nodes, act_func=act_func)]

    def forward_propagate(self, inp):
        """Propagates through the network, activating each layer and returning
        the activation of the last layer (output layer)
        """
        for i in range(self.num_layers):
            inp = self.layers[i].activate(inp)
        return inp
