import random

from LAB_6.lab_6_package.Network import *

TRANSCEIVERS_VARIABLES = {'BERt': 10e-3, 'Rs': 32e9, 'Bn': 12.5e9}


def calculate_bit_rate(snr, strategy: str):
    # if is wanted the number expressed in bits per second uncomment this line
    # Gbps = 1e9  # 1 gbps = 1e9 bits per second
    Gbps = 1
    Bn = TRANSCEIVERS_VARIABLES['Bn']
    Rs = TRANSCEIVERS_VARIABLES['Rs']
    BERt = TRANSCEIVERS_VARIABLES['BERt']
    Gsnr = 10 ** (snr / 10)  # gsnr in linear unit
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
        bit_rate = 2 * Rs * math.log2(1 + Gsnr * RB) * Gbps / 1e9
    else:
        print("Error: it's not possible not having a transceiver not defined")
        return
    return bit_rate


def main():
    snrs = np.linspace(0, 60, num=500)
    bit_rates_fixed = [calculate_bit_rate(snr, 'fixed-rate') for snr in snrs]
    bit_rates_flex = [calculate_bit_rate(snr, 'flex-rate') for snr in snrs]
    bit_rates_shannon = [calculate_bit_rate(snr, 'shannon') for snr in snrs]
    plt.plot(snrs, bit_rates_fixed, label='fixed-rate')
    plt.plot(snrs, bit_rates_flex, label='flex-rate')
    plt.plot(snrs, bit_rates_shannon, label='shannon')
    plt.grid(True)
    plt.legend()
    plt.title("BIT RATE CURVE vs GSNR FOR DIFFERENT TRANSCEIVER TECHNOLOGY\n")
    plt.xlabel('GSNR [dB]')
    plt.ylabel('BIT RATE [Gbps]')
    plt.show()

    network_fixed_rate = Network('../../EXAM/258542_fixed_rate_transceiver.json')
    network_fixed_rate.connect()

    network_shannon = Network('../../EXAM/258542_shannon_transceiver.json')
    network_shannon.connect()

    network_flex_rate = Network('../../EXAM/258542_flex_rate_transceiver.json')
    network_flex_rate.connect()

    number_of_connections = 100
    signal_power_connection = 0.001  # Watts
    # first, create a list of 100 casual entries of connection
    node_list = list(network_fixed_rate.nodes.keys())
    random.seed(2022)
    connections = []
    for i in range(0, number_of_connections):
        random_nodes = random.sample(node_list, 2)  # this function create the random input nodes
        connections.append(Connection(random_nodes[0], random_nodes[1], signal_power_connection))

    print("SNR DISTRIBUTION WITH FIXED RATE TRANSCEIVER")
    connections_streamed = network_fixed_rate.stream(connections, best='snr')
    bit_rates_fixed = np.array([connection.bit_rate for connection in connections_streamed])
    total_network_capacity_fixed = bit_rates_fixed.sum()
    print("Total Network Capacity [gbps]: ", total_network_capacity_fixed)

    print("SNR DISTRIBUTION WITH FLEX RATE TRANSCEIVER")
    connections_streamed = network_flex_rate.stream(connections, best='snr')
    bit_rates_flex = np.array([connection.bit_rate for connection in connections_streamed])
    total_network_capacity_flex = bit_rates_flex.sum()
    print("Total Network Capacity [gbps]: ", total_network_capacity_flex)

    print("SNR DISTRIBUTION WITH SHANNON TRANSCEIVER")
    connections_streamed = network_shannon.stream(connections, best='snr')
    bit_rates_shannon = np.array([connection.bit_rate for connection in connections_streamed])
    total_network_capacity_shannon = bit_rates_shannon.sum()
    print("Total Network Capacity [gbps]: ", total_network_capacity_shannon)

    bit_rates = [bit_rates_fixed[bit_rates_fixed.nonzero()], bit_rates_flex[bit_rates_flex.nonzero()],
                 bit_rates_shannon[bit_rates_shannon.nonzero()]]
    titles = [f'BIT RATE WITH FIXED-RATE TRANSCEIVER\nTOTAL NETWORK CAPACITY: {total_network_capacity_fixed}\n'
              f'Rejeceted connections: {(np.count_nonzero(bit_rates_fixed==0)/number_of_connections)*100}%\n',
              f'BIT RATE WITH FLEX-RATE TRANSCEIVER\nTOTAL NETWORK CAPACITY: {total_network_capacity_flex}\n'
              f'Rejeceted connections: {(np.count_nonzero(bit_rates_flex==0)/number_of_connections)*100}%\n',
              f'BIT RATE WITH SHANNON TRANSCEIVER\nTOTAL NETWORK CAPACITY: {total_network_capacity_shannon}\n'
              f'Rejeceted connections: {(np.count_nonzero(bit_rates_shannon==0)/number_of_connections)*100}%\n']

    fig, axes = plt.subplots(1, 3, figsize=(16, 6))  # rows, columns
    axes = axes.ravel()
    for idx, ax in enumerate(axes):
        ax.hist(bit_rates[idx])
        ax.grid(True)
        ax.set_title(titles[idx])
        ax.set_xlabel('bit rate [Gbps]')

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
