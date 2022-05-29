from itertools import permutations

import pandas as pd
import math

from LAB_3.lab_3_package.Network import Network
from LAB_3.lab_3_package.Signal_information import Signal_information


def main():
    network = Network('../nodes.json')
    network.connect()

    # generating elements for the dataframe
    paths_label = []
    latencies = []
    noises = []
    snrs = []
    df = pd.DataFrame()

    # generating all possible pair nodes
    pairs = list(permutations(network.nodes.keys(), 2))
    # pair -> AC
    for pair in pairs:
        #                           >> A <<   >> C <<
        for path in network.find_path(pair[0], pair[1]):
            path_label = ''
            for node_name in path:
                interline = ' ' if node_name == path[-1] else ' -> '
                path_label += node_name + interline

            #  Propagation of the signal through the path
            #
            signal = Signal_information(0.001, path)
            # propagation of the signal through network
            signal = network.propagate(signal)
            paths_label.append(path_label)
            latencies.append(signal.latency)
            noises.append(signal.noise_power)
            snrs.append(10 * math.log10(signal.signal_power / signal.noise_power))

    df['path'] = paths_label
    df['latency'] = latencies
    df['noise power'] = noises
    df['snr'] = snrs

    # this method will create or rewrite the specified file
    with pd.ExcelWriter("../result.xlsx") as writer:
        df.to_excel(writer)
    print('Data is successfully written into Excel File')

    # it has to be at the end because plt.show() stop the execution of the program
    network.draw()


if __name__ == '__main__':
    main()
