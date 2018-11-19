import threading

import pexpect
from PyQt5 import QtCore

import data
import global_vars

applications_meta = data.set_attribute_data("applications_meta")
status_button_list = {}

meta_data = {}

success_failure = {
    "deploy": "Deployment finished successfully",
    "start": "STARTING",
    "stop": "STOPPED",
    "status": "STARTED"
    # "restart":
}
process_list = {
    "Deploy": 'deploy', "Deploy and Restart": 'deploy,restart', "Restart": 'restart', "Stop": 'stop',
    "Start": "start",
    "Status": "status"}


def set_meta_data():
    for key in applications_meta:
        global meta_data
        meta_data.setdefault(key, [])


# make sure meta_data already have something before

def update(cust_id, app_id):
    if len(meta_data) == 0:
        data.set_attr_data()
        set_meta_data()

    meta_data[app_id].append(cust_id)
    print(meta_data)


def get_command(neo, process, account, application, user, password, host, source):
    command_dict = {"neo": neo, "process": process, "account": account, "application": application, "user": user,
                    "password": password, "host": host}
    if process == process_list["Deploy"]:
        command_dict["source"] = source

    return command_dict


def deserialize_command(command_dict):
    neo_command = command_dict["neo"] + " "
    neo_command = neo_command + command_dict["process"] + " "
    neo_command = neo_command + "--account " + command_dict["account"] + " "
    neo_command = neo_command + "--application " + command_dict["application"] + " "
    neo_command = neo_command + "--user " + command_dict["user"] + " "
    neo_command = neo_command + "--password " + command_dict["password"] + " "
    neo_command = neo_command + "--host " + command_dict["host"] + " "
    if 'source' in command_dict:
        neo_command = neo_command + '--source' + command_dict["source"]

    return neo_command


# for creating neo command array for a specific customer and a number of processses
def create_command_str(cust_id, app_id, processes):
    process_list_cust = processes.split(',')
    print(cust_id, app_id)
    customer_data = data.applications[app_id][cust_id]
    neo_commands = []
    for process in process_list_cust:

        user = ""
        password = ""
        if customer_data["user"]:
            user = customer_data["user"]
        elif data.global_data["user"]:
            user = data.global_data["user"]

        if customer_data["password"]:
            password = customer_data["password"]
        elif data.global_data["password"]:
            password = data.global_data["password"]

        command_dict = get_command(neo=data.global_data["neo_command"], process=process,
                                   account=customer_data["account"],
                                   application=customer_data["application"], user=user, password=password,
                                   host=data.global_data["host"], source=data.global_data["source"][app_id])
        print(command_dict)
        neo_commands.append(command_dict)

    return neo_commands


def run_command_cust(commands, key, checkbox_cust):
    status_button_list[key][0].setText("Thread created")
    checkbox_cust.setDisabled(True)
    # for each customer everything should be in sync

    for command in commands:
        try:
            str_command = deserialize_command(command)
            child = pexpect.spawn(str_command)
            child.expect(r'Are you located inside the EU\?\(yes\/no\) \[Default: no\]')
            child.sendline('yes')
            status_button_list[key][0].setText("Yes...")
            global_vars.status_text[key] = "Yes given\n"
            status = child.expect([success_failure[command["process"]], 'ERROR'])
            print(status)
            if status == 1:
                status_button_list[key][0].setText(status_button_list[key][0].text() + "Error!")
                global_vars.status_text[key] += "Error, please try running the command again\n" + str_command
            else:
                status_button_list[key][0].setText(status_button_list[key][0].text() + "Success!")
                global_vars.status_text[key] += "Process: " + command["process"] + " successful!"
        except:
            status_button_list[key][0].setText(status_button_list[key][0].text() + "Error")
            global_vars.status_text[key] += "Error, please try running the command again\n" + str_command

    checkbox_cust.setDisabled(False)


# data: dict, for key->checkbox
# key: '"cust_id,app_id"'
# value: checkbox
def execute_command(data, process_key):
    child = {}
    for key in data:
        cust_id, app_id = key.split(',')

        if data[key].checkState() == QtCore.Qt.Checked and data[key].isEnabled():
            commands = create_command_str(cust_id, app_id, process_list[process_key])
            # for each checkbox new thread is created
            threading.Thread(target=run_command_cust, args=(commands, key, data[key],)).start()
            # for command in commands:
            #     print("spawning for:" + command)
            #     try:
            #         child[key] = pexpect.spawn(command)
            #         child[key].expect(r'Are you located inside the EU\?\(yes\/no\) \[Default: no\]')
            #         child[key].sendline('yes')
            #         print(child[key].before+child[key].after)
            #         threading.Thread(target=run, args=(child[key],)).start()
            #     except pexpect.EOF:
            #         print("Error:")
            #     except pexpect.TIMEOUT:
            #         print("Timeout for: " + command)
            #     except pexpect.ExceptionPexpect:
            #         print("some error: " + command)
    return