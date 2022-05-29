import random

import matplotlib.pyplot as plt

from LAB_7.lab_7_package.Connection import Connection
from LAB_7.lab_7_package.Network import Network


def main():
    network_fixed_rate = Network('../sources/nodes_fixed-rate_transceiver.json')
    network_fixed_rate.connect()

    network_shannon = Network('../sources/nodes_shannon_transceiver.json')
    network_shannon.connect()

    network_flex_rate = Network('../sources/nodes_flex-rate_transceiver.json')
    network_flex_rate.connect()

    signal_power_connection = 0.001  # Watts
    # first, create a list of 100 casual entries of connection
    node_list = list(network_fixed_rate.nodes.keys())
    connections = []
    for i in range(0, 100):
        random_nodes = random.sample(node_list, 2)  # this function create the random input nodes
        connections.append(Connection(random_nodes[0], random_nodes[1], signal_power_connection))

    print("SNR DISTRIBUTION WITH FIXED RATE TRANSCEIVER")
    connections_streamed = network_fixed_rate.stream(connections, best='snr')
    snr_array_fixed = [connection.snr for connection in connections_streamed]
    total_network_capacity = 0
    for conn in connections_streamed:
        total_network_capacity += conn.bit_rate
    print("Total Network Capacity: ", total_network_capacity)
    """
    plt.hist(snr_array)
    plt.grid(True)
    plt.title('Distribution of SNR along 100 Connections')
    plt.show()
    """

    print("SNR DISTRIBUTION WITH FLEX RATE TRANSCEIVER")
    connections_streamed = network_flex_rate.stream(connections, best='snr')
    snr_array_flex = [connection.snr for connection in connections_streamed]
    total_network_capacity = 0
    for conn in connections_streamed:
        total_network_capacity += conn.bit_rate
    print("Total Network Capacity: ", total_network_capacity)
    """
    plt.hist(snr_array)
    plt.grid(True)
    plt.title('Distribution of SNR along 100 Connections')
    plt.show()
    """

    print("SNR DISTRIBUTION WITH SHANNON TRANSCEIVER")
    connections_streamed = network_shannon.stream(connections, best='snr')
    snr_array_shannon = [connection.snr for connection in connections_streamed]
    total_network_capacity = 0
    for conn in connections_streamed:
        total_network_capacity += conn.bit_rate
    print("Total Network Capacity: ", total_network_capacity)
    """
    plt.hist(snr_array)
    plt.grid(True)
    plt.title('Distribution of SNR along 100 Connections')
    plt.show()
    """


if __name__ == '__main__':
    main()
