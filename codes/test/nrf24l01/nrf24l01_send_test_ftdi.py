import time

from bridges.ftdi.controllers.spi import SpiController
from rf.devices.nrf24l01.nrf24l01 import NRF24l01


spidev = SpiController()
spi = spidev.SpiDev()

radio = NRF24l01(spi = spi)

# ========================================
pipes = [[0xe7, 0xe7, 0xe7, 0xe7, 0xe7], [0xc2, 0xc2, 0xc2, 0xc2, 0xc2]]

radio.setRetries(15, 15)
radio.setPayloadSize(8)
radio.setChannel(0x60)

radio.setDataRate(NRF24l01.BR_250KBPS)
radio.setPALevel(NRF24l01.PA_MAX)

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[0])

radio.startListening()
radio.stopListening()

radio.printDetails()

while True:
    radio.write("PING")
    time.sleep(1)
