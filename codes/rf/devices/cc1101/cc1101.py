from .pycc1101 import TICC1101



class CC1101(TICC1101):

    def __init__(self, spi, debug = True):
        self._spi = spi
        self.debug = debug
