import enum


class NodeType(enum.Enum):

    INPUT_NODE = 1
    HIDDEN_NODE = 2
    OUTPUT_NODE = 3


class NodeGene:

    def __init__(self, node_type):
        """
        Inputs:
        node_type: Type of the node. type: NodeType
        """
        self.id = 0
        self.node_type = node_type


class ConnectionGene:

    def __init__(self, in_id, out_id, weight, enabled, innovation):
        """
        Inputs:
        in_id: Id of in node. type: int
        out_id: Id of out node. type: int
        weight: Weight of connection. type: float
        enabled: Whether or not the connection is expressed. type: bool
        innovation: The innovation number of the connection. type: int
        """
        self.in_id = in_id
        self.out_id = out_id
        self.weight = weight
        self.enabled = enabled
        self.innovation = innovation


