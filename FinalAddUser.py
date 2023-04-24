import pickle

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLineEdit

import FinalMainPage
import GoldFolio
import SetupFile
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
        self.showPassword = QtWidgets.QRadioButton(Form)
        self.showPassword.setObjectName("showPassword")
        self.horizontalLayout_7.addWidget(self.showPassword)
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

        self.Error.setHidden(True)
        self.checkbutton()
        self.showPassword.clicked.connect(self.checkbutton)
        self.currency.currentIndexChanged.connect(self.updateCurrencyText)
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
        self.showPassword.setText(_translate("Form", "Show password"))
        self.CreateButton.setText(_translate("Form", "Create"))

    def checkbutton(self):
        """checks if password is checked and if so show password"""
        if self.showPassword.isChecked():
            self.Password.setEchoMode(QLineEdit.Normal)
            self.ReEnterPassword.setEchoMode(QLineEdit.Normal)
        else:
            self.Password.setEchoMode(QLineEdit.Password)
            self.ReEnterPassword.setEchoMode(QLineEdit.Password)

    def getCurrency(self):
        """get the currency the user has selected."""
        if self.currency.currentIndex() == 0:
            return "$"
        if self.currency.currentIndex() == 1:
            return "£"
        if self.currency.currentIndex() == 2:
            return "€"


    def openMainPage(self):
        """launch the main page."""
        self.window = QtWidgets.QMainWindow()
        self.window = FinalMainPage.MyWindow()
        self.window.show()


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.CreateButton.clicked.connect(self.AddUser)

        self.setWindowTitle("Add user")
        self.setStyleSheet(SetupFile.Background)
        self.FirstName.setStyleSheet(SetupFile.QLineEdit)
        self.LastName.setStyleSheet(SetupFile.QLineEdit)
        self.currency.setStyleSheet(SetupFile.ComboBox)
        self.Money.setStyleSheet(SetupFile.DoubleSpinBox)
        self.Password.setStyleSheet(SetupFile.QLineEdit)
        self.ReEnterPassword.setStyleSheet(SetupFile.QLineEdit)
        self.CreateButton.setStyleSheet(SetupFile.Button)

    def AddUser(self):
        """Add user to the database"""
        if self.FirstName.text() == "" or self.LastName.text() == "":
            self.Error.setText("User credentials are incorrect")
            self.Error.setHidden(False)
            return
        if not self.Password.text() == self.ReEnterPassword.text():
            self.Error.setText("password does not match")
            self.Error.setHidden(False)
            return
        UserID = self.User.generate_unique_initials(self.FirstName.text(), self.LastName.text())
        self.User.insertIntoTable(self.FirstName.text(), self.LastName.text(), self.Money.value(),
                                  self.Password.text(), self.getCurrency(), LogChanges=False)
        # log user in
        with open("my_variable.pickle", "wb") as f:
            pickle.dump(UserID, f)
        self.close()
        self.openMainPage()

    def closeEvent(self, event):
        self.openLogInScreen()

    def openLogInScreen(self):
        """open log in screen"""
        self.window = QtWidgets.QWidget()
        self.window = GoldFolio.MyWindow()
        self.window.show()

