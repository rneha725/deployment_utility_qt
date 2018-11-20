import sys
from functools import partial

from PyQt5.QtWidgets import *

import data
import edit_add_dialog
import execute
import global_vars

execute_for_customer = {}


def open_status_dialog(key):
    print(global_vars.status_text)
    print(key)
    if key not in global_vars.status_text:
        print("here")
        global_vars.status_text.setdefault(key, "__")
    status_message_box = QMessageBox(parent=main_window)
    status_message_box.setWindowTitle("Status")
    status_message_box.setText(global_vars.status_text[key])
    status_message_box.setParent(main_window)
    status_message_box.show()


def get_selection_vbox():
    selection_vbox = QVBoxLayout()

    for app_id in global_vars.application_metadata:
        app_name = global_vars.application_metadata[app_id]["name"]
        customer_list = global_vars.application_metadata[app_id]["customers"]  # type:dict
        form_group = QGroupBox(app_name)
        form_layout = QFormLayout()

        for cust_id in customer_list:  # type: dict
            status_button = QPushButton("__")
            execute.status_button_list.setdefault(cust_id + "," + app_id, [status_button])
            status_button.clicked.connect(partial(open_status_dialog, cust_id + "," + app_id))
            customer_data = global_vars.customer_list[cust_id]
            check_box = QCheckBox()

            execute_for_customer.setdefault(cust_id + "," + app_id, check_box)
            form_layout.addRow(QLabel(customer_data["name"]), check_box)
            form_layout.addRow("Status", status_button)
        form_group.setLayout(form_layout)
        selection_vbox.addWidget(form_group)

    print(execute_for_customer)
    return selection_vbox


def open_edit_dialog():
    edit_add_window = edit_add_dialog.get_window(main_window)
    edit_add_window.show()


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
    edit_data_button.clicked.connect(lambda: open_edit_dialog())

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
    main_window.setWindowTitle("Helper")
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
    app.exec()
