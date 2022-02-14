from rf.devices.fl2k import FL2K


fl2k = FL2K(0x1D5C, 0x2000)

value = fl2k._read_reg(reg_address = 0x8020)
print(value)
print(fl2k._write_reg(reg_address = 0x8020, value = value + 100))
print(fl2k._read_reg(reg_address = 0x8020))
