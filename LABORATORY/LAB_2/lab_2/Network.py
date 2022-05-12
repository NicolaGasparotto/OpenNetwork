import json
from itertools import permutations
from math import dist
import networkx as nx
import matplotlib.pyplot as plt

from LAB_2.lab_2.Line import Line
from LAB_2.lab_2.Node import Node
from LAB_1.lab1_package.Signal_information import Signal_information


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

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def draw(self):
        G = nx.Graph()
        G.add_nodes_from(list(self.nodes.keys()))
        G.add_edges_from(list(self.lines.keys()))
        pos = {}
        for node in self.nodes:
            pos[node] = self.nodes[node].position
        fig, ax = plt.subplots()
        nx.draw_networkx(G, pos=pos, ax=ax, edge_color='dodgerblue', node_color='darkseagreen', width=3.0)
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        plt.title('Network')
        plt.show()

    def connect(self):
        for node_name in self.nodes:
            for connected_node in self.nodes[node_name].connected_nodes:
                line_name = node_name + connected_node
                # i.e: Node 'A' (obj) -> (line AC)(obj): ->(obj)A.successive[AC] = (line AC)(obj)
                self.nodes[node_name].successive[line_name] = self.lines[line_name]
                self.lines[line_name].successive[connected_node] = self.nodes[connected_node]

    def find_path(self, start_node, end_node):
        visited = {}
        for node in self.nodes:
            visited[node] = False
        path_nodes = []
        list_path = []

        def find_path_r(node_s, node_d, visited_nodes, path):

            visited[node_s] = True
            path.append(node_s)

            if node_s == node_d:
                # print(path)
                list_path.append(list(path))
            else:
                for node_i in self.nodes[node_s].connected_nodes:
                    if not visited[node_i]:
                        find_path_r(node_i, node_d, visited_nodes, path)
            path.pop()
            visited_nodes[node_s] = False

        find_path_r(start_node, end_node, visited, path_nodes)
        list_path.sort(key=len)
        return list_path

    def propagate(self, signal_information):
        return self.nodes[signal_information.path[0]].propagate(signal_information)

    def print_nodes_info(self):
        for node_name in self._nodes:
            print(self._nodes[node_name])

    def print_lines_info(self):
        for line_name in self._lines:
            print(self._lines[line_name])

