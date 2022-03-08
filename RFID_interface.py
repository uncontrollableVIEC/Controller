# RFID.py
# Created by: VIEC Team (Team 6)
import smbus
bus = smbus.SMBus(1)
from time import sleep

def Read_RFID():
    block_6 = "0x03"  # Example

    return block_6  # In format 0xXX
