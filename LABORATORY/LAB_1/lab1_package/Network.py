import json

from math import dist

from LAB_1.lab1_package.Line import Line
from LAB_1.lab1_package.Node import Node


class Network:

    def __init__(self, json_path):
        json_data = json.load(open(json_path, 'r'))
        self._nodes = {}
        self._lines = {}

        # lettura e creazione dict di nodi
        for node_name in json_data:
            node_i_dict = json_data[node_name]  # e' un dict contenente connectred_nodes: position:
            # aggiungo la voce label al dict
            node_i_dict['label'] = node_name
            node_i = Node(node_i_dict)  # creo l'oggetto node da inserire nel dict di node della classe: _nodes
            self._nodes[node_name] = node_i

        # lettura e creazione dict di line
        for node_name in self._nodes:
            for connected_node in self._nodes[node_name].connected_nodes:
                line_name = node_name + connected_node
                length = dist(self._nodes[node_name].position, self._nodes[connected_node].position)
                self._lines[line_name] = Line(line_name, length)

    def print_nodes(self):
        for node_name in self._nodes:
            print(self._nodes[node_name])

    def print_lines(self):
        for line_name in self._lines:
            print(self._lines[line_name])


if __name__ == "__main__":
    network1 = Network('../nodes.json')
    network1.print_nodes()
    network1.print_lines()

    """
    jsondata = json.load(open('./nodes.json', 'r'))
    print(type(jsondata))
    print(type(jsondata['A']['connected_nodes']))
    
    for node in jsondata:
        node_dict = jsondata[node]
        
        VOGLIO SALVARMI ANCHE IL NOME DEL NODO -> DIVENTA LABEL
        IL NOME DEL NODO E' IL KEY VALUE DEL NODO 
        
        node_dict['label'] = node
        # print(type(node_dict))
        print(node_dict.get('label'))

    # print(jsondata.keys())

    
    -> dict -> key: "A","B",...
                    ad ogni key: il value e' un altro dict()
                    -> key: connected_nodes: list
                            position: list
    """
