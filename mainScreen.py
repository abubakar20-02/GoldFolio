# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainScreen.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QHeaderView
from Investment import Investment


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.Investment = Investment()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1170, 661)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setMinimumSize(QtCore.QSize(550, 600))
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # set the last column to stretch to fill any remaining space
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.setObjectName("tableWidget")
        # self.tableWidget.setColumnCount(5)
        # self.tableWidget.setRowCount(1)
        self.load_dataframe_to_table(self.Investment.getTable(),self.tableWidget)
        self.tableWidget.setColumnHidden(0, True)
        self.horizontalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(500, 500))
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, -1, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton.clicked.connect(self.getTransactionID)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1170, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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
        print(data)
        # return the list of data
        return data

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
        uniqueID= list(set(id))
        print(uniqueID)
        self.Investment.sell(uniqueID)
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.load_dataframe_to_table(self.Investment.getTable(), self.tableWidget)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))

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
                table_widget.setItem(row, column, item)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
