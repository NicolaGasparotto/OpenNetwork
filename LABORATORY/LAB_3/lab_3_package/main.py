import random

import matplotlib.pyplot as plt

from LAB_3.lab_3_package.Connection import Connection
from LAB_3.lab_3_package.Network import Network


def main():
    network = Network('../nodes.json')
    network.connect()

    signal_power_connection = 0.001  # Watts
    # first, create a list of 100 casual entries of connection
    node_list = list(network.nodes.keys())
    connections = []
    for i in range(0, 100):
        random_nodes = random.sample(node_list, 2)  # this function create the random input nodes
        connections.append(Connection(random_nodes[0], random_nodes[1], signal_power_connection))

    # LATENCY DISTRIBUTION
    connections_streamed = network.stream(connections, best='latency')
    latency_array = [connection.latency if connection.latency is not None else 0 for connection in connections_streamed]
    plt.hist(latency_array)
    plt.grid(True)
    plt.title('Distribution of Latency along 100 Connections')
    plt.show()

    # SNR DISTRIBUTION
    del connections_streamed
    network.set_route_space()
    connections_streamed = network.stream(connections, best='snr')
    snr_array = [connection.snr for connection in connections_streamed]
    plt.hist(snr_array)
    plt.grid(True)
    plt.title('Distribution of SNR along 100 Connections')
    plt.show()


if __name__ == '__main__':
    main()
