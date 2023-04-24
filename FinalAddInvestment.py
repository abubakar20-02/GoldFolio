import datetime

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDate, QObject

import FinalNotEnoughCash
import SetupFile
from Database import Investment, User
from GoldRate import Gold


class Ui_Form(QObject):
    def setupUi(self, Form):
        self.Investment = Investment.Investment()
        self.User = User.User()
        Form.setObjectName("Form")
        Form.resize(383, 305)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Date_Text = QtWidgets.QLabel(Form)
        self.Date_Text.setObjectName("Date_Text")
        self.horizontalLayout.addWidget(self.Date_Text)
        self.Date = QtWidgets.QDateEdit(calendarPopup=True)
        self.Date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.Date.setMaximumDate(QDate.currentDate())
        self.horizontalLayout.addWidget(self.Date)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Gold_Text = QtWidgets.QLabel(Form)
        self.Gold_Text.setObjectName("Gold_Text")
        self.horizontalLayout_2.addWidget(self.Gold_Text)
        self.Gold = QtWidgets.QDoubleSpinBox(Form)
        self.Gold.setObjectName("Gold")
        self.horizontalLayout_2.addWidget(self.Gold)
        self.goldUnit = QtWidgets.QLabel(Form)
        self.goldUnit.setObjectName("goldUnit")
        self.horizontalLayout_2.addWidget(self.goldUnit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.BoughtFor_Text = QtWidgets.QLabel(Form)
        self.BoughtFor_Text.setObjectName("BoughtFor_Text")
        self.horizontalLayout_3.addWidget(self.BoughtFor_Text)
        self.currency = QtWidgets.QLabel(Form)
        self.currency.setObjectName("Currency")
        self.horizontalLayout_3.addWidget(self.currency)
        self.BoughtFor = QtWidgets.QDoubleSpinBox(Form)
        self.BoughtFor.setObjectName("BoughtFor")
        self.horizontalLayout_3.addWidget(self.BoughtFor)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
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
        self.Add = QtWidgets.QPushButton(Form)
        self.Add.setObjectName("Add")
        self.horizontalLayout_5.addWidget(self.Add)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.UseLiveGoldRate.setChecked(True)
        self.BoughtFor.setEnabled(False)
        self.UseLiveGoldRate.clicked.connect(self.useLiveGoldRate)
        self.Date.dateChanged.connect(self.dateChanged)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def updateRate(self, RateinGram):
        """shows cost of the investment"""
        GoldinGram = self.Gold1.convertGtoDifferentUnit(self.Gold.value())
        if not self.UseLiveGoldRate.isChecked():
            self.goldUnit.setText(f"{self.GoldUnit}")
            return
        if GoldinGram > 0:
            self.goldUnit.setText(f"{self.GoldUnit}  {self.Currency}{str(round(GoldinGram * RateinGram,2))}")
        else:
            self.goldUnit.setText(f"{self.GoldUnit}")

    def dateChanged(self):
        """If date is changed the live gold rate is disabled."""
        if not (self.Date.date().toPyDate() == datetime.date.today()):
            self.UseLiveGoldRate.setChecked(False)
            self.UseLiveGoldRate.setEnabled(False)
            self.useLiveGoldRate()
        else:
            self.UseLiveGoldRate.setEnabled(True)
            self.UseLiveGoldRate.setChecked(True)
            self.useLiveGoldRate()

    def useLiveGoldRate(self):
        if self.UseLiveGoldRate.isChecked():
            self.BoughtFor.setEnabled(False)
        else:
            self.BoughtFor.setEnabled(True)
            self.goldUnit.setText(f"{self.GoldUnit}")

    def add(self, Rate, UserID):
        """add investment to the main page."""
        format_str = '%Y-%m-%d'
        Date = self.Date.date().toPyDate()
        date = Date.strftime(format_str)
        Gold = float(self.Gold1.convertGtoDifferentUnit(self.Gold.value()))
        BoughtFor = float(self.BoughtFor.value())

        if self.UseLiveGoldRate.isChecked():
            BoughtFor = Gold * Rate
        self.Investment.setProfile(UserID)
        self.User.SelectProfile(UserID)
        if BoughtFor > self.User.getMoney():
            MoneyMissing = BoughtFor - self.User.getMoney()
            self.window = QtWidgets.QWidget()
            self.window = FinalNotEnoughCash.MyWindow()
            self.window.setUpPage(UserID, MoneyMissing)
            self.window.show()
        else:
            self.Investment.insertIntoTable(Gold, 1, BoughtFor, Date=date)

    def setUpPage(self, UserID):
        """initialize page ui"""
        self.User.SelectProfile(UserID)
        self.loadSettings()
        self.updateVariables()
        self.Gold1 = Gold()
        self.Gold1.changeUnit(self.GoldUnit)

    def loadSettings(self):
        """Get user settings from the user database."""
        _, _, _, self.GoldUnit, self.Currency = self.User.GetSettings()

    def updateVariables(self):
        """Set currency unit and gold unit."""
        self.currency.setText(self.Currency)
        self.goldUnit.setText(self.GoldUnit)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Date_Text.setText(_translate("Form", "Date: "))
        self.Gold_Text.setText(_translate("Form", "Gold:"))
        self.BoughtFor_Text.setText(_translate("Form", "Bought for:"))
        self.UseLiveGoldRate.setText(_translate("Form", "Use live gold rate"))
        self.Add.setText(_translate("Form", "Add"))


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Buy investment")
        self.setStyleSheet(SetupFile.Background)
        self.Date.setStyleSheet(SetupFile.DateEdit)
        self.Gold.setStyleSheet(SetupFile.DoubleSpinBox)
        self.BoughtFor.setStyleSheet(SetupFile.DoubleSpinBox)
        self.Add.setStyleSheet(SetupFile.Button)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
