# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FinalAddUser.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from Database import User


class Ui_Form(object):
    def setupUi(self, Form):
        self.User = User.User()
        Form.setObjectName("Form")
        Form.resize(727, 441)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.FirstName_Text = QtWidgets.QLabel(Form)
        self.FirstName_Text.setObjectName("FirstName_Text")
        self.horizontalLayout.addWidget(self.FirstName_Text)
        self.FirstName = QtWidgets.QLineEdit(Form)
        self.FirstName.setObjectName("FirstName")
        self.horizontalLayout.addWidget(self.FirstName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LastName_Text = QtWidgets.QLabel(Form)
        self.LastName_Text.setObjectName("LastName_Text")
        self.horizontalLayout_2.addWidget(self.LastName_Text)
        self.LastName = QtWidgets.QLineEdit(Form)
        self.LastName.setObjectName("LastName")
        self.horizontalLayout_2.addWidget(self.LastName)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.currency_Text = QtWidgets.QLabel(Form)
        self.currency_Text.setObjectName("currency_Text")
        self.horizontalLayout_8.addWidget(self.currency_Text)
        self.currency = QtWidgets.QComboBox(Form)
        self.currency.setObjectName("currency")
        self.currency.addItem("")
        self.currency.addItem("")
        self.currency.addItem("")
        self.horizontalLayout_8.addWidget(self.currency)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.StartingMoney_Text = QtWidgets.QLabel(Form)
        self.StartingMoney_Text.setObjectName("StartingMoney_Text")
        self.horizontalLayout_5.addWidget(self.StartingMoney_Text)
        self.currencySymbol = QtWidgets.QLabel(Form)
        self.currencySymbol.setObjectName("currencySymbol")
        self.horizontalLayout_5.addWidget(self.currencySymbol)
        self.Money = QtWidgets.QDoubleSpinBox(Form)
        self.Money.setObjectName("Money")
        self.Money.setMaximum(1000000)
        self.horizontalLayout_5.addWidget(self.Money)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Password_Text = QtWidgets.QLabel(Form)
        self.Password_Text.setObjectName("Password_Text")
        self.horizontalLayout_3.addWidget(self.Password_Text)
        self.Password = QtWidgets.QLineEdit(Form)
        self.Password.setObjectName("Password")
        self.horizontalLayout_3.addWidget(self.Password)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ReEnterPassword_Text = QtWidgets.QLabel(Form)
        self.ReEnterPassword_Text.setObjectName("ReEnterPassword_Text")
        self.horizontalLayout_4.addWidget(self.ReEnterPassword_Text)
        self.ReEnterPassword = QtWidgets.QLineEdit(Form)
        self.ReEnterPassword.setObjectName("ReEnterPassword")
        self.horizontalLayout_4.addWidget(self.ReEnterPassword)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_7.addWidget(self.radioButton)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem7)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem8)
        self.Error = QtWidgets.QLabel(Form)
        self.Error.setObjectName("Error")
        self.horizontalLayout_9.addWidget(self.Error)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem9)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem10)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem11)
        self.CreateButton = QtWidgets.QPushButton(Form)
        self.CreateButton.setObjectName("CreateButton")
        self.horizontalLayout_6.addWidget(self.CreateButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.currency.currentIndexChanged.connect(self.updateCurrencyText)
        self.CreateButton.clicked.connect(self.AddUser)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def updateCurrencyText(self):
        self.currencySymbol.setText(self.getCurrency())

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.FirstName_Text.setText(_translate("Form", "First name: "))
        self.LastName_Text.setText(_translate("Form", "Last name: "))
        self.currency_Text.setText(_translate("Form", "Currency: "))
        self.currency.setItemText(0, _translate("Form", "$ USD "))
        self.currency.setItemText(1, _translate("Form", "£ GBP"))
        self.currency.setItemText(2, _translate("Form", "€  EUR"))
        self.StartingMoney_Text.setText(_translate("Form", "Starting money: "))
        self.currencySymbol.setText(_translate("Form", "$"))
        self.Password_Text.setText(_translate("Form", "Password: "))
        self.ReEnterPassword_Text.setText(_translate("Form", "Re-enter Password:"))
        self.radioButton.setText(_translate("Form", "RadioButton"))
        self.Error.setText(_translate("Form", "TextLabel"))
        self.CreateButton.setText(_translate("Form", "Create"))

    def getCurrency(self):
        if self.currency.currentIndex() == 0:
            return "$"
        if self.currency.currentIndex() == 1:
            return "£"
        if self.currency.currentIndex() == 2:
            return "€"

    def AddUser(self):
        if self.Password.text() == self.ReEnterPassword.text():
            self.User.insertIntoTable(self.FirstName.text(), self.LastName.text(), self.Money.value(),
                                      self.Password.text(), self.getCurrency(), LogChanges=False)
        else:
            self.Error.setText("password does not match")


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
