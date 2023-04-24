import os.path
import pickle

import bcrypt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QLineEdit

import FinalAddUser
import FinalAdminPage
import FinalMainPage
import SetupFile
from Database import User, SetUpFile


def verify_password(password, hashed_password):
    """hasp password then compare with hashed password."""
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)


class Ui_Form(QObject):
    def setupUi(self, Form):
        self.User = User.User()
        Form.setObjectName("Form")
        Form.resize(352, 186)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.UserName_Text = QtWidgets.QLabel(Form)
        self.UserName_Text.setObjectName("UserName_Text")
        self.horizontalLayout_4.addWidget(self.UserName_Text)
        self.UserName = QtWidgets.QLineEdit(Form)
        self.UserName.setObjectName("UserName")
        self.horizontalLayout_4.addWidget(self.UserName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Password_text = QtWidgets.QLabel(Form)
        self.Password_text.setObjectName("Password_text")
        self.horizontalLayout_3.addWidget(self.Password_text)
        self.Password = QtWidgets.QLineEdit(Form)
        self.Password.setEchoMode(QLineEdit.Password)
        self.Password.setObjectName("Password")
        self.horizontalLayout_3.addWidget(self.Password)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.CreateNewAccountButton = QtWidgets.QPushButton(Form)
        self.CreateNewAccountButton.setObjectName("CreateNewAccountButton")
        self.horizontalLayout.addWidget(self.CreateNewAccountButton)
        self.LogInButton = QtWidgets.QPushButton(Form)
        self.LogInButton.setObjectName("LogInButton")
        self.horizontalLayout.addWidget(self.LogInButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.label.setHidden(True)
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.LogInButton.clicked.connect(self.LogIn)
        self.CreateNewAccountButton.clicked.connect(self.openCreateAccount)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.UserName_Text.setText(_translate("Form", "User Name:"))
        self.Password_text.setText(_translate("Form", "Password:"))
        self.CreateNewAccountButton.setText(_translate("Form", "Create new account"))
        self.LogInButton.setText(_translate("Form", "Log in"))
        self.label.setText(_translate("Form", "TextLabel"))

    def openAdminPage(self):
        """open admin page"""
        self.window = QtWidgets.QWidget()
        self.window = FinalAdminPage.MyWindow()
        self.window.show()

    def openCreateAccount(self):
        """open create account page"""
        self.close()
        self.window = QtWidgets.QWidget()
        self.window = FinalAddUser.MyWindow()
        self.window.show()

    def LogIn(self):
        """Log in to account or admin"""
        # if admin logs in then they get access to change passwords for users.
        if self.UserName.text() == SetUpFile.AdminUser and self.Password.text() == SetUpFile.AdminPass:
            self.close()
            self.openAdminPage()
            return
        #self.UserName.text()
        if self.UserName.text() == "":
            self.label.setText("Please enter a user name!")
            self.label.setHidden(False)
            return
        if not self.User.isUserExist(self.UserName.text()):
            self.label.setText("Wrong user name or password!")
            self.label.setHidden(False)
            return
        isPassCorrect = verify_password(self.Password.text(), self.User.getHashedPassword(self.UserName.text()))
        if isPassCorrect is False:
            self.label.setText("Wrong user name or password!")
            self.label.setHidden(False)
        else:
            with open("my_variable.pickle", "wb") as f:
                pickle.dump(self.UserName.text(), f)
            self.OpenMainPage()

    def OpenMainPage(self):
        """open main page"""
        self.close()
        self.window = FinalMainPage.MyWindow()
        self.window.show()
        self.window.showMaximized()


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Log in")
        self.setStyleSheet(SetupFile.Background)
        self.UserName.setStyleSheet(SetupFile.QLineEdit)
        self.Password.setStyleSheet(SetupFile.QLineEdit)
        self.LogInButton.setStyleSheet(SetupFile.Button)
        self.CreateNewAccountButton.setStyleSheet(SetupFile.Button)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    if os.path.isfile("my_variable.pickle"):
        window = FinalMainPage.MyWindow()
        window.showMaximized()
        window.show()
    else:
        window = MyWindow()
        window.show()
        # self.close()
    sys.exit(app.exec_())
