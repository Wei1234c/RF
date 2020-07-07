from array import array



def _value_key(dictionary):
    return {v: k for k, v in dictionary.items()}



class RF1101_232:
    BASE_FREQUENCY_MHz = 433.999
    CHANNEL_SPACING_KHz = 199.951
    UART_BAUDS = {4800: 1, 9600: 2, 19200: 3}
    UART_BAUDS_value_key = _value_key(UART_BAUDS)
    BAUDS = {100: 100}
    POWERS_dBm = {0: 0, 5: 5, 7: 7, 10: 10}
    POWERS_dBm_value_key = _value_key(POWERS_dBm)
    BUFFER_SIZE = 30


    def __init__(self, bus, baud_rate = 9600):
        self._bus = bus
        self.set_uart_baud_rate(baud_rate)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self._bus.close()


    def __del__(self):
        self._bus.close()


    def _validate_command(self):
        result = self._bus.read(1)[0]
        assert result == 0xAA, 'Command failed.'


    def _command_bytes(self, command):
        command_reversed = (command << 4 & 0xf0) | (command >> 4 & 0x0f)
        return array('B', [command, command_reversed])


    def _send_command(self, command, value_bytes):
        command = self._command_bytes(command)
        command.extend(value_bytes)
        self._bus.write(command)
        self._validate_command()


    def set_uart_baud_rate(self, baud_rate = 9600):
        valids = self.UART_BAUDS.keys()
        assert baud_rate in valids, 'valid baud_rate: {}'.format(valids)

        self._send_command(0xA3, [self.UART_BAUDS[baud_rate]])


    def set_speed(self, Kbps = 100):  # not available yet.
        valids = self.BAUDS.keys()
        assert Kbps in valids, 'valid Kbps: {}'.format(valids)

        self._send_command(0xA5, [self.BAUDS[Kbps]])


    def set_channel(self, channel = 0x00):
        self._send_command(0xA7, [channel])


    def set_id(self, id = 0x00):
        self._send_command(0xA9, [id >> 8 & 0xff, id & 0xff])


    def set_power(self, power_dBm = 10):
        valids = self.POWERS_dBm.keys()
        assert power_dBm in valids, 'valid power_dBm: {}'.format(valids)

        self._send_command(0xAB, [self.POWERS_dBm[power_dBm]])


    def send(self, bytes_array):
        n_sent = 0
        n_total = len(bytes_array)

        while n_sent < n_total:
            n_to_send = min(self.BUFFER_SIZE, n_total - n_sent)
            self._bus.write(bytes_array[n_sent: n_sent + n_to_send])
            n_sent += n_to_send


    def receive(self, n_bytes):
        self._bus.read(n_bytes)


    @property
    def status(self):
        self._bus.write(self._command_bytes(0xA6))
        return array('B', self._bus.read(7))


    @property
    def channel(self):
        return self.status[1]


    @property
    def frequency(self):
        return self.BASE_FREQUENCY_MHz * 1e6 + self.channel * self.CHANNEL_SPACING_KHz * 1e3


    @property
    def speed(self):
        return self.status[2]


    @property
    def uart_baud_rate(self):
        return self.UART_BAUDS_value_key[self.status[3]]


    @property
    def power_dBm(self):
        return self.POWERS_dBm_value_key[self.status[4]]


    @property
    def id(self):
        value = self.status[5:]
        return value[0] << 8 | value[1]
