# main.py
# Created by: VIEC Team (Team 6)
# ECE 4336 Senior Design

#libraries
from time import sleep
from time import time

from gpiozero import Button

import RPi.GPIO as GPIO

import drivers

from JSON_Input import input_submodule_objects
from JSON_Input import output_submodule_objects

#from JSON_INPUT_NO_CONNECTION import output_submodule_objects
#from JSON_INPUT_NO_CONNECTION import input_submodule_objects

from RFID_RW_Library.RFID_213_rw import read_block6

from module_interface import configure_module
from module_interface import read_module
from module_interface import convert_data
from module_interface import print_data
from module_interface import configure_output
from module_interface import organize_solution
from module_interface import GPIO_init
from server_interface import Import_JSON_From_Server

def main():
    #button = Button(pin #)


    #Intro for VIEC Controller
    display = drivers.Lcd()
    print ("VIEC Controller")
    display.lcd_display_string("VIEC Controller", 1)
    print("By: ECE 4336 Team 6")
    display.lcd_display_string("By: ECE 4336 Team 6", 2)
    sleep(2)
    
    while 1:
        start = time()
        RFID_Value = "EMPTY"
        
        # Identify module by scanning RFID
        while (RFID_Value == "EMPTY"):
            RFID_Value = read_block6()
            now = time()
            print(now)
            if (0): #Get rid of when barcode is implemented
                #nothing
            if ((now - start) > 20 and "EMPTY"):
                #Barcode function
                start_barcode = time()
                display.lcd_clear()
                display.lcd_display_string("Press button", 1)
                display.lcd_display_string("to use barcode", 2)
                while (time() - start_barcode > 3):
                    if (1): #Replace with barGPIO
                        # Barcode function
                        display.lcd_clear()
                        display.lcd_display_string("Activated", 1)
                        display.lcd_display_string("Barcode Scanner", 2)
                        sleep(1)
                continue
            elif ((now - start) > 5 and "EMPTY"):
                display.lcd_clear()
                display.lcd_display_string("ERROR: 0002", 1)
                display.lcd_display_string("RFID NOT FOUND", 2)
                break
            if (RFID_Value == "EMPTY"):
                continue
            RFID_Value = RFID_Value[0] + RFID_Value[1] + RFID_Value[2] + RFID_Value[3]
        
        if (RFID_Value == "EMPTY"):
            continue
        
        print(RFID_Value)  

        # Download Respective .JSON File
        
        while 1: #Testing Server Connection
            input_objects, output_objects = Import_JSON_From_Server(RFID_Value)
            
            if (input_objects == -1 and output_objects == -1):
                display.lcd_clear()
                display.lcd_display_string("ERROR: 0003", 1)
                display.lcd_display_string("SERVER NOT FOUND", 2)
                sleep(4)
            else:
                break
        
        input_objects = input_submodule_objects(input_objects)#submodule_objects
        if (len(input_objects) == 0):
            continue
        output_objects = output_submodule_objects(output_objects)#output_objects

        # Configure module (turn on sensor)
        read_index = configure_module(input_objects)
        if (read_index == -1): #Returns -1 when input is not connected
            display.lcd_clear()
            display.lcd_display_string("ERROR: 0001", 1)
            display.lcd_display_string("DEFECTIVE I/O", 2)
            sleep(4)
            
            continue

        configure_output(input_objects, output_objects)
        
        GPIO.cleanup()
        GPIO_init(output_objects)
        sleep(1)

        display_index = 0 #initializing the display to show the first measured value
        while 1: #for now
            # Read data from input module
            submodule_objects = read_module(input_objects, read_index)
            if (submodule_objects == -1):
                break

            # Convert data from digital to units
            submodule_objects = convert_data(input_objects, read_index)

            # Print data
            display_index = print_data(input_objects, read_index, display, button, display_index)

            # Control output module (Uncomment when testing output)
            organize_solution(submodule_objects, output_objects)

            sleep(2)


if __name__ == "__main__":
    main()
