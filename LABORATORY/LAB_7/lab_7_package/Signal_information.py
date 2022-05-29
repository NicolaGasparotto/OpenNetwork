
class Signal_information(object):

    def __init__(self, signal_power: float, path: list[str]):
        self._signal_power = signal_power
        self._path = path
        self._noise_power = 0
        self._latency = 0
    
    @property
    def signal_power(self):
        return self._signal_power
    
    @signal_power.setter
    def signal_power(self, new_signal_power):
        self._signal_power = new_signal_power

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

    def update_path(self):
        del self._path[0]  # it's a list of char representing the path of the signal

    def __str__(self):
        return f"SIGNAL:\nPath: {self.path}\nSignal Power: {self.signal_power}\nNoise Power: {self.noise_power}\nLatency: {self.latency}\n"
