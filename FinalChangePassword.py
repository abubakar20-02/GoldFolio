from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QLineEdit

import SetupFile
from Database import User


class Ui_Form(QObject):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 473)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.FullName_Text = QtWidgets.QLabel(Form)
        self.FullName_Text.setObjectName("FullName_Text")
        self.horizontalLayout_2.addWidget(self.FullName_Text)
        self.FullName = QtWidgets.QLabel(Form)
        self.FullName.setObjectName("FullName")
        self.horizontalLayout_2.addWidget(self.FullName)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_6.addWidget(self.radioButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_4.addWidget(self.label_7)
        self.Password = QtWidgets.QLineEdit(Form)
        self.Password.setObjectName("Password")
        self.Password.setEchoMode(QLineEdit.Password)
        self.horizontalLayout_4.addWidget(self.Password)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_5.addWidget(self.label_9)
        self.ReEnterPassword = QtWidgets.QLineEdit(Form)
        self.Password.setEchoMode(QLineEdit.Password)
        self.ReEnterPassword.setObjectName("ReEnterPassword")
        self.horizontalLayout_5.addWidget(self.ReEnterPassword)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem6)
        self.SaveButton = QtWidgets.QPushButton(Form)
        self.SaveButton.setObjectName("SaveButton")
        self.horizontalLayout_7.addWidget(self.SaveButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.radioButton.clicked.connect(self.checkbutton)
        self.SaveButton.clicked.connect(lambda: self.Save(self.User.Profile))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def checkbutton(self):
        """checks if show password button is enabled, and if so, show password"""
        if self.radioButton.isChecked():
            self.Password.setEchoMode(QLineEdit.Normal)
            self.ReEnterPassword.setEchoMode(QLineEdit.Normal)
        else:
            self.Password.setEchoMode(QLineEdit.Password)
            self.ReEnterPassword.setEchoMode(QLineEdit.Password)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.FullName_Text.setText(_translate("Form", "Name : "))
        self.FullName.setText(_translate("Form", "TextLabel"))
        self.radioButton.setText(_translate("Form", "Show passwords"))
        self.label_7.setText(_translate("Form", "Password : "))
        self.label_9.setText(_translate("Form", "Re-enter password : "))
        self.SaveButton.setText(_translate("Form", "Save"))

    def setupPage(self, UserID):
        """set up ui page using userID"""
        self.User = User.User()
        self.User.SelectProfile(UserID)
        self.FullName.setText(self.User.getName())

    def Save(self, UserID):
        """change password if password matches."""
        if self.Password.text() == self.ReEnterPassword.text():
            self.User.UpdatePassword(UserID, self.Password.text())


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Change password")
        self.setStyleSheet(SetupFile.Background)
        self.Password.setStyleSheet(SetupFile.QLineEdit)
        self.ReEnterPassword.setStyleSheet(SetupFile.QLineEdit)
        self.SaveButton.setStyleSheet(SetupFile.Button)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
