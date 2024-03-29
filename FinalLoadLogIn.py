import ast

import bcrypt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QLineEdit

import SetupFile


def verify_password(password, hashed_password):
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)

class Ui_Form(QObject):
    def setProfile(self, Profile,Pass):
        """Set up profile."""
        self.Pass = Pass
        self.userID.setText(Profile)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(283, 213)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.userID_Text = QtWidgets.QLabel(Form)
        self.userID_Text.setObjectName("userID_Text")
        self.horizontalLayout_3.addWidget(self.userID_Text)
        self.userID = QtWidgets.QLabel(Form)
        self.userID.setObjectName("userID")
        self.horizontalLayout_3.addWidget(self.userID)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.password_Text = QtWidgets.QLabel(Form)
        self.password_Text.setObjectName("password_Text")
        self.horizontalLayout.addWidget(self.password_Text)
        self.password = QtWidgets.QLineEdit(Form)
        self.password.setObjectName("password")
        self.horizontalLayout.addWidget(self.password)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.showPassword = QtWidgets.QRadioButton(Form)
        self.showPassword.setObjectName("showPassword")
        self.horizontalLayout_2.addWidget(self.showPassword)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.Error = QtWidgets.QLabel(Form)
        self.Error.setObjectName("Error")
        self.horizontalLayout_4.addWidget(self.Error)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.loadButton = QtWidgets.QPushButton(Form)
        self.loadButton.setObjectName("loadButton")
        self.horizontalLayout_5.addWidget(self.loadButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.Error.setHidden(True)
        self.showPassword.setChecked(False)
        self.checkbutton()
        self.loadButton.clicked.connect(self.passwordCorrect)
        self.showPassword.clicked.connect(self.checkbutton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "The file you are trying to load is for a different profile."))
        self.label_3.setText(_translate("Form", "Please log in to load this profile."))
        self.userID_Text.setText(_translate("Form", "User name: "))
        self.password_Text.setText(_translate("Form", "Password: "))
        self.showPassword.setText(_translate("Form", "Show password"))
        self.Error.setText(_translate("Form", "TextLabel"))
        self.loadButton.setText(_translate("Form", "Load"))

    def checkbutton(self):
        """if show password is set enabled then show password."""
        if self.showPassword.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def passwordCorrect(self):
        """log in if password is correct else tell wrong password."""
        string_val = self.Pass
        bytes_val = ast.literal_eval(string_val)
        isPassCorrect = verify_password(self.password.text(), bytes_val)
        if isPassCorrect is False:
            self.Error.setText("Wrong password!")
            self.Error.setHidden(False)
            return False
        else:
            self.close()
            return True

class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Load state")
        self.setStyleSheet(SetupFile.Background)
        self.password.setStyleSheet(SetupFile.QLineEdit)
        self.loadButton.setStyleSheet(SetupFile.Button)


