import threading

import pexpect
from PyQt5 import QtCore
import os

import data
import global_vars

status_button_list = {}
meta_data = {}

success_failure = {
    "deploy": "Deployment finished successfully",
    "start": "STARTING",
    "stop": "STOPPED",
    "status": "STARTED",
    "restart": "STARTING"
}


def set_meta_data():
    for key in data.get_data("applications_meta"):
        global meta_data
        meta_data.setdefault(key, [])


# make sure meta_data already have something before

def update(cust_id, app_id):
    if len(meta_data) == 0:
        data.initialize_data()
        set_meta_data()

    meta_data[app_id].append(cust_id)
    print(meta_data)


def get_command(neo, process, account, application, user, password, host, source):
    command_dict = {"neo": neo, "process": process, "account": account, "application": application, "user": user,
                    "password": password, "host": host}
    if process == global_vars.process_list["Deploy"]:
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
        neo_command = neo_command + '--source ' + command_dict["source"]

    return neo_command


# for creating neo command array for a specific customer and a number of processses
def create_command_str(cust_id, app_id, processes):
    process_list_cust = processes.split(',')
    print(cust_id, app_id)
    customer_data = data.get_data("applications")[app_id][cust_id]
    neo_commands = []
    try:
        for process in process_list_cust:

            user = ""
            password = ""
            if customer_data["user"]:
                user = customer_data["user"]
            elif data.get_data("data")["user"]:
                user = data.get_data("data")["user"]

            if customer_data["password"]:
                password = customer_data["password"]
            elif data.get_data("data")["password"]:
                password = data.get_data("data")["password"]

            command_dict = get_command(neo=data.get_data("data")["neo_command"], process=process,
                                       account=customer_data["account"],
                                       application=customer_data["application"], user=user, password=password,
                                       host=data.get_data("data")["host"],
                                       source=data.get_data("data")["source"][app_id])
            print(command_dict)
            neo_commands.append(command_dict)
    except KeyError as ex:
        return ex

    return neo_commands


def execute_deploy(child, key):
    status = child.expect(["Uploading started", 'ERROR'], timeout=60000)
    if status == 1:
        raise ChildProcessError("Uploading did not start")
    else:
        status_button_list[key][0].setText("Uploading...")
        global_vars.status_text[key] += "\nUploading started..."
    status = child.expect(["Uploaded", 'ERROR'], timeout=180000)
    if status == 1:
        raise ChildProcessError("Error after uploading")
    else:
        status_button_list[key][0].setText("Uploaded")
        global_vars.status_text[key] += "\nUploaded."
    status = child.expect(["Processing started", 'ERROR'], timeout=60000)
    if status == 1:
        raise ChildProcessError("Error after processing started")
    else:
        status_button_list[key][0].setText("Processing...")
        global_vars.status_text[key] += "\nProcessing started..."
    status = child.expect(["Processing completed", 'ERROR'], timeout=60000)
    if status == 1:
        raise ChildProcessError("Error after processing completed")
    else:
        status_button_list[key][0].setText("Processed.")
        global_vars.status_text[key] += "\nProcessing completed."


def execute_child(child, command, key):
    child.expect(r'Are you located inside the EU\?\(yes\/no\) \[Default: no\]')
    child.sendline('yes')
    global_vars.status_text[key] += "Yes given.\n"
    if command["process"] == "deploy":
        execute_deploy(child, key)


def run_for_customer(commands, key, checkbox_cust):
    status_button_list[key][0].setText("Thread created")
    checkbox_cust.setDisabled(True)
    global_vars.status_text[key] = ""

    for command in commands:
        try:
            str_command = deserialize_command(command)
            child = pexpect.spawn(str_command)
            execute_child(child, command, key)
            status = child.expect([success_failure[command["process"]], 'ERROR'], timeout=60000)
            if status == 1:
                child.interact()
                status_button_list[key][0].setText("Error!")
                global_vars.status_text[key] += "Error, please try running the command again\n" + str_command
            else:
                status_button_list[key][0].setText("Success!")
                global_vars.status_text[key] += "Process: " + command["process"] + " successful!"
        except ChildProcessError as ex:
            print("Exception for:")
            # child.interact()
            status_button_list[key][0].setText(status_button_list[key][0].text() + "Error")
            global_vars.status_text[key] += "\nError, please try running the command again\n" + str_command
        except:
            child.interact()
            status_button_list[key][0].setText(status_button_list[key][0].text() + "Error")
            global_vars.status_text[key] += "Error, please try running the command again\n" + str_command
    os.system("osascript -e 'display notification \"Process successful...\"'")
    checkbox_cust.setDisabled(False)


def execute_command(checkboxes, selected_process):
    for key in checkboxes:
        cust_id, app_id = key.split(',')

        if checkboxes[key].checkState() == QtCore.Qt.Checked and checkboxes[key].isEnabled():
            commands = create_command_str(cust_id, app_id, global_vars.process_list[selected_process])
            if isinstance(commands, Exception):
                return commands
            threading.Thread(target=run_for_customer, args=(commands, key, checkboxes[key],)).start()
    return
