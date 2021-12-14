import _bleio
import adafruit_ble
import board
import digitalio
import binascii
import math

from adafruit_ble import BLERadio
from adafruit_ble.advertising import *
from _bleio import adapter
from math import floor
# CircuitPython packages used.

# specifically written for the Adafruit nRF52840 Bluefruit Feather 
# 0x01 => flags
# 0x02 => incomplete list of 16-bit UUIDs
# 0x03 => complete list of 16-bit UUIDs
# 0x04 => incomplete list of 32-bit UUIDs
# 0x05 => complete list of 32-bit UUIDs
# 0x06 => incomplete list of 128-bit UUIDs
# 0x07 => complete list of 128-bit UUIDs
# 0x08 => shortened local name
# 0x09 => complete local name
# 0x0A => Tx power level of packet (1 byte) (-127 to +127 dBm)
# 0xFF => manufacturer specific payload

class AD:
    # make your own Advertising Data packet.
    def __init__(self, length, dtype, payload, endian='little'):
        """
        length: The length (in base 16) of the AD packet including the type byte.
        dtype: A 1-byte string representing one the datatype of the payload as documented in the Bluetooth Generic Access Profile (GAP)
        payload: The actual payload. The length of this should be equal to (length - 1).
        endian: Endianness of the datatype. Specify if 'big' or 'little'. Default 'little'.

        All of these should be in String format. For example, if your dtype is a flag, which would be 0x01, dtype='01'. 
        Similarly for others too.
        """
        self.length = bytes(length, 'utf-8')
        self.dtype = bytes(dtype, 'utf-8')
        self.payload = bytes(payload, 'utf-8') # convert all these to byte format

        self.l = int(self.length, 16) # integer length of (payload + dtype) in bytes
        if endian not in ['big', 'litle']:
            self.endian = 'little'
        else:
            self.endian = endian

    def parse(self):
        p_len = binascii.unhexlify(self.length)
        p_dtype = binascii.unhexlify(self.dtype)
        p_pload = binascii.unhexlify(self.payload)
        return p_len, p_dtype, p_pload

    def join(self):
        l, dt, pl = self.parse() # in pure hex byte representation
        # convert from little to big endian if needed.
        if self.endian != 'little':
            pl = b''.join([pl[i: i+1] for i in range(len(pl)-1, -1, -1)])

        if len(pl) > (self.l - 1):
            pl = pl[:self.l - 1]
        if len(pl) < (self.l - 1) and self.endian == 'little':
            pl = '\x00' * (self.l - 1 - len(pl)) + pl
        if len(pl) < (self.l - 1) and self.endian == 'big':
            pl = pl + '\x00' * (self.l - 1 - len(pl))
        
        return (l + dt + pl)
    
    def get_AD(self):
        return self.join()

def Flag(flag='0x06'):
    """
    Get the AD for the Flag.
    Default: 0x06
    """
    l = '02'
    dt = '01'
    f = flag.split('0x')[1]
    return AD(l, dt, f, 'little').join()

def ShortName(ShortName):
    """
    Get AD for the short name of device.
    """
    l = binascii.hexlify((len(ShortName)+1).to_bytes(1, 'little')).decode('utf-8') # converts the length to a hex representation in a byte in String format
    pl = ''
    for i in to_hex(bytes(ShortName, 'utf-8')).split(' '):
        pl += i
    return AD(l, '08', pl, 'little').join()

def CompleteName(fullName):
    """
    Get AD for the complete name of the device.
    """
    l = binascii.hexlify((len(fullName)+1).to_bytes(1, 'little')).decode('utf-8') # converts the length to a hex representation in a byte in String format
    pl = ''
    for i in to_hex(bytes(fullName, 'utf-8')).split(' '):
        pl += i
    return AD(l, '09', pl, 'little').join()

def UUID_16(uuid, complete=True):
    """
    Get AD packet for in/complete list of 16-bit UUIDs.
    `uuid` should be a string representing the hex, like '0x7e2f' => '7e2f'.
    stored in big endian format.
    """
    l = '03'
    dt = '03' if complete else '02'
    pl = uuid
    return AD(l, dt, pl, 'big').join()

def UUID_128(uuid, complete=True):
    """
    Get AD packet for in/complete list of 128-bit UUIDs.
    `uuid` should be a string representing the hex, like '07f75536-cf60-4289-bb1c-6f50f8daf622'.
    stored in big endian format.
    """
    l = '11'
    dt = '07' if complete else '06'
    pl = ''.join(uuid.split('-'))
    return AD(l, dt, pl, 'big').join()
