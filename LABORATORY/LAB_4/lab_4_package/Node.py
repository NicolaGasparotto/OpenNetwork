from LAB_4.lab_4_package.Signal_information import Signal_information
from LAB_4.lab_4_package.Line import *


class Node(object):

    # node_dictionary it's a dictionary that contains and define all these elements
    def __init__(self, node_dictionary):
        self._label = node_dictionary['label']
        self._connected_nodes = node_dictionary['connected_nodes']
        self._position = node_dictionary['position']
        self._successive = {}  # dict Line

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
        self._position = value

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @connected_nodes.setter
    def connected_nodes(self, new_connected_nodes):
        self._connected_nodes = new_connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def propagate(self, signal_information_i):
        path = signal_information_i.path
        if len(path) > 1:
            line_name = path[0] + path[1]  # this return the string node_0 + node_1 -> ex: AB
            signal_information_i.update_path()
            signal_information_i = self.successive[line_name].propagate(signal_information_i)
        return signal_information_i

    def __str__(self):
        return f"Node: {self.label}\nConnected Nodes: {self.connected_nodes}\nNode position: {self.position}\n"

