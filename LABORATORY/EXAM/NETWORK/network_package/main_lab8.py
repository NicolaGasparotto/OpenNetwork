import matplotlib.pyplot as plt
import numpy as np

from EXAM.NETWORK.network_package import constants
from EXAM.NETWORK.network_package.Network import Network


def main_lab_8():
    network_fixed_rate = Network('../../../LAB_9/sources/nodes_fixed-rate_transceiver.json')
    network_fixed_rate.connect()
    network_shannon = Network('../../../LAB_9/sources/nodes_shannon_transceiver.json')
    network_shannon.connect()
    network_flex_rate = Network('../../../LAB_9/sources/nodes_flex-rate_transceiver.json')
    network_flex_rate.connect()

    # -------------------------------------------------------------------------------------------------------
    m = 4
    print(m)
    # restart the systems each time
    network_fixed_rate.reset_network()
    network_flex_rate.reset_network()
    network_shannon.reset_network()
    tot_sh, l_sh, l_conn_sh = network_shannon.generate_traffic(m, 'list', connection_out=True)
    tot_flex, l_flex, l_conn_flex = network_flex_rate.generate_traffic(m, 'list', l_sh, connection_out=True)
    tot_fixed, l_fixed, l_conn_fixed = network_fixed_rate.generate_traffic(m, 'list', l_flex, connection_out=True)

    network_fixed_rate.reset_network()
    network_flex_rate.reset_network()
    network_shannon.reset_network()
    tot_sh_b, l_sh, l_conn_sh_b = network_shannon.generate_traffic(m, 'list', connection_out=True)
    tot_flex_b, l_flex, l_conn_flex_b = network_flex_rate.generate_traffic(m, 'list', l_sh, connection_out=True)
    tot_fixed_b, l_fixed, l_conn_fixed_b = network_fixed_rate.generate_traffic(m, 'list', l_flex, connection_out=True)

    snr_fixed = [conn.snr for conn in l_conn_fixed]
    snr_flex = [conn.snr for conn in l_conn_flex]
    snr_sh = [conn.snr for conn in l_conn_sh]

    fig, axes = plt.subplots(1, 3, figsize=(16, 6))  # rows, columns
    axes.ravel()

    axes[0].hist(snr_fixed)
    axes[1].hist(snr_flex)
    axes[2].hist(snr_sh)
    for i in range(3):
        axes[i].grid(True)
        axes[i].set_xlabel('SNR [dB]')
        axes[i].set_ylabel('number of connection')

    print(tot_fixed, tot_flex, tot_sh)
    print("Average: ", np.mean(snr_fixed))
    print("Average: ", np.mean(snr_flex))
    print("Average: ", np.mean(snr_sh))
    plt.show()


if __name__ == '__main__':
    main_lab_8()
