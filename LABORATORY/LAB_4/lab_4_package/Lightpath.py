from LAB_4.lab_4_package.Signal_information import Signal_information


class Lightpath(Signal_information):

    def __init__(self, signal_power: float, path: list[str], channel_slot: int):
        super().__init__(signal_power, path)
        self._channel_slot = channel_slot

    @property
    def channel_slot(self):
        return self._channel_slot

    @channel_slot.setter
    def channel_slot(self, new_channel_slot):
        self._channel_slot = new_channel_slot

    def __str__(self):
        return super().__str__() + f"Channel Slot: {self.channel_slot}\n"


if __name__ == '__main__':
    l1 = Lightpath(0.001, ['A', 'C'], 1)
    print(l1)
