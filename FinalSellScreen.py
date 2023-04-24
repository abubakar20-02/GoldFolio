import datetime

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDate, QObject

import FinalShowSellInfo
import SetupFile
from Database import Investment
from GoldRate import Gold


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
        self.RateCurrency = QtWidgets.QLabel(Form)
        self.RateCurrency.setObjectName("RateCurrency")
        self.horizontalLayout_2.addWidget(self.RateCurrency)

        self.Rate = QtWidgets.QDoubleSpinBox(Form)
        self.Rate.setObjectName("Rate")
        self.Rate.setMaximum(100000)
        self.horizontalLayout_2.addWidget(self.Rate)
        self.RateUnit = QtWidgets.QLabel(Form)
        self.RateUnit.setObjectName("RateUnit")
        self.horizontalLayout_2.addWidget(self.RateUnit)

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

        self.UseLiveGoldRate.clicked.connect(self.useLiveGoldRate)
        self.Date.dateChanged.connect(self.dateChanged)

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

    def setUpPage(self, Currency, Unit):
        """set up page"""
        self.Currency = Currency
        self.GoldUnit = Unit
        self.RateCurrency.setText(self.Currency)
        self.RateUnit.setText(f"/{self.GoldUnit}")
        self.Gold = Gold(Unit=self.GoldUnit)

    def setProfile(self, Profile):
        """Select profile"""
        self.Profile = Profile

    def Sell1(self, UserProfile, Rate=None, SellDate=None, TransactionIDs=None, StartDate=None, EndDate=None,
              ProfitMargin=None):
        """Sell in either of 3 modes, sell all, sell profit, sell custom"""
        self.window = QtWidgets.QWidget()
        self.window = FinalShowSellInfo.MyWindow()
        StartRate = Rate
        if not self.UseLiveGoldRate.isChecked():
            Rate = self.Gold.converttToRateInGram(self.Rate.value())
        # use user profile to get profit margin.
        self.Investment.setProfile(UserProfile)
        self.Investment.updateProfitLoss(Rate)
        if self.SellMode.currentIndex() == 2:
            Gold, Sum, Value = self.Investment.showSumSale(uniqueID=TransactionIDs)
            self.Investment.sell(TransactionIDs, Rate=Rate, Date=SellDate)
            # Sell custom
        if self.SellMode.currentIndex() == 1:
            Gold, Sum, Value = self.Investment.showSumSale(StartDate=StartDate, EndDate=EndDate)
            self.Investment.sellAll(Rate=Rate, Date=SellDate, StartDate=StartDate, EndDate=EndDate)
            # Sell All
        if self.SellMode.currentIndex() == 0:
            Gold, Sum, Value = self.Investment.showSumSale(StartDate=StartDate, EndDate=EndDate,
                                                           MinimumProfitMargin=ProfitMargin)
            self.Investment.sellProfit(Rate=Rate, Date=SellDate, StartDate=StartDate, EndDate=EndDate,
                                       ProfitMargin=ProfitMargin)
            # Sell Profit
        if Gold is not None and Sum is not None and Value is not None:
            self.window.setUpPage(self.Profile, Gold, Sum, Value)
            self.window.show()
        self.Investment.updateProfitLoss(GoldRate=StartRate)

    def dateChanged(self):
        """if date changed then lock some variables."""
        if not (self.Date.date().toPyDate() == datetime.date.today()):
            self.UseLiveGoldRate.setChecked(False)
            self.UseLiveGoldRate.setEnabled(False)
            self.useLiveGoldRate()
        else:
            self.UseLiveGoldRate.setEnabled(True)
            self.UseLiveGoldRate.setChecked(True)
            self.useLiveGoldRate()

    def useLiveGoldRate(self):
        """user may use live gold rate."""
        if self.UseLiveGoldRate.isChecked():
            self.Rate.setEnabled(False)
        else:
            self.Rate.setEnabled(True)


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Sell investment")
        self.setStyleSheet(SetupFile.Background)
        self.SellMode.setStyleSheet(SetupFile.ComboBox)
        self.Date.setStyleSheet(SetupFile.DateEdit)
        self.Rate.setStyleSheet(SetupFile.DoubleSpinBox)
        self.Sell.setStyleSheet(SetupFile.Button)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
