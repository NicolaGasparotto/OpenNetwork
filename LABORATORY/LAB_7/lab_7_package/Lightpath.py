from LAB_7.lab_7_package.Signal_information import Signal_information

from constants import CONSTANTS


class Lightpath(Signal_information):

    def __init__(self, signal_power: float, path: list[str], channel_slot=None):
        super().__init__(signal_power, path)
        self._channel_slot = channel_slot
        self._Rs = CONSTANTS['Rs']
        self._df = CONSTANTS['df']

    @property
    def Rs(self):
        return self._Rs

    @Rs.setter
    def Rs(self, new_Rs):
        self._Rs = new_Rs

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, new_df):
        self._df = new_df

    @property
    def channel_slot(self):
        return self._channel_slot

    @channel_slot.setter
    def channel_slot(self, new_channel_slot):
        self._channel_slot = new_channel_slot

    def __str__(self):
        return super().__str__() + f"Channel Slot: {self.channel_slot}\n"

