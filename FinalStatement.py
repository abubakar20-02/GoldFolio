import os
import pickle
from datetime import date
from datetime import timedelta

import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import xlwings as xw
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QTableWidget, QAbstractItemView, QFileDialog, QDesktopWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import SetupFile
from Database import Statement, User


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Ui_Form(object):
    def setupUi(self, Form):
        self.Startdate = None
        self.Enddate = None
        self.YAxisValue = "Value_Change"
        self.Statement = Statement.Statement()
        self.UserProfile = User.User()
        with open("my_variable.pickle", "rb") as f:
            UserID = pickle.load(f)
            self.UserProfile.SelectProfile(UserID)
        self.loadSettings()
        Form.setObjectName("Form")
        Form.resize(778, 602)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.Preset_Text = QtWidgets.QLabel(Form)
        self.Preset_Text.setObjectName("Preset_Text")
        self.horizontalLayout_11.addWidget(self.Preset_Text)
        self.PresetComboBox = QtWidgets.QComboBox(Form)
        self.PresetComboBox.setObjectName("PresetComboBox")
        self.horizontalLayout_11.addWidget(self.PresetComboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setText("")
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)

        self.StartDate = QtWidgets.QDateEdit(calendarPopup=True)
        self.StartDate.setMaximumDate(QDate.currentDate())
        self.StartDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.StartDate.dateChanged.connect(self.updateDateRangeForEndDate)

        self.horizontalLayout_3.addWidget(self.StartDate)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.EndDate_Text = QtWidgets.QLabel(Form)
        self.EndDate_Text.setObjectName("EndDate_Text")
        self.horizontalLayout_2.addWidget(self.EndDate_Text)

        self.EndDate = QtWidgets.QDateEdit(calendarPopup=True)
        self.EndDate.setMaximumDate(QDate.currentDate())
        self.EndDate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.EndDate.dateChanged.connect(self.updateDateRangeForStartDate)

        self.horizontalLayout_2.addWidget(self.EndDate)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.YAxis_Text = QtWidgets.QLabel(Form)
        self.YAxis_Text.setObjectName("YAxis_Text")
        self.horizontalLayout_6.addWidget(self.YAxis_Text)
        self.YAxis = QtWidgets.QComboBox(Form)
        self.YAxis.setObjectName("YAxis")
        self.YAxis.addItem("Profit Loss")
        self.YAxis.addItem("Gold")
        self.YAxis.addItem("Bought For")
        self.horizontalLayout_6.addWidget(self.YAxis)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.Graph = QtWidgets.QWidget(Form)
        self.Graph.setStyleSheet(
            'QWidget#Graph { border: 2px solid black; border-radius: 10px; background-color: white; }')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Graph.sizePolicy().hasHeightForWidth())
        self.Graph.setSizePolicy(sizePolicy)
        self.Graph.setMinimumSize(QtCore.QSize(300, 300))
        self.Graph.setObjectName("Graph")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Graph)
        self.verticalLayout.setObjectName("verticalLayout")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.canvas = MplCanvas(self, height=2, width=4, dpi=100)
        desktop = QDesktopWidget()
        width = int(desktop.availableGeometry().width() * 0.5)
        self.canvas.setMaximumWidth(width)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setMinimumSize(QtCore.QSize(300, 300))
        self.canvas.setObjectName("canvas")
        self.canvas.setSizePolicy(sizePolicy)
        self.verticalLayout.addWidget(self.canvas)
        self.verticalLayout_3.addWidget(self.Graph)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem3)
        self.ExportButton = QtWidgets.QPushButton(Form)
        self.ExportButton.setObjectName("ExportButton")
        self.horizontalLayout_12.addWidget(self.ExportButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_12)

        self.PresetComboBox.currentIndexChanged.connect(self.checkIfCustom)
        self.PresetComboBox.addItem("Month")
        self.PresetComboBox.addItem("2 Weeks")
        self.PresetComboBox.addItem("Year")
        self.PresetComboBox.addItem("5 Years")
        self.PresetComboBox.addItem("Custom")
        self.YAxis.currentIndexChanged.connect(self.changeYAxis)
        self.radioButton.setEnabled(False)
        self.EnableDates(False)
        self.radioButton.clicked.connect(self.checkRadioButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def loadSettings(self):
        """load settings from user database"""
        _, self.DecimalPoints, _, _, self.Currency = self.UserProfile.GetSettings()

    def changeYAxis(self):
        """change y axis of the graph"""
        if self.YAxis.currentIndex() == 0:
            self.YAxisValue = "Value_Change"
        if self.YAxis.currentIndex() == 1:
            self.YAxisValue = "Gold"
        if self.YAxis.currentIndex() == 2:
            self.YAxisValue = "BoughtFor"
        self.checkIfCustom()

    def updateDateRangeForEndDate(self):
        """update date range for end date"""
        self.Search()
        self.EndDate.setMinimumDate(self.StartDate.date())

    def updateDateRangeForStartDate(self):
        """update date range for start date"""
        self.Search()
        self.StartDate.setMaximumDate(self.EndDate.date())

    def Search(self):
        """find best suitable graph mode to display data."""
        self.Startdate = self.StartDate.date().toPyDate()
        self.Enddate = self.EndDate.date().toPyDate()

        self.loadDataFromTable(StartDate=self.Startdate, EndDate=self.Enddate)
        self.line(self.YAxisValue, StartDate=self.Startdate, EndDate=self.Enddate)
        self.canvas.draw()

    def checkIfCustom(self):
        """check if custom is clicked"""
        if self.PresetComboBox.currentIndex() == self.PresetComboBox.count() - 1:
            self.radioButton.setEnabled(True)
            self.checkRadioButton()
        else:
            self.EnableDates(False)
            self.radioButton.setEnabled(False)

        from datetime import date

        today = date.today()
        if self.PresetComboBox.currentIndex() == 0:
            timedelta1 = 30
        elif self.PresetComboBox.currentIndex() == 1:
            timedelta1 = 14
        elif self.PresetComboBox.currentIndex() == 2:
            timedelta1 = 365
        elif self.PresetComboBox.currentIndex() == 3:
            timedelta1 = 1826

        if self.PresetComboBox.currentIndex() != 4:
            self.Startdate = today - timedelta(days=timedelta1)
            self.Enddate = today
            self.loadDataFromTable(StartDate=self.Startdate, EndDate=self.Enddate)
            # self.MoneyLog.Overall("Change", StartDate=today - timedelta(days=timedelta1), EndDate=today)
            self.line(self.YAxisValue, StartDate=self.Startdate, EndDate=self.Enddate)
            self.canvas.draw()

    def checkRadioButton(self):
        """check if radio button clicked."""
        if self.radioButton.isChecked():
            self.EnableDates(True)
            self.Search()
        else:
            self.Startdate = None
            self.Enddate = None
            self.loadDataFromTable(StartDate=self.Startdate, EndDate=self.Enddate)
            self.EnableDates(False)
            self.line(self.YAxisValue)
            self.canvas.draw()

    def EnableDates(self, Bool):
        """enable or disable dates."""
        self.StartDate.setEnabled(Bool)
        self.EndDate.setEnabled(Bool)

    def loadDataFromTable(self, StartDate=None, EndDate=None):
        """Load data from database"""
        with open("my_variable.pickle", "rb") as f:
            UserID = pickle.load(f)
        self.Statement.setProfile(UserID)
        self.load_dataframe_to_table(self.Statement.getTable(StartDate=StartDate, EndDate=EndDate), self.tableWidget)

    def load_dataframe_to_table(self, dataframe, table_widget):
        # Set the number of rows and columns for the table
        table_widget.setRowCount(len(dataframe))
        table_widget.setColumnCount(len(dataframe.columns))

        dataframe.columns = ["Investment_ID", "Date", "Gold (g)", f"Bought for({self.Currency})", "Profit/Loss (%)",
                             f"Value change ({self.Currency})"]

        # Add the headers for the table columns
        table_widget.setHorizontalHeaderLabels(dataframe.columns)

        # Populate the table with data
        for row in range(len(dataframe)):
            for column in range(len(dataframe.columns)):
                item = QTableWidgetItem()
                # column 0 is transaction id
                if column == 0 or column == 1:
                    item.setData(QtCore.Qt.DisplayRole, str(dataframe.iloc[row, column]))
                else:
                    item.setData(QtCore.Qt.DisplayRole, round(float(dataframe.iloc[row, column]), self.DecimalPoints))

                # Set the color based on the value
                if item.text() == "0.0":
                    item = QTableWidgetItem(str("-"))
                if column == len(dataframe.columns) - 1 or column == len(dataframe.columns) - 2:
                    if dataframe.iloc[row, column] == 0:
                        item.setForeground(QColor('black'))
                    if dataframe.iloc[row, column] > 0:
                        item.setForeground(QColor('green'))
                    if dataframe.iloc[row, column] < 0:
                        item.setForeground(QColor('red'))
                item.setTextAlignment(Qt.AlignCenter)
                table_widget.setItem(row, column, item)

    def line(self, ValueSelect, StartDate=None, EndDate=None):
        self.canvas.axes.clear()

        data = self.Statement.Overall(ValueSelect, StartDate, EndDate)
        if data is None:
            return
        x = list(data.keys())
        y = list(data.values())
        self.canvas.axes.plot(x, y, '-o')
        self.canvas.axes.grid(True)
        self.canvas.axes.set_xlabel('Date')
        self.canvas.axes.set_ylabel(ValueSelect)

        # # # # Format the x-axis ticks as dates
        if self.check_date_format(x[0]) == '000000':
            # set the x-axis tick labels as dates
            date_format = mdates.DateFormatter('%Y-%m-%d')
            self.canvas.axes.xaxis.set_major_formatter(date_format)

            # set the x-axis major tick locations to every week
            self.canvas.axes.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        else:
            self.canvas.axes.xaxis.set_major_locator(ticker.MultipleLocator(3))

    def closeExcel(self, FilePath):
        # Connect to the Excel application
        if not os.path.exists(FilePath):
            return

        try:
            book = xw.Book(FilePath)
            book.close()
        except Exception as e:
            print(e)

    def export(self):
        """export as excel or pdf."""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filepath, _ = QFileDialog.getSaveFileName(None, 'Investment',
                                                  "", "Excel Work Book(*.xlsx);; PDF(*.pdf)", options=options)
        # Check if the file extension is ".xlsx"
        if filepath.lower().endswith('.xlsx'):
            self.closeExcel(filepath)
            self.Statement.convertToExcel(self.Currency, self.DecimalPoints, StartDate=self.Startdate,
                                          EndDate=self.Enddate, FilePath=filepath)
        else:
            self.Statement.PDF(filepath, self.Currency, self.DecimalPoints, StartDate=self.Startdate,
                               EndDate=self.Enddate)

    def check_date_format(self, date_str):
        """checks if date is in Y-m-d"""
        try:
            format_str = date_str.strftime('%f')
        except:
            return "a"
        return format_str

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Preset_Text.setText(_translate("Form", "Preset: "))
        self.label_2.setText(_translate("Form", "Start Date: "))
        self.EndDate_Text.setText(_translate("Form", "End Date: "))
        self.YAxis_Text.setText(_translate("Form", "Y axis:"))
        self.YAxis.setItemText(0, _translate("Form", "ProfitLoss"))
        self.YAxis.setItemText(1, _translate("Form", "Gold"))
        self.YAxis.setItemText(2, _translate("Form", "BoughtFor"))
        self.ExportButton.setText(_translate("Form", "Export"))


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        today = date.today()
        self.Startdate = today - timedelta(days=30)
        self.Enddate = today
        self.loadDataFromTable(StartDate=self.Startdate, EndDate=self.Enddate)
        self.tableWidget.setColumnHidden(0, True)
        self.line(self.YAxisValue, StartDate=self.Startdate, EndDate=self.Enddate)
        self.ExportButton.clicked.connect(self.export)

        self.setWindowTitle("Statement")
        self.setStyleSheet(SetupFile.Background)
        self.tableWidget.setStyleSheet(SetupFile.QTable)
        self.EndDate.setStyleSheet(SetupFile.DateEdit)
        self.StartDate.setStyleSheet(SetupFile.DateEdit)
        self.PresetComboBox.setStyleSheet(SetupFile.ComboBox)
        self.YAxis.setStyleSheet(SetupFile.ComboBox)
        self.ExportButton.setStyleSheet(SetupFile.Button)

