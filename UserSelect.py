# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UserSelect.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import pickle

from PyQt5.QtCore import QObject

import mainScreen


class Ui_MainWindow(QObject):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(397, 112)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.UserIDText = QtWidgets.QLabel(self.centralwidget)
        self.UserIDText.setObjectName("UserIDText")
        self.horizontalLayout.addWidget(self.UserIDText)
        self.UserID = QtWidgets.QLineEdit(self.centralwidget)
        self.UserID.setObjectName("UserID")
        self.horizontalLayout.addWidget(self.UserID)
        self.SelectButton = QtWidgets.QPushButton(self.centralwidget)
        self.SelectButton.setObjectName("SelectButton")
        self.SelectButton.clicked.connect(self.get_text)
        self.horizontalLayout.addWidget(self.SelectButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.UserIDText.setText(_translate("MainWindow", "UserID: "))
        self.SelectButton.setText(_translate("MainWindow", "Select"))

    def get_text(self):
        text = self.UserID.text()
        # Save the variable to a file
        UserID = text
        with open("my_variable.pickle", "wb") as f:
            pickle.dump(UserID, f)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
