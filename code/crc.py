#!/usr/bin/env python
# -*- coding: utf-8 -*-

def calc_crc(string):
    data = bytearray.fromhex(string)
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return hex(((crc & 0xff) << 8) + (crc >> 8))

crc = calc_crc('010414000041A000004120000042C8000040E0000041F0BC73').encode('unicode_escape')[2:].decode('utf-8').upper()
print(crc)

