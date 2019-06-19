import sys
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtWidgets import *

import data
import edit_add_dialog
import execute
import global_vars

execute_for_customer = {}


def open_status_dialog(key):
    if key not in global_vars.status_text:
        global_vars.status_text.setdefault(key, "...")
    status_message_box = QMessageBox(parent=main_window)
    status_message_box.setWindowTitle("Status")
    status_message_box.setText(global_vars.status_text[key])
    status_message_box.setParent(main_window)
    status_message_box.show()


def get_layout_for_app(customer_list, app_id):
    form_layout = QFormLayout()
    for cust_id in customer_list:
        status_button = QPushButton("...")
        check_box = QCheckBox()
        row = QHBoxLayout()
        # creates a mapping [cust_id,"app_id]: status_button
        mapping_key = cust_id + "," + app_id
        execute.status_button_list.setdefault(mapping_key, [status_button])
        execute_for_customer.setdefault(mapping_key, check_box)
        status_button.clicked.connect(partial(open_status_dialog, mapping_key))

        row.addWidget(check_box)
        row.addWidget(status_button)
        form_layout.addRow(QLabel(data.get_data("customers")[cust_id]["name"]), row)
    return form_layout;


def get_selection_vbox():
    vbox = QVBoxLayout()
    for app_id in data.get_data("applications_meta"):
        app_name = data.get_data("applications_meta")[app_id]["name"]
        customer_list = data.get_data("applications_meta")[app_id]["customers"]  # type:dict
        form_group = QGroupBox(app_name)
        form_group.setLayout(get_layout_for_app(customer_list, app_id))
        vbox.addWidget(form_group)
    return vbox


def open_edit_dialog():
    edit_add_window = edit_add_dialog.get_window(main_window)
    edit_add_window.show()


def open_configure_dialog():
    configure_window = QWidget()
    form_layout = QFormLayout()
    neo_path = QLineEdit()
    user = QLineEdit()
    password = QLineEdit()
    host = QLineEdit()

    # add sources input

    save = QPushButton("Save")
    # todo check for source

    form_layout.addRow("Neo Path: ", neo_path)
    form_layout.addRow("Username: ", user)
    form_layout.addRow("Password", password)
    form_layout.addRow("Host: ", host)
    form_layout.addRow("Sources")


    form_layout.addRow(save)

    configure_window.setLayout(form_layout)
    configure_window.setParent(main_window)
    configure_window.setWindowFlags(QtCore.Qt.Window)
    configure_window.setWindowTitle("Configure global settings")

    configure_window.show()

    save.clicked.connect(lambda: data.add_configuration(neo_path.text(), user.text(), password.text(), host.text()))


def get_actions_vbox():
    actions_vbox = QVBoxLayout()

    # Processes Drop down
    process_dropdown = QComboBox()
    process_dropdown.addItems(global_vars.process_list.keys())
    actions_vbox.addWidget(process_dropdown)

    # Execute button
    execute_button = QPushButton("Execute")
    global execute_for_customer
    try:
        execute_button.clicked.connect(
            lambda: execute.execute_command(execute_for_customer, process_dropdown.currentText()))
    except:
        print("here")
    actions_vbox.addWidget(execute_button)

    # Configure button
    configure_app_button = QPushButton("Configure")
    configure_app_button.clicked.connect(lambda: open_configure_dialog())
    actions_vbox.addWidget(configure_app_button)

    # Edit button
    edit_data_button = QPushButton("Edit Data")
    edit_data_button.clicked.connect(lambda: open_edit_dialog())
    actions_vbox.addWidget(edit_data_button)

    # Exit button
    exit_button = QPushButton("Exit")
    exit_button.clicked.connect(lambda: app.exit(0))
    actions_vbox.addWidget(exit_button)

    return actions_vbox


def get_main_layout():
    layout = QHBoxLayout()
    layout.addLayout(get_selection_vbox())
    layout.addStretch()
    layout.addLayout(get_actions_vbox())

    return layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QWidget()
    main_window.setWindowTitle("Deployment Helper")
    data.initialize_data()
    edit_add_dialog.get_customer_drop_down()
    main_window.setLayout(get_main_layout())
    main_window.show()
    app.exec()
    # sys.exit(app.exec())
