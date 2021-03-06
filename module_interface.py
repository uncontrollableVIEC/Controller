# i2c.py
# Created by: VIEC Team (Team 6)
import smbus
bus = smbus.SMBus(1)

from time import sleep
from sigfig import round
from time import time
import drivers
import Constants

class submodule_id:
    def __init__(self, id, system_name, device_address, config_type, measured_value, address, io_value):
        self.id = id
        self.system_name = system_name
        self.device_address = device_address
        self.config_type = config_type
        self.measured_value = measured_value
        self.address = address
        self.io_value = io_value

class output_obj:
    def __init__(self, id, GPIO_pin, config_mode, high_input, low_input, high_output, low_output, divider, measured_value, io_value):
        self.id = id
        self.GPIO_pin = GPIO_pin
        self.config_mode = config_mode
        self.high_input = high_input
        self.low_input = low_input
        self.high_output = high_output
        self.low_output = low_output
        self.divider = divider
        self.measured_value = measured_value
        self.io_value = io_value
        self.input_index = 0
        
def convert_address(sub_obj):
    for i in sub_obj:
        sub_obj[i].device_address = int(sub_obj[i].device_address, 16)
        sub_obj[i].address = int(sub_obj[i].address, 16)
    return 0


def configure_module(sub_obj):
    i  = 0 # Initialize the index
    convert_address(sub_obj)
    while "setup" in sub_obj[i].config_type:
        try:
            if ("32" in sub_obj[i].config_type):
                sub_obj[i].io_value = sub_obj[i].io_value.split()
                sub_obj[i].io_value = [int(j) for j in sub_obj[i].io_value]
                bus.write_i2c_block_data(sub_obj[i].device_address, sub_obj[i].address, sub_obj[i].io_value)
            elif (sub_obj[i].address == 0):
                bus.write_byte(sub_obj[i].device_address, int(sub_obj[i].io_value,10))
            else:
                bus.write_byte_data(sub_obj[i].device_address, sub_obj[i].address, int(sub_obj[i].io_value,10))
            i = i + 1
        except:
            return -1
   # while "initialize" in sub_obj[i].config_type: #Ignores the sensor initializations
    #    i = i + 1
    return i


def read_module(sub_obj, index):
    i = 0 # Initialize the index
    while "read" in sub_obj[index + i].config_type:
        try:
            if "initialize" in sub_obj[index + i].config_type:
                if "8" not in sub_obj[index + i].config_type:
                    if type(sub_obj[index + i].io_value) == str:
                        sub_obj[index + i].io_value = sub_obj[index + i].io_value.split()
                        sub_obj[index + i].io_value = [int(j) for j in sub_obj[index + i].io_value]
                    bus.write_i2c_block_data(sub_obj[index + i].device_address, sub_obj[index + i].address, sub_obj[index + i].io_value)
                else:
                    bus.write_byte(sub_obj[i].device_address, int(sub_obj[i].io_value,10))
                    
            elif "24" in sub_obj[index + i].config_type:
                data = bus.read_i2c_block_data(sub_obj[index + i].device_address, sub_obj[index + i].address)
                if "custom" in sub_obj[index + i].config_type:
                    value = ((data[sub_obj[index + i].address] & 0x0F) << 16) | (data[sub_obj[index + i].address + 1] << 8) | data[sub_obj[index + i].address + 2] >> 4
                else:
                    value = ((data[0] & 0x0F) << 16) | (data[1] << 8) | data[2]
                sub_obj[index + i].io_value = value
                
            elif "16" in sub_obj[index + i].config_type:
                # if (sub_obj[i].address == 0):
                data = bus.read_i2c_block_data(sub_obj[index + i].device_address, sub_obj[index + i].address)
                value = (data[1] + (256 * data[0]))

                if value > 32768:
                    value = value - 65536
                sub_obj[index + i].io_value = value

            elif ("8" in sub_obj[index + i].config_type):
                value = bus.read_byte_data(sub_obj[index + i].device_address, sub_obj[index + i].address)
                sub_obj[index + i].io_value = value
            i = i + 1
        except:
            return -1
        
    return sub_obj


def convert_data(sub_obj, r_index):
    r = c = 0
    c_index = r_index
    while "read" in sub_obj[c_index].config_type:
        c_index = c_index + 1

    while "read" in sub_obj[r_index + r].config_type:
        c = 0
        while (c_index + c) < len(sub_obj): #Will need to change when output classes are added
            if sub_obj[r_index + r].measured_value.find(sub_obj[c_index + c].measured_value) != -1:
                value = 0
                data = float(sub_obj[r_index + r].io_value)
                value = eval(sub_obj[c_index + c].io_value)
                value = round(value, sigfigs = 6)
                sub_obj[r_index + r].io_value = value
            c = c + 1
        r = r + 1
    return sub_obj


def print_data(sub_obj, r_index, display, count):
    display.lcd_clear()
    display.lcd_display_string(sub_obj[0].system_name + ":", 1)
    if (Constants.time_interval > 0):
        start = time()
        Constants.time_interval = 0
        display.lcd_clear()
        display.lcd_display_string("Choose value:", 1)
        display.lcd_display_string(sub_obj[r_index + count].measured_value, 2)
        while(1):
            display.lcd_display_string(sub_obj[r_index + count].measured_value, 2)
            if (time() - start > 3): #Wait at least 3 seconds to have user iterate through displays
                return count
            if (Constants.time_interval > 0):
                count = count + 1
                if (sub_obj[r_index + count].config_type == "conversion"):
                    count = 0
                    while "initialize" in sub_obj[r_index + count].config_type: #Ignores the sensor initializations
                        count = count + 1 
                display.lcd_clear()
                display.lcd_display_string("Choose value:", 1)
                display.lcd_display_string(sub_obj[r_index + count].measured_value, 2)
                Constants.time_interval = 0

    display.lcd_clear()
    display.lcd_display_string(sub_obj[0].system_name + ":", 1)
    display.lcd_display_string(str(sub_obj[r_index + count].io_value) + " " + sub_obj[r_index + count].measured_value, 2)
    print(str(sub_obj[r_index + count].io_value) + " " + sub_obj[r_index + count].measured_value)
    Constants.time_interval = 0
    return count

def configure_output(input_objs, output_objs):
    for i in output_objs:
        output_objs[i].high_input = int(output_objs[i].high_input, 10)
        output_objs[i].low_input = int(output_objs[i].low_input, 10)
        output_objs[i].high_output = int(output_objs[i].high_output, 10)
        output_objs[i].low_output = int(output_objs[i].low_output, 10)
        output_objs[i].divider = int(output_objs[i].divider, 10)
        output_objs[i].GPIO_pin = int(output_objs[i].GPIO_pin,10)
        
        for j in input_objs:
            if (input_objs[j].measured_value == output_objs[i].measured_value and input_objs[j].config_type != "conversion"):
                output_objs[i].input_index = j


def GPIO_init(output_objs):
    import RPi.GPIO as GPIO
    for i in output_objs:
        if ("digital" in output_objs[i].config_mode):
            GPIO.setup(output_objs[i].GPIO_pin, GPIO.OUT)
            
        elif ("PWM" in output_objs[i].config_mode):
            GPIO.setup(output_objs[i].GPIO_pin, GPIO.OUT)
            output_objs[i].pi_pwm = GPIO.PWM(output_objs[i].GPIO_pin, 1000)
            output_objs[i].pi_pwm.start(0)
            
def organize_solution(input_objs, output_objs):
    for i in output_objs:
        output_solution(input_objs[output_objs[i].input_index], output_objs[i])

def output_solution(input_obj,output_obj):
    import RPi.GPIO as GPIO
    input_obj.io_value = float(input_obj.io_value)
    
    if ("digital" in output_obj.config_mode):
        if (input_obj.io_value > (output_obj.high_input - output_obj.low_input)/2):
            if ("invert" in output_obj.config_mode):
                GPIO.output(output_obj.GPIO_pin, GPIO.LOW)
            else:
                GPIO.output(output_obj.GPIO_pin, GPIO.HIGH)
        else:
            if ("invert" in output_obj.config_mode):
                GPIO.output(output_obj.GPIO_pin, GPIO.HIGH)
            else:
                GPIO.output(output_obj.GPIO_pin, GPIO.LOW)
        return

    elif ("PWM" in output_obj.config_mode):
    
        input_step = (output_obj.high_input - output_obj.low_input) / output_obj.divider
        output_step = (output_obj.high_output - output_obj.low_output) / output_obj.divider
        multiple = int((input_obj.io_value - output_obj.low_input)/ input_step)
        
        if ("invert" in output_obj.config_mode):
            output_obj.io_value = output_obj.high_output - output_step * multiple
        else:
            output_obj.io_value = output_step * multiple + output_obj.low_output
        
        if output_obj.io_value > output_obj.high_output:
            output_obj.io_value = output_obj.high_output
            
        if output_obj.io_value < output_obj.low_output:
            output_obj.io_value = output_obj.low_output
        output_obj.pi_pwm.ChangeDutyCycle(int(output_obj.io_value))
        return
    
    else:
        GPIO.output(output_obj.GPIO_pin, GPIO.LOW)
        return

    sleep(6)
    print("\n")
    return 0