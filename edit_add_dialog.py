from PyQt5 import QtCore
from PyQt5.QtWidgets import *

import data
import global_vars

TEXT = "<if different than global>"


def open_name_dialog(layout):
    c = QInputDialog()
    c.setParent(layout)
    c.show()


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
        application_drop_down.addItem(text, userData=key)

    return application_drop_down


def save_app_data(application, account, host, source, user, password, app_id, cust_id):
    # todo assuming that only two applications are there, "1" & "2" are there in applications
    object = {
        "application": application,
        "account": account,
        "source": source,
        "host": host,
        "user": user,
        "password": password
    }
    global_vars.data['applications'][app_id].setdefault(cust_id, object)
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
        app_dict = global_vars.applications[app_id][cust_id]
        # if no keyerror: open edit
        open_edit_dialog(object=app_dict, parent=parent, app_id=app_id, cust_id=cust_id)
    except KeyError:
        # if value is no there then open add
        open_edit_dialog({}, parent=parent, app_id=app_id, cust_id=cust_id)


def get_window(main_window):
    selection_window = QWidget()
    selection_window.setParent(main_window)
    selection_window.setWindowFlags(QtCore.Qt.Window)
    selection_window.setWindowTitle("Edit/Add")

    mainhbox = QHBoxLayout()

    # two drop down
    combohbox = QHBoxLayout()
    customer_drop_down = get_customer_drop_down()
    combohbox.addStretch()
    application_drop_down = get_applications_drop_down()
    # add a button
    edit_add_button = QPushButton("Add/Edit")
    edit_add_button.clicked.connect(lambda: edit_click(customer_drop_down, application_drop_down, selection_window))
    exit = QPushButton("Exit")
    exit.clicked.connect(lambda: selection_window.destroy())

    add_customer = QPushButton("Add Customer")
    combohbox.addWidget(customer_drop_down)
    combohbox.addWidget(application_drop_down)

    buttonvbox = QVBoxLayout()
    buttonvbox.addWidget(edit_add_button)
    buttonvbox.addWidget(add_customer)
    buttonvbox.addWidget(exit)
    add_customer.clicked.connect(lambda: open_name_dialog(add_customer))

    mainhbox.addLayout(combohbox)
    mainhbox.addLayout(buttonvbox)

    selection_window.setLayout(mainhbox)
    return selection_window
