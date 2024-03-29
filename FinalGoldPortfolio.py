import pickle

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import SetupFile
from Database import Investment, User
from GoldRate import Gold


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Ui_Form(QObject):
    def setupUi(self, Form):
        self.Investment = Investment.Investment()
        self.User = User.User()
        Form.setObjectName("Form")
        Form.resize(334, 520)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.setMinimumSize(QtCore.QSize(500, 500))
        self.canvas.setObjectName("canvas")
        self.horizontalLayout_6.addWidget(self.canvas)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.SummaryWidget = QtWidgets.QWidget(Form)
        self.SummaryWidget.setObjectName("SummaryWidget")
        self.SummaryWidget.setStyleSheet("background-color: white;")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.SummaryWidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Summary_Text = QtWidgets.QLabel(self.SummaryWidget)
        self.Summary_Text.setObjectName("Summary_Text")
        self.horizontalLayout_2.addWidget(self.Summary_Text)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.SummaryWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Gold_Text = QtWidgets.QLabel(self.SummaryWidget)
        self.Gold_Text.setObjectName("Gold_Text")
        self.horizontalLayout.addWidget(self.Gold_Text)
        self.CurrentGoldValue = QtWidgets.QLabel(self.SummaryWidget)
        self.CurrentGoldValue.setObjectName("CurrentGoldValue")
        self.horizontalLayout.addWidget(self.CurrentGoldValue)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.TotalAcquisition_Text = QtWidgets.QLabel(self.SummaryWidget)
        self.TotalAcquisition_Text.setObjectName("TotalAcquisition_Text")
        self.horizontalLayout_4.addWidget(self.TotalAcquisition_Text)
        self.GoldCost = QtWidgets.QLabel(self.SummaryWidget)
        self.GoldCost.setObjectName("GoldCost")
        self.horizontalLayout_4.addWidget(self.GoldCost)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.TotalOwned_Text = QtWidgets.QLabel(self.SummaryWidget)
        self.TotalOwned_Text.setObjectName("TotalOwned_Text")
        self.horizontalLayout_3.addWidget(self.TotalOwned_Text)
        self.TotalGoldWeight = QtWidgets.QLabel(self.SummaryWidget)
        self.TotalGoldWeight.setObjectName("TotalGoldWeight")
        self.horizontalLayout_3.addWidget(self.TotalGoldWeight)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.line_2 = QtWidgets.QFrame(self.SummaryWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.CashBalance_Text = QtWidgets.QLabel(self.SummaryWidget)
        self.CashBalance_Text.setObjectName("CashBalance_Text")
        self.horizontalLayout_5.addWidget(self.CashBalance_Text)
        self.Cash = QtWidgets.QLabel(self.SummaryWidget)
        self.Cash.setObjectName("Cash")
        self.horizontalLayout_5.addWidget(self.Cash)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem8)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_5.addWidget(self.SummaryWidget)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.Gold_Text.setStyleSheet(SetupFile.GoldColorText)
        self.CurrentGoldValue.setStyleSheet(SetupFile.GoldColorText)

        self.CashBalance_Text.setStyleSheet(SetupFile.BlueColorText)
        self.Cash.setStyleSheet(SetupFile.BlueColorText)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Summary_Text.setText(_translate("Form", "Summary"))
        self.Gold_Text.setText(_translate("Form", "Gold value: "))
        self.TotalAcquisition_Text.setText(_translate("Form", "Total Acquisition Cost: "))
        self.TotalOwned_Text.setText(_translate("Form", "Total Owned: "))
        self.CashBalance_Text.setText(_translate("Form", "Cash Balance: "))

    def setCurrentGoldRate(self, Rate):
        """use current gold rate to find current gold value."""
        self.Rate = Rate
        self.CurrentGoldValue.setText(f"{self.Currency} " + str(round(self.Investment.getSUM("Gold") * self.Rate, self.DecimalPoints)))
        self.pie()

    def setupPage(self):
        """Set up ui page."""
        with open("my_variable.pickle", "rb") as f:
            self.UserID = pickle.load(f)
        self.Investment.setProfile(self.UserID)
        self.User.SelectProfile(self.UserID)
        _, self.DecimalPoints, _, self.GoldUnit, self.Currency = self.User.GetSettings()
        self.Gold = Gold(Unit=self.GoldUnit)
        self.GoldCost.setText(f"{self.Currency} " + str(round(self.Investment.getGoldAcquisitionCost(), self.DecimalPoints)))
        self.TotalGoldWeight.setText(str(round(self.Gold.convertWeight(self.Investment.getSUM("Gold")), self.DecimalPoints)) + f" {self.GoldUnit}")
        self.Cash.setText(f"{self.Currency} " + str(round(self.User.getMoney(), self.DecimalPoints)))

    def pie(self):
        """draw pie graph"""
        a = ("RawCash", round(self.User.getMoney(), self.DecimalPoints))
        b = ("GoldMoney", round(self.Investment.getSUM("Gold") * self.Rate, self.DecimalPoints))
        data = dict([a, b])
        colors = [SetupFile.BlueColor, SetupFile.GoldColor]
        data_without_zero = {k: v for k, v in data.items() if v > 0}
        names = list(data_without_zero.keys())
        values = list(data_without_zero.values())
        wp = {'linewidth': 1, 'edgecolor': "black"}
        _, _, autotexts = self.canvas.axes.pie(values, labels=[''] * len(values), shadow=True, autopct='%1.1f%%',
                                               wedgeprops=wp, pctdistance=1.3, colors=colors)


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setupPage()

        self.setWindowTitle("Gold portfolio")
        self.setStyleSheet(SetupFile.Background)
        self.SummaryWidget.setStyleSheet(
            'QWidget#SummaryWidget { border: 2px solid black; border-radius: 10px; background-color: white; }')
        self.Summary_Text.setStyleSheet(SetupFile.Label)
        self.TotalAcquisition_Text.setStyleSheet(SetupFile.Label)
        self.TotalOwned_Text.setStyleSheet(SetupFile.Label)
        self.TotalOwned_Text.setStyleSheet(SetupFile.Label)
        self.GoldCost.setStyleSheet(SetupFile.Label)
        self.TotalGoldWeight.setStyleSheet(SetupFile.Label)

