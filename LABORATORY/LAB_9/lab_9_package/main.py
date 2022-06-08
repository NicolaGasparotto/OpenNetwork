import matplotlib.pyplot as plt

from LAB_9.lab_9_package.Network import *


def main():
    network_fixed_rate = Network('../sources/nodes_fixed-rate_transceiver.json')
    network_fixed_rate.connect()

    network_shannon = Network('../sources/nodes_shannon_transceiver.json')
    network_shannon.connect()

    network_flex_rate = Network('../sources/nodes_flex-rate_transceiver.json')
    network_flex_rate.connect()

    number_of_connections = 100
    # first, create a list of 100 casual entries of connection
    node_list = list(network_fixed_rate.nodes.keys())
    connections = []
    for i in range(0, number_of_connections):
        random_nodes = random.sample(node_list, 2)  # this function create the random input nodes
        connections.append(Connection(random_nodes[0], random_nodes[1], 0))

    # print("SNR DISTRIBUTION WITH FIXED RATE TRANSCEIVER")
    connections_streamed = network_fixed_rate.stream(connections, best='snr')
    bit_rates_fixed = np.array([connection.bit_rate for connection in connections_streamed])
    total_network_capacity_fixed = bit_rates_fixed.sum()
    # print("Total Network Capacity [gbps]: ", total_network_capacity_fixed)

    # print("SNR DISTRIBUTION WITH FLEX RATE TRANSCEIVER")
    connections_streamed = network_flex_rate.stream(connections, best='snr')
    bit_rates_flex = np.array([connection.bit_rate for connection in connections_streamed])
    total_network_capacity_flex = bit_rates_flex.sum()
    # print("Total Network Capacity [gbps]: ", total_network_capacity_flex)

    # print("SNR DISTRIBUTION WITH SHANNON TRANSCEIVER")
    connections_streamed = network_shannon.stream(connections, best='snr')
    bit_rates_shannon = np.array([connection.bit_rate for connection in connections_streamed])
    total_network_capacity_shannon = bit_rates_shannon.sum()
    # print("Total Network Capacity [gbps]: ", total_network_capacity_shannon)

    bit_rates = [bit_rates_fixed[bit_rates_fixed.nonzero()], bit_rates_flex[bit_rates_flex.nonzero()],
                 bit_rates_shannon[bit_rates_shannon.nonzero()]]
    titles = [f'BIT RATE WITH FIXED-RATE TRANSCEIVER\nTOTAL NETWORK CAPACITY: {total_network_capacity_fixed}\n'
              f'Rejeceted connections: {(np.count_nonzero(bit_rates_fixed == 0) / number_of_connections) * 100}%\n',
              f'BIT RATE WITH FLEX-RATE TRANSCEIVER\nTOTAL NETWORK CAPACITY: {total_network_capacity_flex}\n'
              f'Rejeceted connections: {(np.count_nonzero(bit_rates_flex == 0) / number_of_connections) * 100}%\n',
              f'BIT RATE WITH SHANNON TRANSCEIVER\nTOTAL NETWORK CAPACITY: {total_network_capacity_shannon}\n'
              f'Rejeceted connections: {(np.count_nonzero(bit_rates_shannon == 0) / number_of_connections) * 100}%\n']

    fig, axes = plt.subplots(1, 3, figsize=(16, 6))  # rows, columns
    axes = axes.ravel()
    for idx, ax in enumerate(axes):
        ax.hist(bit_rates[idx])
        ax.grid(True)
        ax.set_title(titles[idx])
        ax.set_xlabel('bit rate [Gbps]')

    fig.tight_layout()
    plt.show()

    # -------------------------------------------------------------------------------------------------------
    M = list(range(1, 100))
    total_network_capacity_fixed = []
    total_network_capacity_flex = []
    total_network_capacity_shannon = []

    for m in M:
        # restart the systems each time
        network_fixed_rate.reset_network()
        network_flex_rate.reset_network()
        network_shannon.reset_network()
        total_network_capacity_fixed.append(100-network_fixed_rate.generate_traffic(m))
        total_network_capacity_flex.append(100-network_flex_rate.generate_traffic(m))
        total_network_capacity_shannon.append(100-network_shannon.generate_traffic(m))

    plt.plot(M, total_network_capacity_fixed, label='fixed-rate')
    plt.plot(M, total_network_capacity_flex, label='flex-rate')
    plt.plot(M, total_network_capacity_shannon, label='shannon')
    plt.legend()
    plt.title('Saturation for the different Networks')
    plt.ylabel('% of Unsatisfied Traffic')
    plt.xlabel('M')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
