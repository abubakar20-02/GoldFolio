# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Statistics2.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import pickle
import calendar
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QDate
from PyQt5.QtWidgets import QCalendarWidget, QDesktopWidget

from Database import Statement, Log, Investment

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.patches import Patch
import matplotlib.ticker as ticker


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=4, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Ui_Form(QObject):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1110, 792)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)

        self.Date = QtWidgets.QDateEdit()
        self.Date.setDisplayFormat("MM-yyyy")
        self.Date.setCalendarPopup(True)
        self.Date.setMaximumDate(QDate.currentDate())
        self.Date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.horizontalLayout.addWidget(self.Date)

        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setMinimumSize(QtCore.QSize(300, 300))
        self.widget.setObjectName("widget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.canvas = MplCanvas(self, height=300, width=600, dpi=100)
        self.canvas.setMinimumSize(QtCore.QSize(600, 300))
        # set the maximum height for the canvas to 40% of the page size
        desktop = QDesktopWidget()
        height = int(desktop.availableGeometry().height() * 0.4)
        self.canvas.setMaximumHeight(height)

        self.canvas.setStyleSheet('border: 2px solid black;')

        self.canvas.setObjectName("canvas")
        self.verticalLayout_6.addWidget(self.canvas)
        self.horizontalLayout_2.addWidget(self.widget)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.widget_2 = QtWidgets.QWidget(Form)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.MoneyLayout = QtWidgets.QVBoxLayout()
        self.MoneyLayout.setContentsMargins(10, 10, 10, -1)
        self.MoneyLayout.setObjectName("MoneyLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem3)
        self.label_18 = QtWidgets.QLabel(self.widget_2)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_10.addWidget(self.label_18)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem4)
        self.MoneyLayout.addLayout(self.horizontalLayout_10)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.MoneyLayout.addItem(spacerItem5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.MoneyIn_Text = QtWidgets.QLabel(self.widget_2)
        self.MoneyIn_Text.setObjectName("MoneyIn_Text")
        self.horizontalLayout_4.addWidget(self.MoneyIn_Text)
        self.MoneyIn = QtWidgets.QLabel(self.widget_2)
        self.MoneyIn.setObjectName("MoneyIn")
        self.horizontalLayout_4.addWidget(self.MoneyIn)
        self.MoneyInChange = QtWidgets.QLabel(self.widget_2)
        self.MoneyInChange.setObjectName("MoneyInChange")
        self.horizontalLayout_4.addWidget(self.MoneyInChange)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem6)
        self.MoneyLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.MoneyOut_Text = QtWidgets.QLabel(self.widget_2)
        self.MoneyOut_Text.setObjectName("MoneyOut_Text")
        self.horizontalLayout_3.addWidget(self.MoneyOut_Text)
        self.MoneyOut = QtWidgets.QLabel(self.widget_2)
        self.MoneyOut.setObjectName("MoneyOut")
        self.horizontalLayout_3.addWidget(self.MoneyOut)
        self.MoneyOutChange = QtWidgets.QLabel(self.widget_2)
        self.MoneyOutChange.setObjectName("MoneyOutChange")
        self.horizontalLayout_3.addWidget(self.MoneyOutChange)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.MoneyLayout.addLayout(self.horizontalLayout_3)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.MoneyLayout.addItem(spacerItem8)
        self.verticalLayout.addLayout(self.MoneyLayout)
        self.horizontalLayout_8.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(Form)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.InvestmentLayout = QtWidgets.QVBoxLayout()
        self.InvestmentLayout.setContentsMargins(10, 10, 10, -1)
        self.InvestmentLayout.setObjectName("InvestmentLayout")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem9)
        self.label_17 = QtWidgets.QLabel(self.widget_3)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_9.addWidget(self.label_17)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem10)
        self.InvestmentLayout.addLayout(self.horizontalLayout_9)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.InvestmentLayout.addItem(spacerItem11)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.InvestmentSold_Text = QtWidgets.QLabel(self.widget_3)
        self.InvestmentSold_Text.setObjectName("InvestmentSold_Text")
        self.horizontalLayout_5.addWidget(self.InvestmentSold_Text)
        self.InvestmentSold = QtWidgets.QLabel(self.widget_3)
        self.InvestmentSold.setObjectName("InvestmentSold")
        self.horizontalLayout_5.addWidget(self.InvestmentSold)
        self.InvestmentSoldChange = QtWidgets.QLabel(self.widget_3)
        self.InvestmentSoldChange.setObjectName("InvestmentSoldChange")
        self.horizontalLayout_5.addWidget(self.InvestmentSoldChange)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem12)
        self.InvestmentLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.GoldSold_Text = QtWidgets.QLabel(self.widget_3)
        self.GoldSold_Text.setObjectName("GoldSold_Text")
        self.horizontalLayout_6.addWidget(self.GoldSold_Text)
        self.GoldSold = QtWidgets.QLabel(self.widget_3)
        self.GoldSold.setObjectName("GoldSold")
        self.horizontalLayout_6.addWidget(self.GoldSold)
        self.GoldSoldChange = QtWidgets.QLabel(self.widget_3)
        self.GoldSoldChange.setObjectName("GoldSoldChange")
        self.horizontalLayout_6.addWidget(self.GoldSoldChange)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem13)
        self.InvestmentLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.AverageProfitLoss_Text = QtWidgets.QLabel(self.widget_3)
        self.AverageProfitLoss_Text.setObjectName("AverageProfitLoss_Text")
        self.horizontalLayout_7.addWidget(self.AverageProfitLoss_Text)
        self.AverageProfitLoss = QtWidgets.QLabel(self.widget_3)
        self.AverageProfitLoss.setObjectName("AverageProfitLoss")
        self.horizontalLayout_7.addWidget(self.AverageProfitLoss)
        self.AverageProfitLossChange = QtWidgets.QLabel(self.widget_3)
        self.AverageProfitLossChange.setObjectName("AverageProfitLossChange")
        self.horizontalLayout_7.addWidget(self.AverageProfitLossChange)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem14)
        self.InvestmentLayout.addLayout(self.horizontalLayout_7)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.InvestmentLayout.addItem(spacerItem15)
        self.verticalLayout_2.addLayout(self.InvestmentLayout)
        self.horizontalLayout_8.addWidget(self.widget_3)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem16)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_8)
        self.verticalLayout_4.addLayout(self.horizontalLayout_11)
        spacerItem17 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem17)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.widget.setStyleSheet(
            'QWidget#widget { border: 2px solid black; border-radius: 10px; background-color: white; }')
        self.widget_2.setStyleSheet(
            'QWidget#widget_2 { border: 2px solid black; border-radius: 10px; background-color: white; }')
        self.widget_3.setStyleSheet(
            'QWidget#widget_3 { border: 2px solid black; border-radius: 10px; background-color: white; }')

        self.SetupPage()
        self.Date.dateChanged.connect(self.updateGraph)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "TextLabel"))
        self.label_18.setText(_translate("Form", "Money"))
        self.MoneyIn_Text.setText(_translate("Form", "Money in: "))
        self.MoneyIn.setText(_translate("Form", "TextLabel"))
        self.MoneyInChange.setText(_translate("Form", "TextLabel"))
        self.MoneyOut_Text.setText(_translate("Form", "Money out:"))
        self.MoneyOut.setText(_translate("Form", "TextLabel"))
        self.MoneyOutChange.setText(_translate("Form", "TextLabel"))
        self.label_17.setText(_translate("Form", "Investment"))
        self.InvestmentSold_Text.setText(_translate("Form", "Investment sold: "))
        self.InvestmentSold.setText(_translate("Form", "TextLabel"))
        self.InvestmentSoldChange.setText(_translate("Form", "TextLabel"))
        self.GoldSold_Text.setText(_translate("Form", "Gold sold: "))
        self.GoldSold.setText(_translate("Form", "TextLabel"))
        self.GoldSoldChange.setText(_translate("Form", "TextLabel"))
        self.AverageProfitLoss_Text.setText(_translate("Form", "Average profit/loss: "))
        self.AverageProfitLoss.setText(_translate("Form", "TextLabel"))
        self.AverageProfitLossChange.setText(_translate("Form", "TextLabel"))

    def updateDateEdit(self):
        if self.Mode.currentIndex() == 0:
            self.Date.setDisplayFormat("MM-yyyy")
            self.Date.setEnabled(True)
        elif self.Mode.currentIndex() == 1:
            self.Date.setDisplayFormat("yyyy")
            self.Date.setEnabled(True)
        elif self.Mode.currentIndex() == 2:
            self.Date.setEnabled(False)

    def updateGraph(self):
        self.BarGraph()
        self.canvas.draw()
        # go back 1 month instead of using date
        days_in_month = calendar.monthrange(self.Date.date().year(), self.Date.date().month())[1]
        self.start_date = datetime(self.Date.date().year(), self.Date.date().month(), 1).date()
        self.end_date = datetime(self.Date.date().year(), self.Date.date().month(), days_in_month).date()

        days_in_month = calendar.monthrange(self.Date.date().year(), self.Date.date().month() - 1)[1]
        self.start_date1 = datetime(self.Date.date().year(), self.Date.date().month() - 1, 1).date()
        self.end_date1 = datetime(self.Date.date().year(), self.Date.date().month() - 1, days_in_month).date()
        self.updateVariables()

        # for year set start start date to year-1-1 end date= year-12-31

    def SetupPage(self):
        with open("my_variable.pickle", "rb") as f:
            UserID = pickle.load(f)
        self.Investment = Investment.Investment()
        self.Statement = Statement.Statement()
        self.Log = Log.Log.Money()

        self.Investment.setProfile(UserID)
        self.Statement.setProfile(UserID)
        self.Log.setProfile(UserID)
        days_in_month = calendar.monthrange(self.Date.date().year(), self.Date.date().month())[1]
        self.start_date = datetime(self.Date.date().year(), self.Date.date().month(), 1).date()
        self.end_date = datetime(self.Date.date().year(), self.Date.date().month(), days_in_month).date()

        days_in_month = calendar.monthrange(self.Date.date().year(), self.Date.date().month() - 1)[1]
        self.start_date1 = datetime(self.Date.date().year(), self.Date.date().month() - 1, 1).date()
        self.end_date1 = datetime(self.Date.date().year(), self.Date.date().month() - 1, days_in_month).date()

        # increase = ((current value - previous value) / previous value) * 100

        self.updateVariables()

        self.BarGraph()

    def updateVariables(self):
        self.MoneyIn.setText(str(self.Log.getMoneyAdded(StartDate=self.start_date, EndDate=self.end_date)))
        self.MoneyOut.setText(str(self.Log.getMoneyOut(StartDate=self.start_date, EndDate=self.end_date)))
        # use MoneyLog to get count.
        # self.InvestmentMade.setText(str(self.Log.getInvestmentMade(StartDate=self.start_date, EndDate=self.end_date)))
        self.InvestmentSold.setText(
            str(self.Statement.getInvestmentCount(StartDate=self.start_date, EndDate=self.end_date)))
        self.GoldSold.setText(str(self.Statement.getSum("Gold", StartDate=self.start_date, EndDate=self.end_date)))
        self.AverageProfitLoss.setText(
            str(round(self.Statement.getAvgProfitLoss(StartDate=self.start_date, EndDate=self.end_date), 2)))

        if self.Log.getMoneyAdded(StartDate=self.start_date1, EndDate=self.end_date1) == 0:
            self.MoneyInChange.setText(str(""))
        else:
            self.MoneyInChange.setText(str((self.Log.getMoneyAdded(StartDate=self.start_date,
                                                                   EndDate=self.end_date) - self.Log.getMoneyAdded(
                StartDate=self.start_date1, EndDate=self.end_date1)) / self.Log.getMoneyAdded(
                StartDate=self.start_date1, EndDate=self.end_date1)) * 100)

        if self.Log.getMoneyOut(StartDate=self.start_date1, EndDate=self.end_date1) == 0:
            self.MoneyOutChange.setText(str(""))
        else:
            self.MoneyOutChange.setText(str((self.Log.getMoneyOut(StartDate=self.start_date,
                                                                  EndDate=self.end_date) - self.Log.getMoneyOut(
                StartDate=self.start_date1, EndDate=self.end_date1)) / self.Log.getMoneyOut(StartDate=self.start_date1,
                                                                                            EndDate=self.end_date1)) * 100)

        if self.Statement.getInvestmentCount(StartDate=self.start_date1, EndDate=self.end_date1) == 0:
            self.InvestmentSoldChange.setText(str(""))
        else:
            self.InvestmentSoldChange.setText(str((self.Statement.getInvestmentCount(StartDate=self.start_date,
                                                                                     EndDate=self.end_date) - self.Statement.getInvestmentCount(
                StartDate=self.start_date1, EndDate=self.end_date1)) / self.Statement.getInvestmentCount(
                StartDate=self.start_date1, EndDate=self.end_date1)) * 100)

        if self.Statement.getSum("Gold", StartDate=self.start_date1, EndDate=self.end_date1) == 0:
            self.GoldSoldChange.setText(str(""))
        else:
            self.GoldSoldChange.setText(str((self.Statement.getSum("Gold", StartDate=self.start_date,
                                                                   EndDate=self.end_date) - self.Statement.getSum(
                "Gold", StartDate=self.start_date1, EndDate=self.end_date1)) / self.Statement.getSum("Gold",
                                                                                                     StartDate=self.start_date1,
                                                                                                     EndDate=self.end_date1)) * 100)
        if self.Statement.getAvgProfitLoss(StartDate=self.start_date1, EndDate=self.end_date1) ==0:
            self.AverageProfitLossChange.setText(str(""))
        else:
            self.AverageProfitLossChange.setText(str((self.Statement.getAvgProfitLoss(StartDate=self.start_date,
                                                                                     EndDate=self.end_date) - self.Statement.getAvgProfitLoss(
                StartDate=self.start_date1, EndDate=self.end_date1)) / self.Statement.getAvgProfitLoss(
                StartDate=self.start_date1, EndDate=self.end_date1)) * 100)

    def BarGraph(self):
        self.canvas.axes.clear()
        self.Statement.getProfitLossData(self.Date.date().year(), self.Date.date().month())
        Add, Withdrawn = self.Log.getDatesInWeekFormatForMonth(self.Date.date().year(), self.Date.date().month())

        labels = list(Add.keys())
        y = list(Add.values())
        y1 = list(Withdrawn.values())

        self.canvas.axes.bar(labels, y, width=0.3, align='center', label='Data 1', color="Green")
        self.canvas.axes.bar(labels, y1, width=0.3, align='center', label='Data 2', color="Red")

        self.canvas.axes.set_xlabel('Date')
        self.canvas.axes.set_ylabel('Money')

        # Create a custom legend
        legend_elements = [Patch(facecolor='g', edgecolor='black', label='Money Added'),
                           Patch(facecolor='r', edgecolor='black', label='Money Withdrawn')]
        self.canvas.axes.legend(handles=legend_elements)

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
