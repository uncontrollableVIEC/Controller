# Button.py
# Created by: VIEC Team

from time import time
from reset_config import reset_Controller

def button_pressed(GPIO, display, interval):
    initial_time = time()
    while !GPIO.input(11):
        if (GPIO.input(11)):
            break

    time_interval = time() - initial_time

    if (time_interval > 5):
        #RESET
        reset_Controller(display)

    interval[0] = time_interval