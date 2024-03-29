from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject

import GoldUnits
import SetupFile
from Database import User


class Ui_Form(QObject):
    def setupUi(self, Form):
        self.User = User.User()
        Form.setObjectName("Form")
        Form.resize(775, 662)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.GoldUnit_Text = QtWidgets.QLabel(Form)
        self.GoldUnit_Text.setObjectName("GoldUnit_Text")
        self.horizontalLayout_5.addWidget(self.GoldUnit_Text)
        self.GoldUnit = QtWidgets.QComboBox(Form)
        self.GoldUnit.setObjectName("GoldUnit")
        self.GoldUnit.addItem("")
        self.GoldUnit.addItem("")
        self.GoldUnit.addItem("")
        self.GoldUnit.addItem("")
        self.horizontalLayout_5.addWidget(self.GoldUnit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.UpdateFrequency_Text = QtWidgets.QLabel(Form)
        self.UpdateFrequency_Text.setObjectName("UpdateFrequency_Text")
        self.horizontalLayout.addWidget(self.UpdateFrequency_Text)
        self.UpdateFrequency = QtWidgets.QSpinBox(Form)
        self.UpdateFrequency.setObjectName("UpdateFrequency")
        self.horizontalLayout.addWidget(self.UpdateFrequency)
        self.UpdateFrequencyUnit = QtWidgets.QLabel(Form)
        self.UpdateFrequencyUnit.setObjectName("UpdateFrequencyUnit")
        self.UpdateFrequencyUnit.setText("s")
        self.horizontalLayout.addWidget(self.UpdateFrequencyUnit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
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
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.MinmumProfitMargin_Text = QtWidgets.QLabel(Form)
        self.MinmumProfitMargin_Text.setObjectName("MinmumProfitMargin_Text")
        self.horizontalLayout_3.addWidget(self.MinmumProfitMargin_Text)
        self.MinimumProfitMargin = QtWidgets.QDoubleSpinBox(Form)
        self.MinimumProfitMargin.setObjectName("MinimumProfitMargin")
        self.horizontalLayout_3.addWidget(self.MinimumProfitMargin)
        self.MinimumProfitMarginUnit = QtWidgets.QLabel(Form)
        self.MinimumProfitMarginUnit.setObjectName("MinimumProfitMarginUnit")
        self.MinimumProfitMarginUnit.setText("%")
        self.horizontalLayout_3.addWidget(self.MinimumProfitMarginUnit)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
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
        self.GoldUnit_Text.setText(_translate("Form", "Gold unit: "))
        self.GoldUnit.setItemText(0, _translate("Form", "Gram"))
        self.GoldUnit.setItemText(1, _translate("Form", "Tola"))
        self.GoldUnit.setItemText(2, _translate("Form", "Troy ounce"))
        self.GoldUnit.setItemText(3, _translate("Form", "Kilogram"))
        self.UpdateFrequency_Text.setText(_translate("Form", "Update frequency: "))
        self.DecimalPoints_Text.setText(_translate("Form", "Decimal points: "))
        self.MinmumProfitMargin_Text.setText(_translate("Form", "Minimum profit margin : "))
        self.SaveButton.setText(_translate("Form", "Save"))

    def setProfile(self, Profile):
        """set profile and settings"""
        self.Profile = Profile
        self.User.SelectProfile(self.Profile)
        MinimumProfit, dp, self.updatefreq, GoldUnit,_ = self.User.GetSettings()
        self.MinimumProfitMargin.setValue(MinimumProfit)
        self.UpdateFrequency.setValue(self.updatefreq)
        self.DecimalPoints.setValue(dp)
        if GoldUnit == GoldUnits.gram:
            self.GoldUnit.setCurrentIndex(0)
        elif GoldUnit == GoldUnits.tola:
            self.GoldUnit.setCurrentIndex(1)
        elif GoldUnit == GoldUnits.troyounce:
            self.GoldUnit.setCurrentIndex(2)
        elif GoldUnit == GoldUnits.kilogram:
            self.GoldUnit.setCurrentIndex(3)

    def Save(self):
        """save settings"""
        if self.GoldUnit.currentIndex() == 0:
            unit = GoldUnits.gram
        elif self.GoldUnit.currentIndex() == 1:
            unit = GoldUnits.tola
        elif self.GoldUnit.currentIndex() == 2:
            unit = GoldUnits.troyounce
        elif self.GoldUnit.currentIndex() == 3:
            unit = GoldUnits.kilogram
        self.User.ChangeSettings(self.MinimumProfitMargin.value(), self.DecimalPoints.value(),
                                 self.UpdateFrequency.value(), unit)

    def updatefreqchanged(self):
        """check if update frequency changed."""
        if self.updatefreq == self.UpdateFrequency.value():
            return False
        else:
            return True


class MyWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.SaveButton.clicked.connect(self.close)

        self.setWindowTitle("Settings")
        self.setStyleSheet(SetupFile.Background)
        self.GoldUnit.setStyleSheet(SetupFile.ComboBox)
        self.UpdateFrequency.setStyleSheet(SetupFile.SpinBox)
        self.DecimalPoints.setStyleSheet(SetupFile.SpinBox)
        self.MinimumProfitMargin.setStyleSheet(SetupFile.DoubleSpinBox)
        self.SaveButton.setStyleSheet(SetupFile.Button)

