# main.py
# Created by: VIEC Team (Team 6)
# ECE 4336 Senior Design

#libraries
<<<<<<< HEAD
from time import sleep 
=======
>>>>>>> c4862df5f80c5f81d13362150356a2c45c5124a8
from JSON_Input import input_submodule_objects
from JSON_Input import output_submodule_objects
from module_interface import configure_module
from module_interface import read_module
from module_interface import convert_data
from module_interface import print_data
<<<<<<< HEAD
from module_interface import configure_output
from module_interface import organize_solution
from module_interface import GPIO_init
from server_interface import Import_JSON_From_Server
import json
=======
from module_interface import top_output_module
from module_interface import config_output
from module_interface import output_solution
>>>>>>> c4862df5f80c5f81d13362150356a2c45c5124a8

def main():
    # Identify module by scanning RFID

    # Download Respective .JSON File
<<<<<<< HEAD
    RFID_value = "0000CCCC"
    submodule_objects, output_objects = Import_JSON_From_Server(RFID_value)
    input_objects = input_submodule_objects(submodule_objects)#submodule_objects
    #output_objects = output_submodule_objects(output_objects)#output_objects

    # Configure module (turn on sensor)
    read_index = configure_module(input_objects)
    
    #configure_output(input_objects, output_objects)
    
    # pi_pwm = GPIO_init(output_objects)
    sleep(1)

    while 1: #for now
        # Read data from input module
        submodule_objects = read_module(input_objects, read_index)

        # Convert data from digital to units
        submodule_objects = convert_data(input_objects, read_index)

        # Print data
        print_data(input_objects, read_index)

        # Control output module (Uncomment when testing output)
        #organize_solution(submodule_objects, output_objects, pi_pwm)
        
        sleep(.5)
=======
    choice = input("Gyro(a) or light sensor(b)")
    print(choice)
    if (choice == "a"):
        file = "GYRO_ACCEL.json"
    else:
        file = "LIGHT.json"

    # Import I2C Addresses
    submodule_objects = input_submodule_objects(file)
    output_objects = output_submodule_objects("LIGHT_Output.json")

    # Configure module (turn on sensor)
    read_index = configure_module(submodule_objects)

    while 1: #for now
        # Read data from input module
        submodule_objects = read_module(submodule_objects, read_index)

        # Convert data from digital to units
        submodule_objects = convert_data(submodule_objects, read_index)

        # Print data
        print_data(submodule_objects, read_index)

        # Control output module (Uncomment when testing output)
        # top_output_module(submodule_objects, output_objects)
>>>>>>> c4862df5f80c5f81d13362150356a2c45c5124a8


if __name__ == "__main__":
    main()
