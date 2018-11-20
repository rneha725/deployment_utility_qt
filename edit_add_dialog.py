from PyQt5 import QtCore
from PyQt5.QtWidgets import *

import global_vars


def get_customer_drop_down():
    customer_drop_down = QComboBox()
    for key in global_vars.customer_list:
        text = global_vars.customer_list[key]["name"]
        customer_drop_down.addItem(text, userData=key)
    return customer_drop_down


def get_applications_drop_down():
    application_drop_down = QComboBox()
    for key in global_vars.application_metadata:
        print(global_vars.application_metadata[key])
        text = global_vars.application_metadata[key]['name']
        application_drop_down.addItem(text)

    return application_drop_down


def edit_click(customer, application):
    cust_id = customer.currentData()
    app_id = application.currentData()


def get_window(main_window):
    selection_window = QWidget()
    selection_window.setParent(main_window)
    selection_window.setWindowFlags(QtCore.Qt.Window)
    selection_window.setWindowTitle("Edit/Add")

    # two drop down
    combohbox = QHBoxLayout()
    customer_drop_down = get_customer_drop_down()
    combohbox.addStretch()
    application_drop_down = get_applications_drop_down()
    # add a button
    edit_add_button = QPushButton("Add/Edit")
    edit_add_button.clicked.connect(lambda: edit_click(customer_drop_down, application_drop_down))
    combohbox.addWidget(customer_drop_down)
    combohbox.addWidget(application_drop_down)
    combohbox.addWidget(edit_add_button)
    selection_window.setLayout(combohbox)
    return selection_window
