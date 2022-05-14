import json
from itertools import permutations
import math
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from LAB_2.lab_2.Line import Line
from LAB_2.lab_2.Node import Node
from LAB_2.lab_2.Connection import Connection
from LAB_1.lab1_package.Signal_information import Signal_information


class Network:

    def __init__(self, json_path):
        json_data = json.load(open(json_path, 'r'))
        self._nodes = {}
        self._lines = {}
        # the dataframe it's set when you call the function connect()
        # otherwise you can not create a dataframe or a network if you don't connect the nodes
        self._weighted_paths = None
        # for default the signal power propagating along the network it's set to be
        # 0.001 Watts
        self._signal_power = 0.001
        for node_name in json_data:
            node_i_dict = json_data[node_name]
            node_i_dict['label'] = node_name
            node_i = Node(node_i_dict)
            self._nodes[node_name] = node_i
        for node_name in self._nodes:
            for connected_node in self._nodes[node_name].connected_nodes:
                line_name = node_name + connected_node
                length = math.dist(self._nodes[node_name].position, self._nodes[connected_node].position)
                self._lines[line_name] = Line(line_name, length)

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    @property
    def weighted_paths(self):
        return self._weighted_paths

    @weighted_paths.setter
    def weighted_paths(self, value):
        self._weighted_paths = value

    @property
    def signal_power(self):
        return self._signal_power

    @signal_power.setter
    def signal_power(self, new_signal_power):
        self._signal_power = new_signal_power

    # for default the signal_power is set to be 0.001 Watts
    def set_weighted_paths(self, signal_power: float):
        paths_label = []
        latencies = []
        noises = []
        snrs = []
        df = pd.DataFrame()
        pairs = list(permutations(self.nodes.keys(), 2))
        for pair in pairs:
            for path in self.find_path(pair[0], pair[1]):
                path_label = ''
                for node_name in path:
                    interline = '' if node_name == path[-1] else '->'
                    path_label += node_name + interline
                signal = Signal_information(signal_power, path)
                signal = self.propagate(signal)
                paths_label.append(path_label)
                latencies.append(signal.latency)
                noises.append(signal.noise_power)
                snrs.append(10 * math.log10(signal.signal_power / signal.noise_power))
        df['path'] = paths_label
        df['latency'] = latencies
        df['noise power'] = noises
        df['snr'] = snrs
        self.weighted_paths = df

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
                self.nodes[node_name].successive[line_name] = self.lines[line_name]
                self.lines[line_name].successive[connected_node] = self.nodes[connected_node]

        self.set_weighted_paths(self.signal_power)

    def find_path(self, start_node: str, end_node: str):
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

    def propagate(self, signal_information: Signal_information):
        return self.nodes[signal_information.path[0]].propagate(signal_information)

    def find_best_snr(self, input_node: str, output_node: str):
        if self.weighted_paths is None:
            self.connect()
        # possible_paths_i_o is a list with the possible path that connects node input to output
        possible_paths_i_o = [path for path in self.weighted_paths['path'].tolist()
                              if (path[0] == input_node and path[-1] == output_node)]
        possible_paths_i_o_df = self.weighted_paths.loc[self.weighted_paths['path'].isin(possible_paths_i_o)]
        return possible_paths_i_o_df['path'][possible_paths_i_o_df['snr'].idxmax()]

    def stream(self, connections: list[Connection], best='latency'):
        if self.weighted_paths is None:
            print("The network it's not yet connected or doesn't exist")
            return
        for connection in connections:
            # if the signal power of the connection it's different also the dataframe will have different values
            # so in that case it's needed to redefine the dataframe
            if connection.signal_power != self.signal_power:
                self.set_weighted_paths(connection.signal_power)

    def print_nodes_info(self):
        for node_name in self._nodes:
            print(self._nodes[node_name])

    def print_lines_info(self):
        for line_name in self._lines:
            print(self._lines[line_name])


if __name__ == '__main__':
    network = Network('../nodes.json')
    network.connect()
    network.find_best_snr('A', 'C')
