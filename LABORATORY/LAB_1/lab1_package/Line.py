class Line:

    def __init__(self, label, length):
        self._length = length
        self._label = label
        self._successive = {}  # empty dictionary[type Node]

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, new_length):
        self._length = new_length

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, new_label):
        self._label = new_label

    def latency_generation(self):
        c = 3 * (10 ** 9)
        latency = float(self.length / (c * 2 / 3))
        return latency

    def noise_generation(self, signal_power):
        return signal_power * self.length * (10 ** -9)

    def propagate(self, signal_information):
        signal_information.add_latency(self.latency_generation())
        signal_information.add_noise_power(self.noise_generation(signal_information.noise_power))
        # next element is given by the path of signal_information
        # i want a node type element so:
        # node = self.successive[signal_information.path[0]]
        return

    def __str__(self):
        return f"Node line: {self.label}\nLength: {self.length}\n"


if __name__ == '__main__':
    linea1 = Line('A', 15.0)
    print(linea1)
