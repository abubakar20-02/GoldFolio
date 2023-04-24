import bcrypt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QLineEdit

import SetupFile
from Database import User


def verify_password(password, hashed_password):
    """hash password then compare to hashed password."""
    password_bytes = password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password)

class Ui_Form(QObject):

    def setProfile(self, Profile):
        """Select user ID"""
        self.Profile = Profile
        self.User = User.User()
        self.User.SelectProfile(Profile)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(411, 289)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.password_Text = QtWidgets.QLabel(Form)
        self.password_Text.setObjectName("password_Text")
        self.horizontalLayout_4.addWidget(self.password_Text)
        self.password = QtWidgets.QLineEdit(Form)
        self.password.setObjectName("password")
        self.horizontalLayout_4.addWidget(self.password)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.showPassword = QtWidgets.QRadioButton(Form)
        self.showPassword.setObjectName("showPassword")
        self.horizontalLayout_3.addWidget(self.showPassword)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem5)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.Error = QtWidgets.QLabel(Form)
        self.Error.setObjectName("Error")
        self.Error.setHidden(True)
        self.horizontalLayout_6.addWidget(self.Error)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem8)
        self.deleteButton = QtWidgets.QPushButton(Form)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout_5.addWidget(self.deleteButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.showPassword.setChecked(False)
        self.checkbutton()
        self.deleteButton.clicked.connect(self.passwordCorrect)
        self.showPassword.clicked.connect(self.checkbutton)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Are you sure you want to delete your account?"))
        self.label_2.setText(_translate("Form", "Once deleted, your account cannot be recovered."))
        self.password_Text.setText(_translate("Form", "Password: "))
        self.showPassword.setText(_translate("Form", "Show password"))
        self.deleteButton.setText(_translate("Form", "Delete"))

    def checkbutton(self):
        """If show password is set enabled then show password text."""
        if self.showPassword.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def passwordCorrect(self):
        """If wrong password entered, give warning."""
        isPassCorrect = verify_password(self.password.text(), self.User.getHashedPassword(self.Profile))
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
        self.setWindowTitle("Delete account")  # set the window title
        self.setStyleSheet(SetupFile.Background)
        self.deleteButton.setStyleSheet(SetupFile.Button)
        self.password.setStyleSheet(SetupFile.QLineEdit)


