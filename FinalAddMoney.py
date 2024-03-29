from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject

import FinalDialogBox
import SetupFile
from Database import User


class Ui_Form(QObject):
    def setupUi(self, Form):
        self.User = User.User()
        Form.setObjectName("Form")
        Form.setMaximumSize(100, 100)
        Form.setStyleSheet(SetupFile.Background)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.Deposit = QtWidgets.QRadioButton(Form)
        self.Deposit.setObjectName("Deposit")
        self.Deposit.setChecked(True)

        self.horizontalLayout_3.addWidget(self.Deposit)

        self.Withdraw = QtWidgets.QRadioButton(Form)
        self.Withdraw.setObjectName("Withdraw")

        self.horizontalLayout_3.addWidget(self.Withdraw)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.Money_Text = QtWidgets.QLabel(Form)
        self.Money_Text.setObjectName("Money_Text")
        self.horizontalLayout.addWidget(self.Money_Text)

        self.Currency = QtWidgets.QLabel(Form)
        self.Currency.setObjectName("Currency")
        self.horizontalLayout.addWidget(self.Currency)

        self.Money = QtWidgets.QDoubleSpinBox(Form)
        self.Money.setMaximum(1000000.0)
        self.Money.setObjectName("Money")
        self.Money.setStyleSheet(SetupFile.DoubleSpinBox)
        self.horizontalLayout.addWidget(self.Money)

        spacerItem = QtWidgets.QSpacerItem(561, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)

        self.AddMoney = QtWidgets.QPushButton(Form)
        self.AddMoney.setObjectName("AddMoney")
        self.AddMoney.setStyleSheet(SetupFile.Button)
        self.horizontalLayout_2.addWidget(self.AddMoney)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.Deposit.clicked.connect(self.checkDeposit)
        self.Withdraw.clicked.connect(self.checkDeposit)

        self.AddMoney.clicked.connect(self.AddWithdrawCash)

        self.AddMoney.clicked.connect(self.close)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Deposit.setText(_translate("Form", "Deposit"))
        self.Withdraw.setText(_translate("Form", "Withdraw"))
        self.Money_Text.setText(_translate("Form", "Money: "))
        self.AddMoney.setText(_translate("Form", "Add Cash"))

    def setUserID(self, UserID):
        """Set user ID to the page"""
        self.User.SelectProfile(UserID)
        self.loadSettings()
        self.Currency.setText(self.currency)

    def checkDeposit(self):
        """update button to display appropriate text"""
        if self.Deposit.isChecked():
            self.AddMoney.setText("Deposit Cash")
        else:
            self.AddMoney.setText("Withdraw Cash")

    def AddWithdrawCash(self):
        if self.Deposit.isChecked():
            self.addMoney()
        else:
            self.withdrawMoney()

    def addMoney(self):
        """Add money to the system."""
        self.User.addMoney(self.Money.value())

    def withdrawMoney(self):
        """withdraw cash from the system."""
        if self.Money.value() > self.User.getMoney():
            self.window = QtWidgets.QWidget()
            self.window = FinalDialogBox.MyWindow()
            self.window.setText("You do not have enough money!")
            self.window.OkButton.setHidden(True)
            self.window.CancelButton.setText("Close")
            self.window.show()
        else:
            self.User.cashout(self.Money.value())

    def loadSettings(self):
        """load user settings"""
        _, _, _, _, self.currency = self.User.GetSettings()


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

