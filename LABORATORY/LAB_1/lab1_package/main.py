from itertools import permutations

import pandas as pd
import math

from LAB_1.lab1_package.Network import Network
from LAB_1.lab1_package.Signal_information import Signal_information


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
                path_label += node_name + '->'

            #  Propagation of the signal through the path
            #
            signal = Signal_information(0.001, path)
            # propagation of the signal through network
            signal = network.propagate(signal)
            paths_label.append(path_label)
            latencies.append(signal.latency)
            noises.append(signal.noise_power)
            print(signal)
            snrs.append(10*math.log10(signal.signal_power/signal.noise_power))


if __name__ == '__main__':
    main()
