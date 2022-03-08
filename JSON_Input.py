# JSON_Input.py
# Created by: VIEC Team


class submodule_id:
    def __init__(self, id, device_address, config_type, measured_value, address, io_value):
        self.id = id
        self.device_address = device_address
        self.config_type = config_type
        self.measured_value = measured_value
        self.address = address
        self.io_value = io_value

class output_obj:
    def __init__(self, id, GPIO_pin, config_mode, tf_function, peak_voltage, io_value, measured_value):
        self.id = id
        self.GPIO_pin = GPIO_pin
        self.config_mode = config_mode
        self.tf_function = tf_function
        self.peak_voltage: peak_voltage
        self.io_value = io_value
        self.measured_value = measured_value


def input_submodule_objects(file):
    import json
    
    
    with open(file) as jsonFile:
        submodule = json.load(jsonFile)

    submodule_objects = {submodule_object['id']: submodule_id(submodule_object['id'],
                                                              submodule_object['device_address'], submodule_object['config_type'],
                                                              submodule_object['measured_value'],
                                                              submodule_object['address'], submodule_object['io_value'])
                         for submodule_object in submodule}
    return submodule_objects


def output_submodule_objects(file):
    import json

    with open(file) as jsonFile:
        submodule = json.load(jsonFile)

    submodule_objects = {submodule_object['id']: submodule_id(submodule_object['id'],
                                                              submodule_object['GPIO_Pin'],
                                                              submodule_object['config_mode'],
                                                              submodule_object['tf_function'],
                                                              submodule_object['peak_voltage'], submodule_object['set_point'], submodule_object['measured_value'])
                         for submodule_object in submodule}
    return submodule_objects
