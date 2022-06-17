import random

import matplotlib.pyplot as plt
import numpy as np

from EXAM.NETWORK.network_package.Connection import Connection
from EXAM.NETWORK.network_package.Network import Network


# N.B --> IN THIS CASE I'M USING THE FORMULA FOR NOISE GENERATION OF LAB 7 8 AND 9
#         AND NOT THE ONE OF LAB 4 AND 5 REPORTED ON THE SLIDES OF THE PRESENTATION

def main_lab_4_and_5():
    # LAB 4 e 5:
    network = Network('../../258542.json')
    network.connect()

    # caso con 1 canale per linea
    network.channels_number = 1
    network.reset_network()
    # network.draw()
    # print(network.weighted_paths)
    signal_power_connection = 0.001  # Watts
    # first, create a list of 100 casual entries of connection
    node_list = list(network.nodes.keys())
    connections = []
    random.seed(2022)
    for i in range(0, 100):
        random_nodes = random.sample(node_list, 2)  # this function create the random input nodes
        connections.append(Connection(random_nodes[0], random_nodes[1], signal_power_connection))

    connections_streamed = network.stream(connections, best='latency')
    # [print(conn) for conn in connections_streamed]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # rows, columns
    axes.ravel()

    latency_array = [connection.latency for connection in connections_streamed]
    latencies = list(filter(None, latency_array))
    count_null = len(list(filter(lambda elm: elm is None, latency_array)))
    print(count_null)
    # [0 if val is None else val for val in latency_array]
    # print(latency_array)
    axes[0].hist(latencies)
    axes[0].grid(True)
    axes[0].set_xlabel('latency')
    axes[0].set_ylabel('number of accepted connection')
    axes[0].set_title(f'Distribution of Latency along 100 Connections\nConnections rejected: {count_null}')

    # OBSERVATION: !!!
    # After a series of connections is streamed the database of state lines has to be reset free
    network.reset_network()  # this function set all the line as free
    del connections_streamed
    connections_streamed = network.stream(connections, best='snr')
    snr_array = [connection.snr for connection in connections_streamed]
    snrs = [snr for snr in snr_array if snr]
    count_null = len([zero for zero in snr_array if not zero])
    # print(count_null)
    axes[1].hist(snrs)
    axes[1].grid(True)
    axes[1].set_xlabel('snr')
    axes[1].set_ylabel('number of accepted connection')
    axes[1].set_title(f'Distribution of Snr along 100 Connections\nConnections rejected: {count_null}')

    plt.show()
    print("Average Latency: ", np.mean(latencies))
    print("Average Snr: ", np.mean(snrs))

    # LAB 5
    # caso con 10 canale per linea
    network.channels_number = 10
    network.reset_network()
    connections_streamed = network.stream(connections, best='latency')
    # [print(conn) for conn in connections_streamed]

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))  # rows, columns
    axes.ravel()

    latency_array = [connection.latency for connection in connections_streamed]
    latencies = list(filter(None, latency_array))
    count_null = len(list(filter(lambda elm: elm is None, latency_array)))
    print(count_null)
    # [0 if val is None else val for val in latency_array]
    # print(latency_array)
    axes[0].hist(latencies)
    axes[0].grid(True)
    axes[0].set_xlabel('latency')
    axes[0].set_ylabel('number of accepted connection')
    axes[0].set_title(f'Distribution of Latency along 100 Connections\nConnections rejected: {count_null}')

    # OBSERVATION: !!!
    # After a series of connections is streamed the database of state lines has to be reset free
    network.reset_network()  # this function set all the line as free
    del connections_streamed
    connections_streamed = network.stream(connections, best='snr')
    snr_array = [connection.snr for connection in connections_streamed]
    snrs = [snr for snr in snr_array if snr]
    count_null = len([zero for zero in snr_array if not zero])
    # print(count_null)
    axes[1].hist(snrs)
    axes[1].grid(True)
    axes[1].set_xlabel('snr')
    axes[1].set_ylabel('number of accepted connection')
    axes[1].set_title(f'Distribution of Snr along 100 Connections\nConnections rejected: {count_null}')

    plt.show()
    print("Average Latency: ", np.mean(latencies))
    print("Average Snr: ", np.mean(snrs))


if __name__ == '__main__':
    main_lab_4_and_5()
