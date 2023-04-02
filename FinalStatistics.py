# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FinalStatistics.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import pickle

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject

from Database import Statement,Log,Investment


class Ui_Form(QObject):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(331, 556)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout_10.addWidget(self.label)
        self.Mode = QtWidgets.QComboBox(Form)
        self.Mode.setObjectName("Mode")
        self.Mode.addItem("")
        self.Mode.addItem("")
        self.horizontalLayout_10.addWidget(self.Mode)
        self.Date = QtWidgets.QDateEdit(Form)
        self.Date.setObjectName("Date")
        self.horizontalLayout_10.addWidget(self.Date)
        self.verticalLayout_9.addLayout(self.horizontalLayout_10)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.MoneyAdded_Text = QtWidgets.QLabel(Form)
        self.MoneyAdded_Text.setObjectName("MoneyAdded_Text")
        self.horizontalLayout_12.addWidget(self.MoneyAdded_Text)
        self.MoneyAdded = QtWidgets.QLabel(Form)
        self.MoneyAdded.setObjectName("MoneyAdded")
        self.horizontalLayout_12.addWidget(self.MoneyAdded)
        self.horizontalLayout_14.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.MoneyWithdrawn_Text = QtWidgets.QLabel(Form)
        self.MoneyWithdrawn_Text.setObjectName("MoneyWithdrawn_Text")
        self.horizontalLayout_11.addWidget(self.MoneyWithdrawn_Text)
        self.MoneyWithdrawn = QtWidgets.QLabel(Form)
        self.MoneyWithdrawn.setObjectName("MoneyWithdrawn")
        self.horizontalLayout_11.addWidget(self.MoneyWithdrawn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem1)
        self.horizontalLayout_14.addLayout(self.horizontalLayout_11)
        self.verticalLayout_6.addLayout(self.horizontalLayout_14)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_6.addItem(spacerItem2)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setMinimumSize(QtCore.QSize(0, 200))
        self.widget.setObjectName("widget")
        self.verticalLayout_6.addWidget(self.widget)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_16.addWidget(self.label_15)
        self.label_16 = QtWidgets.QLabel(Form)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_16.addWidget(self.label_16)
        self.horizontalLayout_15.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_20 = QtWidgets.QLabel(Form)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_17.addWidget(self.label_20)
        self.label_21 = QtWidgets.QLabel(Form)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_17.addWidget(self.label_21)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem3)
        self.horizontalLayout_15.addLayout(self.horizontalLayout_17)
        self.verticalLayout_7.addLayout(self.horizontalLayout_15)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_7.addItem(spacerItem4)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.widget_2 = QtWidgets.QWidget(Form)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_18.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(Form)
        self.widget_3.setMinimumSize(QtCore.QSize(0, 200))
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_18.addWidget(self.widget_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_18)
        self.verticalLayout_6.addLayout(self.verticalLayout_7)
        self.verticalLayout_9.addLayout(self.verticalLayout_6)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.AverageProfitLoss_Text = QtWidgets.QLabel(Form)
        self.AverageProfitLoss_Text.setObjectName("AverageProfitLoss_Text")
        self.horizontalLayout_13.addWidget(self.AverageProfitLoss_Text)
        self.AverageProfitLoss = QtWidgets.QLabel(Form)
        self.AverageProfitLoss.setObjectName("AverageProfitLoss")
        self.horizontalLayout_13.addWidget(self.AverageProfitLoss)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem5)
        self.verticalLayout_9.addLayout(self.horizontalLayout_13)
        self.verticalLayout_10.addLayout(self.verticalLayout_9)

        self.SetupPage()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Mode:"))
        self.Mode.setItemText(0, _translate("Form", "Month"))
        self.Mode.setItemText(1, _translate("Form", "Year"))
        self.MoneyAdded_Text.setText(_translate("Form", "Money Added: "))
        self.MoneyWithdrawn_Text.setText(_translate("Form", "Money Withdrawn: "))
        self.label_15.setText(_translate("Form", "Total Investments: "))
        self.label_20.setText(_translate("Form", "Investment Sold:  "))
        self.AverageProfitLoss_Text.setText(_translate("Form", "Average Profit/Loss : "))
        self.AverageProfitLoss.setText(_translate("Form", "TextLabel"))

    def SetupPage(self):
        with open("my_variable.pickle", "rb") as f:
            UserID = pickle.load(f)
        self.Investment = Investment.Investment()
        self.Statement = Statement.Statement()
        self.Log = Log.Log.Money()

        self.Investment.setProfile(UserID)
        self.Statement.setProfile(UserID)
        self.Log.setProfile(UserID)

        self.MoneyAdded.setText(str(self.Log.getMoneyAdded()))
        self.MoneyWithdrawn.setText(str(self.Log.getMoneyOut()))
        self.label_16.setText(str(self.Investment.getInvestmentCount()))
        self.label_21.setText(str(self.Statement.getInvestmentCount()))


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
