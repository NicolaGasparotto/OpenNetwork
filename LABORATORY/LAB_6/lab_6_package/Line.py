from LAB_7.lab_7_package.Node import *


class Line(object):

    # i.e:
    # line_label = AC, length = 12.5
    def __init__(self, label: str, length: float, channels_number: int):
        self._length = length
        self._label = label
        self._successive = {}  # dict_ node
        self._state = [1]*channels_number  # 1 means 'free', 0 means 'occupied'

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

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
        # print(type(signal_power), signal_power)
        return signal_power * self.length * (10 ** -9)

    def probe(self, signal_i: Signal_information):
        signal_i.add_latency(self.latency_generation())
        signal_i.add_noise_power(self.noise_generation(signal_i.signal_power))
        # it will recall the method probe for the next node
        signal_i = self.successive[signal_i.path[0]].probe(signal_i)
        return signal_i

    def update_state(self):
        # update the state of the channel in the list of available channels
        # the first free channel found will be changed and the function will stop
        # there is no control for the condition when all the channels are occupied
        for i, ch in enumerate(self.state):
            if ch:
                self.state[i] = 0
                return

    def __str__(self):
        return f"Node line: {self.label}\nLength: {self.length}\nState (1->Free, 0->Occupied): {self.state}\n"


if __name__ == '__main__':
    line = Line('AC', 12.3, 5)
    print(line)
