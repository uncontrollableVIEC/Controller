# main.py
# Created by: VIEC Team (Team 6)
# ECE 4336 Senior Design

#libraries
from JSON_Input import import_submodule_objects
from module_interface import configure_module
from module_interface import read_module
from module_interface import convert_data
from module_interface import print_data

def main():
    # Identify module by scanning RFID

    # Download Respective .JSON File

    # Import I2C Addresses
    submodule_objects = import_submodule_objects()

    # Configure module (turn on sensor)
    read_index = configure_module(submodule_objects)

    while 1: #for now
        # Read data from input module
        submodule_objects = read_module(submodule_objects, read_index)

        # Convert data from digital to units
        submodule_objects = convert_data(submodule_objects, read_index)

        # Print data
        print_data(submodule_objects, read_index)

    # Control output module

if __name__ == "__main__":
    main()