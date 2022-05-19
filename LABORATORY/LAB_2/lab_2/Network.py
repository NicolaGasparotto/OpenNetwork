import json

# To do the math
from itertools import permutations
import math
# To do a better drawing of the network graph
import networkx as nx
# Plots
import matplotlib.pyplot as plt
# Dataframe
import pandas as pd

from LAB_2.lab_2.Line import Line
from LAB_2.lab_2.Node import Node
from LAB_2.lab_2.Connection import Connection
from LAB_2.lab_2.Signal_information import Signal_information


class Network(object):

    def __init__(self, json_path):
        json_data = json.load(open(json_path, 'r'))
        self._nodes = {}
        self._lines = {}

        # the dataframe it's set when you call the function connect()
        # otherwise you can not create a dataframe or a network if you don't connect the nodes
        self._weighted_paths = None

        # Dataframe that contains path and availability of the path/lines for the connection
        self._lines_state = None

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

    @property
    def lines_state(self):
        return self._lines_state

    @lines_state.setter
    def lines_state(self, new_lines_state):
        self._lines_state = new_lines_state

    # for default the signal_power is set to be 0.001 Watts
    def set_weighted_paths(self):
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
                signal = Signal_information(self.signal_power, path)
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
        self.set_weighted_paths()

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
        # path_list = []
        # path_list[:0] = possible_paths_i_o_df['path'][possible_paths_i_o_df['snr'].idxmax()].replace('->', '')
        # return path_list
        return possible_paths_i_o_df['path'][possible_paths_i_o_df['snr'].idxmax()]

    def find_best_latency(self, input_node: str, output_node: str):
        if self.weighted_paths is None:
            self.connect()
        # possible_paths_i_o is a list with the possible path that connects node input to output
        possible_paths_i_o = [path for path in self.weighted_paths['path'].tolist()
                              if (path[0] == input_node and path[-1] == output_node)]
        possible_paths_i_o_df = self.weighted_paths.loc[self.weighted_paths['path'].isin(possible_paths_i_o)]
        # path_list = []
        # path_list[:0] = possible_paths_i_o_df['path'][possible_paths_i_o_df['latency'].idxmin()].replace('->', '')
        # return path_list
        return possible_paths_i_o_df['path'][possible_paths_i_o_df['latency'].idxmin()]

    def stream(self, connections: list[Connection], best='latency'):
        connections_out = []
        if self.weighted_paths is None:
            print("The network it's not yet connected or doesn't exist")
            return
        if self._lines_state is None:
            self.set_lines_state()
        for connection in connections:
            # if the signal power of the connection it's different from the signal power of the network, it's
            # necessary to set the dataframe of the system with the new signal power and so the entire network
            # will have a different signal_power
            if connection.signal_power != self.signal_power:
                self.signal_power = connection.signal_power
                self.set_weighted_paths()

            # path is a string not a list of string, such as the attribute path in signal_information
            if best == 'latency':
                path = self.find_best_latency(connection.input_node, connection.output_node)
            elif best == 'snr':
                path = self.find_best_snr(connection.input_node, connection.output_node)
            else:
                print("Choice for Best Value do not exist")
                return

            # when we have the free path the connection will occupy it so the path has to be set as occupied -> 0
            # and so the lines in the path
            self.update_line_state(path)

            df = self.weighted_paths
            # It will do a query on the dataframe to have the value of latency and snr
            connection.latency = float(df.loc[df['path'] == path]['latency'])
            connection.snr = float(df.loc[df['path'] == path]['snr'])

            connections_out.append(connection)

        return connections_out

    def update_line_state(self, path):
        # setting the state of the line in the dataframe as occupied
        df_tmp = self.lines_state
        #       >> this one is a mask that filter the string and return the indexes <<<<
        df_tmp['state'][df_tmp['path'].str.contains('A->C')] = 0
        self.lines_state = df_tmp

        # setting the state of each line in the path as occupied
        # remove the -> from the path
        path = path[::3]
        lines_list = [path[i]+path[i+1] for i in range(len(path)-1)]
        # setting state of lines of the network as occupied
        for line_label in lines_list:
            self.lines[line_label].state = 0

    def set_lines_state(self):
        # this method will create and set a dataframe with paths and states of the lines, initially set to free
        if self.weighted_paths is None:
            return
        df = pd.DataFrame()
        df['path'] = self.weighted_paths['path']
        states = [1 for _ in self.weighted_paths['path']]
        df['state'] = states
        self.lines_state = df

    def print_nodes_info(self):
        for node_name in self._nodes:
            print(self._nodes[node_name])

    def print_lines_info(self):
        for line_name in self._lines:
            print(self._lines[line_name])


if __name__ == '__main__':
    network = Network('../nodes.json')
    network.connect()

    """
    network.set_lines_state()

    df = network.lines_state
    df['state'][df['path'].str.contains('A->C')] = 0
    print(df)

    string = 'ABCDEF'
    lists = [string[i]+string[i+1] for i in range(len(string)-1)]
    print(lists)
    
    print(type(network.find_best_snr('A', 'C')))
    print(network.find_best_latency('A', 'C'))

    snr = float(network.weighted_paths.loc[network.weighted_paths['path'] == 'A->B']['snr'])
    snr += 100
    print(snr)

    conn1 = Connection('A', 'C', 0.002)
    conn2 = Connection('C', 'A', 0.002)
    # [print(conn) for conn in network.stream([conn1, conn2])]
    """
