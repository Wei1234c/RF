from bridges.ftdi.controllers.spi import SpiController
from rf.devices.cc1101.cc1101 import CC1101


spidev = SpiController()
spi = spidev.SpiDev()

cc = CC1101(spi = spi)
cc.setCarrierFrequency(freq = 433)

cc.reset()
cc.selfTest()

print(cc.getRSSI())
print('version', cc._readSingleByte(0xF1))



def send():
    from struct import pack
    import time

    cc.reset()
    cc.selfTest()
    cc.setDefaultValues()
    cc.setFilteringAddress(0x0A)
    # cc.setPacketMode("PKT_LEN_VARIABLE")
    cc.setPacketMode("PKT_LEN_FIXED")
    cc.configureAddressFiltering("ENABLED_NO_BROADCAST")

    count = 0

    while True:
        data = pack('<I', count)
        # toSend = [x for x in data]
        toSend = data
        cc.sendData(toSend)
        count += 1
        time.sleep(1)



send()
