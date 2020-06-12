from typing import Set


class Node:
    def __init__(self, identifier: any):
        self.identifier = identifier
        self.connected_nodes: Set[Node] = set()

    def __eq__(self, value):
        if not isinstance(value, Node):
            return False
        other_node: Node = value
        return self.identifier == other_node.identifier

    def __hash__(self):
        return self.identifier
