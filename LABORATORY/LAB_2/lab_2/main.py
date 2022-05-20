import random

import matplotlib.pyplot as plt

from LAB_2.lab_2.Connection import Connection
from LAB_2.lab_2.Network import Network


def main():
    network = Network('../nodes.json')
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
    latency_array = [connection.latency if connection.latency is not None else 0 for connection in connections_streamed]
    # [0 if val is None else val for val in latency_array]
    print(latency_array)
    plt.hist(latency_array)
    plt.grid(True)
    plt.title('Distribution of Latency along 100 Connections')
    plt.show()

    # OBSERVATION: !!!
    # After a series of connections is streamed the database of state lines has to be reset free
    network.set_lines_state()  # this function set all the line as free
    del connections_streamed
    connections_streamed = network.stream(connections, best='snr')
    snr_array = [connection.snr for connection in connections_streamed]
    print(snr_array)
    plt.hist(snr_array)
    plt.grid(True)
    plt.title('Distribution of Snr along 100 Connections')
    plt.show()


if __name__ == '__main__':
    main()
