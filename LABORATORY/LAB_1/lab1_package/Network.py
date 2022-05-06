import json


class Network:

    def __init__(self, json_path):
        self.jsondata = json.load(open(json_path, 'r'))


if __name__ == "__main__":
    network1 = Network('../nodes.json')
    print(network1.jsondata)