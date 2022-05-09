class Line:

    def __init__(self, label, length):
        self._length = length
        self._label = label
        self._successive = {}  # empty dictionary[type Node]

    @property
    def length(self):
        return self._length

    @property
    def label(self):
        return self._label

    @property
    def successive(self):
        return self._successive

    @length.setter
    def length(self, new_length):
        self._length = new_length

    @label.setter
    def label(self, new_label):
        self._label = new_label

    @successive.setter
    def successive(self, new_successive):
        self.successive = new_successive

    def latency_generation(self):
        c = 3 * (10 ** 9)  # light speed
        return float(self.length / (c * 2 / 3))  # this is the latency calculated

    def noise_generation(self, signal_power):
        return signal_power * self.length * (10 ** -9)

    def propagate(self, signal_i):
        signal_i.add_latency(self.latency_generation())
        signal_i.add_noise_power(self.noise_generation(signal_i.noise_power))
        # it will recall the method propagate for the next node
        self._successive[signal_i.path[0]].propagate(signal_i)

    def __str__(self):
        return f"Node line: {self.label}\nLength: {self.length}\n"


if __name__ == '__main__':
    linea1 = Line('A', 15.0)
    print(linea1)
