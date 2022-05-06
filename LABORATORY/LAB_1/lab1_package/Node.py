
class Node:

    # node_dictionary it's a dictionary that contains and define all these elements
    def __init__(self, node_dictionary):
        self._successive = {}
        self._connected_nodes = node_dictionary['connected_nodes']
        self._position = node_dictionary['position']
        self._label = node_dictionary['label']

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._postion = value

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @connected_nodes.setter
    def connected_nodes(self, newconnected_nodes):
        self._connected_nodes = newconnected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, newsuccessive):
        self._successive = newsuccessive


    """
    MANCA LA PARTE
    Define a propagate method that update a signal information object
    modifying its path attribute and call the successive element propagate
    method, accordingly to the specified path."""
    def propagate(self, signal_information):
        pass