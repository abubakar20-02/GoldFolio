# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FinalStatistics.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import pickle

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QDate
from PyQt5.QtWidgets import QCalendarWidget

from Database import Statement,Log,Investment

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.patches import Patch
import matplotlib.ticker as ticker

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, height=4, dpi=100):
        fig = Figure(figsize=(height, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class Ui_Form(QObject):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(955, 729)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 953, 727))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName("label")
        self.horizontalLayout_10.addWidget(self.label)
        self.Mode = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.Mode.setObjectName("Mode")
        self.Mode.addItem("")
        self.Mode.addItem("")
        self.Mode.addItem("")
        self.horizontalLayout_10.addWidget(self.Mode)
        self.Date = QtWidgets.QDateEdit()
        self.Date.setDisplayFormat("MM-yyyy")
        self.Date.setCalendarPopup(True)
        self.Date.setMaximumDate(QDate.currentDate())
        self.Date.setDateTime(QtCore.QDateTime.currentDateTime())


        #self.EndDate.dateChanged.connect(self.updateDateRangeForStartDate)
        self.horizontalLayout_10.addWidget(self.Date)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem1)
        self.verticalLayout_9.addLayout(self.horizontalLayout_10)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem2)
        self.MoneyAdded_Layout = QtWidgets.QHBoxLayout()
        self.MoneyAdded_Layout.setObjectName("MoneyAdded_Layout")
        self.MoneyAdded_Text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.MoneyAdded_Text.setObjectName("MoneyAdded_Text")
        self.MoneyAdded_Layout.addWidget(self.MoneyAdded_Text)
        self.MoneyAdded = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.MoneyAdded.setObjectName("MoneyAdded")
        self.MoneyAdded_Layout.addWidget(self.MoneyAdded)
        self.horizontalLayout_14.addLayout(self.MoneyAdded_Layout)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem3)
        self.MoneyWithdrawn_Layout = QtWidgets.QHBoxLayout()
        self.MoneyWithdrawn_Layout.setObjectName("MoneyWithdrawn_Layout")
        self.MoneyWithdrawn_Text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.MoneyWithdrawn_Text.setObjectName("MoneyWithdrawn_Text")
        self.MoneyWithdrawn_Layout.addWidget(self.MoneyWithdrawn_Text)
        self.MoneyWithdrawn = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.MoneyWithdrawn.setObjectName("MoneyWithdrawn")
        self.MoneyWithdrawn_Layout.addWidget(self.MoneyWithdrawn)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.MoneyWithdrawn_Layout.addItem(spacerItem4)
        self.horizontalLayout_14.addLayout(self.MoneyWithdrawn_Layout)
        self.verticalLayout_6.addLayout(self.horizontalLayout_14)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_6.addItem(spacerItem5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)

        self.canvas = MplCanvas(self, height=650, dpi=100)
        self.canvas.setMinimumSize(QtCore.QSize(650, 650))
        self.canvas.setObjectName("canvas")
        self.horizontalLayout_6.addWidget(self.canvas)

        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem7)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem8)
        self.TotalInvestments_Layout = QtWidgets.QHBoxLayout()
        self.TotalInvestments_Layout.setObjectName("TotalInvestments_Layout")
        self.TotalInvestments_Text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.TotalInvestments_Text.setObjectName("TotalInvestments_Text")
        self.TotalInvestments_Layout.addWidget(self.TotalInvestments_Text)
        self.TotalInvestments = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.TotalInvestments.setObjectName("TotalInvestments")
        self.TotalInvestments_Layout.addWidget(self.TotalInvestments)
        self.horizontalLayout_15.addLayout(self.TotalInvestments_Layout)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem9)
        self.InvestmentSold_Layout = QtWidgets.QHBoxLayout()
        self.InvestmentSold_Layout.setObjectName("InvestmentSold_Layout")
        self.InvestmentSold_Text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.InvestmentSold_Text.setObjectName("InvestmentSold_Text")
        self.InvestmentSold_Layout.addWidget(self.InvestmentSold_Text)
        self.InvestmentSold = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.InvestmentSold.setObjectName("InvestmentSold")
        self.InvestmentSold_Layout.addWidget(self.InvestmentSold)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.InvestmentSold_Layout.addItem(spacerItem10)
        self.horizontalLayout_15.addLayout(self.InvestmentSold_Layout)
        self.verticalLayout_7.addLayout(self.horizontalLayout_15)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_7.addItem(spacerItem11)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem12)

        self.canvas2 = MplCanvas(self, height=650, dpi=100)
        self.canvas2.setMinimumSize(QtCore.QSize(650, 650))
        self.canvas2.setObjectName("canvas")
        self.horizontalLayout_18.addWidget(self.canvas2)

        self.canvas3 = MplCanvas(self, height=650, dpi=100)
        self.canvas3.setMinimumSize(QtCore.QSize(650, 650))
        self.canvas3.setObjectName("canvas")
        self.horizontalLayout_18.addWidget(self.canvas3)

        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem13)
        self.verticalLayout_7.addLayout(self.horizontalLayout_18)
        self.verticalLayout_6.addLayout(self.verticalLayout_7)
        self.verticalLayout_9.addLayout(self.verticalLayout_6)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem14)
        self.AverageProfitLoss_Text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.AverageProfitLoss_Text.setObjectName("AverageProfitLoss_Text")
        self.horizontalLayout_13.addWidget(self.AverageProfitLoss_Text)
        self.AverageProfitLoss = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.AverageProfitLoss.setObjectName("AverageProfitLoss")
        self.horizontalLayout_13.addWidget(self.AverageProfitLoss)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem15)
        self.verticalLayout_9.addLayout(self.horizontalLayout_13)
        self.verticalLayout_2.addLayout(self.verticalLayout_9)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.SetupPage()
        self.Mode.currentIndexChanged.connect(self.updateDateEdit)
        self.Date.dateChanged.connect(self.updateGraph)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Mode:"))
        self.Mode.setItemText(0, _translate("Form", "Month"))
        self.Mode.setItemText(1, _translate("Form", "Year"))
        self.Mode.setItemText(2, _translate("Form", "Overall"))
        self.MoneyAdded_Text.setText(_translate("Form", "Money Added: "))
        self.MoneyWithdrawn_Text.setText(_translate("Form", "Money Withdrawn: "))
        self.TotalInvestments_Text.setText(_translate("Form", "Total Investments: "))
        self.InvestmentSold_Text.setText(_translate("Form", "Investment Sold:  "))
        self.AverageProfitLoss_Text.setText(_translate("Form", "Average Profit/Loss : "))
        self.AverageProfitLoss.setText(_translate("Form", "TextLabel"))

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

    def SetupPage(self):
        with open("my_variable.pickle", "rb") as f:
            UserID = pickle.load(f)
        self.Investment = Investment.Investment()
        self.Statement = Statement.Statement()
        self.Log = Log.Log.Money()

        self.Investment.setProfile(UserID)
        self.Statement.setProfile(UserID)
        self.Log.setProfile(UserID)

        self.BarGraph()

        self.MoneyAdded.setText(str(self.Log.getMoneyAdded()))
        self.MoneyWithdrawn.setText(str(self.Log.getMoneyOut()))
        self.TotalInvestments.setText(str(self.Investment.getInvestmentCount()))
        self.InvestmentSold.setText(str(self.Statement.getInvestmentCount()))

    def BarGraph(self):
        self.canvas.axes.clear()
        Add,Withdrawn=self.Log.getDatesInWeekFormatForMonth(self.Date.date().year(),self.Date.date().month())

        labels = list(Add.keys())
        y = list(Add.values())
        y1 = list(Withdrawn.values())

        self.canvas.axes.bar(labels, y, width=0.3, align='center', label='Data 1', color= "Green")
        self.canvas.axes.bar(labels, y1, width=0.3, align='center', label='Data 2', color = "Red")

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
