class Line:

    def __init__(self, label, length):
        self._length = length
        self._label = label
        self._successive = {}  # empty dictionary[type Node]

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, newlength):
        self._length = newlength

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, newlabel):
        self._label = newlabel

    def latency_generation(self):
        c = 3 * (10 ** 9)
        latency = self.lenght / (c * 2 / 3)
        return latency

    def noise_genaration(self, signal_power):
        return signal_power * self.length * (10 ** -9)

    """
    Updating signal_information obj:
        - updating latency
        - updating noise_power
         
    """

    def propagate(self, signal_information):
        signal_information.add_latency(self.latency_generation())
        signal_information.add_noise_power(self.noise_genaration(signal_information.noise_power))

        """ 
        manca la parte
        and call the successive element propagate
        method, accordingly to the specified path
        """
