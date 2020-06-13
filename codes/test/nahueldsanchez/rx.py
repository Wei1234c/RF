#!/usr/bin/python3
from bridges.ftdi.controllers.spi import SpiController
from rf.devices.cc1101.cc1101 import CC1101


spidev = SpiController()
spi = spidev.SpiDev()

cc = CC1101(spi = spi)

from struct import pack
import binascii
import time


ticc1101 = CC1101(spi)
ticc1101.reset()
ticc1101.selfTest()
ticc1101.setDefaultValues()
ticc1101.setFilteringAddress(0x0A)
# ticc1101.setPacketMode("PKT_LEN_VARIABLE")
ticc1101.setPacketMode("PKT_LEN_FIXED")
ticc1101.configureAddressFiltering("ENABLED_NO_BROADCAST")
ticc1101._setRXState()

while True:
    ticc1101._setRXState()
    ticc1101.recvData()
