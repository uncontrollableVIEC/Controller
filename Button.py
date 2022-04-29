# Button.py
# Created by: VIEC Team

from time import time
from time import sleep
from reset_config import reset_VIEC_Controller
import RPi.GPIO as GPIO
import Constants
import drivers

def button_pressed(callback):
    global time_interval
    initial_time = time()
    while not GPIO.input(23):
        if (GPIO.input(23)):
            break
        Constants.time_interval = time() - initial_time
        if (Constants.time_interval > 5):
            #RESET
            display = drivers.Lcd()
            display.lcd_clear()
            display.lcd_display_string("Controller will", 1)
            display.lcd_display_string("RESET", 2)
            sleep(3)
            display.lcd_clear()
            GPIO.cleanup()
            
            reset_VIEC_Controller()

    print(Constants.time_interval)
