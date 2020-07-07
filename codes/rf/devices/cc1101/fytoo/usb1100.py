import serial

from .rf1100_232 import RF1101_232



class USB1101(RF1101_232):

    def __init__(self, port, baud_rate = 9600):
        bus = serial.Serial(port, baudrate = baud_rate, timeout = 1)
        super().__init__(bus, baud_rate)
