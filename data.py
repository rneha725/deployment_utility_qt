import json

import global_vars


def refresh_data():
    with open(global_vars.FILE, 'w') as outfile:
        json.dump(global_vars.data, outfile)

    # todo refresh data


def add_customer(name):
    with open(global_vars.FILE) as data_file: \
            global_vars.data = json.load(data_file)

    print("this" + str(global_vars.data))
    id = int(len(global_vars.data["customers"].keys()))
    global_vars.data["customers"].setdefault(str(id), name)


def set_attribute_data(attribute):
    with open(global_vars.FILE) as data_file:
        global_vars.data = json.load(data_file)
    print(global_vars.data)
    attribute_data = global_vars.data[attribute]
    return attribute_data


def set_attr_data():
    global_vars.global_data = set_attribute_data("data")

    global_vars.customer_list = set_attribute_data("customers")

    global_vars.application_metadata = set_attribute_data("applications_meta")

    global_vars.applications = set_attribute_data("applications")
