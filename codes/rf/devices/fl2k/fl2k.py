# https://github.com/peterbmarks/fl2k/blob/master/libosmo-fl2k.c

import usb
import usb.backend.libusb1 as libusb1


_fl2k_device = None



def _get_fl2k(idVendor = 0x1d5c, idProduct = 0x2000) -> usb.core.Device:
    global _fl2k_device

    _fl2k_device = usb.core.find(idVendor = idVendor, idProduct = idProduct, backend = libusb1.get_backend())

    if _fl2k_device is not None:
        _fl2k_device.set_configuration()

    return _fl2k_device



def release_fl2k():
    global _fl2k_device
    _fl2k_device = None



class FL2K:

    def __init__(self, idVendor = 0x1d5c, idProduct = 0x2000):
        self._bus = self.dev = _get_fl2k(idVendor, idProduct)


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()


    def __del__(self):
        self._bus = self.dev = None


    def _read_reg(self, reg_address):
        bytes_array = self.dev.ctrl_transfer(bmRequestType = 0xC0, bRequest = 0x40,
                                             wValue = 0, wIndex = reg_address, data_or_wLength = 4)
        return int.from_bytes(bytes_array, byteorder = 'little', signed = False)


    def _write_reg(self, reg_address, value):
        bytes_array = value.to_bytes(4, byteorder = 'little', signed = False)
        return self.dev.ctrl_transfer(bmRequestType = 0x40, bRequest = 0x41,
                                      wValue = 0, wIndex = reg_address, data_or_wLength = bytes_array)
