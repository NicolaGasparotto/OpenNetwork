

class Connection(object):

    def __init__(self, input_node: str, output_node: str, signal_power: float):
        self._input_node = input_node
        self._output_node = output_node
        self._signal_power = signal_power
        self._latency = 0
        self._snr = 0

    @property
    def input_node(self):
        return self._input_node

    @input_node.setter
    def input_node(self, new_input_node):
        self._input_node = new_input_node

    @property
    def output_node(self):
        return self._output_node

    @output_node.setter
    def output_node(self, new_output_node):
        self._output_node = new_output_node

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, new_latency):
        self._latency = new_latency

    @property
    def signal_power(self):
        return self._signal_power

    @signal_power.setter
    def signal_power(self, new_signal_power):
        self._signal_power = new_signal_power

    @property
    def snr(self):
        return self._snr

    @snr.setter
    def snr(self, new_snr):
        self._snr = new_snr

    def __str__(self):
        return f"Connection\nInput Node:{self._input_node}\tOutput Node:{self._output_node}\nSignal Power: {self.signal_power}\n "
