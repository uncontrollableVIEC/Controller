# i2c.py
# Created by: VIEC Team (Team 6)
import smbus
bus = smbus.SMBus(1)
from time import sleep 

class submodule_id:
    def __init__(self, id, device_address, config_type, measured_value, address, io_value):
        self.id = id
        self.device_address = device_address
        self.config_type = config_type
        self.measured_value = measured_value
        self.address = address
        self.io_value = io_value
        
def convert_address(sub_obj):
    for i in range(len(sub_obj)):
      #  print(int(sub_obj[i].device_address,16))
        sub_obj[i].device_address = int(sub_obj[i].device_address, 16)
        sub_obj[i].address = int(sub_obj[i].address, 16)
    return 0


def configure_module(sub_obj):
    i = 0 # Initialize the index
    convert_address(sub_obj)
    while sub_obj[i].config_type == "setup":
        bus.write_byte_data(sub_obj[i].device_address, sub_obj[i].address, int(sub_obj[i].io_value,10))
        i = i + 1
    return i


def read_module(sub_obj, index):
    i = 0 # Initialize the index
    while "read" in sub_obj[index + i].config_type:
        if "16" in sub_obj[index + i].config_type:
            high = bus.read_byte_data(sub_obj[index + i].device_address, sub_obj[index + i].address)
            low = bus.read_byte_data(sub_obj[index + i].device_address, sub_obj[index + i].address + 1)
            value = ((high << 8) | low)

            if value > 32768:
                value = value - 65536
            sub_obj[index + i].io_value = value
        i = i + 1
    return sub_obj


def convert_data(sub_obj, r_index):
    r = c = 0
    c_index = r_index
    while "read" in sub_obj[c_index].config_type:
        c_index = c_index + 1

    while "read" in sub_obj[r_index + r].config_type:
        while c_index + c < len(sub_obj): #Will need to change when output classes are added
            if sub_obj[r_index + r].measured_value.find(sub_obj[c_index + c].measured_value) != -1:
                sub_obj[r_index + r].io_value = float(sub_obj[r_index + r].io_value) / float(sub_obj[c_index + c].io_value)
            c = c + 1
        r = r + 1
    return sub_obj


def print_data(sub_obj, r_index):
    print("GYRO_X")  #GYRO_X is printed for demonstration. Any variable can be printed
    print(sub_obj[8].io_value)
    sleep(1)
    return 0
