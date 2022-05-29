import random

import matplotlib.pyplot as plt
import pandas as pd

from LAB_5.lab_5_package.Connection import Connection
from LAB_5.lab_5_package.Network import Network


def main():
    connections_number = 100
    network = Network('../nodes.json')
    network.connect()

    signal_power_connection = 0.001  # Watts
    # first, create a list of 100 casual entries of connection
    node_list = list(network.nodes.keys())
    connections = []
    for i in range(0, connections_number):
        random_nodes = random.sample(node_list, 2)  # this function create the random input nodes
        connections.append(Connection(random_nodes[0], random_nodes[1], signal_power_connection))

    print([conn.input_node + conn.output_node for conn in connections])
    # LATENCY DISTRIBUTION
    connections_streamed = network.stream(connections, best='latency')
    latency_array = [connection.latency for connection in connections_streamed]
    latencies = list(filter(None, latency_array))
    count_null = len(list(filter(lambda elm: elm is None, latency_array)))
    plt.hist(latencies)
    plt.grid(True)
    plt.title(f'Distribution of Latency along {connections_number} Connections\nConnections rejected: {count_null}')
    plt.show()

    # SNR DISTRIBUTION
    del connections_streamed
    network.set_route_space()
    connections_streamed = network.stream(connections, best='snr')
    snr_array = [connection.snr for connection in connections_streamed]
    snrs = [snr for snr in snr_array if snr]
    count_null = len([zero for zero in snr_array if not zero])
    plt.hist(snrs)
    plt.grid(True)
    plt.title(f'Distribution of SNR along {connections_number} Connections\nConnections rejected: {count_null}')
    plt.show()


if __name__ == '__main__':
    main()
