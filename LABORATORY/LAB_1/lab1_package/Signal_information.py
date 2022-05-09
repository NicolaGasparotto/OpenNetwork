
class Signal_information:

    def __init__(self, signal_power, path):
        self._signal_power = signal_power
        self._path = path
        self._noise_power = 0
        self._latency = 0

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
    def path(self, new_path):
        self.path = new_path

    @noise_power.setter
    def noise_power(self, new_noise_power):
        self._noise_power = new_noise_power

    @latency.setter
    def latency(self, new_latency):
        self._latency = new_latency

    def add_latency(self, more_latency):
        self.latency += more_latency

    def add_noise_power(self, more_noise_power):
        self.noise_power += more_noise_power

    """
    this method will update the path once a node is crossed
    --> the crossed node will be removed from the path_list
    """
    def update_path(self):
        del self._path[0]

