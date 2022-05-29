import json

# To do the math
from itertools import permutations
import math

import numpy as np
from scipy.special import erfcinv

# To do a better drawing of the network graph
import networkx as nx
# Plots
import matplotlib.pyplot as plt
# Dataframe
import pandas as pd

# Classes of the Network
from LAB_6.lab_6_package.Line import Line
from LAB_6.lab_6_package.Node import Node
from LAB_6.lab_6_package.Connection import Connection
from LAB_6.lab_6_package.Signal_information import Signal_information

TRANSCEIVERS_VARIABLES = {'BERt': 10e-3, 'Rs': 32e9, 'Bn': 12.5e9}


class Network(object):

    def __init__(self, json_path):
        json_data = json.load(open(json_path, 'r'))
        self._nodes = {}
        self._lines = {}
        self._channels_number = 10  # the network it's set by default to have 10 channels
        # the dataframe it's set when you call the function connect()
        # otherwise you can not create a dataframe or a network if you don't connect the nodes
        self._weighted_paths = None
        # Dataframe that contains path and availability of the channels for the connection
        self._route_space = None
        # it's the same dataframe but when a connection occupies a channel the path and so the channel will be removed
        self._route_space_without_occupied_channels = None
        # for default the signal power propagating along the network it's set to be
        # 0.001 Watts
        self._signal_power = 0.001

        # definition of nodes and lines
        for node_name in json_data:
            node_i_dict = json_data[node_name]
            node_i_dict['label'] = node_name
            node_i = Node(node_i_dict)
            self._nodes[node_name] = node_i
        for node_name in self._nodes:
            for connected_node in self._nodes[node_name].connected_nodes:
                line_name = node_name + connected_node
                length = math.dist(self._nodes[node_name].position, self._nodes[connected_node].position)
                self._lines[line_name] = Line(line_name, length, self.channels_number)

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
    def channels_number(self):
        return self._channels_number

    @channels_number.setter
    def channels_number(self, new_channels_number):
        self._channels_number = new_channels_number

    @property
    def route_space(self):
        return self._route_space

    @route_space.setter
    def route_space(self, new_route_space):
        self._route_space = new_route_space

    @property
    def route_space_without_occupied_channels(self):
        return self._route_space_without_occupied_channels

    @route_space_without_occupied_channels.setter
    def route_space_without_occupied_channels(self, new_route_space_without_occupied_channels):
        self._route_space_without_occupied_channels = new_route_space_without_occupied_channels

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
                signal = self.probe(signal)
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
        self.set_route_space()

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
        # I want the path from node_start to node_end sort by len
        list_path.sort(key=len)
        return list_path

    def probe(self, signal_information: Signal_information):
        return self.nodes[signal_information.path[0]].probe(signal_information)

    def find_best_snr(self, input_node: str, output_node: str):
        # possible_paths_i_o is a list with the possible path that connects node input to output
        # in this way when it searches, it will do it directly on the database of available path
        # in the update method when a line it's occupied it will be removed from the database
        possible_paths_i_o = [path for path in self.route_space_without_occupied_channels['path'].tolist()
                              if (path[0] == input_node and path[-1] == output_node)]
        # if the list of possible path is empty it means that there are no free path
        if not possible_paths_i_o:
            return None

        possible_paths_i_o_df = self.weighted_paths.loc[self.weighted_paths['path'].isin(possible_paths_i_o)]

        return possible_paths_i_o_df['path'][possible_paths_i_o_df['snr'].idxmax()]

    def find_best_latency(self, input_node: str, output_node: str):
        # possible_paths_i_o is a list with the possible path that connects node input to output
        possible_paths_i_o = [path for path in self.route_space_without_occupied_channels['path'].tolist()
                              if (path[0] == input_node and path[-1] == output_node)]
        # if the list of possible path is empty it means that there are no free path
        if not possible_paths_i_o:
            return None

        possible_paths_i_o_df = self.weighted_paths.loc[self.weighted_paths['path'].isin(possible_paths_i_o)]

        return possible_paths_i_o_df['path'][possible_paths_i_o_df['latency'].idxmin()]

    def stream(self, connections: list[Connection], best='latency'):
        # inner method to reject a connection
        def reject_connection(connection_i: Connection):
            connection_i.latency = None
            connection_i.snr = 0
            connection_i.bit_rate = 0

        connections_out = []
        if self.weighted_paths is None:
            print("The network it's not yet connected or doesn't exist")
            return
        if self._route_space is None:
            self.set_route_space()
        for connection in connections:
            # if the signal power of the connection it's different from the signal power of the network, it's
            # necessary to set the dataframe of the system with the new signal power and so the entire network
            # will have a different signal_power
            if connection.signal_power != self.signal_power:
                self.signal_power = connection.signal_power
                self.set_weighted_paths()

            # path is a string not a list of string, such as the attribute path in signal_information
            # i.e: path = 'A->B->C'
            if best == 'latency':
                path = self.find_best_latency(connection.input_node, connection.output_node)
            elif best == 'snr':
                path = self.find_best_snr(connection.input_node, connection.output_node)
            else:
                print("Choice for Best Value do not exist")
                return

            if path is None:
                reject_connection(connection)
            else:
                dft = self.route_space_without_occupied_channels
                channel = (dft.loc[(dft['path'] == path) & (dft['channel_state'] == 1)].index[0]) % self.channels_number
                # the path exist, the bit_rate will be calculated with the transceiver of the first node of the given path
                bit_rate = self.calculate_bit_rate(path, self.nodes[path[0]].transceiver)
                if bit_rate:
                    # when we have the free path the connection will occupy it, then the path has to be set as occupied -> 0 (in this case)
                    # the path will be removed from the database route_space but the lines in the path will be set as occupied
                    self.update_path_channels(path, channel)
                    df = self.weighted_paths
                    # It will do a query on the dataframe to have the value of latency and snr
                    connection.latency = float(df.loc[df['path'] == path]['latency'])
                    connection.snr = float(df.loc[df['path'] == path]['snr'])
                    connection.bit_rate = bit_rate
                    print(path)
                else:
                    reject_connection(connection)

            connections_out.append(connection)
        return connections_out

    def update_path_channels(self, path, channel):
        paths = [path[i * 3:i * 3 + 4] for i in range(int(len(path) / 3))]  # paths contains all the line of the path
        df_tmp = self.route_space_without_occupied_channels
        selected_paths = df_tmp.loc[df_tmp['path'].apply(lambda x: True if any(i in x for i in paths) else False), 'path']

        indexes = [i for i in selected_paths.index if (i % self.channels_number) == channel]
        self.route_space.loc[indexes, 'channel_state'] = 0
        self.route_space_without_occupied_channels = self.route_space_without_occupied_channels.drop(indexes)

        # setting the state of each line in the path as occupied
        lines_list = [path.replace('->', '') for path in paths]
        [self.lines[line_name].update_state() for line_name in
         lines_list]  # setting the channel of each lines of the network as occupied

    def set_route_space(self):
        # this method will create and set a dataframe with paths and states of the lines, initially set to free
        if self.weighted_paths is None:
            return
        df = pd.DataFrame()
        df['path'] = self.weighted_paths['path']
        df = df.loc[df.index.repeat(self.channels_number)].reset_index(
            drop=True)  # without the drop=Ture it will maintain also the old indexes
        df['channel_state'] = 1  # setting all the channel as free -> value 1
        self.route_space = df
        self.route_space_without_occupied_channels = df.copy()  # this copy will be modified removing the occupied channels

    def calculate_bit_rate(self, path, strategy: str):
        # if is wanted the number expressed in bits per second uncomment this line
        # Gbps = 1e9  # 1 gbps = 1e9 bits per second
        Gbps = 1
        Bn = TRANSCEIVERS_VARIABLES['Bn']
        Rs = TRANSCEIVERS_VARIABLES['Rs']
        BERt = TRANSCEIVERS_VARIABLES['BERt']
        Gsnr = float(self.weighted_paths.loc[self.weighted_paths['path'] == path, 'snr'])
        RB = (Rs/Bn)
        if strategy == 'fixed-rate':
            bit_rate = 100*Gbps if Gsnr >= (2*(erfcinv(2*BERt)**2)*RB) else 0
        elif strategy == 'flex-rate':
            if Gsnr < 2*(erfcinv(2*BERt)**2)*RB:
                bit_rate = 0
            elif Gsnr < (14/3)*(erfcinv(1.5*BERt)**2)*RB:
                bit_rate = 100*Gbps
            elif Gsnr < 10*(erfcinv((8/3)*BERt)**2)*RB:
                bit_rate = 200*Gbps
            else:
                bit_rate = 400*Gbps
        elif strategy == 'shannon':
            bit_rate = 2*Rs*math.log2(1 + Gsnr*RB)*Gbps/1e9
        else:
            print("Error: it's not possible not having a transceiver not defined")
            return
        return bit_rate

    def print_nodes_info(self):
        for node_name in self._nodes:
            print(self._nodes[node_name])

    def print_lines_info(self):
        for line_name in self._lines:
            print(self._lines[line_name])


if __name__ == '__main__':
    network = Network('../sources/nodes_shannon_transceiver.json')
    network.connect()
    # network.draw()
    # network.update_path_channels('A->B->D->C', 2)
    # network.print_nodes_info()

    out = []
    for _ in range(20):
        conn = Connection('A', 'F', 0.001)
        o = network.stream([conn])
        out.append(o)
    print('-------------')
    for _ in range(2):
        conn = Connection('A', 'B', 0.001)
        o = network.stream([conn])
        out.append(o)

    lines_list = [line for line in network.lines]
    matrix_state = np.array([network.lines[line].state for line in lines_list])
    print(lines_list, '\n', matrix_state)
    # print(len(out))
    # [print(o) for i in out for o in i]

    with pd.ExcelWriter("../route_space_without.xlsx") as writer:
        network.route_space_without_occupied_channels.to_excel(writer)
    with pd.ExcelWriter("../route_space.xlsx") as writer:
        network.route_space.to_excel(writer)

    """
    # Fun fact, the net support around 120 connection for each repeated node in node out 
    out = []
    for _ in range(122):
        conn = Connection('A', 'B', 0.001)
        o = network.stream([conn])
        out.append(o)
    print(network.route_space_without_occupied_channels)
    [print(o) for i in out for o in i]

    

    # print(network.route_space)
    network.update_path_channels('A->B')
    network.update_path_channels('A->B')
    network.update_path_channels('A->B')
    network.update_path_channels('A->B')
    network.update_path_channels('A->B')
    network.update_path_channels('A->B')
    network.update_path_channels('A->B')
    network.update_path_channels('A->B')
    network.update_path_channels('A->B')
    network.update_path_channels('A->B')
    # print(network.route_space.loc[network.route_space['channel state'] == 0])
    with pd.ExcelWriter("../route_space_without.xlsx") as writer:
        network.route_space_without_occupied_channels.to_excel(writer)
    with pd.ExcelWriter("../route_space.xlsx") as writer:
        network.route_space.to_excel(writer)
    
    df_tmp = network.route_space
    # ['path'].tolist()
    selected_path = df_tmp.loc[df_tmp['path'].str.contains('A->C')]
    print(selected_path)

    UPDATED = 0
    indexes = []
    start = selected_path['path'].iat[0]  # independently of the numeric index with iat[0] you get the first row absolutely
    for i in selected_path.index:
        if selected_path.at[i, 'path'] == start:
            if not UPDATED:
                UPDATED = 1
                indexes.append(i)
        else:
            start = selected_path.at[i, 'path']
            indexes.append(i)
    #df_tmp.loc[indexes, 'channel state'] = 0
    df_tmp = df_tmp.drop(indexes)
    print(df_tmp)
    """
