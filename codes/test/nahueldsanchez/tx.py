#!/usr/bin/python3

import binascii
import time
from struct import pack

from bridges.ftdi.controllers.spi import SpiController
from rf.devices.cc1101.cc1101 import CC1101


spidev = SpiController()
spi = spidev.SpiDev()

ticc1101 = CC1101(spi = spi)
ticc1101.reset()
ticc1101.selfTest()
ticc1101.setDefaultValues()
ticc1101.setFilteringAddress(0x0A)
# ticc1101.setPacketMode("PKT_LEN_VARIABLE")
ticc1101.setPacketMode("PKT_LEN_FIXED")
ticc1101.configureAddressFiltering("ENABLED_NO_BROADCAST")

count = 0

while True:
    data = pack('<I', count)
    # toSend = [int(binascii.hexlify(x), 16) for x in  data]
    toSend = bytearray([0] * count)
    ticc1101.sendData(toSend)
    count += 1
    time.sleep(1)
