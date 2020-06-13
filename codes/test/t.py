from bridges.ftdi.controllers.spi import SpiController
from rf.devices.cc1101.cc1101 import CC1101


spidev = SpiController()
spi = spidev.SpiDev()

cc = CC1101(spi = spi)

cc.reset()
cc.selfTest()

print(cc.getRSSI())
print('version', cc._readSingleByte(0xF1))

# for i in range(0x3d + 1):
#     print(ticc1101._readSingleByte(i))
