from LAB_7.lab_7_package.Signal_information import Signal_information


class Lightpath(Signal_information):

    def __init__(self, signal_power: float, path: list[str], channel: int):
        super().__init__(signal_power, path)
        self._channel = channel

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, new_channel):
        self._channel = new_channel

    def __str__(self):
        return super().__str__() + f"Channel Slot: {self.channel}\n"


if __name__ == '__main__':
    l1 = Lightpath(0.001, ['A', 'C'], 1)
    print(l1)
