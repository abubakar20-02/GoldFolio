# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FinalSettings.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os
import pickle

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
from Database import User


class Ui_Form(QObject):
    def setupUi(self, Form):
        self.Profile = None
        self.User = User.User()
        Form.setObjectName("Form")
        Form.resize(496, 454)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.UpdateFrequency_Text = QtWidgets.QLabel(Form)
        self.UpdateFrequency_Text.setObjectName("UpdateFrequency_Text")
        self.horizontalLayout.addWidget(self.UpdateFrequency_Text)
        self.UpdateFrequency = QtWidgets.QSpinBox(Form)
        self.UpdateFrequency.setObjectName("UpdateFrequency")
        self.horizontalLayout.addWidget(self.UpdateFrequency)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.DecimalPoints_Text = QtWidgets.QLabel(Form)
        self.DecimalPoints_Text.setObjectName("DecimalPoints_Text")
        self.horizontalLayout_2.addWidget(self.DecimalPoints_Text)
        self.DecimalPoints = QtWidgets.QSpinBox(Form)
        self.DecimalPoints.setMaximum(5)
        self.DecimalPoints.setObjectName("DecimalPoints")
        self.horizontalLayout_2.addWidget(self.DecimalPoints)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.MinmumProfitMargin_Text = QtWidgets.QLabel(Form)
        self.MinmumProfitMargin_Text.setObjectName("MinmumProfitMargin_Text")
        self.horizontalLayout_3.addWidget(self.MinmumProfitMargin_Text)
        self.MinimumProfitMargin = QtWidgets.QDoubleSpinBox(Form)
        self.MinimumProfitMargin.setObjectName("MinimumProfitMargin")
        self.horizontalLayout_3.addWidget(self.MinimumProfitMargin)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.SaveButton = QtWidgets.QPushButton(Form)
        self.SaveButton.setObjectName("SaveButton")
        self.horizontalLayout_4.addWidget(self.SaveButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.SaveButton.clicked.connect(self.Save)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.UpdateFrequency_Text.setText(_translate("Form", "Update frequency: "))
        self.DecimalPoints_Text.setText(_translate("Form", "Decimal points: "))
        self.MinmumProfitMargin_Text.setText(_translate("Form", "Minimum profit margin : "))
        self.SaveButton.setText(_translate("Form", "Save"))

    def setProfile(self, Profile):
        self.Profile = Profile
        self.User.SelectProfile(self.Profile)
        MinimumProfit, dp, updatefreq = self.User.GetSettings()
        print(f"MPM {MinimumProfit},dp {dp} , uf {updatefreq}")
        self.MinimumProfitMargin.setValue(MinimumProfit)
        self.UpdateFrequency.setValue(updatefreq)
        self.DecimalPoints.setValue(dp)

    def Save(self):
        self.User.ChangeSettings(self.MinimumProfitMargin.value(), self.DecimalPoints.value(),
                                 self.UpdateFrequency.value())


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.SaveButton.clicked.connect(self.close)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
