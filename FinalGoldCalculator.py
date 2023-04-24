from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject

import SetupFile
from GoldRate import Gold


class Ui_MainWindow(QObject):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(369, 301)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Gold_Text = QtWidgets.QLabel(self.centralwidget)
        self.Gold_Text.setObjectName("Gold_Text")
        self.horizontalLayout.addWidget(self.Gold_Text)
        self.Gold = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.Gold.setKeyboardTracking(True)
        self.Gold.setObjectName("Gold")
        self.horizontalLayout.addWidget(self.Gold)
        self.goldUnit = QtWidgets.QLabel(self.centralwidget)
        self.goldUnit.setObjectName("goldUnit")
        self.horizontalLayout.addWidget(self.goldUnit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.currency = QtWidgets.QLabel(self.centralwidget)
        self.currency.setObjectName("currency")
        self.horizontalLayout_3.addWidget(self.currency)
        self.Cost = QtWidgets.QLabel(self.centralwidget)
        self.Cost.setObjectName("Cost")
        self.horizontalLayout_3.addWidget(self.Cost)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.Purity_Text = QtWidgets.QLabel(self.centralwidget)
        self.Purity_Text.setObjectName("Purity_Text")
        self.horizontalLayout_4.addWidget(self.Purity_Text)
        self.Purity = QtWidgets.QComboBox(self.centralwidget)
        self.Purity.setObjectName("Purity")
        self.Purity.addItem("")
        self.Purity.addItem("")
        self.Purity.addItem("")
        self.Purity.addItem("")
        self.Purity.addItem("")
        self.Purity.addItem("")
        self.Purity.addItem("")
        self.Purity.addItem("")
        self.Purity.addItem("")
        self.horizontalLayout_4.addWidget(self.Purity)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.Check = QtWidgets.QPushButton(self.centralwidget)
        self.Check.setObjectName("Check")
        self.horizontalLayout_2.addWidget(self.Check)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Gold_Text.setText(_translate("MainWindow", "Gold :"))
        self.label_3.setText(_translate("MainWindow", "Cost: "))
        self.Cost.setText(_translate("MainWindow", "0"))
        self.Purity_Text.setText(_translate("MainWindow", "Purity:"))
        self.Purity.setItemText(0, _translate("MainWindow", "24K"))
        self.Purity.setItemText(1, _translate("MainWindow", "22K"))
        self.Purity.setItemText(2, _translate("MainWindow", "21K"))
        self.Purity.setItemText(3, _translate("MainWindow", "18K"))
        self.Purity.setItemText(4, _translate("MainWindow", "16K"))
        self.Purity.setItemText(5, _translate("MainWindow", "14K"))
        self.Purity.setItemText(6, _translate("MainWindow", "12K"))
        self.Purity.setItemText(7, _translate("MainWindow", "10K"))
        self.Purity.setItemText(8, _translate("MainWindow", "9K"))
        self.Check.setText(_translate("MainWindow", "Check"))

    def setUpPage(self, Currency, Unit, DecimalPoint):
        """Set up Ui page"""
        self.Currency = Currency
        self.Unit = Unit
        self.DecimalPoint = DecimalPoint

        self.Gold1 = Gold(Currency=Currency, Unit=Unit)
        self.goldUnit.setText(Unit)
        self.currency.setText(Currency)

    def getRate(self, Rate):
        """get rate of the given gold"""

        if self.Purity.currentIndex() == 0:
            Purity = 24
        if self.Purity.currentIndex() == 1:
            Purity = 22
        if self.Purity.currentIndex() == 2:
            Purity = 21
        if self.Purity.currentIndex() == 3:
            Purity = 18
        if self.Purity.currentIndex() == 4:
            Purity = 16
        if self.Purity.currentIndex() == 5:
            Purity = 14
        if self.Purity.currentIndex() == 6:
            Purity = 12
        if self.Purity.currentIndex() == 7:
            Purity = 10
        if self.Purity.currentIndex() == 8:
            Purity = 9
        self.Gold1.getLatestExchangeRate()
        self.Cost.setText(str(round(
            Rate * self.Gold1.convertGtoDifferentUnit(self.Gold.value()) * (Purity / 24),
            self.DecimalPoint)))


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle("Gold calculator")
        self.setStyleSheet(SetupFile.Background)
        self.Gold.setStyleSheet(SetupFile.DoubleSpinBox)
        self.Purity.setStyleSheet(SetupFile.ComboBox)
        self.Check.setStyleSheet(SetupFile.Button)


