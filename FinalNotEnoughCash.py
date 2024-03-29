from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject

import FinalAddMoney
import SetupFile
from Database import User


class Ui_Form(QObject):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.text = QtWidgets.QLabel(Form)
        self.text.setObjectName("text")
        self.verticalLayout.addWidget(self.text)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.text_2 = QtWidgets.QLabel(Form)
        self.text_2.setObjectName("text_2")
        self.horizontalLayout.addWidget(self.text_2)
        self.Cash = QtWidgets.QLabel(Form)
        self.Cash.setObjectName("Cash")
        self.horizontalLayout.addWidget(self.Cash)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.closeButton = QtWidgets.QPushButton(Form)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.addCashButton = QtWidgets.QPushButton(Form)
        self.addCashButton.setObjectName("addCashButton")
        self.horizontalLayout_2.addWidget(self.addCashButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.text.setText(_translate("Form", "You do not have enough cash!"))
        self.text_2.setText(_translate("Form", "You are short by : "))
        self.Cash.setText(_translate("Form", "TextLabel"))
        self.closeButton.setText(_translate("Form", "Close"))
        self.addCashButton.setText(_translate("Form", "Add Cash"))

    def setUpPage(self, UserID, MoneyMissing):
        """Setup ui page"""
        self.UserID = UserID
        self.User = User.User()
        self.User.SelectProfile(self.UserID)
        self.loadSettings()
        self.MoneyMissing = MoneyMissing

        self.updateVariables()

    def updateVariables(self):
        """Set currency unit and value missing in the correct dp"""
        self.Cash.setText(f"{self.Currency} {round(self.MoneyMissing,self.DecimalPoints)}")

    def loadSettings(self):
        """load user settings."""
        _, self.DecimalPoints, _, _, self.Currency = self.User.GetSettings()

    def openAddCash(self):
        """open add cash screen."""
        self.window = QtWidgets.QWidget()
        self.window = FinalAddMoney.MyWindow()
        self.window.setUserID(self.UserID)
        self.window.Money.setValue(self.MoneyMissing)
        self.window.show()
        self.close()

class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.closeButton.clicked.connect(self.close)
        self.addCashButton.clicked.connect(self.openAddCash)

        self.setWindowTitle("Warning")
        self.setStyleSheet(SetupFile.Background)
        self.closeButton.setStyleSheet(SetupFile.Button)
        self.addCashButton.setStyleSheet(SetupFile.Button)

