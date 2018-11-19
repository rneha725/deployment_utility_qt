import sys
from functools import partial

from PyQt5.QtWidgets import *

import data
import execute
import global_vars

execute_for_customer = {}


def ini():
    for key in execute.status_button_list:  # type: QPushButton
        button = execute.status_button_list[key][0]
        button.clicked.connect(partial(open_status_dialog, key))


def open_status_dialog(key):
    print(global_vars.status_text)
    print(key)
    if key not in global_vars.status_text:
        print("here")
        global_vars.status_text.setdefault(key, "__")
    status_message_box = QMessageBox(parent=main_window)
    status_message_box.setText(global_vars.status_text[key])
    status_message_box.setParent(main_window)
    status_message_box.show()


def get_selection_vbox():
    selection_vbox = QVBoxLayout()

    for app_id in data.application_metadata:
        app_name = data.application_metadata[app_id]["name"]
        customer_list = data.application_metadata[app_id]["customers"]
        form_group = QGroupBox(app_name)
        form_layout = QFormLayout()

        for cust_id in customer_list:
            status_button = QPushButton("__")
            execute.status_button_list.setdefault(cust_id + "," + app_id, [status_button])
            customer_data = data.customer_list[cust_id]
            check_box = QCheckBox()

            execute_for_customer.setdefault(cust_id + "," + app_id, check_box)
            form_layout.addRow(QLabel(customer_data["name"]), check_box)
            form_layout.addRow("Status", status_button)
        form_group.setLayout(form_layout)
        selection_vbox.addWidget(form_group)

    print(execute_for_customer)
    return selection_vbox


def open_edit_dialog():
    selection_window = QWidget(parent=main_window)
    selection_window.setWindowTitle("Edit/Add")
    # two drop down
    combohbox = QHBoxLayout(QWidget=selection_window)

    customer_drop_down = QComboBox()
    for key in data.customer_list:
        text = key + "." + data.customer_list[key]["name"]
        print(text)
        customer_drop_down.addItem(text)

    combohbox.addWidget(customer_drop_down)
    selection_window.setLayout(combohbox)

    selection_window.show()


def get_actions_vbox():
    actions_vbox = QVBoxLayout()

    process_dropdown = QComboBox()
    process_dropdown.addItems(execute.process_list.keys())

    execute_button = QPushButton("Execute")
    # Todo according to user's choice
    global execute_for_customer
    execute_button.clicked.connect(
        lambda: execute.execute_command(execute_for_customer, process_dropdown.currentText()))

    edit_data_button = QPushButton("Edit Data")
    edit_data_button.clicked.connect(lambda: QDialog().show())

    exit_button = QPushButton("Exit")
    exit_button.clicked.connect(lambda: app.exit(0))

    actions_vbox.addWidget(process_dropdown)
    actions_vbox.addWidget(execute_button)
    actions_vbox.addWidget(edit_data_button)
    actions_vbox.addWidget(exit_button)
    return actions_vbox


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = QWidget()
    data.set_attr_data()
    execute.set_meta_data()

    main_layout = QHBoxLayout()
    main_layout.addLayout(get_selection_vbox())
    main_layout.addStretch()
    main_layout.addLayout(get_actions_vbox())
    print(execute.status_button_list.keys())
    # Todo 1. create a toolbar-menu

    main_window.setLayout(main_layout)
    main_window.show()
    ini()
    app.exec()
