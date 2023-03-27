# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FinalAdminPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QHeaderView, QTableWidget, QAbstractItemView

import FinalChangePassword
from Database import User


class Ui_Form(QObject):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(630, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.UserId_text = QtWidgets.QLabel(Form)
        self.UserId_text.setObjectName("UserId_text")
        self.horizontalLayout.addWidget(self.UserId_text)
        self.UserID = QtWidgets.QLineEdit(Form)
        self.UserID.setObjectName("UserID")
        self.horizontalLayout.addWidget(self.UserID)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.SearchButton = QtWidgets.QPushButton(Form)
        self.SearchButton.setObjectName("SearchButton")
        self.horizontalLayout.addWidget(self.SearchButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.DeleteUserButton = QtWidgets.QPushButton(Form)
        self.DeleteUserButton.setObjectName("DeleteUserButton")
        self.horizontalLayout_2.addWidget(self.DeleteUserButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.ChangePasswordButton = QtWidgets.QPushButton(Form)
        self.ChangePasswordButton.setObjectName("ChangePasswordButton")
        self.horizontalLayout_2.addWidget(self.ChangePasswordButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.loadDataFromTable()
        # if no record selected it crashes.
        self.ChangePasswordButton.clicked.connect(lambda: self.changePassScreen(self.get_selected_row()))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.UserId_text.setText(_translate("Form", "User ID:"))
        self.SearchButton.setText(_translate("Form", "Search"))
        self.DeleteUserButton.setText(_translate("Form", "Delete User"))
        self.ChangePasswordButton.setText(_translate("Form", "Change Password"))

    def loadDataFromTable(self):
        self.User = User.User()
        table = self.User.getTable()
        print(table)
        self.load_dataframe_to_table(table, self.tableWidget)

    def load_dataframe_to_table(self, dataframe, table_widget):
        # Set the number of rows and columns for the table
        table_widget.setRowCount(len(dataframe))
        table_widget.setColumnCount(len(dataframe.columns))

        # Add the headers for the table columns
        table_widget.setHorizontalHeaderLabels(dataframe.columns)

        for row in range(len(dataframe)):
            for column in range(len(dataframe.columns)):
                item = QtWidgets.QTableWidgetItem()
                print(dataframe.iloc[row, column])
                item.setData(QtCore.Qt.DisplayRole, str(dataframe.iloc[row, column]))
                table_widget.setItem(row, column, item)

    def get_selected_row(self):
        row = self.tableWidget.currentRow()
        if row == -1:
            print("No row is selected.")
        else:
            item = self.tableWidget.item(row, 0).text()
            return item

    def changePassScreen(self, UserID):
        self.window = QtWidgets.QWidget()
        self.window = FinalChangePassword.MyWindow()
        self.window.setupPage(UserID)
        self.window.show()


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())