from datetime import datetime
import itertools
import json
import math
# To do the math
import random
from itertools import permutations

# Plots
import matplotlib.pyplot as plt
# To do a better drawing of the network graph
import networkx as nx
# Dataframe
import numpy as np
import pandas as pd
from scipy.special import erfcinv

from EXAM.NETWORK.network_package.Connection import Connection
# Classes of the Network
from EXAM.NETWORK.network_package.Lightpath import Lightpath
from EXAM.NETWORK.network_package.Line import Line
from EXAM.NETWORK.network_package.Node import Node
from constants import CONSTANTS


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
        # for default the signal power propagating along the network it's set to be
        self.traffic_matrix = None
        self.logger = None
        self._congested_line = None

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
    def traffic_matrix(self):
        return self._traffic_matrix

    @traffic_matrix.setter
    def traffic_matrix(self, new_traffic_matrix):
        self._traffic_matrix = new_traffic_matrix

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, new_logger):
        self._logger = new_logger

    @property
    def congested_line(self):
        return self._congested_line

    @congested_line.setter
    def congested_line(self, new_congested_line):
        self._congested_line = new_congested_line

    def connect(self):
        for node_name in self.nodes:
            for connected_node in self.nodes[node_name].connected_nodes:
                line_name = node_name + connected_node
                self.nodes[node_name].successive[line_name] = self.lines[line_name]
                self.lines[line_name].successive[connected_node] = self.nodes[connected_node]
        self.set_weighted_paths()
        self.set_route_space()

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
                # initially the lightpath has a signal power of 0, and then it will be calculated
                lightpath = Lightpath(0, path)
                lightpath = self.probe(lightpath)
                paths_label.append(path_label)
                latencies.append(lightpath.latency)
                noises.append(lightpath.noise_power)
                snrs.append(10 * math.log10(lightpath.signal_power / lightpath.noise_power))
        df['path'] = paths_label
        df['latency'] = latencies
        df['noise power'] = noises
        df['snr'] = snrs
        self.weighted_paths = df

    def set_route_space(self):
        # this method will create and set a dataframe with paths and states of the lines, initially set to free
        if self.weighted_paths is None:
            return
        columns = [f'channel{i}' for i in range(self.channels_number)]
        df = pd.DataFrame(1, columns=columns, index=self.weighted_paths['path'])
        self.route_space = df

    def set_logger(self):
        columns = ['path', 'epoch_time', 'channel_ID', 'bit_rate']
        df = pd.DataFrame(columns=columns)
        self.logger = df

    def probe(self, lightpath: Lightpath):
        return self.nodes[lightpath.path[0]].probe(lightpath)

    def propagate(self, lightpath):
        return self.nodes[lightpath.path[0]].propagate(lightpath)

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

    def find_best_snr(self, input_node: str, output_node: str):
        # possible_paths_i_o is a list with the possible path that connects node input to output
        # in this way when it searches, it will do it directly on the database of available path
        # in the update method when a line it's occupied it will be removed from the database
        possible_paths_i_o = [path for path in list(self.route_space.index)
                              if (path[0] == input_node and path[-1] == output_node) and (
                                  self.route_space.loc[path].any())]
        # if the list of possible path is empty it means that there are no free path
        if not possible_paths_i_o:
            return None

        possible_paths_i_o_df = self.weighted_paths.loc[self.weighted_paths['path'].isin(possible_paths_i_o)]

        return possible_paths_i_o_df['path'][possible_paths_i_o_df['snr'].idxmax()]

    def find_best_latency(self, input_node: str, output_node: str):
        # possible_paths_i_o is a list with the possible path that connects node input to output
        possible_paths_i_o = [path for path in list(self.route_space.index)
                              if (path[0] == input_node and path[-1] == output_node)
                              and (self.route_space.loc[path].any())]
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
                # creating a lightpath object that has to be propagated along the path to retrieve the information about
                # the connection
                lightpath = Lightpath(0, path.split('->'))
                channel = np.nonzero(self.route_space.loc[path].values[:])[0][
                    0]  # taking the first channel that is not 0
                # the path exist, the bit_rate will be calculated with the transceiver of the first node of the given path
                lightpath.channel_slot = channel
                bit_rate = self.calculate_bit_rate(lightpath, self.nodes[path[0]].transceiver)
                if bit_rate:
                    lightpath_out = self.propagate(lightpath)
                    # when we have the free path the connection will occupy it, then the path has to be set as occupied -> 0 (in this case)
                    # the path will be removed from the database route_space but the lines in the path will be set as occupied
                    self.update_paths_channel(path, channel)
                    self.update_logger(path, channel, bit_rate)
                    # setting the value of the connection
                    connection.signal_power = lightpath_out.signal_power
                    connection.latency = lightpath_out.latency
                    connection.snr = 10 * math.log10(lightpath_out.signal_power / lightpath_out.noise_power)
                    connection.bit_rate = bit_rate
                else:
                    reject_connection(connection)

            connections_out.append(connection)
        return connections_out

    def calculate_bit_rate(self, lightpath: Lightpath, strategy: str):
        # if is wanted the number expressed in bits per second uncomment this line
        # Gbps = 1e9  # 1 gbps = 1e9 bits per second
        path = '->'.join([str(item) for item in lightpath.path])
        Gbps = 1
        Bn = CONSTANTS['Bn']
        Rs = lightpath.Rs  # specific symbol rate of the lightpath
        BERt = CONSTANTS['BERt']
        Gsnr = 10 ** (float(
            self.weighted_paths.loc[self.weighted_paths['path'] == path, 'snr']) / 10)  # gsnr in linear unit
        RB = (Rs / Bn)
        if strategy == 'fixed-rate':
            bit_rate = 100 * Gbps if Gsnr >= (2 * (erfcinv(2 * BERt) ** 2) * RB) else 0
        elif strategy == 'flex-rate':
            if Gsnr < 2 * (erfcinv(2 * BERt) ** 2) * RB:
                bit_rate = 0
            elif Gsnr < (14 / 3) * (erfcinv(1.5 * BERt) ** 2) * RB:
                bit_rate = 100 * Gbps
            elif Gsnr < 10 * (erfcinv((8 / 3) * BERt) ** 2) * RB:
                bit_rate = 200 * Gbps
            else:
                bit_rate = 400 * Gbps
        elif strategy == 'shannon':
            bit_rate = 2 * Rs * math.log2(1 + Gsnr * RB) * Gbps / 1e9  # to have the bit_rate in Gbps
        else:
            print("Error: it's not possible not having a transceiver not defined")
            return
        return bit_rate

    def update_logger(self, path: str, channel_id: int, bit_rate: float):
        if self.logger is None:
            self.set_logger()
        value = {'path': path, 'epoch_time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'), 'channel_ID': channel_id,
                 'bit_rate': bit_rate}
        self.logger = self.logger.append(value, ignore_index=True)

    def update_paths_channel(self, path, channel):
        paths = [path[i * 3:i * 3 + 4] for i in range(int(len(path) / 3))]  # all the lines inside the path
        paths = '|'.join(paths)
        self.route_space.loc[self.route_space.index.str.contains(paths), f'channel{channel}'] = 0

    def generate_traffic_matrix(self, M: int):
        traffic_matrix = np.where(np.eye(len(self.nodes)) > 0, 0, 100 * M)
        index_values = column_values = self.nodes.keys()
        return pd.DataFrame(data=traffic_matrix, index=index_values, columns=column_values)

    def update_traffic_matrix(self, nodes, bit_rate_connection, elements):
        node_I = nodes[0]
        node_O = nodes[1]
        # updating value inside the traffic matrix
        matrix_value = self.traffic_matrix.at[node_I, node_O]
        traffic = matrix_value - bit_rate_connection
        if traffic > 0:
            self.traffic_matrix.loc[node_I, node_O] = traffic
        else:
            self.traffic_matrix.loc[node_I, node_O] = 0
            elements.remove(nodes)

    def strong_failure(self, line_label: str):
        self.lines[line_label].in_service = 0
        self.lines[line_label].state = [0] * self.channels_number
        self.route_space = self.route_space[self.route_space.index.str.contains(line_label) == False]

    def set_list_of_possible_connection(self):
        elements = list(permutations(self.nodes.keys(), 2))
        elements_without_null_connection = [conn for conn in elements if self.traffic_matrix[conn[1]][conn[0]]]
        return elements_without_null_connection

    def recovery_traffic(self):
        if self.congested_line is None:
            return
        path_line = '->'.join(self.congested_line[i:i + 1] for i in range(0, len(self.congested_line)))
        df = self.logger
        for row in df[df['path'].str.contains(path_line)][['path', 'bit_rate', 'channel_ID']].to_numpy():
            lines = [row[0][i * 3:i * 3 + 4] for i in range(int(len(row[0]) / 3))]
            for line in lines:
                if line != path_line:
                    self.lines[line.replace('->', '')].update_state(row[2], 1)
                    self.route_space.loc[self.route_space.index.str.contains(line), f'channel{row[2]}'] = 1
            self.traffic_matrix.loc[row[0][0], row[0][-1]] += row[1]

    def generate_traffic(self, M: int, randomization='random', random_nodes_list=None, connection_out=False):
        if random_nodes_list is None:
            random_nodes_list = []
            list_flag = False
        else:
            list_flag = True
        cnt = 0
        congested_line = False
        if connection_out:
            streamed_connection = []

        max_channel_occupied = self.channels_number
        if self.traffic_matrix is None:
            self.traffic_matrix = self.generate_traffic_matrix(M)

        total_capacity = np.sum(self.generate_traffic_matrix(M).to_numpy())
        # counter for the number of connection
        failed_connection = 0
        successful_connection = 0
        # represent the percentage of missed connection
        percentage = 10 / 100
        elements = self.set_list_of_possible_connection()
        # this will guarantee always the same sequence of random nodes even if the number of picked connection change
        if randomization != 'random':
            np.random.seed(2022)
        # generate connections until the traffic matrix is all 0 OR
        # the connection failed are greater than the connection streamed in percentage
        while (failed_connection <= percentage * successful_connection) and np.count_nonzero(
                self.traffic_matrix.to_numpy()):
            random_nodes = elements[np.random.choice(len(elements))]
            if randomization == 'list':
                if cnt < len(random_nodes_list) and list_flag:
                    random_nodes = random_nodes_list[cnt]
                    cnt += 1
                else:
                    list_flag = False
                    random_nodes_list.append(random_nodes)
            out_conn = self.stream([Connection(random_nodes[0], random_nodes[1], 0)], 'snr').pop()
            if connection_out:
                streamed_connection.append(out_conn)
            bit_rate_connection = out_conn.bit_rate
            if not congested_line:
                for line in self.lines:
                    if self.lines[line].in_service:
                        tmp = np.sum(self.lines[line].state)
                        if not tmp:
                            congested_line = True
                            self.congested_line = line
                            break
                        if tmp < max_channel_occupied:
                            max_channel_occupied = tmp
                            self.congested_line = line
            if bit_rate_connection != 0:
                successful_connection += 1
                self.update_traffic_matrix(random_nodes, bit_rate_connection, elements)
            else:
                failed_connection += 1

        total_satisfied_traffic = total_capacity - np.sum(self.traffic_matrix.to_numpy())

        if randomization == 'list':
            if connection_out:
                return total_satisfied_traffic, random_nodes_list, streamed_connection
            return total_satisfied_traffic, random_nodes_list
        return total_satisfied_traffic

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
        plt.xlabel("[meters]")
        plt.ylabel("[meters]")
        plt.grid(True)
        plt.show()

    def print_nodes_info(self):
        for node_name in self._nodes:
            print(self._nodes[node_name])

    def print_lines_info(self):
        for line_name in self._lines:
            print(self._lines[line_name])

    def reset_network(self):
        self.congested_line = None
        self.traffic_matrix = None
        self.set_route_space()
        self.set_logger()
        for line in self.lines:
            self.lines[line].state = [1] * self.lines[line].n_channel
            self.lines[line].in_service = 1


if __name__ == '__main__':
    """
        with pd.ExcelWriter("../logger.xlsx") as writer:
            network.logger.to_excel(writer)
    
    network = Network('../sources/nodes_shannon_transceiver.json')
    network.connect()

    network1 = Network('../sources/nodes_flex-rate_transceiver.json')
    network1.connect()

    network2 = Network('../sources/nodes_fixed-rate_transceiver.json')
    network2.connect()

    m = 14
    # sh
    tot, l_sh = network.generate_traffic(m, 'list')
    print(tot)
    network.strong_failure(network.congested_line)
    network.recovery_traffic()
    print(network.generate_traffic(m, 'seed'))
    print(network.congested_line)

    # flex
    tot, l_flex = network1.generate_traffic(m, 'list', l_sh)
    print(tot)
    network1.strong_failure(network1.congested_line)
    network1.recovery_traffic()
    print(network1.generate_traffic(m, 'seed'))
    print(network1.congested_line)

    # fixed
    tot, l_fxd = network2.generate_traffic(m, 'list', l_flex)
    print(tot)
    network2.strong_failure(network2.congested_line)
    network2.recovery_traffic()
    print(network2.generate_traffic(m, 'seed'))
    print(network2.congested_line)
    """
