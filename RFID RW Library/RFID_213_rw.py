"""
This is a library for reading/writing to Block 6 of an RFID 213 tag
213 Tags have 180 bytes of memory spread across 45 pages of 4 bytes
"""
import RPi.GPIO as GPIO
import pn532.pn532 as nfc
from pn532 import *


#pn532 = PN532_SPI(cs=4, reset=20, debug=False)
pn532 = PN532_I2C(debug=False, reset=20, req=16)
#pn532 = PN532_UART(debug=False, reset=20)

def read_block6():
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

    # Configure PN532 to communicate with NTAG215 cards
    pn532.SAM_configuration()

    print('Waiting for RFID/NFC card to read from!')
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        print('.', end="")
        # Try again if no card is available.
        if uid is not None:
            break
    print('Found card with UID:', [hex(i) for i in uid])

    # But let's just look at page 6
    print('Block 6: ', pn532.ntag2xx_read_block(6))
    return self.pn532.ntag2xx_read_block(6)
    GPIO.cleanup()

def write_block6(data):
#data is byte array of length 4
    assert data is not None and len(data) == 4, 'Data must be an array of 4 bytes!'

    # import RPi.GPIO as GPIO
    # import pn532.pn532 as nfc
    # from pn532 import *

    # pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    # pn532 = PN532_I2C(debug=False, reset=20, req=16)
    # pn532 = PN532_UART(debug=False, reset=20)

    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

    # Configure PN532 to communicate with NTAG215 cards
    pn532.SAM_configuration()

    # I need to define a function to read block 6 given a 4 byte array input
    # I can likely put this into 1 code

    print('Waiting for RFID/NFC card to write to!')
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        print('.', end="")
        # Try again if no card is available.
        if uid is not None:
            break
    print('Found card with UID:', [hex(i) for i in uid])

    # Set Block number = 6
    block_number = 6

    try:
        pn532.ntag2xx_write_block(block_number, data)
        # ntag2xx_write_block(self, block_number, data):
        # data is a byte array of length 4
        if pn532.ntag2xx_read_block(block_number) == data:
            # ntag2xx_read_block(self, block_number):
            print('write block %d successfully' % block_number)
    except nfc.PN532Error as e:
        print(e.errmsg)
    GPIO.cleanup()
# Now just def a function in main to read block 6 or define function in pn532


