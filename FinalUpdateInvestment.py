from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject

import SetupFile
from Database import User, Investment


class Ui_Form(QObject):
    def setupUi(self, Form):
        self.User = User.User()
        self.Investment = Investment.Investment()
        Form.setObjectName("Form")
        Form.resize(344, 209)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.goldText = QtWidgets.QLabel(Form)
        self.goldText.setObjectName("goldText")
        self.horizontalLayout.addWidget(self.goldText)
        self.gold = QtWidgets.QDoubleSpinBox(Form)
        self.gold.setObjectName("gold")
        self.horizontalLayout.addWidget(self.gold)
        self.goldUnit = QtWidgets.QLabel(Form)
        self.goldUnit.setObjectName("goldUnit")
        self.horizontalLayout.addWidget(self.goldUnit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.goldText_2 = QtWidgets.QLabel(Form)
        self.goldText_2.setObjectName("goldText_2")
        self.horizontalLayout_2.addWidget(self.goldText_2)
        self.currency = QtWidgets.QLabel(Form)
        self.currency.setObjectName("currency")
        self.horizontalLayout_2.addWidget(self.currency)
        self.boughtFor = QtWidgets.QDoubleSpinBox(Form)
        self.boughtFor.setObjectName("boughtFor")
        self.horizontalLayout_2.addWidget(self.boughtFor)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.updateButton = QtWidgets.QPushButton(Form)
        self.updateButton.setObjectName("updateButton")
        self.horizontalLayout_3.addWidget(self.updateButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.updateButton.clicked.connect(self.Update)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.goldText.setText(_translate("Form", "Gold: "))
        self.goldUnit.setText(_translate("Form", "g"))
        self.goldText_2.setText(_translate("Form", "Bought for: "))
        self.updateButton.setText(_translate("Form", "Update"))

        self.boughtFor.setMaximum(1000000)
        self.gold.setMaximum(1000000)

    def loadSettings(self):
        """load user settings"""
        _, _, _, _, self.Currency = self.User.GetSettings()

    def setUpPage(self, InvestmentID,UserID):
        """setup ui page"""
        self.User = User.User()
        self.User.SelectProfile(UserID)
        self.loadSettings()
        self.InvestmentID = InvestmentID
        self.UserID = UserID
        self.Gold, self.BoughtFor = self.Investment.getInvestmentDetail(InvestmentID)
        self.gold.setValue(self.Gold)
        self.boughtFor.setValue(self.BoughtFor)
        self.currency.setText(self.Currency)

    def Update(self):
        """update investments."""
        if self.gold.value() == self.Gold and self.boughtFor.value() == self.BoughtFor:
            return
        self.Investment.setProfile(self.UserID)
        self.Investment.updateRecord(self.InvestmentID, self.gold.value(), self.boughtFor.value())
        self.close()


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Update investment")
        self.setStyleSheet(SetupFile.Background)
        self.gold.setStyleSheet(SetupFile.DoubleSpinBox)
        self.boughtFor.setStyleSheet(SetupFile.DoubleSpinBox)
        self.updateButton.setStyleSheet(SetupFile.Button)

