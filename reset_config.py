# reset_config.py
# Created by: VIEC Team

import os, sys
from time import sleep

def reset_Controller(display):
    display.lcd_clear()
    display.lcd_display_string("Controller will", 1)
    display.lcd_display_string("RESET", 2)
    sleep(3)
    os.system("sudo shutdown -r now")
    sys.exit()