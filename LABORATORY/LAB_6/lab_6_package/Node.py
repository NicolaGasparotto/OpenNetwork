from LAB_6.lab_6_package.Signal_information import Signal_information
from LAB_6.lab_6_package.Line import *


class Node(object):

    # node_dictionary it's a dictionary that contains and define all these elements
    def __init__(self, node_dictionary):
        transceiver = node_dictionary.get('transceiver')
        self._transceiver = 'fixed-rate' if (transceiver is None) else transceiver  # default value is fixed-rate if not defined
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

    @property
    def transceiver(self):
        return self._transceiver

    @transceiver.setter
    def transceiver(self, new_transceiver):
        self._transceiver = new_transceiver

    def probe(self, signal_information_i):
        path = signal_information_i.path
        if len(path) > 1:
            line_name = path[0] + path[1]  # this return the string node_0 + node_1 -> ex: AB
            signal_information_i.update_path()
            signal_information_i = self.successive[line_name].probe(signal_information_i)
        return signal_information_i

    def __str__(self):
        return f"Node: {self.label}\nConnected Nodes: {self.connected_nodes}\nNode position: {self.position}\n" \
               f"Transceiver: {self.transceiver}\n"


if __name__ == '__main__':
    dict_n = {'label': 'A', 'connected_nodes': ['C', 'B'], 'position': 12.3}
    node = Node(dict_n)
    print(node)

