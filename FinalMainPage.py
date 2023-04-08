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

import FinalAddInvestment
import FinalAddMoney
import FinalAddMoney1
import FinalDialogBox
import FinalGoldPortfolio
import FinalImport
import FinalMoneyLog
import FinalSellScreen
import FinalSettings
import FinalStatement
import FinalStatistics
import FinalStatistics1
import GoldCalculator
import SetupFile
from Database import User, DBFunctions
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QDate, QObject, pyqtSignal, QThread, Qt
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView, QTableWidget, QSplashScreen, QDesktopWidget

from Database.Investment import Investment
from GoldRate import Gold

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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
        MainWindow.resize(1000, 1000)
        MainWindow.setStyleSheet(SetupFile.Background)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.BaseLayout = QtWidgets.QVBoxLayout()
        self.BaseLayout.setObjectName("BaseLayout")
        desktop = QDesktopWidget()
        height = int(desktop.availableGeometry().height() * 0.2)
        self.Banner = QtWidgets.QLabel(self.centralwidget)
        self.Banner.setMinimumSize(QtCore.QSize(0, 100))
        self.Banner.setSizeIncrement(QtCore.QSize(1, 1))
        self.Banner.setObjectName("Banner")
        self.Banner.setStyleSheet(SetupFile.Banner)
        self.Banner.setMinimumHeight(height)
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

        self.ChangeUserButton = QtWidgets.QPushButton(self.centralwidget)
        self.ChangeUserButton.setObjectName("ChangeUserButton")
        self.ChangeUserButton.setStyleSheet(SetupFile.Button)

        self.UserLayout.addWidget(self.ChangeUserButton)
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
        self.AddCashButton.setStyleSheet(SetupFile.Button)

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
        self.DatesLayout.addWidget(self.radioButton)
        self.StartDate_Text = QtWidgets.QLabel(self.centralwidget)
        self.StartDate_Text.setObjectName("StartDate_Text")
        self.DatesLayout.addWidget(self.StartDate_Text)

        self.StartDate = QtWidgets.QDateEdit(calendarPopup=True)
        self.StartDate.setMaximumDate(QDate.currentDate())
        self.StartDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.StartDate.dateChanged.connect(self.updateDateRangeForEndDate)
        self.StartDate.setStyleSheet(SetupFile.DateEdit)
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
        self.EndDate.setStyleSheet(SetupFile.DateEdit)
        self.DatesLayout.addWidget(self.EndDate)

        self.LeftSideLayout.addLayout(self.DatesLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setStyleSheet(
            """
            QTableWidget {
                background-color: white;
            }
            """)
        self.LeftSideLayout.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.RateRequired_Text = QtWidgets.QLabel(self.centralwidget)
        self.RateRequired_Text.setObjectName("RateRequired_Text")
        self.horizontalLayout.addWidget(self.RateRequired_Text)

        self.RateRequired = QtWidgets.QLabel(self.centralwidget)
        self.RateRequired.setObjectName("RateRequired")
        self.RateRequired.setStyleSheet(SetupFile.NoChangeTextColor)

        self.horizontalLayout.addWidget(self.RateRequired)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.LeftSideLayout.addLayout(self.horizontalLayout)
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
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.Ask_Text = QtWidgets.QLabel(self.centralwidget)
        self.Ask_Text.setObjectName("Ask_Text")
        self.horizontalLayout_4.addWidget(self.Ask_Text)
        self.Ask = QtWidgets.QLabel(self.centralwidget)
        self.Ask.setObjectName("Ask")
        self.horizontalLayout_4.addWidget(self.Ask)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.GraphLayout = QtWidgets.QVBoxLayout()
        self.GraphLayout.setObjectName("GraphLayout")
        self.Graph = QtWidgets.QWidget(self.centralwidget)
        self.Graph.setMinimumSize(QtCore.QSize(600, 600))
        self.Graph.setObjectName("Graph")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Graph)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.canvas = MplCanvas(self, height=2, width=4, dpi=100)
        desktop = QDesktopWidget()
        width = int(desktop.availableGeometry().width() * 0.5)
        self.canvas.setMaximumWidth(width)
        self.verticalLayout_2.addWidget(self.canvas)
        self.GraphLayout.addWidget(self.Graph)
        self.horizontalLayout_3.addLayout(self.GraphLayout)
        self.BuyAndSellLayout = QtWidgets.QVBoxLayout()
        self.BuyAndSellLayout.setObjectName("BuyAndSellLayout")
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.BuyAndSellLayout.addItem(spacerItem5)

        self.BuyButton = QtWidgets.QPushButton(self.centralwidget)
        self.BuyButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.BuyButton.setObjectName("BuyButton")
        self.BuyButton.setStyleSheet(SetupFile.Button)

        self.BuyAndSellLayout.addWidget(self.BuyButton)

        self.SellButton = QtWidgets.QPushButton(self.centralwidget)
        self.SellButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.SellButton.setObjectName("SellButton")
        self.SellButton.setStyleSheet(SetupFile.Button)

        self.BuyAndSellLayout.addWidget(self.SellButton)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.BuyAndSellLayout.addItem(spacerItem6)
        self.horizontalLayout_3.addLayout(self.BuyAndSellLayout)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem7)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.RightSideLayout.addLayout(self.verticalLayout_6)
        self.BaseLayout.addLayout(self.RightSideLayout)
        self.verticalLayout.addLayout(self.BaseLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1020, 22))
        self.menubar.setObjectName("menubar")
        self.menubar.setStyleSheet(SetupFile.MenuBar)

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
        self.actionGold_Calculator.triggered.connect(self.openGoldCalculator)

        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")

        self.actionImport_Data = QtWidgets.QAction(MainWindow)
        self.actionImport_Data.setObjectName("actionImport_Data")
        self.actionImport_Data.triggered.connect(self.openImportData)

        self.actionExport_Data = QtWidgets.QAction(MainWindow)
        self.actionExport_Data.setObjectName("actionExport_Data")

        self.actionCash = QtWidgets.QAction(MainWindow)
        self.actionCash.setObjectName("actionCash")
        self.actionCash.triggered.connect(self.openMoneyLog)

        self.actionInvestment = QtWidgets.QAction(MainWindow)
        self.actionInvestment.setObjectName("actionInvestment")
        self.actionInvestment.triggered.connect(self.openStatement)

        self.actionGraphs = QtWidgets.QAction(MainWindow)
        self.actionGraphs.setObjectName("actionGraphs")
        self.actionGraphs.triggered.connect(self.openGoldPortfolio)

        self.actionGold_Portfolio = QtWidgets.QAction(MainWindow)
        self.actionGold_Portfolio.setObjectName("actionGold_Portfolio")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName("actionLoad")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionImport_Data)
        self.menuEdit.addAction(self.actionUndo)
        self.menuSettings.addAction(self.actionSettings)
        self.menuTools.addAction(self.actionGold_Calculator)
        self.menuStatistics.addAction(self.actionGraphs)
        self.menuStatistics.addAction(self.actionGold_Portfolio)
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

        self.Graph.setStyleSheet(
            'QWidget#Graph { border: 2px solid black; border-radius: 10px; background-color: white; }')
        self.getUserData()
        self.AddCashButton.clicked.connect(lambda: self.addCash())
        self.ChangeUserButton.clicked.connect(lambda: self.LogOut())
        self.SellButton.clicked.connect(lambda: self.openSell())
        self.radioButton.clicked.connect(lambda: self.updateTable())
        self.loadModel()

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.updateTable()
        self.tableWidget.setColumnHidden(0, True)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.User_Text.setText(_translate("MainWindow", "User: "))
        self.ChangeUserButton.setText(_translate("MainWindow", "Manage Account"))
        self.Cash_Text.setText(_translate("MainWindow", "Cash: "))
        self.AddCashButton.setText(_translate("MainWindow", "Manage Cash"))
        self.StartDate_Text.setText(_translate("MainWindow", "Start Date:"))
        self.EndDate_Text.setText(_translate("MainWindow", "End Date:"))
        self.RateRequired_Text.setText(_translate("MainWindow", "Rate required to break even :"))
        self.RateRequired.setText(_translate("MainWindow", "TextLabel"))
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
        self.actionGraphs.setText(_translate("MainWindow", "Statistics"))
        self.actionGold_Portfolio.setText(_translate("MainWindow", "Gold Portfolio"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))

    def openImportData(self):
        self.window = QtWidgets.QWidget()
        self.window = FinalImport.MyWindow()
        self.window.setProfile(self.UserID)
        self.window.show()
        # should update only if value added
        self.window.ImportButton.clicked.connect(lambda: self.updateTable(Rate=self.Gold.getBidinGrams()))

    def openGoldPortfolio(self):
        self.window = QtWidgets.QWidget()
        self.window = FinalStatistics1.MyWindow()
        self.window.showMaximized()
        # self.window.setCurrentGoldRate(self.Gold.getBidinGrams())
        self.window.show()

    def openGoldCalculator(self):
        self.window = QtWidgets.QWidget()
        self.window = GoldCalculator.MyWindow()
        self.window.show()
        self.window.Check.clicked.connect(lambda: self.window.getRate(self.Gold.getAsk()))

    def LogOut(self):
        self.window = QtWidgets.QWidget()
        self.window = FinalDialogBox.MyWindow()
        self.window.setText("Are you sure you want to log out?")
        self.window.show()
        self.window.OkButton.clicked.connect(lambda: os.remove("my_variable.pickle"))
        self.window.OkButton.clicked.connect(lambda: self.close())

    def openMoneyLog(self):
        self.window = QtWidgets.QWidget()
        self.window = FinalMoneyLog.MyWindow()
        self.window.show()

    def openStatement(self):
        self.window = QtWidgets.QWidget()
        self.window = FinalStatement.MyWindow()
        self.window.show()

    def addCash(self):
        self.window = QtWidgets.QWidget()
        self.window = FinalAddMoney.MyWindow()
        self.window.setUserID(self.UserID)
        self.window.show()
        self.window.AddMoney.clicked.connect(self.window.close)
        self.window.AddMoney.clicked.connect(self.getUserData)
        # self.window.AddButton.clicked.connect(self.loadDataFromTable)
        # self.window.AddButton.clicked.connect(self.window.close)

    def updateTable(self, Rate=None):
        startDate = endDate = None
        if Rate is not None:
            print("update table rate")
            self.Investment.updateProfitLoss(Rate)
        if self.radioButton.isChecked():
            startDate = self.StartDate.date().toPyDate()
            endDate = self.EndDate.date().toPyDate()
            self.StartDate.setEnabled(True)
            self.EndDate.setEnabled(True)
        else:
            self.StartDate.setEnabled(False)
            self.EndDate.setEnabled(False)
        self.loadDataFromTable(StartDate=startDate, EndDate=endDate)
        # get rate required
        self.RateRequired.setText(self.Currency + " " + str(
            round(self.Gold.convertRate(self.Investment.getRateRequired(StartDate=startDate, EndDate=endDate)),
                  self.DecimalPoints)) + f" /{self.GoldUnit}")

    def loadDataFromTable(self, StartDate=None, EndDate=None):
        with open("my_variable.pickle", "rb") as f:
            self.UserID = pickle.load(f)
        self.Investment.setProfile(self.UserID)
        print("yo" + str(StartDate))
        table = self.Investment.getTable(StartDate=StartDate, EndDate=EndDate)
        print(self.Gold.convertRate(self.Investment.getRateRequired(StartDate=StartDate, EndDate=EndDate)))
        self.load_dataframe_to_table(table, self.tableWidget)

    def load_dataframe_to_table(self, dataframe, table_widget):
        # Set the number of rows and columns for the table
        table_widget.setRowCount(len(dataframe))
        table_widget.setColumnCount(len(dataframe.columns))

        # Add the headers for the table columns
        dataframe.columns = ["Investment_ID", "Date", "Gold (g)", f"Bought for({self.Currency})", "Profit/Loss (%)",
                             f"Value change ({self.Currency})"]
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
                    item.setData(QtCore.Qt.DisplayRole, round(float(dataframe.iloc[row, column]), self.DecimalPoints))
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

    def openSell(self):
        if self.StartDate.isEnabled():
            StartDate = self.StartDate.date().toPyDate()
            EndDate = self.EndDate.date().toPyDate()
        else:
            StartDate = None
            EndDate = None
        self.window = QtWidgets.QWidget()
        self.window = FinalSellScreen.MyWindow()
        self.window.show()
        self.window.Sell.clicked.connect(
            lambda: self.window.Sell1(self.UserID, Rate=self.Gold.getBidinGrams(),
                                      SellDate=self.window.Date.date().toPyDate(),
                                      TransactionIDs=self.getTransactionID(), StartDate=StartDate, EndDate=EndDate,
                                      ProfitMargin=self.ProfitMargin))
        self.window.Sell.clicked.connect(lambda: self.updateTable())
        self.window.Sell.clicked.connect(self.window.close)
        self.window.Sell.clicked.connect(self.getUserData)

    def getTransactionID(self):
        # could be better.
        # assigned transaction id 5 times.
        selected_rows = self.tableWidget.selectedItems()
        id = []
        column_index = 0
        for item in selected_rows:
            row = item.row()
            # Get the QTableWidgetItem for the cell in the specified row and column
            item = self.tableWidget.item(row, column_index)

            # Retrieve the data from the QTableWidgetItem
            data = item.data(Qt.DisplayRole)
            id.append(data)
        uniqueID = list(set(id))
        return uniqueID

    def loadSettings(self):
        self.ProfitMargin, self.DecimalPoints, self.UpdateFrequency, self.GoldUnit, self.Currency = self.UserProfile.GetSettings()
        self.Gold = Gold(24, self.GoldUnit, self.Currency)
        # close previous timer and start new one

    def updateDateRangeForEndDate(self):
        self.updateTable()
        self.EndDate.setMinimumDate(self.StartDate.date())

    def updateDateRangeForStartDate(self):
        self.updateTable()
        self.StartDate.setMaximumDate(self.EndDate.date())

    def prevStage(self):
        DBFunctions.previousStage(self.UserID)
        # still not good as it keeps asking api for asking values over and over again.
        self.updateTable(Rate=self.Gold.getBidinGrams())
        self.getUserData()

    def getUserData(self):
        self.Cash.setText(f"{self.Currency} {str(round(self.UserProfile.getMoney(), 2))}")
        # add function in user to get user name.
        self.User.setText(self.UserProfile.getName())

    def line(self, Mode="Month", ValueSelect="Gold", StartDate=None, EndDate=None):
        self.canvas.axes.clear()
        self.canvas.draw()

    def series_to_supervised(self, data, n_in=1, n_out=1, dropnan=True):
        n_vars = 1 if type(data) is list else data.shape[1]
        dff = pd.DataFrame(data)
        cols, names = list(), list()
        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(dff.shift(i))
            names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
        # forecast sequence (t, t+1, ... t+n)
        for i in range(0, n_out):
            cols.append(dff.shift(-i))
            if i == 0:
                names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
            else:
                names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]
        # put it all together
        agg = pd.concat(cols, axis=1)
        agg.columns = names
        # drop rows with NaN values
        if dropnan:
            agg.dropna(inplace=True)
        return agg

    def loadModel(self):
        from joblib import load

        model = load_model('model.h5')

        df = pd.read_excel("gold_data.xlsx")
        df = df.iloc[:, 1:]
        df = pd.DataFrame(df)
        scaler = MinMaxScaler(feature_range=(0, 1))
        df = scaler.fit_transform(df)

        reframed = self.series_to_supervised(df, 1, 1)
        print("-----------")
        # split into train and test sets
        values = reframed.values

        n_train_time = 80
        train = values[:n_train_time, :]
        test = values[n_train_time:, :]
        ##test = values[n_train_time:n_test_time, :]
        # split into input and outputs
        train_X, train_y = train[:, :-1], train[:, -1]
        test_X, test_y = test[:, :-1], test[:, -1]
        # reshape input to be 3D [samples, timesteps, features]
        train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
        test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
        print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

        test_X = test_X.reshape((test_X.shape[0], 21))
        test_y = test_y.reshape((len(test_y), 1))
        inv_y = np.concatenate((test_X[:, -10:], test_y), axis=1)
        inv_y = scaler.inverse_transform(inv_y)
        inv_y = inv_y[:, -1]

        n_days = 7
        yhat = self.recursive_forecast(model, test_X, n_days)
        # Reshape yhat to (1, n_days)
        yhat = yhat.reshape(-1, 1)
        print(yhat)

        inv_yhat = np.concatenate((test_X[:n_days, -10:], yhat), axis=1)
        inv_yhat = scaler.inverse_transform(inv_yhat)
        inv_yhat = inv_yhat[:, -1]

        print(inv_yhat)

        interval = 60
        predictinterval = interval + n_days
        aa = [x for x in range(interval)]
        bb = [x for x in range(interval - 1, predictinterval)]
        print(bb)

        self.canvas.axes.plot(aa, inv_y[len(inv_y) - interval:], marker='.', label="actual")
        inv_yhat = np.insert(inv_yhat, 0, inv_y[-1])
        self.canvas.axes.plot(bb, inv_yhat[:], 'r', marker='.', label="predicition")

    def recursive_forecast(self, model, input_data, n_days):
        # load model.
        forecast = []
        current_input = input_data[-1].copy()

        for _ in range(n_days):
            prediction = model.predict(current_input.reshape(1, 1, -1))
            forecast.append(prediction[0, 0])
            current_input = np.roll(current_input, -1)
            current_input[-1] = prediction

        return np.array(forecast)

    # closeExcelFile()


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        self.value = 0
        super().__init__()
        pixmap = QPixmap("Aesthetic-boy-pfp.jpeg")
        splash = QSplashScreen(pixmap)
        splash.show()
        self.setupUi(self)
        self.StartThread()
        print("ready")

        self.actionSettings.triggered.connect(self.openSettings)
        self.BuyButton.clicked.connect(lambda: self.openBuyInvestment())

    def StartThread(self):
        self.my_thread = QThread()
        self.worker = UpdateRatesContinuously(self.Gold, self.UpdateFrequency)
        # We're connecting things to the correct spots
        self.worker.moveToThread(self.my_thread)  # move worker to thread.
        # Note: Ui elements should only be updated via the main thread.
        self.my_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.my_thread.quit)  # safely close the thread.
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.values.connect(self.ApplyChanges)
        self.worker.error.connect(self.ClearRates)
        self.my_thread.start()

    def openSettings(self):
        self.window = QtWidgets.QWidget()
        self.window = FinalSettings.MyWindow()
        self.window.setProfile(self.UserID)
        self.window.SaveButton.clicked.connect(self.loadSettings)
        self.window.SaveButton.clicked.connect(self.restartThread)
        # self.window.SaveButton.clicked.connect(
        #     lambda: self.restartThread() if self.window.updatefreqchanged() else None)
        self.window.show()

    def openBuyInvestment(self):
        self.window = QtWidgets.QWidget()
        self.window = FinalAddInvestment.MyWindow()
        self.window.Add.clicked.connect(lambda: self.window.add(self.Gold.getBidinGrams()))
        self.window.Add.clicked.connect(self.window.close)
        # maybe come up with a way to calculate the rate from existing data
        self.window.Add.clicked.connect(lambda: self.updateTable(Rate=self.Gold.getBidinGrams()))
        self.window.Add.clicked.connect(self.getUserData)
        self.window.show()

    def restartThread(self):
        print("restart")
        self.worker.StopThread()
        self.StartThread()

    def ClearRates(self):
        self.Bid.setText("")
        self.Ask.setText("")

    def ApplyChanges(self, rates):
        Ask = str(f"{rates.getCurrency()} {rates.getAsk()}")
        Bid = str(f"{rates.getCurrency()} {rates.getBid()}")

        if self.value > float(rates.getAsk()):
            self.Bid.setStyleSheet(SetupFile.NegativeChangeTextColor)
            self.Ask.setStyleSheet(SetupFile.NegativeChangeTextColor)
        if self.value < float(rates.getAsk()):
            self.Bid.setStyleSheet(SetupFile.PositiveChangeTextColor)
            self.Ask.setStyleSheet(SetupFile.PositiveChangeTextColor)
        if self.value == float(rates.getAsk()):
            self.Bid.setStyleSheet(SetupFile.NoChangeTextColor)
            self.Ask.setStyleSheet(SetupFile.NoChangeTextColor)
        self.updateTable(Rate=rates.getBidinGrams())
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

    def __init__(self, Gold, TimeFreq):
        super(UpdateRatesContinuously, self).__init__()
        self.isRunning = True
        self.GoldRate = Gold
        self.TimeFreq = TimeFreq

    def getGoldRate(self, GoldRate):
        self.GoldRate = GoldRate

    def run(self):
        while True:
            try:
                rates = self.GoldRate
                rates.getLatestRate()
                self.values.emit(rates)
                print("emitted")
            except:
                self.error.emit()
            print(f"time freq: {self.TimeFreq}")
            for i in range(self.TimeFreq):
                if not self.isRunning:
                    self.finished.emit()
                    return
                time.sleep(1)
                # print("working")
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
