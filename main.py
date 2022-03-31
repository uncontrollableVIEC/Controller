# main.py
# Created by: VIEC Team (Team 6)
# ECE 4336 Senior Design

#libraries
from time import sleep

import RPi.GPIO as GPIO

#from JSON_Input import input_submodule_objects
#from JSON_Input import output_submodule_objects

from JSON_INPUT_NO_CONNECTION import output_submodule_objects
from JSON_INPUT_NO_CONNECTION import input_submodule_objects

from RFID_RW_Library.RFID_213_rw import read_block6

from module_interface import configure_module
from module_interface import read_module
from module_interface import convert_data
from module_interface import print_data
from module_interface import configure_output
from module_interface import organize_solution
from module_interface import GPIO_init
from server_interface import Import_JSON_From_Server
import json

def main():
    #Intro for VIEC Controller
    print ("VIEC Controller")
    sleep(2)
    print("By: ECE 4336 Team 6")
    sleep(2)
    
    while 1:
        # Identify module by scanning RFID
        RFID_Value = read_block6()
        RFID_Value = RFID_Value[0] + RFID_Value[1] + RFID_Value[2] + RFID_Value[3]
        print(RFID_Value)

        # Download Respective .JSON File

        #input_objects, output_objects = Import_JSON_From_Server(RFID_value)
        input_objects = input_submodule_objects(RFID_Value)#submodule_objects
        if (len(input_objects) == 0):
            continue
        output_objects = output_submodule_objects(RFID_Value)#output_objects

        # Configure module (turn on sensor)
        read_index = configure_module(input_objects)
        if (read_index == -1): #Returns -1 when input is not connected
            continue

        configure_output(input_objects, output_objects)
        
        GPIO.cleanup()
        GPIO_init(output_objects)
        sleep(1)

        while 1: #for now
            # Read data from input module
            submodule_objects = read_module(input_objects, read_index)
            if (submodule_objects == -1):
                break

            # Convert data from digital to units
            submodule_objects = convert_data(input_objects, read_index)

            # Print data
            print_data(input_objects, read_index)

            # Control output module (Uncomment when testing output)
            organize_solution(submodule_objects, output_objects)

            sleep(2)


if __name__ == "__main__":
    main()
