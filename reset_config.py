# reset_config.py
# Created by: VIEC Team

import os, sys
from time import sleep
import drivers

def reset_VIEC_Controller():
    os.system("sudo reboot")
    sys.exit()