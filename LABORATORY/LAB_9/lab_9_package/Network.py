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

from LAB_9.lab_9_package.Connection import Connection
# Classes of the Network
from LAB_9.lab_9_package.Lightpath import Lightpath
from LAB_9.lab_9_package.Line import Line
from LAB_9.lab_9_package.Node import Node
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
        # it's the same dataframe but when a connection occupies a channel the path and so the channel will be removed
        self._route_space_without_occupied_channels = None
        # for default the signal power propagating along the network it's set to be
        self.traffic_matrix = None
        self.logger = None
        
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
    def route_space_without_occupied_channels(self):
        return self._route_space_without_occupied_channels

    @route_space_without_occupied_channels.setter
    def route_space_without_occupied_channels(self, new_route_space_without_occupied_channels):
        self._route_space_without_occupied_channels = new_route_space_without_occupied_channels

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
        df = pd.DataFrame()
        df['path'] = self.weighted_paths['path']
        df = df.loc[df.index.repeat(self.channels_number)].reset_index(
            drop=True)  # without the drop=Ture it will maintain also the old indexes
        df['channel_state'] = 1  # setting all the channel as free -> value 1
        self.route_space = df
        self.route_space_without_occupied_channels = df.copy()  # this copy will be modified removing the occupied channels

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
                dft = self.route_space_without_occupied_channels
                channel = (dft.loc[(dft['path'] == path) & (dft['channel_state'] == 1)].index[0]) % self.channels_number
                # the path exist, the bit_rate will be calculated with the transceiver of the first node of the given path
                lightpath.channel_slot = channel
                bit_rate = self.calculate_bit_rate(lightpath, self.nodes[path[0]].transceiver)
                if bit_rate:
                    lightpath_out = self.propagate(lightpath)
                    # when we have the free path the connection will occupy it, then the path has to be set as occupied -> 0 (in this case)
                    # the path will be removed from the database route_space but the lines in the path will be set as occupied
                    self.update_paths_channel(path, channel)

                    # setting the value of the connection
                    connection.signal_power = lightpath_out.signal_power
                    connection.latency = lightpath_out.latency
                    connection.snr = 10*math.log10(lightpath_out.signal_power/lightpath_out.noise_power)
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
        Gsnr = 10**(float(self.weighted_paths.loc[self.weighted_paths['path'] == path, 'snr'])/10)  # gsnr in linear unit
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
            bit_rate = 2*Rs*math.log2(1 + Gsnr*RB)*Gbps/1e9  # to have the bit_rate in Gbps
        else:
            print("Error: it's not possible not having a transceiver not defined")
            return
        return bit_rate

    def update_paths_channel(self, path, channel):
        paths = [path[i * 3:i * 3 + 4] for i in range(int(len(path) / 3))]  # paths contains all the line of the path
        df_tmp = self.route_space_without_occupied_channels
        selected_paths = df_tmp.loc[df_tmp['path'].apply(lambda x: True if any(i in x for i in paths) else False), 'path']

        indexes = [i for i in selected_paths.index if (i % self.channels_number) == channel]
        self.route_space.loc[indexes, 'channel_state'] = 0
        self.route_space_without_occupied_channels = self.route_space_without_occupied_channels.drop(indexes)

    def generate_traffic_matrix(self, M: int):
        traffic_matrix = np.where(np.eye(len(self.nodes)) > 0, 0, 100 * M)
        index_values = column_values = self.nodes.keys()
        self.traffic_matrix = pd.DataFrame(data=traffic_matrix, index=index_values, columns=column_values)

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

    def generate_traffic(self, M: int):
        self.generate_traffic_matrix(M)
        total_capacity = np.sum(self.traffic_matrix.to_numpy())
        # counter for the number of connection
        failed_connection = 0
        successful_connection = 0
        # represent the percentage of missed connection
        percentage = 10/100
        elements = list(permutations(self.nodes.keys(), 2))
        # generate connections until the traffic matrix is all 0 OR
        # the connection failed are greater than the connection streamed in percentage
        while (failed_connection <= percentage * successful_connection) and np.count_nonzero(self.traffic_matrix.to_numpy()):
            random_nodes = random.choices(elements).pop()
            bit_rate_connection = self.stream([Connection(random_nodes[0], random_nodes[1], 0)], 'snr').pop().bit_rate
            if bit_rate_connection != 0:
                successful_connection += 1
                self.update_traffic_matrix(random_nodes, bit_rate_connection, elements)
            else:
                failed_connection += 1

        total_satisfied_traffic = total_capacity - np.sum(self.traffic_matrix.to_numpy())
        """
        if not np.count_nonzero(matrix):
            return M, total_capacity
        return -1, total_capacity
        """
        return (total_satisfied_traffic/total_capacity)*100

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

    def print_nodes_info(self):
        for node_name in self._nodes:
            print(self._nodes[node_name])

    def print_lines_info(self):
        for line_name in self._lines:
            print(self._lines[line_name])

    def reset_network(self):
        self.route_space['channel_state'] = 1
        self.route_space_without_occupied_channels = self.route_space.copy()
        for line in self.lines:
            self.lines[line].state = [1] * self.lines[line].n_channel


if __name__ == '__main__':
    network = Network('../sources/nodes_shannon_transceiver.json')
    network.connect()
    network.generate_traffic(30)
    print(network.traffic_matrix)


