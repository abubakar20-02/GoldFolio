# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FinalSellScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QObject

from Database import Investment


class Ui_Form(QObject):
    def setupUi(self, Form):
        self.Investment = Investment.Investment()
        Form.setObjectName("Form")
        Form.resize(309, 280)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.SellMode_Text = QtWidgets.QLabel(Form)
        self.SellMode_Text.setObjectName("SellMode_Text")
        self.horizontalLayout_3.addWidget(self.SellMode_Text)
        self.SellMode = QtWidgets.QComboBox(Form)
        self.SellMode.setObjectName("SellMode")
        self.SellMode.addItem("")
        self.SellMode.addItem("")
        self.SellMode.addItem("")
        self.horizontalLayout_3.addWidget(self.SellMode)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Date_Text = QtWidgets.QLabel(Form)
        self.Date_Text.setObjectName("Date_Text")
        self.horizontalLayout.addWidget(self.Date_Text)
        self.Date = QtWidgets.QDateEdit(calendarPopup=True)
        self.Date.setMaximumDate(QDate.currentDate())
        self.Date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.horizontalLayout.addWidget(self.Date)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Rate_Text = QtWidgets.QLabel(Form)
        self.Rate_Text.setObjectName("Rate_Text")
        self.horizontalLayout_2.addWidget(self.Rate_Text)
        self.Rate = QtWidgets.QDoubleSpinBox(Form)
        self.Rate.setObjectName("Rate")
        self.horizontalLayout_2.addWidget(self.Rate)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.UseLiveGoldRate = QtWidgets.QRadioButton(Form)
        self.UseLiveGoldRate.setObjectName("UseLiveGoldRate")
        self.horizontalLayout_4.addWidget(self.UseLiveGoldRate)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.Sell = QtWidgets.QPushButton(Form)
        self.Sell.setObjectName("Sell")
        self.horizontalLayout_5.addWidget(self.Sell)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.SellMode_Text.setText(_translate("Form", "Sell mode:"))
        self.SellMode.setItemText(0, _translate("Form", "Sell profitable"))
        self.SellMode.setItemText(1, _translate("Form", "Sell all"))
        self.SellMode.setItemText(2, _translate("Form", "Custom"))
        self.Date_Text.setText(_translate("Form", "Date:"))
        self.Rate_Text.setText(_translate("Form", "Rate: "))
        self.UseLiveGoldRate.setText(_translate("Form", "Use live gold rate"))
        self.Sell.setText(_translate("Form", "Sell"))

    def Sell1(self, UserProfile, Rate=None, SellDate=None, TransactionIDs=None, StartDate=None, EndDate=None):
        print(Rate)
        # use user profile to get profit margin.
        self.Investment.setProfile(UserProfile)
        if self.SellMode.currentIndex() == 2:
            self.Investment.sell(TransactionIDs, Rate=Rate, Date=SellDate)
            print("Sell custom")
        if self.SellMode.currentIndex() == 1:
            self.Investment.sellAll(Rate=Rate, Date=SellDate, StartDate=StartDate, EndDate=EndDate)
            print("Sell All")
        if self.SellMode.currentIndex() == 0:
            self.Investment.sellProfit(Rate=Rate, Date=SellDate, StartDate=StartDate, EndDate=EndDate)
            print("Sell Profit")
            # sellAll


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