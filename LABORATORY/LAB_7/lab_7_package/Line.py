import math

from scipy.constants import Planck

from LAB_7.lab_7_package.Lightpath import Lightpath
from LAB_7.lab_7_package.Node import *

from constants import *


class Line(object):

    # i.e:
    # line_label = AC, length = 12.5
    def __init__(self, label: str, length: float, channels_number: int):
        self._length = length
        self._label = label
        self._successive = {}  # dict_ node
        self._n_channel = channels_number
        self._state = [1] * self.n_channel  # 1 means 'free', 0 means 'occupied'
        self._n_amplifier = math.ceil(
            self.length / CONSTANTS['amplifier_every_km']) + 1  # at the end it's necessary another one

        # constants
        self._gain = CONSTANTS['gain']
        self._noise_figure = CONSTANTS['noise_figure']
        self._df = CONSTANTS['df']
        self._Rs = CONSTANTS['Rs']
        self._gamma = CONSTANTS['gamma']
        self._abs_beta2 = CONSTANTS['abs_beta2']
        self._alfa_dB = CONSTANTS['alfa_dB']

    @property
    def n_channel(self):
        return self._n_channel

    @n_channel.setter
    def n_channel(self, new_n_channel):
        self._n_channel = new_n_channel

    @property
    def alfa_dB(self):
        return self._alfa_dB

    @alfa_dB.setter
    def alfa_dB(self, new_alfa_dB):
        self._alfa_dB = new_alfa_dB

    @property
    def abs_beta2(self):
        return self._abs_beta2

    @abs_beta2.setter
    def abs_beta2(self, new_abs_beta2):
        self._abs_beta2 = new_abs_beta2

    @property
    def gamma(self):
        return self._gamma

    @gamma.setter
    def gamma(self, new_gamma):
        self._gamma = new_gamma

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
    def noise_figure(self):
        return self._noise_figure

    @noise_figure.setter
    def noise_figure(self, new_noise_figure):
        self._noise_figure = new_noise_figure

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, new_gain):
        self._gain = new_gain

    @property
    def n_amplifier(self):
        return self._n_amplifier

    @n_amplifier.setter
    def n_amplifier(self, new_n_amplifier):
        self._n_amplifier = new_n_amplifier

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

    def ase_generation(self):
        return (self.n_amplifier - 2) * (Planck * CONSTANTS['frequency'] * CONSTANTS['Bn'] *
                                         from_dB_to_linear(self.noise_figure) * (from_dB_to_linear(self.gain) - 1))

    def nli_generation(self, lightpath: Lightpath):
        # signal_power^3 * eta_nli * Nspan * noise_bandwidth
        #                        >>> N span--> numero fibre lungo la linea --> NUMERO AMPLFIEIR -1
        return lightpath.signal_power ** 3 * self.eta_nli(lightpath.df,
                                                          lightpath.Rs) * (self.n_amplifier - 1) * CONSTANTS['Bn']

    def eta_nli(self, df, Rs):
        # 16/27pi * log(pi^2/2 * beta2*Rs^2/alfa * N^(2*Rf/df) ) * gamma^2/4alfa*beta2 * 1/Rs**3
        a = self.alfa_dB / (10 * math.log10(math.e))
        e_nli = 16 / (27 * math.pi) * math.log(
            math.pi ** 2 * self.abs_beta2 * Rs ** 2 * self.n_channel ** (2 * Rs / df) / (2 * a)) * self.gamma ** 2 / (
                        4 * a * self.abs_beta2 * Rs ** 3)

        return e_nli

    def optimized_launch_power(self, eta):
        # (NF * f * h * G/2*eta) ^ 1/3
        return ((from_dB_to_linear(self.noise_figure)*from_dB_to_linear(self.gain)*Planck*CONSTANTS['frequency']) / (2 * eta)) ** (1 / 3)

    def latency_generation(self):
        c = 3 * (10 ** 9)  # light speed
        return float(self.length / (c * 2 / 3))  # this is the latency calculated

    def noise_generation(self, lightpath: Lightpath):
        return self.ase_generation() + self.nli_generation(lightpath)

    def probe(self, lightpath: Lightpath):
        # setting the s_p for the signal
        lightpath.signal_power = self.optimized_launch_power(self.eta_nli(lightpath.df, lightpath.Rs))
        lightpath.add_latency(self.latency_generation())
        lightpath.add_noise_power(self.noise_generation(lightpath))
        # it will recall the method probe for the next node
        lightpath = self.successive[lightpath.path[0]].probe(lightpath)
        return lightpath

    def update_state(self, channel: int):
        # update the state of the channel in the list of available channels
        # the first free channel found will be changed and the function will stop
        # there is no control for the condition when all the channels are occupied
        self._state[channel] = 0

    def __str__(self):
        return f"Node line: {self.label}\nLength: {self.length}\nState (1->Free, 0->Occupied): {self.state}\n"


if __name__ == '__main__':
    line = Line('AC', 353553.39059327374, 10)
    print('eta_nli', line.eta_nli(50e9, 32e9))
    print('ase_gen ', line.ase_generation())
    print('olp ', line.optimized_launch_power(line.eta_nli(50e9, 32e9)))
