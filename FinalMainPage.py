# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FinalMainPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os
import pickle
import time
from datetime import datetime

import numpy as np
import pandas as pd

import FinalAddMoney
import FinalMoneyLog
import SetupFile
from Database import User, DBFunctions
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QDate, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView, QTableWidget

from Database.Investment import Investment
from GoldRate import Gold

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Ui_MainWindow(QObject):
    def setupUi(self, MainWindow):
        self.Gold = Gold(24, "Gram", "USD")
        # Retrieve the variable from the file
        with open("my_variable.pickle", "rb") as f:
            self.UserID = pickle.load(f)
        self.UserProfile = User.User()
        self.UserProfile.SelectProfile(self.UserID)
        self.loadSettings()

        self.val = 0
        self.Investment = Investment()
        self.Investment.setProfile(self.UserID)

        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.BaseLayout = QtWidgets.QVBoxLayout()
        self.BaseLayout.setObjectName("BaseLayout")
        self.Banner = QtWidgets.QLabel(self.centralwidget)
        self.Banner.setMinimumSize(QtCore.QSize(0, 100))
        self.Banner.setSizeIncrement(QtCore.QSize(1, 1))
        self.Banner.setObjectName("Banner")
        self.BaseLayout.addWidget(self.Banner)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem)
        self.CashAndUser = QtWidgets.QVBoxLayout()
        self.CashAndUser.setObjectName("CashAndUser")
        self.UserLayout = QtWidgets.QHBoxLayout()
        self.UserLayout.setObjectName("UserLayout")
        self.User_Text = QtWidgets.QLabel(self.centralwidget)
        self.User_Text.setObjectName("User_Text")
        self.UserLayout.addWidget(self.User_Text)
        self.User = QtWidgets.QLabel(self.centralwidget)
        self.User.setObjectName("User")
        self.UserLayout.addWidget(self.User)
        self.LogOutButton = QtWidgets.QPushButton(self.centralwidget)
        self.LogOutButton.setObjectName("LogOutButton")
        self.UserLayout.addWidget(self.LogOutButton)
        self.CashAndUser.addLayout(self.UserLayout)
        self.CashLayout = QtWidgets.QHBoxLayout()
        self.CashLayout.setObjectName("CashLayout")
        self.Cash_Text = QtWidgets.QLabel(self.centralwidget)
        self.Cash_Text.setObjectName("Cash_Text")
        self.CashLayout.addWidget(self.Cash_Text)
        self.Cash = QtWidgets.QLabel(self.centralwidget)
        self.Cash.setObjectName("Cash")
        self.CashLayout.addWidget(self.Cash)
        self.AddCashButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddCashButton.setObjectName("AddCashButton")
        self.CashLayout.addWidget(self.AddCashButton)
        self.CashAndUser.addLayout(self.CashLayout)
        self.horizontalLayout_9.addLayout(self.CashAndUser)
        self.BaseLayout.addLayout(self.horizontalLayout_9)
        self.RightSideLayout = QtWidgets.QHBoxLayout()
        self.RightSideLayout.setObjectName("RightSideLayout")
        self.LeftSideLayout = QtWidgets.QVBoxLayout()
        self.LeftSideLayout.setObjectName("LeftSideLayout")
        self.DatesLayout = QtWidgets.QHBoxLayout()
        self.DatesLayout.setObjectName("DatesLayout")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setText("")
        self.radioButton.setObjectName("radioButton")
        self.radioButton.clicked.connect(self.updateTable)
        self.DatesLayout.addWidget(self.radioButton)
        self.StartDate_Text = QtWidgets.QLabel(self.centralwidget)
        self.StartDate_Text.setObjectName("StartDate_Text")
        self.DatesLayout.addWidget(self.StartDate_Text)
        self.StartDate = QtWidgets.QDateEdit(calendarPopup=True)
        self.StartDate.setMaximumDate(QDate.currentDate())
        self.StartDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.StartDate.dateChanged.connect(self.updateDateRangeForEndDate)
        self.DatesLayout.addWidget(self.StartDate)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.DatesLayout.addItem(spacerItem1)
        self.EndDate_Text = QtWidgets.QLabel(self.centralwidget)
        self.EndDate_Text.setObjectName("EndDate_Text")
        self.DatesLayout.addWidget(self.EndDate_Text)
        self.EndDate = QtWidgets.QDateEdit(calendarPopup=True)
        self.EndDate.setMaximumDate(QDate.currentDate())
        self.EndDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.EndDate.dateChanged.connect(self.updateDateRangeForStartDate)
        self.DatesLayout.addWidget(self.EndDate)
        self.LeftSideLayout.addLayout(self.DatesLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setMinimumSize(700, 700)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.updateTable()
        self.tableWidget.setColumnHidden(0, True)
        self.timer.timeout.connect(self.updateTable)
        self.timer.start(self.UpdateFrequency * 1000)

        self.LeftSideLayout.addWidget(self.tableWidget)
        self.RightSideLayout.addLayout(self.LeftSideLayout)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.Bid_Text = QtWidgets.QLabel(self.centralwidget)
        self.Bid_Text.setObjectName("Bid_Text")
        self.horizontalLayout_5.addWidget(self.Bid_Text)
        self.Bid = QtWidgets.QLabel(self.centralwidget)
        self.Bid.setObjectName("Bid")
        self.horizontalLayout_5.addWidget(self.Bid)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.Ask_Text = QtWidgets.QLabel(self.centralwidget)
        self.Ask_Text.setObjectName("Ask_Text")
        self.horizontalLayout_4.addWidget(self.Ask_Text)
        self.Ask = QtWidgets.QLabel(self.centralwidget)
        self.Ask.setObjectName("Ask")
        self.horizontalLayout_4.addWidget(self.Ask)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.GraphLayout = QtWidgets.QVBoxLayout()
        self.GraphLayout.setObjectName("GraphLayout")
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.GraphLayout.addItem(spacerItem4)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.setMinimumSize(QtCore.QSize(500, 500))
        self.canvas.setObjectName("canvas")
        self.GraphLayout.addWidget(self.canvas)
        self.line()
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.GraphLayout.addItem(spacerItem5)
        self.horizontalLayout_3.addLayout(self.GraphLayout)
        self.BuyAndSellLayout = QtWidgets.QVBoxLayout()
        self.BuyAndSellLayout.setObjectName("BuyAndSellLayout")
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.BuyAndSellLayout.addItem(spacerItem6)
        self.BuyButton = QtWidgets.QPushButton(self.centralwidget)
        self.BuyButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.BuyButton.setObjectName("BuyButton")
        self.BuyAndSellLayout.addWidget(self.BuyButton)
        self.SellButton = QtWidgets.QPushButton(self.centralwidget)
        self.SellButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.SellButton.setObjectName("SellButton")
        self.BuyAndSellLayout.addWidget(self.SellButton)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.BuyAndSellLayout.addItem(spacerItem7)
        self.horizontalLayout_3.addLayout(self.BuyAndSellLayout)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem8)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.RightSideLayout.addLayout(self.verticalLayout_6)
        self.BaseLayout.addLayout(self.RightSideLayout)
        self.verticalLayout_9.addLayout(self.BaseLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 722, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuStatistics = QtWidgets.QMenu(self.menubar)
        self.menuStatistics.setObjectName("menuStatistics")
        self.menuStatements = QtWidgets.QMenu(self.menubar)
        self.menuStatements.setObjectName("menuStatements")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionUndo = QtWidgets.QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        self.actionUndo.triggered.connect(self.prevStage)

        self.actionGold_Calculator = QtWidgets.QAction(MainWindow)
        self.actionGold_Calculator.setObjectName("actionGold_Calculator")
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionImport_Data = QtWidgets.QAction(MainWindow)
        self.actionImport_Data.setObjectName("actionImport_Data")
        self.actionExport_Data = QtWidgets.QAction(MainWindow)
        self.actionExport_Data.setObjectName("actionExport_Data")

        self.actionCash = QtWidgets.QAction(MainWindow)
        self.actionCash.setObjectName("actionCash")
        self.actionCash.triggered.connect(self.openMoneyLog)

        self.actionInvestment = QtWidgets.QAction(MainWindow)
        self.actionInvestment.setObjectName("actionInvestment")
        self.actionGraphs = QtWidgets.QAction(MainWindow)
        self.actionGraphs.setObjectName("actionGraphs")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionImport_Data)
        self.menuFile.addAction(self.actionExport_Data)
        self.menuEdit.addAction(self.actionUndo)
        self.menuSettings.addAction(self.actionSettings)
        self.menuTools.addAction(self.actionGold_Calculator)
        self.menuStatistics.addAction(self.actionGraphs)
        self.menuStatements.addAction(self.actionCash)
        self.menuStatements.addAction(self.actionInvestment)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuStatistics.menuAction())
        self.menubar.addAction(self.menuStatements.menuAction())

        self.User.setStyleSheet(SetupFile.NoChangeTextColor)
        self.Cash.setStyleSheet(SetupFile.NoChangeTextColor)

        self.getUserData()
        self.AddCashButton.clicked.connect(lambda: self.addCash())
        self.LogOutButton.clicked.connect(lambda: self.LogOut())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Banner.setText(_translate("MainWindow", "Banner"))
        self.User_Text.setText(_translate("MainWindow", "User: "))
        self.LogOutButton.setText(_translate("MainWindow", "Log out"))
        self.Cash_Text.setText(_translate("MainWindow", "Cash: "))
        self.AddCashButton.setText(_translate("MainWindow", "Add"))
        self.StartDate_Text.setText(_translate("MainWindow", "Start Date:"))
        self.EndDate_Text.setText(_translate("MainWindow", "End Date:"))
        self.Bid_Text.setText(_translate("MainWindow", "   Bid: "))
        self.Bid.setText(_translate("MainWindow", "TextLabel"))
        self.Ask_Text.setText(_translate("MainWindow", "   Ask: "))
        self.Ask.setText(_translate("MainWindow", "TextLabel"))
        self.BuyButton.setText(_translate("MainWindow", "Buy"))
        self.SellButton.setText(_translate("MainWindow", "Sell"))
        self.label_7.setText(_translate("MainWindow", "TextLabel"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuStatistics.setTitle(_translate("MainWindow", "Statistics"))
        self.menuStatements.setTitle(_translate("MainWindow", "Statements"))
        self.actionUndo.setText(_translate("MainWindow", "Undo"))
        self.actionGold_Calculator.setText(_translate("MainWindow", "Gold Calculator"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionImport_Data.setText(_translate("MainWindow", "Import Data"))
        self.actionExport_Data.setText(_translate("MainWindow", "Export Data"))
        self.actionCash.setText(_translate("MainWindow", "Cash "))
        self.actionInvestment.setText(_translate("MainWindow", "Investment"))
        self.actionGraphs.setText(_translate("MainWindow", "Graphs"))

    def LogOut(self):
        os.remove("my_variable.pickle")
        self.close()

    def openMoneyLog(self):
        self.window = QtWidgets.QWidget()
        self.window = FinalMoneyLog.MyWindow()
        self.window.show()

    def addCash(self):
        self.window = QtWidgets.QWidget()
        self.window = FinalAddMoney.MyWindow()
        self.window.show()
        self.window.AddMoney.clicked.connect(lambda: self.UserProfile.addMoney(self.window.Money.value()))
        self.window.AddMoney.clicked.connect(self.window.close)
        self.window.AddMoney.clicked.connect(self.getUserData)
        # self.window.AddButton.clicked.connect(self.loadDataFromTable)
        # self.window.AddButton.clicked.connect(self.window.close)

    def updateTable(self):
        startDate = endDate = None
        self.Investment.updateProfitLoss(self.Gold.getAsk())
        print(self.Gold.getAsk())
        if self.radioButton.isChecked():
            startDate = self.StartDate.date().toPyDate()
            endDate = self.EndDate.date().toPyDate()
            self.StartDate.setEnabled(True)
            self.EndDate.setEnabled(True)
        else:
            self.StartDate.setEnabled(False)
            self.EndDate.setEnabled(False)
        self.loadDataFromTable(StartDate=startDate, EndDate=endDate)

    def loadDataFromTable(self, StartDate=None, EndDate=None):
        with open("my_variable.pickle", "rb") as f:
            self.UserID = pickle.load(f)
        self.Investment.setProfile(self.UserID)
        print("yo" + str(StartDate))
        table = self.Investment.getTable(StartDate=StartDate, EndDate=EndDate)
        print(self.Investment.getRateRequired(StartDate=StartDate, EndDate=EndDate))
        self.load_dataframe_to_table(table, self.tableWidget)

    def load_dataframe_to_table(self, dataframe, table_widget):
        # Set the number of rows and columns for the table
        table_widget.setRowCount(len(dataframe))
        table_widget.setColumnCount(len(dataframe.columns))

        # Add the headers for the table columns
        table_widget.setHorizontalHeaderLabels(dataframe.columns)

        # Populate the table with data
        for row in range(len(dataframe)):
            for column in range(len(dataframe.columns)):
                item = QtWidgets.QTableWidgetItem()
                if dataframe.iloc[row, column] is None:
                    dataframe.iloc[row, column] = 0
                if column == 0 or column == 1:
                    item.setData(QtCore.Qt.DisplayRole, str(dataframe.iloc[row, column]))
                else:
                    item.setData(QtCore.Qt.DisplayRole, float(dataframe.iloc[row, column]))
                # item = QTableWidgetItem(str(dataframe.iloc[row, column]))
                # Set the color based on the value
                if column == len(dataframe.columns) - 1 or column == len(dataframe.columns) - 2:
                    #
                    if dataframe.iloc[row, column] == 0:
                        item.setForeground(QColor('black'))
                    if dataframe.iloc[row, column] > 0:
                        item.setForeground(QColor('green'))
                    if dataframe.iloc[row, column] < 0:
                        item.setForeground(QColor('red'))
                table_widget.setItem(row, column, item)

    def loadSettings(self):
        with open("Settings.pickle", "rb") as f:
            self.ProfitMargin, self.UpdateFrequency = pickle.load(f)
            # close previous timer and start new one
            self.timer = QTimer()
            self.timer.stop()
            self.timer.start(self.UpdateFrequency * 1000)
            self.timer.timeout.connect(self.updateTable)

    def updateDateRangeForEndDate(self):
        self.updateTable()
        self.EndDate.setMinimumDate(self.StartDate.date())

    def updateDateRangeForStartDate(self):
        self.updateTable()
        self.StartDate.setMaximumDate(self.EndDate.date())

    def prevStage(self):
        DBFunctions.previousStage(self.UserID)
        self.loadDataFromTable()
        self.getUserData()

    def getUserData(self):
        self.Cash.setText(str(self.UserProfile.getMoney()))
        # add function in user to get user name.
        self.User.setText(self.UserProfile.getName())

    def line(self, Mode="Month", ValueSelect="Gold", StartDate=None, EndDate=None):
        self.canvas.axes.clear()
        # self.canvas.axes.xaxis.set_major_locator(MaxNLocator(nbins=5))
        # self.canvas.axes.xaxis.set_major_locator(FixedLocator([15500, 16500, 17500, 18500, 19500]))
        from Database.Statement import Statement
        Statement = Statement()

        if StartDate is not None and EndDate is not None:
            data = Statement.Overall(ValueSelect, StartDate, EndDate)
            x = list(data.keys())
            # xv = range(0,len(x))
            y = list(data.values())
            print(x)
            print(y)
            self.canvas.axes.plot(x, y, '-o')
            self.canvas.axes.grid(True)
            self.canvas.axes.set_xlabel('Date')
            self.canvas.axes.set_ylabel(ValueSelect)

            # # Format the x-axis ticks as dates
            if Mode in ("Week", "2Week", "Month"):
                date_format = mdates.DateFormatter('%Y-%m-%d')
                self.canvas.axes.xaxis.set_major_formatter(date_format)
                self.canvas.axes.xaxis.set_major_locator(mdates.DayLocator())
            self.canvas.draw()
            return

        # self.cursor = mplcursors.cursor(self.canvas.axes, hover=True)
        # self.cursor.connect("add", lambda sel: sel.annotation.set_text(
        #     f"{sel.artist.get_xdata()[sel.target.index]:.2f}, {sel.artist.get_ydata()[sel.target.index]:.2f}"))
        if Mode == "Year":
            print(datetime.now().year)
            data = Statement.trial(ValueSelect, Start=datetime(datetime.now().year, 1, 1),
                                   End=datetime(datetime.now().year, 12, 31))
            print("year")
        if Mode == "5Years":
            data = Statement.trial1(ValueSelect, Start=datetime(datetime.now().year - 5, 1, 1),
                                    End=datetime(datetime.now().year, 12, 31))
        if Mode in ("Week", "2Week", "Month"):
            data = Statement.traverse_all_dates(ValueSelect, Preset=Mode, Mode=1)
        x = list(data.keys())
        # xv = range(0,len(x))
        y = list(data.values())
        print(x)
        print(y)
        ########################
        #
        # Define the format of the date string
        # format_str = '%Y-%m-%d'
        # # Convert each dictionary key to a datetime object
        # for key in data:
        #     datetime_obj = datetime.datetime.strptime(key, format_str)
        #     data[datetime_obj] = data.pop(key)
        # print(data)
        # x = [datetime.datetime(2022, 1, 1, 0, 0),
        #      datetime.datetime(2022, 1, 2, 0, 0),
        #      datetime.datetime(2022, 1, 3, 0, 0),
        #      datetime.datetime(2022, 1, 4, 0, 0),
        #      datetime.datetime(2022, 1, 5, 0, 0)]
        if Mode in ("Week", "2Week", "Month"):
            self.canvas.axes.set_xticks(x)
            self.canvas.axes.set_xticklabels(x, rotation=45)
            # x = [1, 2, 3, 4, 5]
            # y = [1850, 1800, 1900, 1950, 1750]
        self.canvas.axes.plot(x, y, '-o')
        self.canvas.axes.grid(True)
        self.canvas.axes.set_xlabel('Date')
        self.canvas.axes.set_ylabel(ValueSelect)

        # # Format the x-axis ticks as dates
        if Mode in ("Week", "2Week", "Month"):
            self.canvas.axes.xaxis.set_major_locator(mdates.DayLocator())
            date_format = mdates.DateFormatter('%Y-%m-%d')
            self.canvas.axes.xaxis.set_major_formatter(date_format)
        self.canvas.draw()

    # def series_to_supervised(self, data, n_in=1, n_out=1, dropnan=True):
    #     n_vars = 1 if type(data) is list else data.shape[1]
    #     dff = pd.DataFrame(data)
    #     cols, names = list(), list()
    #     # input sequence (t-n, ... t-1)
    #     for i in range(n_in, 0, -1):
    #         cols.append(dff.shift(i))
    #         names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
    #     # forecast sequence (t, t+1, ... t+n)
    #     for i in range(0, n_out):
    #         cols.append(dff.shift(-i))
    #         if i == 0:
    #             names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
    #         else:
    #             names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]
    #     # put it all together
    #     agg = pd.concat(cols, axis=1)
    #     agg.columns = names
    #     # drop rows with NaN values
    #     if dropnan:
    #         agg.dropna(inplace=True)
    #     return agg
    #
    # df = pd.read_excel("gold_data.xlsx")
    # df = df.iloc[:, 1:]
    #
    # reframed = series_to_supervised(df, 1, 1)
    # values = reframed.values
    # n_train_time = 80
    # test = values[n_train_time:, :]
    # test_X, test_y = test[:, :-1], test[:, -1]
    # test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
    #
    # def recursive_forecast(self, model, input_data, n_days):
    #     forecast = []
    #     current_input = input_data[-1].copy()
    #
    #     for _ in range(n_days):
    #         prediction = model.predict(current_input.reshape(1, 1, -1))
    #         forecast.append(prediction[0, 0])
    #         current_input = np.roll(current_input, -1)
    #         current_input[-1] = prediction
    #
    #     return np.array(forecast)
    #
    # n_days = 7
    # yhat = recursive_forecast(model, test_X, n_days)
    # # Reshape yhat to (1, n_days)
    # yhat = yhat.reshape(-1, 1)
    #
    # inv_yhat = np.concatenate((test_X[:n_days, -10:], yhat), axis=1)
    # # inv_yhat = scaler.inverse_transform(inv_yhat)
    # inv_yhat = inv_yhat[:, -1]
    #
    # interval = 60
    # predictinterval = interval + n_days
    # aa = [x for x in range(interval)]
    # bb = [x for x in range(interval - 1, predictinterval)]
    # print(bb)
    #
    # plt.plot(aa, inv_y[len(inv_y) - interval:], marker='.', label="actual")
    # inv_yhat = np.insert(inv_yhat, 0, inv_y[-1])
    # plt.plot(bb, inv_yhat[:], 'r', marker='.', label="predicition")
    # # plt.plot(aa, inv_yhat[:interval], 'r', label="prediction")
    # plt.ylabel('Price', size=15)
    # plt.xlabel('Time step', size=15)
    # plt.legend(fontsize=15)

    # closeExcelFile()


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        print("init")
        self.value = 0
        super().__init__()
        self.setupUi(self)
        self.my_thread = QThread()
        self.worker = UpdateRatesContinuously("24", "Oz", "USD", self.UpdateFrequency)
        # We're connecting things to the correct spots
        self.worker.moveToThread(self.my_thread)  # move worker to thread.
        # Note: Ui elements should only be updated via the main thread.
        self.my_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.my_thread.quit)  # safely close the thread.
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.values.connect(self.ApplyChanges)
        self.worker.error.connect(self.ClearRates)

        self.my_thread.start()

    def ClearRates(self):
        self.Bid.setText("")
        self.Ask.setText("")

    def ApplyChanges(self, rates):
        Ask = "$ " + str(rates.getAsk())
        Bid = "$ " + str(rates.getBid())

        if self.value > float(rates.getAsk()):
            self.Bid.setStyleSheet(SetupFile.NegativeChangeTextColor)
            self.Ask.setStyleSheet(SetupFile.NegativeChangeTextColor)
        if self.value < float(rates.getAsk()):
            self.Bid.setStyleSheet(SetupFile.PositiveChangeTextColor)
            self.Ask.setStyleSheet(SetupFile.PositiveChangeTextColor)
        if self.value == float(rates.getAsk()):
            self.Bid.setStyleSheet(SetupFile.NoChangeTextColor)
            self.Ask.setStyleSheet(SetupFile.NoChangeTextColor)
        self.Ask.setText(Ask)
        self.Bid.setText(Bid)
        self.value = float(rates.getAsk())

        # When user closes the application, loop turns false which results in exiting the thread.

    def closeEvent(self, event):
        print("closed")
        self.worker.StopThread()


class UpdateRatesContinuously(QObject):
    finished = pyqtSignal()
    values = pyqtSignal(object)
    error = pyqtSignal()

    def __init__(self, Purity, Unit, Currency, TimeFreq):
        super(UpdateRatesContinuously, self).__init__()
        self.isRunning = True
        self.Purity = Purity
        self.Unit = Unit
        self.Currency = Currency
        self.TimeFreq = TimeFreq

    def run(self):
        while True:
            try:
                rates = Gold(self.Purity, self.Unit, self.Currency)
                self.values.emit(rates)
                print("emitted")
            except:
                self.error.emit()
            print(f"time freq: {self.TimeFreq}")
            for i in range(self.TimeFreq):
                if not self.isRunning:
                    return
                time.sleep(1)
                #print("working")
                # global Change
                # if Change:
                #     Change = not Change
                #     break

    def StopThread(self):
        self.isRunning = False


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MyWindow()
    MainWindow.show()
    sys.exit(app.exec_())
