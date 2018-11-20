import json

import global_vars


def set_attribute_data(attribute):
    with open(global_vars.FILE) as data_file:
        global data
        data = json.load(data_file)
    attribute_data = data[attribute]
    return attribute_data


def set_attr_data():
    global_vars.global_data = set_attribute_data("data")

    global_vars.customer_list = set_attribute_data("customers")

    global_vars.application_metadata = set_attribute_data("applications_meta")

    global_vars.applications = set_attribute_data("applications")
