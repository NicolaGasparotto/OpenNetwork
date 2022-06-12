import matplotlib.pyplot as plt

from LAB_9.lab_9_package.Network import *


def main():
    network_fixed_rate = Network('../sources/nodes_fixed-rate_transceiver.json')
    network_fixed_rate.connect()
    network_shannon = Network('../sources/nodes_shannon_transceiver.json')
    network_shannon.connect()
    network_flex_rate = Network('../sources/nodes_flex-rate_transceiver.json')
    network_flex_rate.connect()

    # -------------------------------------------------------------------------------------------------------
    M = list(range(1, 61))
    total_network_capacity_fixed = []
    total_network_capacity_flex = []
    total_network_capacity_shannon = []

    tot_unsatisfied_traffic_fixed = []
    tot_unsatisfied_traffic_flex = []
    tot_unsatisfied_traffic_shannon = []

    total_network_capacity_fixed_after_cut = []
    total_network_capacity_flex_after_cut = []
    total_network_capacity_shannon_after_cut = []

    tot_unsatisfied_traffic_fixed_after_cut = []
    tot_unsatisfied_traffic_flex_after_cut = []
    tot_unsatisfied_traffic_shannon_after_cut = []

    for m in M:
        print(m)
        # restart the systems each time
        network_fixed_rate.reset_network()
        network_flex_rate.reset_network()
        network_shannon.reset_network()
        tot_sh, l_sh = network_shannon.generate_traffic(m, 'list')
        tot_flex, l_flex = network_flex_rate.generate_traffic(m, 'list', l_sh)
        tot_fixed, l_fixed = network_fixed_rate.generate_traffic(m, 'list', l_flex)

        total_network_capacity_fixed.append(tot_fixed/1000)
        total_network_capacity_flex.append(tot_flex/1000)
        total_network_capacity_shannon.append(tot_sh/1000)

        tot_unsatisfied_traffic_fixed.append(((1-(tot_fixed / np.sum(network_fixed_rate.generate_traffic_matrix(m).to_numpy()))) * 100))
        tot_unsatisfied_traffic_flex.append(((1 - (tot_flex / np.sum(network_flex_rate.generate_traffic_matrix(m).to_numpy()))) * 100))
        tot_unsatisfied_traffic_shannon.append(((1 - (tot_sh / np.sum(network_shannon.generate_traffic_matrix(m).to_numpy()))) * 100))

        # CUTTING THE MOST CONGESTED LINE AND VERIFY IF IT'S POSSIBLE TO RESTORE THE TRAFFIC REQUEST
        network_fixed_rate.strong_failure(network_fixed_rate.congested_line)
        network_flex_rate.strong_failure(network_flex_rate.congested_line)
        network_shannon.strong_failure(network_shannon.congested_line)
        network_fixed_rate.recovery_traffic()
        network_flex_rate.recovery_traffic()
        network_shannon.recovery_traffic()

        tot_fixed_after_cut = network_fixed_rate.generate_traffic(m, 'seed')
        tot_flex_after_cut = network_flex_rate.generate_traffic(m, 'seed')
        tot_sh_after_cut = network_shannon.generate_traffic(m, 'seed')

        total_network_capacity_fixed_after_cut.append(tot_fixed_after_cut / 1000)
        total_network_capacity_flex_after_cut.append(tot_flex_after_cut / 1000)
        total_network_capacity_shannon_after_cut.append(tot_sh_after_cut / 1000)

    plt.plot(M, total_network_capacity_fixed, label='fixed-rate')
    plt.plot(M, total_network_capacity_flex, label='flex-rate')
    plt.plot(M, total_network_capacity_shannon, label='shannon')
    plt.plot(M, total_network_capacity_fixed_after_cut, label='fixed-rate-AFTER-CUT')
    plt.plot(M, total_network_capacity_flex_after_cut, label='flex-rate-AFTER-CUT')
    plt.plot(M, total_network_capacity_shannon_after_cut, label='shannon-AFTER-CUT')
    plt.legend()
    plt.title('Saturation for the different Networks')
    plt.ylabel('Total Capacity of Satisfied Traffic [Terabitps]')
    plt.xlabel('M')
    plt.grid(True)
    plt.show()

    plt.plot(M, tot_unsatisfied_traffic_fixed, label='fixed-rate')
    plt.plot(M, tot_unsatisfied_traffic_flex, label='flex-rate')
    plt.plot(M, tot_unsatisfied_traffic_shannon, label='shannon')
    plt.legend()
    plt.title('Saturation for the different Networks')
    plt.ylabel('% of Unsatisfied Traffic Request')
    plt.xlabel('M')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    main()
