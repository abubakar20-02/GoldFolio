from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject

import SetupFile
from Database import User
from GoldRate import Gold


class Ui_Form(QObject):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(418, 255)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.totalGoldSold_Text = QtWidgets.QLabel(Form)
        self.totalGoldSold_Text.setObjectName("totalGoldSold_Text")
        self.horizontalLayout.addWidget(self.totalGoldSold_Text)
        self.totalGoldSold = QtWidgets.QLabel(Form)
        self.totalGoldSold.setObjectName("totalGoldSold")
        self.horizontalLayout.addWidget(self.totalGoldSold)
        self.goldUnit = QtWidgets.QLabel(Form)
        self.goldUnit.setObjectName("goldUnit")
        self.horizontalLayout.addWidget(self.goldUnit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.totalBoughtFor_Text = QtWidgets.QLabel(Form)
        self.totalBoughtFor_Text.setObjectName("totalBoughtFor_Text")
        self.horizontalLayout_2.addWidget(self.totalBoughtFor_Text)
        self.currency = QtWidgets.QLabel(Form)
        self.currency.setObjectName("currency")
        self.horizontalLayout_2.addWidget(self.currency)
        self.totalBoughtFor = QtWidgets.QLabel(Form)
        self.totalBoughtFor.setObjectName("totalBoughtFor")
        self.horizontalLayout_2.addWidget(self.totalBoughtFor)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.totalValueChange_Text = QtWidgets.QLabel(Form)
        self.totalValueChange_Text.setObjectName("totalValueChange_Text")
        self.horizontalLayout_3.addWidget(self.totalValueChange_Text)
        self.currency_2 = QtWidgets.QLabel(Form)
        self.currency_2.setObjectName("currency_2")
        self.horizontalLayout_3.addWidget(self.currency_2)
        self.totalValueChange = QtWidgets.QLabel(Form)
        self.totalValueChange.setObjectName("totalValueChange")
        self.horizontalLayout_3.addWidget(self.totalValueChange)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.closeButton = QtWidgets.QPushButton(Form)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_4.addWidget(self.closeButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def setUpPage(self, UserID, GoldWeight, Sum, Value):
        """Set up page"""
        self.User = User.User()
        self.User.SelectProfile(UserID)
        self.loadSettings()
        self.Gold = Gold()
        self.Gold.changeUnit(self.GoldUnit)

        self.GoldWeight = self.Gold.convertWeight(GoldWeight)
        self.Sum = Sum
        self.Value = Value
        self.updateVariables()

    def loadSettings(self):
        """Load user settings"""
        _, self.DecimalPoints, _, self.GoldUnit, self.Currency = self.User.GetSettings()

    def updateVariables(self):
        """set value and unit of currency,and gold unit """
        self.currency.setText(self.Currency)
        self.currency_2.setText(self.Currency)
        self.goldUnit.setText(self.GoldUnit)

        if self.Value > 0:
            self.totalValueChange.setStyleSheet(SetupFile.Positive)
            self.currency_2.setStyleSheet(SetupFile.Positive)
        elif self.Value < 0:
            self.totalValueChange.setStyleSheet(SetupFile.Negative)
            self.currency_2.setStyleSheet(SetupFile.Negative)

        self.totalGoldSold.setText(str(round(self.GoldWeight, self.DecimalPoints)))
        self.totalBoughtFor.setText(str(round(self.Sum, self.DecimalPoints)))
        self.totalValueChange.setText(str(round(self.Value, self.DecimalPoints)))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.totalGoldSold_Text.setText(_translate("Form", "Total gold sold:  "))
        self.totalBoughtFor_Text.setText(_translate("Form", "Total bought for: "))
        self.totalValueChange_Text.setText(_translate("Form", "Total value change:  "))
        self.closeButton.setText(_translate("Form", "Close"))


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.closeButton.clicked.connect(self.close)
        self.setWindowTitle("Sell info")
        self.setStyleSheet(SetupFile.Background)
        self.closeButton.setStyleSheet(SetupFile.Button)



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
