from array import array

from rf.devices.cc1101 import USB1101


with USB1101(port = 'COM3', baud_rate = 9600) as cc:
    cc.set_uart_baud_rate(baud_rate = 9600)
    # cc.set_speed( bps = 100)
    cc.set_channel(channel = 0)
    cc.set_id(id = 0x5502)
    cc.set_power(power_dBm = 10)

    print('channel', cc.channel)
    print('frequency', cc.frequency)
    print('speed', cc.speed)
    print('uart_baud_rate', cc.uart_baud_rate)
    print('power_dBm', cc.power_dBm)
    print('id', cc.id)

    cc.send(array('B', range(45)))

    for c in range(255):
        print(c)
        cc.send(array('B', range(45)))
        # try:
        #     # cc.send(array('B', range(45)))
        #     # cc.set_channel(c)
        #     cc.send(array('B', range(45)))
        # except:
        #     print(c)
