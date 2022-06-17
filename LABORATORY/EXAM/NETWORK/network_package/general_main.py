from EXAM.NETWORK.network_package.Network import *


def main():
    network = Network("../../258542.json")
    network.connect()
    network.draw()


if __name__ == '__main__':
    main()
