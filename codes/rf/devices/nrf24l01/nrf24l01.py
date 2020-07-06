# origin: https://github.com/jpbarraca/pynrf24
# datasheet: https://datasheet.octopart.com/NRF24L01-Nordic-Semiconductor-datasheet-10541936.pdf

from rf.devices.nrf24l01.nrf24 import NRF24, time



class NRF24l01(NRF24):

    def __init__(self, spi, ce_pin = None, irq_pin = None):
        super().__init__()
        self.spidev = spi
        self.begin(ce_pin, irq_pin)


    def begin(self, ce_pin, irq_pin):
        # Initialize SPI bus
        # self.spidev.bits_per_word = 8

        try:
            self.spidev.max_speed_hz = 10000000  # Maximum supported by NRF24L01+
        except IOError:
            pass  # Hardware does not support this speed

        # self.spidev.cshigh = False
        # self.spidev.mode = 0
        # self.spidev.loop = False
        self.spidev.lsbfirst = False
        # self.spidev.threewire = False

        self.ce_pin = ce_pin
        self.irq_pin = irq_pin

        time.sleep(5 / 1000000.0)

        # Reset radio configuration
        self.reset()

        # Set 1500uS (minimum for 32B payload in ESB@250KBPS) timeouts, to make testing a little easier
        # WARNING: If this is ever lowered, either 250KBS mode with AA is broken or maximum packet
        # sizes must never be used. See documentation for a more complete explanation.
        self.setRetries(int('0101', 2), 15)

        # Restore our default PA level
        self.setPALevel(NRF24.PA_MAX)

        # Determine if this is a p or non-p RF24 module and then
        # reset our data rate back to default value. This works
        # because a non-P variant won't allow the data rate to
        # be set to 250Kbps.
        if self.setDataRate(NRF24.BR_250KBPS):
            self.p_variant = True

        # Then set the data rate to the slowest (and most reliable) speed supported by all
        # hardware.
        self.setDataRate(NRF24.BR_1MBPS)

        # Initialize CRC and request 2-byte (16bit) CRC
        self.setCRCLength(NRF24.CRC_16)

        # Disable dynamic payloads, to match dynamic_payloads_enabled setting
        self.write_register(NRF24.DYNPD, 0)

        # Reset current status
        # Notice reset and flush is the last thing we do
        self.write_register(NRF24.STATUS, NRF24.RX_DR | NRF24.TX_DS | NRF24.MAX_RT)

        # Set up default configuration.  Callers can always change it later.
        # This channel should be universally safe and not bleed over into adjacent
        # spectrum.
        self.setChannel(self.channel)

        self.setRetries(15, 15)

        # Flush buffers
        self.flush_rx()
        self.flush_tx()
        self.clear_irq_flags()


    def ce(self, level, pulse = 0):
        if self.ce_pin is not None:
            self.ce_pin.value(level)

            if pulse > 0:
                time.sleep(pulse)
                self.ce_pin.value(1 - level)


    def irqWait(self, timeout = 30000):
        if self.irq_pin is not None:
            if self.irq_pin.value() == 0:  # Pin is already down. Packet is waiting?
                return True

            timeout /= 1000
            start = time.time()
            while self.irq_pin.value() == 1:
                if time.time() - start > timeout:
                    raise RuntimeError("Timeout.")
