from PyQt5 import QtCore
from PyQt5.QtWidgets import *

import data
import global_vars

TEXT = "<if different than global>"


def add_customer_dialog(layout):
    customer_name, ok = QInputDialog.getText(layout, 'Text Input Dialog', 'Enter customer name:')
    print("here" + customer_name)
    data.add_customer(customer_name)
    if ok:
        data.refresh_data()

# todo adding An application should also ask for global path
def add_application_dialog(layout, application_drop_down):
    application_name, ok = QInputDialog.getText(layout, 'Text Input Dialog', 'Enter application display name:')
    print("here" + application_name)
    data.add_application(application_name)
    if ok:
        data.refresh_data()
        application_drop_down.destroy()
        layout.update()


def get_customer_drop_down():
    customer_drop_down = QComboBox()
    for key in data.get_data("customers"):
        text = data.get_data("customers")[key]["name"]
        customer_drop_down.addItem(text, userData=key)
    global_vars.customer_drop_down = customer_drop_down


def get_applications_drop_down():
    application_drop_down = QComboBox()
    for key in data.get_data("applications_meta"):
        print(data.get_data("applications_meta")[key])
        text = data.get_data("applications_meta")[key]['name']
        application_drop_down.addItem(text, userData=key)

    return application_drop_down


def save_app_data(application, account, host, source, user, password, app_id, cust_id):
    # todo assuming that only two applications are there, "1" & "2" are there in applications
    object = {
        "application": application.text(),
        "account": account.text(),
        "source": source.text(),
        "host": host.text(),
        "user": user.text(),
        "password": password.text()
    }
    try:
        global_vars.data['applications'][app_id][cust_id] = object
        if cust_id not in global_vars.data['applications_meta'][app_id]["customers"]:
            global_vars.data['applications_meta'][app_id]["customers"].append(cust_id)
    except KeyError:
        global_vars.data['applications'][app_id].setdefault(cust_id, object)

    print("Data: " + app_id + " " + cust_id)
    print(global_vars.data)
    print(object)
    data.refresh_data()


def open_edit_dialog(object, parent, app_id, cust_id):
    print(object.keys())
    edit_window = QWidget()
    edit_window.setParent(parent)
    edit_window.setGeometry(100, 100, 500, 300)
    edit_window.setWindowFlags(QtCore.Qt.Window)

    form_layout = QFormLayout()
    application = QLineEdit()
    account = QLineEdit()
    host = QLineEdit()
    source = QLineEdit()
    user = QLineEdit()
    password = QLineEdit()

    password.setText(TEXT)
    if object != {}:
        application.setText(object['application'])
        account.setText(object['account'])
        host.setText(object['host'])
        if host.text() == "": host.setText(TEXT)
        source.setText(object['source'])
        if source.text() == "": source.setText(TEXT)
        user.setText(object['user'])
        if user.text() == "": user.setText(TEXT)
        password.setText(object['password'])
        if password.text() == "": password.setText(TEXT)

    form_layout.addRow("Application*", application)
    form_layout.addRow("Account*", account)
    form_layout.addRow("Host", host)
    form_layout.addRow("Source", source)
    form_layout.addRow("User", user)
    form_layout.addRow("Password", password)

    submit = QPushButton("Submit")
    cancel = QPushButton("Cancel")
    cancel.clicked.connect(lambda: edit_window.destroy())

    submit.clicked.connect(lambda: save_app_data(application, account, host, source, user, password, app_id, cust_id))
    form_layout.addWidget(submit)
    form_layout.addWidget(cancel)

    edit_window.setLayout(form_layout)
    edit_window.show()


def edit_click(customer, application, parent):
    cust_id = customer.currentData()
    app_id = application.currentData()
    try:
        app_dict = data.get_data("applications")[app_id][cust_id]
        # if no keyerror: open edit
        open_edit_dialog(object=app_dict, parent=parent, app_id=app_id, cust_id=cust_id)
    except KeyError:
        # if value is no there then open add
        open_edit_dialog({}, parent=parent, app_id=app_id, cust_id=cust_id)


def delete_customer(customer):
    # pop from customer
    global_vars.data["customers"].pop(customer, None)
    applications = global_vars.data["applications"]
    for key in applications:
        applications[key].pop(customer, None)

    applications_meta = global_vars.data["applications_meta"]
    for key in applications_meta:
        applications_meta[key]["customers"].remove(customer)


def delete_customer_dialog(parent):
    form_group = QFormLayout()
    form_group.addRow(global_vars.customer_drop_down)
    ok_button = QPushButton("Delete")
    ok_button.clicked.connect(lambda: delete_customer(customer_dropdown.currentData()))
    form_group.addRow(ok_button)
    window = QWidget()
    window.setLayout(form_group)
    window.setParent(parent)
    window.setWindowFlags(QtCore.Qt.Window)
    window.setWindowTitle("Select customer")
    window.show()


def get_window(main_window):
    selection_window = QWidget()
    selection_window.setParent(main_window)
    selection_window.setWindowFlags(QtCore.Qt.Window)
    selection_window.setWindowTitle("Edit/Add")

    mainhbox = QHBoxLayout()

    selection_boxes = QHBoxLayout()
    # customer drop down
    selection_boxes.addWidget(global_vars.customer_drop_down)
    selection_boxes.addStretch()
    # application drop down
    application_drop_down = get_applications_drop_down()
    selection_boxes.addWidget(application_drop_down)

    button_vbox = QVBoxLayout()
    # Add/Edit button
    edit_add_button = QPushButton("Edit Application Data")
    edit_add_button.clicked.connect(lambda: edit_click(global_vars.customer_drop_down, application_drop_down, selection_window))
    button_vbox.addWidget(edit_add_button)

    # Add application button
    add_application_button = QPushButton("Add application")
    add_application_button.clicked.connect(lambda: add_application_dialog(add_application_button, application_drop_down))
    add_application_button.clicked.connect(lambda: application_drop_down.repaint())
    add_application_button.clicked.connect(lambda: selection_window.repaint())
    # add_application_button.clicked.connect(lambda: application_drop_down.update())
    # add_application_button.clicked.connect(lambda: selection_boxes.update())
    # add_application_button.clicked.connect(lambda: mainhbox.update())
    button_vbox.addWidget(add_application_button)

    # Add customer button
    add_customer = QPushButton("Add Customer")
    add_customer.clicked.connect(lambda: add_customer_dialog(add_customer))
    add_application_button.clicked.connect(lambda: global_vars.customer_drop_down.repaint())
    add_application_button.clicked.connect(lambda: selection_window.repaint())
    button_vbox.addWidget(add_customer)

    # Delete customer button
    delete_customer = QPushButton("Delete Customer")
    delete_customer.clicked.connect(lambda: delete_customer_dialog(selection_window))
    button_vbox.addWidget(delete_customer)

    # exit button
    exit = QPushButton("Exit")
    exit.clicked.connect(lambda: selection_window.close())
    button_vbox.addWidget(exit)

    mainhbox.addLayout(selection_boxes)
    mainhbox.addLayout(button_vbox)

    selection_window.setLayout(mainhbox)
    return selection_window
