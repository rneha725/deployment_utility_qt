import json

import global_vars


def refresh_data():
    with open(global_vars.FILE, 'w') as outfile:
        json.dump(global_vars.data, outfile)

    # refresh_customer_data()
    # refresh_applications_data()


def refresh_customer_data():
    # get customer related drop downs
    # 1. for edit data
    global_vars.customer_drop_down


def refresh_applications_data():
    # get application related data
    # 1. get applications related data
    pass


def add_customer(name):
    with open(global_vars.FILE) as data_file:
        global_vars.data = json.load(data_file)

    id = int(len(global_vars.data["customers"].keys()))
    print(str(id + 1))
    name_obj = {}
    name_obj.setdefault("name", name)
    global_vars.data["customers"].setdefault(str(id + 1), name_obj)
    # todo, refresh customer data in whole application
    # refresh_data()


def add_application(name):
    with open(global_vars.FILE) as data_file:
        global_vars.data = json.load(data_file)

    id = int(len(global_vars.data["applications_meta"].keys()))
    print("Adding a application with id" + str(id + 1))
    meta_obj = {}
    meta_obj.setdefault(id + 1, {})
    meta_obj.setdefault("name", name)
    meta_obj.setdefault("customers", [])
    global_vars.data["applications_meta"].setdefault(id + 1, meta_obj)
    global_vars.data["applications"].setdefault(id + 1, {})


def add_configuration(neo_command, user, password, host):
    global_vars.data["data"].setdefault("neo_command", neo_command)
    global_vars.data["data"].setdefault("user", user)
    global_vars.data["data"].setdefault("password", password)
    global_vars.data["data"].setdefault("host", host)
    refresh_data()


def set_attribute_data(attribute):
    with open(global_vars.FILE) as data_file:
        global_vars.data = json.load(data_file)
    attribute_data = global_vars.data[attribute]
    return attribute_data


def get_data(attribute):
    with open(global_vars.FILE) as data_file:
        json_data = json.load(data_file)
    attribute_data = json_data[attribute]
    return attribute_data


def initialize_data():
    global_vars.application_metadata = set_attribute_data("applications_meta")
    global_vars.global_data = set_attribute_data("data")
    global_vars.applications = set_attribute_data("applications")
    global_vars.customer_list = set_attribute_data("customers")
