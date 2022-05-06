
class Signal_information:

    def __int__(self, signal_power, path):
        self._signal_power = signal_power
        self._path = path
        self._noise_power = 0
        self._latency = 0

    """
        path is string list that contains the path of the signal 
    """

    @property
    def path(self):
        return self._path

    @property
    def latency(self):
        return self._latency

    @property
    def noise_power(self):
        return self._noise_power

    @path.setter
    def path(self, newPath):
        self.path = newPath

    @noise_power.setter
    def noise_power(self, newNoise_power):
        self._noise_power = newNoise_power

    """latency it's the total latency due to the passage of the signal
    through all of the elements in the network"""
    @latency.setter
    def latency(self, newLatency):
        self._latency = newLatency

    def add_latency(self, moreLatency):
        self._latency += moreLatency

    def add_noise_power(self, moreNoise_power):
        self._noise_power += moreNoise_power

    """this method will update the path once a node is crossed"""
    def updatePath(self):
        self._path = self.path()

