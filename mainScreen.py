# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import pickle

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView

import Add
import AddUser
import MoneyLogScreen
import Setting
import StatementScreen
import UserSelect
import graph
import graph1
import sellRate
from Database import DBFunctions
from Database.Investment import Investment

from GoldRate import Gold


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.Gold = Gold(24, "Gram", "USD")
        # Retrieve the variable from the file
        with open("my_variable.pickle", "rb") as f:
            UserID = pickle.load(f)

        self.loadSettings()

        self.val = 0
        self.Investment = Investment()
        self.Investment.setProfile(UserID)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(664, 693)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_9.addWidget(self.label_2)
        self.StartDate = QtWidgets.QDateEdit(calendarPopup=True)
        self.StartDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.horizontalLayout_9.addWidget(self.StartDate)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.End = QtWidgets.QLabel(self.centralwidget)
        self.End.setObjectName("End")
        self.horizontalLayout_8.addWidget(self.End)
        self.EndDate = QtWidgets.QDateEdit(calendarPopup=True)
        self.EndDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.horizontalLayout_8.addWidget(self.EndDate)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_8)
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_10.addWidget(self.radioButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(550, 600))
        self.tableWidget.setObjectName("tableWidget")

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.updateTable()
        self.timer.timeout.connect(self.updateTable)
        self.timer.start(self.UpdateFrequency * 1000)

        # set the last column to stretch to fill any remaining space
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setObjectName("tableWidget")
        # self.tableWidget.setColumnCount(5)
        # self.tableWidget.setRowCount(1)
        self.updateTable()
        self.tableWidget.setColumnHidden(0, True)
        # make the table uneditable
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        # self.tableWidget.setSortingEnabled()

        # set the selection mode to select entire rows
        # self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.horizontalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.Sell = QtWidgets.QPushButton(self.centralwidget)
        self.Sell.setObjectName("Sell")
        self.Sell.clicked.connect(self.openSell)
        self.verticalLayout.addWidget(self.Sell)
        self.AddButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddButton.setObjectName("AddButton")
        self.AddButton.clicked.connect(self.addInvestment)
        self.verticalLayout.addWidget(self.AddButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1170, 36))
        self.menubar.setObjectName("menubar")

        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName("menuOptions")

        self.menuExports = QtWidgets.QMenu(self.menubar)
        self.menuExports.setObjectName("menuExports")

        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionChange_User = QtWidgets.QAction(MainWindow)
        self.actionChange_User.setObjectName("actionChange_User")
        self.actionChange_User.triggered.connect(self.openWindow)
        self.actionAdd_User = QtWidgets.QAction(MainWindow)
        self.actionAdd_User.setObjectName("actionAdd_User")
        self.actionAdd_User.triggered.connect(self.openAddUser)
        self.actionPrevious = QtWidgets.QAction(MainWindow)
        self.actionPrevious.setObjectName("actionPrevious")
        self.actionPrevious.triggered.connect(self.prevStage)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.triggered.connect(self.Save)
        self.actionGraph = QtWidgets.QAction(MainWindow)
        self.actionGraph.setObjectName("actionGraph")
        self.actionGraph.triggered.connect(self.Graph)
        self.actionStatement = QtWidgets.QAction(MainWindow)
        self.actionStatement.setObjectName("actionStatement")
        self.actionStatement.triggered.connect(self.Statement)
        self.actionMoneyLog = QtWidgets.QAction(MainWindow)
        self.actionMoneyLog.setObjectName("actionMoneyLog")
        self.actionMoneyLog.triggered.connect(self.MoneyLog)
        self.actionSellAll = QtWidgets.QAction(MainWindow)
        self.actionSellAll.setObjectName("actionSellAll")
        self.actionSellAll.triggered.connect(self.sellAll)
        self.actionSellProfit = QtWidgets.QAction(MainWindow)
        self.actionSellProfit.setObjectName("actionSellProfit")
        self.actionSellProfit.triggered.connect(self.sellProfit)
        self.actionShowMoneyGraph = QtWidgets.QAction(MainWindow)
        self.actionShowMoneyGraph.setObjectName("actionSellProfit")
        self.actionShowMoneyGraph.triggered.connect(self.showMoneyGraph)

        self.actionExportInvestment = QtWidgets.QAction(MainWindow)
        self.actionExportInvestment.setObjectName("actionSellProfit")
        self.actionExportInvestment.triggered.connect(self.InvestmentExcel)

        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionSettings.triggered.connect(self.Setting)

        self.menuSettings.addAction(self.actionSettings)

        self.menuExports.addAction(self.actionExportInvestment)

        self.menuOptions.addAction(self.actionChange_User)
        self.menuOptions.addAction(self.actionAdd_User)
        self.menuOptions.addAction(self.actionPrevious)
        self.menuOptions.addAction(self.actionSave)
        self.menuOptions.addAction(self.actionGraph)
        self.menuOptions.addAction(self.actionStatement)
        self.menuOptions.addAction(self.actionMoneyLog)
        self.menuOptions.addAction(self.actionSellAll)
        self.menuOptions.addAction(self.actionSellProfit)
        self.menuOptions.addAction(self.actionShowMoneyGraph)
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuExports.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        # set stylesheet for QTableWidget
        table_style = '''
            QTableWidget {
                border: 1px solid gray;
                border-radius: 3px;
                font-size: 12px;
                font-family: 'Segoe UI', sans-serif;
                background-color: white;
                selection-background-color: #99ccff;
                selection-color: white;
            }
            QTableWidget::item:selected {
                background-color: #99ccff;
                color: white;
            }
            QTableWidget::item:focus {
                background-color: #f0f0f0;
                color: black;
            }
            QHeaderView::section {
                background-color: #f2f2f2;
                padding: 4px;
                border: none;
                font-size: 12px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
                color: #333333;
            }
            QHeaderView::section:checked {
                background-color: #e6e6e6;
            }
        '''

        # set stylesheet for QScrollBar
        scrollbar_style = '''
            QScrollBar:vertical {
                border: none;
                background-color: #f2f2f2;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #d9d9d9;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                border: none;
                background-color: #f2f2f2;
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                border: none;
                background-color: #f2f2f2;
                height: 0 px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        '''

        # apply stylesheets to table widget and scrollbar
        self.tableWidget.setStyleSheet(table_style)
        self.tableWidget.verticalScrollBar().setStyleSheet(scrollbar_style)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def loadSettings(self):
        with open("Settings.pickle", "rb") as f:
            self.ProfitMargin, self.UpdateFrequency = pickle.load(f)
            # close previous timer and start new one
            self.timer = QTimer()
            self.timer.stop()
            self.timer.start(self.UpdateFrequency * 1000)
            self.timer.timeout.connect(self.updateTable)

    def InvestmentExcel(self):
        self.Investment.convertToExcel()

    def showMoneyGraph(self):
        self.window = QtWidgets.QMainWindow()
        self.window = graph.MyWindow()
        self.window.show()

    def Setting(self):
        self.window = QtWidgets.QMainWindow()
        self.window = Setting.MyWindow()
        self.window.show()
        print(self.UpdateFrequency)
        self.window.SubmitButton.clicked.connect(self.loadSettings)
        self.window.SubmitButton.clicked.connect(self.window.close)

    def MoneyLog(self):
        self.window = QtWidgets.QMainWindow()
        self.window = MoneyLogScreen.MyWindow()
        self.window.show()

    def Statement(self):
        self.window = QtWidgets.QMainWindow()
        self.window = StatementScreen.MyWindow()
        self.window.show()

    def Graph(self):
        self.window = QtWidgets.QMainWindow()
        self.window = graph1.MyWindow()
        self.window.show()

    def updateTable(self):
        startDate = endDate = None
        self.val += 1
        self.Investment.updateProfitLoss(self.Gold.getAsk())
        print(self.Gold.getAsk())
        if self.radioButton.isChecked():
            startDate = self.StartDate.date().toPyDate()
            endDate = self.EndDate.date().toPyDate()
        self.loadDataFromTable(StartDate=startDate, EndDate=endDate)

    def Save(self):
        DBFunctions.ClearTables()

    def prevStage(self):
        DBFunctions.previousStage()
        self.loadDataFromTable()

    def loadDataFromTable(self, StartDate=None, EndDate=None):
        with open("my_variable.pickle", "rb") as f:
            UserID = pickle.load(f)
        self.Investment.setProfile(UserID)
        print("yo" + str(StartDate))
        table = self.Investment.getTable(StartDate=StartDate, EndDate=EndDate)
        print(self.Investment.getRateRequired(StartDate=StartDate, EndDate=EndDate))
        self.load_dataframe_to_table(table, self.tableWidget)

    def sellAll(self):
        startdate = enddate = None
        if self.radioButton.isChecked():
            startdate = self.StartDate.date().toPyDate()
            enddate = self.EndDate.date().toPyDate()
        self.window = QtWidgets.QMainWindow()
        self.window = sellRate.MyWindow()
        self.window.show()
        self.window.pushButton.clicked.connect(lambda: self.Investment.sellAll(Rate=float(self.window.Rate.text()),
                                                                               Date=self.window.Date.date().toPyDate(),
                                                                               StartDate=startdate, EndDate=enddate))
        self.window.pushButton.clicked.connect(self.updateTable)
        self.window.pushButton.clicked.connect(self.window.close)

    def sellProfit(self):
        startdate = enddate = None
        if self.radioButton.isChecked():
            startdate = self.StartDate.date().toPyDate()
            enddate = self.EndDate.date().toPyDate()
        self.window = QtWidgets.QMainWindow()
        self.window = sellRate.MyWindow()
        self.window.show()
        self.window.pushButton.clicked.connect(
            lambda: self.Investment.sellProfit(Rate=float(self.window.Rate.text()),
                                               Date=self.window.Date.date().toPyDate(), StartDate=startdate,
                                               EndDate=enddate, ProfitMargin=self.ProfitMargin))
        self.window.pushButton.clicked.connect(self.updateTable)
        self.window.pushButton.clicked.connect(self.window.close)

    def openSell(self):
        self.window = QtWidgets.QMainWindow()
        self.window = sellRate.MyWindow()
        self.window.show()
        self.window.pushButton.clicked.connect(
            lambda: self.getTransactionID(self.window.Rate.text(), self.window.Date.date().toPyDate()))
        self.window.pushButton.clicked.connect(self.updateTable)
        self.window.pushButton.clicked.connect(self.window.close)
        # self.window.AddButton.clicked.connect(self.loadDataFromTable)

    def openAddUser(self):
        self.window = QtWidgets.QMainWindow()
        self.window = AddUser.MyWindow()
        self.window.show()
        # self.window.AddButton.clicked.connect(self.loadDataFromTable)
        self.window.AddButton.clicked.connect(self.window.close)

    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.window = UserSelect.MyWindow()
        self.window.show()
        self.window.SelectButton.clicked.connect(self.updateTable)
        self.window.SelectButton.clicked.connect(self.window.close)

    def addInvestment(self):
        self.window = QtWidgets.QMainWindow()
        self.window = Add.MyWindow()
        self.window.show()
        self.window.AddButton.clicked.connect(self.updateTable)
        self.window.AddButton.clicked.connect(self.window.close)

    def get_selected_data(self):
        selected_rows = self.tableWidget.selectedItems()
        data = []
        for item in selected_rows:
            # get the row and column indexes of the selected cell
            row = item.row()
            column = item.column()
            # get the data from the cell
            cell_data = self.tableWidget.item(row, column).text()
            # append the cell data to the list of data
            data.append(cell_data)
        # return the list of data
        return data

    def getTransactionID(self, Rate=None, Date=None):
        if Rate == "":
            Rate = None
        else:
            Rate = float(Rate)
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
        self.Investment.sell(uniqueID, Rate=Rate, Date=Date)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.updateTable()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Sell.setText(_translate("MainWindow", "Sell"))
        self.AddButton.setText(_translate("MainWindow", "AddButton"))
        self.menuOptions.setTitle(_translate("MainWindow", "Options"))
        self.actionChange_User.setText(_translate("MainWindow", "Change User"))
        self.actionAdd_User.setText(_translate("MainWindow", "Add User"))
        self.actionPrevious.setText(_translate("MainWindow", "Undo"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionGraph.setText(_translate("MainWindow", "Graph"))
        self.actionStatement.setText(_translate("MainWindow", "Statement"))
        self.actionMoneyLog.setText(_translate("MainWindow", "MoneyLog"))
        self.actionSellAll.setText(_translate("MainWindow", "SellAll"))
        self.actionSellProfit.setText(_translate("MainWindow", "SellProfit"))
        self.actionShowMoneyGraph.setText(_translate("MainWindow", "MoneyGraph"))

        self.menuExports.setTitle(_translate("MainWindow", "Export"))
        self.actionExportInvestment.setText(_translate("MainWindow", "Export Investments"))

        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))

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
                if column == len(dataframe.columns) - 1:
                    #
                    if dataframe.iloc[row, column] == 0:
                        item.setForeground(QColor('black'))
                    if dataframe.iloc[row, column] > 0:
                        item.setForeground(QColor('green'))
                    if dataframe.iloc[row, column] < 0:
                        item.setForeground(QColor('red'))
                table_widget.setItem(row, column, item)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
