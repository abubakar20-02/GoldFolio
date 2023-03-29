# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FinalMoneyLog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import pickle
from datetime import timedelta, datetime
from datetime import date

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QObject, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QTableWidget, QAbstractItemView
from Database import Statement

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import matplotlib.ticker as ticker


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Ui_Form(QObject):
    def setupUi(self, Form):
        self.Statement = Statement.Statement()
        Form.setObjectName("Form")
        Form.resize(646, 353)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.Preset_Text = QtWidgets.QLabel(Form)
        self.Preset_Text.setObjectName("Preset_Text")
        self.horizontalLayout_11.addWidget(self.Preset_Text)
        self.PresetComboBox = QtWidgets.QComboBox(Form)
        self.PresetComboBox.addItem("Month")
        self.PresetComboBox.addItem("2 Weeks")
        self.PresetComboBox.addItem("Year")
        self.PresetComboBox.addItem("5 Years")
        self.PresetComboBox.addItem("Custom")
        self.PresetComboBox.setObjectName("PresetComboBox")
        self.PresetComboBox.currentIndexChanged.connect(self.checkIfCustom)
        self.horizontalLayout_11.addWidget(self.PresetComboBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
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
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout_10.addLayout(self.verticalLayout)
        self.horizontalLayout_9.addLayout(self.horizontalLayout_10)
        self.canvas = MplCanvas(self, width=650, height=650, dpi=100)
        self.canvas.setMinimumSize(QtCore.QSize(650, 650))
        self.canvas.setObjectName("canvas")
        self.horizontalLayout_9.addWidget(self.canvas)
        self.verticalLayout_2.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem2)
        self.ExportButton = QtWidgets.QPushButton(Form)
        self.ExportButton.setObjectName("ExportButton")
        self.horizontalLayout_12.addWidget(self.ExportButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_12)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.radioButton.setEnabled(False)
        self.EnableDates(False)
        self.radioButton.clicked.connect(self.checkRadioButton)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def updateDateRangeForEndDate(self):
        self.Search()
        self.EndDate.setMinimumDate(self.StartDate.date())

    def updateDateRangeForStartDate(self):
        self.Search()
        self.StartDate.setMaximumDate(self.EndDate.date())

    def Search(self):
        StartDate = self.StartDate.date().toPyDate()
        EndDate = self.EndDate.date().toPyDate()

        self.loadDataFromTable(StartDate=StartDate, EndDate=EndDate)
        # self.MoneyLog.Overall("Change", StartDate=StartDate, EndDate=EndDate)
        self.line("Value_Change", StartDate=StartDate, EndDate=EndDate)
        self.canvas.draw()

    def checkIfCustom(self):
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
            self.loadDataFromTable(StartDate=today - timedelta(days=timedelta1), EndDate=today)
            # self.MoneyLog.Overall("Change", StartDate=today - timedelta(days=timedelta1), EndDate=today)
            self.line("Value_Change",StartDate=today - timedelta(days=timedelta1), EndDate=today)
            self.canvas.draw()
            print("work")

    def checkRadioButton(self):
        if self.radioButton.isChecked():
            self.EnableDates(True)
            self.Search()
        else:
            self.loadDataFromTable()
            self.EnableDates(False)
            self.line("Value_Change")
            self.canvas.draw()
            # self.MoneyLog.Overall("Change")

    def EnableDates(self, Bool):
        self.StartDate.setEnabled(Bool)
        self.EndDate.setEnabled(Bool)

    def loadDataFromTable(self, StartDate=None, EndDate=None):
        with open("my_variable.pickle", "rb") as f:
            UserID = pickle.load(f)
        self.Statement.setProfile(UserID)
        self.load_dataframe_to_table(self.Statement.getTable(StartDate=StartDate, EndDate=EndDate), self.tableWidget)

    def load_dataframe_to_table(self, dataframe, table_widget):
        # Set the number of rows and columns for the table
        table_widget.setRowCount(len(dataframe))
        table_widget.setColumnCount(len(dataframe.columns))

        # Add the headers for the table columns
        table_widget.setHorizontalHeaderLabels(dataframe.columns)

        # Populate the table with data
        for row in range(len(dataframe)):
            for column in range(len(dataframe.columns)):
                item = QTableWidgetItem(str(dataframe.iloc[row, column]))
                print(item.text())
                # Set the color based on the value
                if item.text() =="0.0":
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

    def line(self, ValueSelect="Value_Change", StartDate=None, EndDate=None):
        self.canvas.axes.clear()

        # self.canvas.axes.xaxis.set_major_locator(MaxNLocator(nbins=5))
        # self.canvas.axes.xaxis.set_major_locator(FixedLocator([15500, 16500, 17500, 18500, 19500]))

        data = self.Statement.Overall(ValueSelect, StartDate, EndDate)
        x = list(data.keys())
        # xv = range(0,len(x))
        y = list(data.values())
        print(x)
        print(y)
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
        print("inside")

    def check_date_format(self, date_str):
        try:
            format_str = date_str.strftime('%f')
            print(format_str)
        except:
            return "a"
        return format_str
        # for fmt in ('%Y-%m-%d', '%Y-%m', '%Y'):
        #     try:
        #         # Get the format of the datetime object
        #         # date_obj = datetime.strptime(date_str, fmt)
        #         return fmt
        #     except ValueError:
        #         pass
        # raise ValueError("Invalid date format")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Preset_Text.setText(_translate("Form", "Preset: "))
        self.label_2.setText(_translate("Form", "Start Date: "))
        self.EndDate_Text.setText(_translate("Form", "End Date: "))
        self.ExportButton.setText(_translate("Form", "Export"))


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        today = date.today()
        self.loadDataFromTable(StartDate=today - timedelta(days=30), EndDate=today)
        self.tableWidget.setColumnHidden(0, True)
        self.line("Value_Change", StartDate=today - timedelta(days=30), EndDate=today)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    Form = MyWindow()
    Form.show()
    sys.exit(app.exec_())
