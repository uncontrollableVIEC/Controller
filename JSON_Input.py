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


def import_submodule_objects():
    import json
    
    # Temporary Code
    choice = input("Gyro(a) or light sensor(b)")
    print(choice)
    if (choice == "a"):
        file = "GYRO_ACCEL.json"
    else:
        file = "LIGHT.json"
    
    
    with open(file) as jsonFile:
        submodule = json.load(jsonFile)

    submodule_objects = {submodule_object['id']: submodule_id(submodule_object['id'],
                                                              submodule_object['device_address'], submodule_object['config_type'],
                                                              submodule_object['measured_value'],
                                                              submodule_object['address'], submodule_object['io_value'])
                         for submodule_object in submodule}
    return submodule_objects
