import json

FILE = "attributes.json"
global_data = {}
customer_list = {}
application_metadata = {}
applications = {}


def set_attribute_data(attribute):
    with open(FILE) as data_file:
        global data
        data = json.load(data_file)
    attribute_data = data[attribute]
    return attribute_data


def set_attr_data():
    global global_data
    global_data = set_attribute_data("data")

    global customer_list
    customer_list = set_attribute_data("customers")

    global application_metadata
    application_metadata = set_attribute_data("applications_meta")

    global applications
    applications = set_attribute_data("applications")

