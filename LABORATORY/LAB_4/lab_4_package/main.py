import random

import matplotlib.pyplot as plt
import numpy as np

from LAB_4.lab_4_package.Connection import Connection
from LAB_4.lab_4_package.Network import Network


def main():
    network = Network('../../LAB_9/sources/258542.json')
    network.connect()
    # network.draw()
    # print(network.weighted_paths)
    signal_power_connection = 0.001  # Watts
    # first, create a list of 100 casual entries of connection
    node_list = list(network.nodes.keys())
    connections = []
    for i in range(0, 100):
        random_nodes = random.sample(node_list, 2)  # this function create the random input nodes
        connections.append(Connection(random_nodes[0], random_nodes[1], signal_power_connection))

    connections_streamed = network.stream(connections, best='latency')
    # [print(conn) for conn in connections_streamed]
    latency_array = [connection.latency for connection in connections_streamed]
    latencies = list(filter(None, latency_array))
    count_null = len(list(filter(lambda elm: elm is None, latency_array)))
    print(count_null)
    # [0 if val is None else val for val in latency_array]
    # print(latency_array)
    plt.hist(latencies)
    plt.grid(True)
    plt.xlabel('latency')
    plt.ylabel('number of accepted connection')
    plt.title(f'Distribution of Latency along 100 Connections\nConnections rejected: {count_null}')
    plt.show()

    # OBSERVATION: !!!
    # After a series of connections is streamed the database of state lines has to be reset free
    network.set_lines_state()  # this function set all the line as free
    del connections_streamed
    connections_streamed = network.stream(connections, best='snr')
    snr_array = [connection.snr for connection in connections_streamed]
    snrs = [snr for snr in snr_array if snr]
    count_null = len([zero for zero in snr_array if not zero])
    # print(count_null)
    plt.hist(snrs)
    plt.grid(True)
    plt.xlabel('snr')
    plt.ylabel('number of accepted connection')
    plt.title(f'Distribution of Snr along 100 Connections\nConnections rejected: {count_null}')
    plt.show()

    print(np.mean(latencies), np.mean(snrs))


if __name__ == '__main__':
    main()
