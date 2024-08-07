# -*- coding: utf-8 -*-
"""
Version 2.1
Modified : Wed May 1, 2024 
@author acases
@author cfigueroa

Version 1.0
Created  : Fri Sep 25 18:24:06 2020
@author: facua
"""


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guiPlasma.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import numpy as np
import time
#import piplates.DAQC2plate as DAQC2
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import datetime
import csv
from scipy import signal
from PyQt5 import QtCore, QtGui, QtWidgets

matplotlib.rcParams['toolbar'] = 'None'

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.numberMeasurements = 500
        self.sweepTime = 0.25
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 420)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 600))
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.magneticField = QtWidgets.QComboBox(self.centralwidget)
        self.magneticField.setGeometry(QtCore.QRect(10, 90, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.magneticField.setFont(font)
        self.magneticField.setObjectName("magneticField")
        self.magneticField.addItem("")
        self.magneticField.addItem("")
        self.lowerVoltage = QtWidgets.QComboBox(self.centralwidget)
        self.lowerVoltage.setGeometry(QtCore.QRect(180, 90, 91, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lowerVoltage.setFont(font)
        self.lowerVoltage.setObjectName("lowerVoltage")
        self.lowerVoltage.addItem("")
        self.lowerVoltage.addItem("")
        self.lowerVoltage.addItem("")
        self.lowerVoltage.addItem("")
        self.lowerVoltage.addItem("")
        self.lowerVoltage.addItem("")
        self.lowerVoltage.addItem("")
        self.higherVoltage = QtWidgets.QComboBox(self.centralwidget)
        self.higherVoltage.setGeometry(QtCore.QRect(290, 90, 91, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.higherVoltage.setFont(font)
        self.higherVoltage.setObjectName("higherVoltage")
        self.higherVoltage.addItem("")
        self.higherVoltage.addItem("")
        self.higherVoltage.addItem("")
        self.higherVoltage.addItem("")
        self.higherVoltage.addItem("")
        self.higherVoltage.addItem("")
        self.higherVoltage.addItem("")
        self.gas = QtWidgets.QComboBox(self.centralwidget)
        self.gas.setGeometry(QtCore.QRect(410, 90, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.gas.setFont(font)
        self.gas.setStyleSheet("")
        self.gas.setObjectName("gas")
        self.gas.addItem("")
        self.gas.addItem("")
        self.gas.addItem("")
        self.gas.addItem("")
        self.sweepTimeLCD = QtWidgets.QLCDNumber(self.centralwidget)
        self.sweepTimeLCD.setGeometry(QtCore.QRect(50, 260, 121, 71))
        self.sweepTimeLCD.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sweepTimeLCD.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sweepTimeLCD.setObjectName("sweepTimeLCD")
        self.sweepTimeLCD.smallDecimalPoint()
        self.numberMeasurementsLCD = QtWidgets.QLCDNumber(self.centralwidget)
        self.numberMeasurementsLCD.setGeometry(QtCore.QRect(340, 260, 121, 71))
        self.numberMeasurementsLCD.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.numberMeasurementsLCD.setFrameShadow(QtWidgets.QFrame.Raised)
        self.numberMeasurementsLCD.setObjectName("numberMeasurementsLCD")
        self.runButton = QtWidgets.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(600, 130, 151, 121))
        self.downVoltageSweep = QtWidgets.QPushButton(self.centralwidget)
        self.downVoltageSweep.setGeometry(QtCore.QRect(20, 350, 71, 61))
        self.downVoltageSweep.setStyleSheet("background-image: url(Resources/downarrow.png);")
        self.downVoltageSweep.setText("")
        self.downVoltageSweep.setObjectName("downVoltageSweep")
        self.downVoltageSweep.clicked.connect(self.SubstractSweepTime)
        self.upVoltageSweep = QtWidgets.QPushButton(self.centralwidget)
        self.upVoltageSweep.setGeometry(QtCore.QRect(130, 350, 71, 61))
        self.upVoltageSweep.setStyleSheet("background-image: url(Resources/uparrow.png);")
        self.upVoltageSweep.setText("")
        self.upVoltageSweep.setObjectName("upVoltageSweep")
        self.upVoltageSweep.clicked.connect(self.AddSweepTime)
        self.downMeasurements = QtWidgets.QPushButton(self.centralwidget)
        self.downMeasurements.setGeometry(QtCore.QRect(320, 350, 71, 61))
        self.downMeasurements.setStyleSheet("background-image: url(Resources/downarrow.png);")
        self.downMeasurements.setText("")
        self.downMeasurements.setObjectName("downMeasurements")
        self.downMeasurements.clicked.connect(self.SubstractMeasurements)
        self.upMeasurements = QtWidgets.QPushButton(self.centralwidget)
        self.upMeasurements.setGeometry(QtCore.QRect(430, 350, 71, 61))
        self.upMeasurements.setStyleSheet("background-image: url(Resources/uparrow.png);")
        self.upMeasurements.setText("")
        self.upMeasurements.setObjectName("upMeasurements")
        self.upMeasurements.clicked.connect(self.AddMeasurements)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.runButton.setFont(font)
        self.runButton.setStyleSheet("background-image: url(Resources/green.png); \n""color: rgb(255, 255, 255); \n")
        self.runButton.setObjectName("runButton")
        self.runButton.clicked.connect(self.RunButton)
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(600, 260, 151, 121))
        self.exitButton.setFont(font)
        self.exitButton.setStyleSheet("color: rgb(255, 255, 255);\n" "background-image: url(Resources/red.png);")
        self.exitButton.setObjectName("exitButton")
        self.exitButton.clicked.connect(app.quit)
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(140, 10, 491, 31))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(650, 10, 111, 111))
        self.logo.setObjectName("logo")
        self.magFieldLabel = QtWidgets.QLabel(self.centralwidget)
        self.magFieldLabel.setGeometry(QtCore.QRect(20, 50, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.magFieldLabel.setFont(font)
        self.magFieldLabel.setObjectName("magFieldLabel")
        self.voltageRampLabel = QtWidgets.QLabel(self.centralwidget)
        self.voltageRampLabel.setGeometry(QtCore.QRect(220, 50, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.voltageRampLabel.setFont(font)
        self.voltageRampLabel.setObjectName("voltageRampLabel")
        self.gasLabel = QtWidgets.QLabel(self.centralwidget)
        self.gasLabel.setGeometry(QtCore.QRect(460, 50, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.gasLabel.setFont(font)
        self.gasLabel.setObjectName("gasLabel")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 230, 211, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(320, 230, 241, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.magneticField.setItemText(0, _translate("MainWindow", "Mirror"))
        self.magneticField.setItemText(1, _translate("MainWindow", "Cusp"))
        self.lowerVoltage.setItemText(0, _translate("MainWindow", "-300"))
        self.lowerVoltage.setItemText(1, _translate("MainWindow", "-250"))
        self.lowerVoltage.setItemText(2, _translate("MainWindow", "-200"))
        self.lowerVoltage.setItemText(3, _translate("MainWindow", "-150"))
        self.lowerVoltage.setItemText(4, _translate("MainWindow", "-100"))
        self.lowerVoltage.setItemText(5, _translate("MainWindow", "-50"))
        self.lowerVoltage.setItemText(6, _translate("MainWindow", "0"))
        self.higherVoltage.setItemText(0, _translate("MainWindow", "300"))
        self.higherVoltage.setItemText(1, _translate("MainWindow", "250"))
        self.higherVoltage.setItemText(2, _translate("MainWindow", "200"))
        self.higherVoltage.setItemText(3, _translate("MainWindow", "150"))
        self.higherVoltage.setItemText(4, _translate("MainWindow", "100"))
        self.higherVoltage.setItemText(5, _translate("MainWindow", "50"))
        self.higherVoltage.setItemText(6, _translate("MainWindow", "0"))
        self.gas.setItemText(0, _translate("MainWindow", "Air"))
        self.gas.setItemText(1, _translate("MainWindow", "Argon"))
        self.gas.setItemText(2, _translate("MainWindow", "Helium"))
        self.gas.setItemText(3, _translate("MainWindow", "Hydrogen"))
        self.runButton.setText(_translate("MainWindow", "RUN"))
        self.exitButton.setText(_translate("MainWindow", "EXIT"))
        self.title.setText(_translate("MainWindow", "LANGMUIR PROBE DIAGNOSTICS"))
        self.logo.setText(_translate("MainWindow", "<html><head/><body><p><img src=\"Resources/logo.png\"/></p></body></html>"))
        self.magFieldLabel.setText(_translate("MainWindow", "Magnetic Field"))
        self.voltageRampLabel.setText(_translate("MainWindow", "Voltage Ramp"))
        self.gasLabel.setText(_translate("MainWindow", "Gas"))
        self.label_6.setText(_translate("MainWindow", "Voltage Sweep Time (s)"))
        self.label_7.setText(_translate("MainWindow", "Number of Measurements"))
        self.numberMeasurementsLCD.display(self.numberMeasurements)
        self.sweepTimeLCD.display('%.2f' % self.sweepTime)
    def AddMeasurements(self):
        if self.numberMeasurements < 1000:
            self.numberMeasurements += 50
            self.numberMeasurementsLCD.display(self.numberMeasurements)
            
    def SubstractMeasurements(self):
        if self.numberMeasurements > 50:
            self.numberMeasurements -= 50
            self.numberMeasurementsLCD.display(self.numberMeasurements)
            
    def AddSweepTime(self):
        if self.sweepTime < 10 and self.sweepTime >= 0.25:
            self.sweepTime += 0.25
            self.sweepTime = np.round(self.sweepTime, 2)
            self.sweepTimeLCD.display('%.2f' % self.sweepTime)
        elif self.sweepTime < 10:
            self.sweepTime += 0.05
            self.sweepTime = np.round(self.sweepTime, 2)
            self.sweepTimeLCD.display('%.2f' % self.sweepTime)
            
    def SubstractSweepTime(self):
        if self.sweepTime > 0.25:
            self.sweepTime -= 0.25
            self.sweepTime = np.round(self.sweepTime, 2)
            self.sweepTimeLCD.display('%.2f' % self.sweepTime)
        elif self.sweepTime > 0.05:
            self.sweepTime -= 0.05
            self.sweepTime = np.round(self.sweepTime, 2)
            self.sweepTimeLCD.display('%.2f' % self.sweepTime)
            
    def RunButton(self):
        
        self.ParametersWindow = QtWidgets.QMainWindow()
        self.w = AnotherWindow(self.ParametersWindow)
        self.ParametersWindow.show()
        
    def UserSettingsExport(self):
        self.userSettings = {"sweepTime": float(self.sweepTime),
                             "numberMeasurements": int(self.numberMeasurements),
                             "magneticField": str(self.magneticField.currentText()),
                             "voltageRange": [int(self.lowerVoltage.currentText()), int(self.higherVoltage.currentText())],
                             "gas": self.gas.currentText()
                             }
        return self.userSettings, self.w, self.ParametersWindow
        
class AnotherWindow(object):
    """
    This "window" is a QWidget. If it has no parent, it 
    will appear as a free-floating window as we want.
    """
    
    def __init__(self, ParametersWindow):
        super().__init__()
        plasmaParameters = {"Density": 0,
                            "KTe_eV": 0,
                            "KTe": 0,
                            "vP": [0,0],
                            "vF": [0,0],
                            "DebyeLength": 0,
                            "Larmor_Radius": 0,
                            "Mean_Free_Path": 0                        
                            }
        self.switch = False
        ParametersWindow.setObjectName("ParametersWindow")
        ParametersWindow.resize(800, 434)
        ParametersWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(ParametersWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pauseButton = QtWidgets.QPushButton(self.centralwidget)
        self.pauseButton.setGeometry(QtCore.QRect(630, 180, 151, 121))
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.pauseButton.setFont(font)
        self.pauseButton.setStyleSheet("color: rgb(255, 255, 255);\n" "background-image: url(Resources/green.png);")
        self.pauseButton.setObjectName("pauseButton")
        self.pauseButton.clicked.connect(self.ToggleSwitch)
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(650, 10, 111, 111))
        self.logo.setObjectName("logo")
        self.densityLabel = QtWidgets.QLabel(self.centralwidget)
        self.densityLabel.setGeometry(QtCore.QRect(390, 90, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.densityLabel.setFont(font)
        self.densityLabel.setObjectName("densityLabel")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(150, 10, 491, 31))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.kte_evLabel = QtWidgets.QLabel(self.centralwidget)
        self.kte_evLabel.setGeometry(QtCore.QRect(390, 150, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.kte_evLabel.setFont(font)
        self.kte_evLabel.setObjectName("kte_evLabel")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(390, 210, 221, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.plasmaPotentialLabel = QtWidgets.QLabel(self.centralwidget)
        self.plasmaPotentialLabel.setGeometry(QtCore.QRect(20, 340, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.plasmaPotentialLabel.setFont(font)
        self.plasmaPotentialLabel.setObjectName("plasmaPotentialLabel")
        self.floatingPotentialLabel = QtWidgets.QLabel(self.centralwidget)
        self.floatingPotentialLabel.setGeometry(QtCore.QRect(360, 340, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.floatingPotentialLabel.setFont(font)
        self.floatingPotentialLabel.setObjectName("floatingPotentialLabel")
        self.debyeLenghtLabel = QtWidgets.QLabel(self.centralwidget)
        self.debyeLenghtLabel.setGeometry(QtCore.QRect(40, 90, 331, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.debyeLenghtLabel.setFont(font)
        self.debyeLenghtLabel.setObjectName("debyeLenghtLabel")
        self.larmorRadiusLabel = QtWidgets.QLabel(self.centralwidget)
        self.larmorRadiusLabel.setGeometry(QtCore.QRect(40, 150, 331, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.larmorRadiusLabel.setFont(font)
        self.larmorRadiusLabel.setObjectName("larmorRadiusLabel")
        self.meanFreePathLabel = QtWidgets.QLabel(self.centralwidget)
        self.meanFreePathLabel.setGeometry(QtCore.QRect(40, 210, 331, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.meanFreePathLabel.setFont(font)
        self.meanFreePathLabel.setObjectName("meanFreePathLabel")
        ParametersWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ParametersWindow)
        self.statusbar.setObjectName("statusbar")
        ParametersWindow.setStatusBar(self.statusbar)
        _translate = QtCore.QCoreApplication.translate
        self.pauseButton.setText(_translate("ParametersWindow", "RUN"))

        self.retranslateUi(ParametersWindow, plasmaParameters)
        QtCore.QMetaObject.connectSlotsByName(ParametersWindow)
        
    def retranslateUi(self, ParametersWindow, plasmaParameters):
        _translate = QtCore.QCoreApplication.translate
        ParametersWindow.setWindowTitle(_translate("ParametersWindow", "Plasma Parameters"))
        self.logo.setText(_translate("ParametersWindow", "<html><head/><body><p><img src=\"Resources/logo.png\"/></p></body></html>"))
        self.densityLabel.setText(_translate("ParametersWindow", "Density: " + str(format(plasmaParameters['Density'], "2.2e"))))
        self.title.setText(_translate("ParametersWindow", "LANGMUIR PROBE DIAGNOSTICS"))
        self.kte_evLabel.setText(_translate("ParametersWindow", "KTe_eV: " + str(format(plasmaParameters['KTe_eV'], ".2f"))))
        self.label_3.setText(_translate("ParametersWindow", "KTe: " + str(format(plasmaParameters['KTe'], "2.2e"))))
        self.plasmaPotentialLabel.setText(_translate("ParametersWindow", "Plasma Potential: " + str(format(plasmaParameters['vP'][0], ".2f"))+"V"))
        self.floatingPotentialLabel.setText(_translate("ParametersWindow", "Floating Potential: " + str(format(plasmaParameters['vF'][0], ".2f"))+"V"))
        self.debyeLenghtLabel.setText(_translate("ParametersWindow", "Debye Length: " + str(format(plasmaParameters['DebyeLength'], "2.2e"))))
        self.larmorRadiusLabel.setText(_translate("ParametersWindow", "Larmor Radius: " + str(plasmaParameters['Larmor_Radius'])))
        self.meanFreePathLabel.setText(_translate("ParametersWindow", "Mean Free Path: " + str(format(plasmaParameters['Mean_Free_Path'], "2.2e"))))
    
    # Save a separate CSV for plasma parameters
    def ParametersToCsv(self, listOfParameters, fname):
        
        keys = list(listOfParameters[0].keys())
        
        for row in listOfParameters:
            row['vP'] = row['vP'][0]
            row['vF'] = row['vF'][0]
        with open("Measurements/Parameters__" + fname+ ".csv", "w", newline='') as csv_file:
            dict_writer= csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(listOfParameters)
    
    def ToggleSwitch(self):
        if not self.switch:
            _translate = QtCore.QCoreApplication.translate
            self.pauseButton.setText(_translate("ParametersWindow", "STOP"))
            self.pauseButton.setStyleSheet("color: rgb(255, 255, 255);\n" "background-image: url(Resources/red.png);")
#            DAQC2.setDAC(0, 1, 4)
            time.sleep(1.5)
        else:
            _translate = QtCore.QCoreApplication.translate
            self.pauseButton.setText(_translate("ParametersWindow", "RUN"))
            self.pauseButton.setStyleSheet("color: rgb(255, 255, 255);\n" "background-image: url(Resources/green.png);")
#            DAQC2.setDAC(0, 1, 0)
            
        self.userSettings, self.w, self.ParametersWindow = ui.UserSettingsExport()
        QtWidgets.QApplication.processEvents()
        self.switch = not self.switch

        if self.switch:
            #list of parameters will contain parameter dictionaries
            listOfParameters = []
            applied_voltages = []
            unfiltered_currents_list = []
            filtered_currents_list = []
            sweep_indices = []
            sweep_counter = 1
            while self.switch == True:
                #self.w.retranslateUi(self.w.ParametersWindow, self.plasmaParameters)
                QtWidgets.QApplication.processEvents()
                params, voltages, unfiltered_currents, filtered_currents = self.RunProgramSLP(self.userSettings)
                listOfParameters.append(params)
                applied_voltages.extend(voltages)
                filtered_currents_list.extend(filtered_currents)
                unfiltered_currents_list.extend(unfiltered_currents)
                sweep_number = [sweep_counter for _ in range(0, len(voltages))]
                sweep_indices.extend(sweep_number)
                sweep_counter += 1
            now = datetime.datetime.now()
            probeConfig = "SLP"
            fname = self.userSettings['magneticField']+probeConfig+now.strftime("_%Y_%m_%d-%H_%M_%S-")+str(abs(self.userSettings['voltageRange'][0]))+'Vto'+str(abs(self.userSettings['voltageRange'][1]))+'V'   
            self.ParametersToCsv(listOfParameters, fname)
            self.SaveData(unfiltered_currents_list, applied_voltages, filtered_currents_list, sweep_indices, fname)

     
    def VoltageConversion(self, voltageRange, opAmpGain):
        """
        Converts the desired amplified output voltage to the
        output signal needed from the Raspberry Pi.
        
        Inputs:
            voltageRange = list of desired voltage range at the probe output. Minimum value to maximum value.
            opAmpGain = Amplifier Gain Conversion y = mx + b; opAmpGain[0] = m, opAmpGain[1] = b.
        
        Outputs:
            voltageRangeRPI = list(range) of converted voltage to be applied by the raspberry pi.
            zeroVoltageRPI = output signal voltage to obtain ~0V on the output of the 
            high power amplifier. This is used to set the high output voltage to approx 0V while not in use.
        """
        
        voltageRangeRPI = [(voltageRange[0] - opAmpGain[1])/opAmpGain[0], (voltageRange[1] - opAmpGain[1])/opAmpGain[0]]
        zeroVoltageRPI = -opAmpGain[1]/opAmpGain[0]
        
        return zeroVoltageRPI, voltageRangeRPI
    
    def DefineVoltageRampRPI(self, numberPoints, voltageRangeRPI, opAmpGain):
        """
        Generates the output signal voltage ramp given
        the maximimum, minimum and amount of steps.
        
        Inputs:
           voltageRangeRPI = list of output signal voltage from raspberry pi.        
            numberPoints = number of measurements.
            opAmpGain = Amplifier Gain Conversion y = mx + b; opAmpGain[0] = m, opAmpGain[1] = b.
            
        Outputs:
            voltageRampRPI = array of voltages representing the voltage signal output 
            from the raspberry pi rounded to 3 decimal places.
            voltageSLP = array of voltages representing the amplified output voltage. 
        """
    
        voltageRampRPI = np.linspace(voltageRangeRPI[0], voltageRangeRPI[1], numberPoints)
        voltageSLP = np.around(voltageRampRPI, 3)*opAmpGain[0] + opAmpGain[1]
        print('\nNumber of measurements:',str(numberPoints) +'.')
        print('Voltage step size:', str(np.around(voltageSLP[-1]-voltageSLP[-2], 3)) + 'V.\n')
        
        return np.around(voltageRampRPI, 3), voltageSLP
    
    def GenerateVoltageRampRPI(self, voltageRampRPI, zeroVoltageRPI, shuntResistor, voltageSweep):
        """
        Generates the voltage ramp and reads the current across the shunt resistor. 
        
        Inputs:
            zeroVoltageRPI = output signal voltage to obtain ~0V on the output of the 
            high power amplifier.
            voltageRampRPI = array of voltages representing the voltage signal output 
            from the raspberry pi.
            shuntResistor = shunt resistor in series with langmuir Probe.
            stepTime = wait time between voltage steps.
            
        Outputs:
            current = array representing the langmuir Probe current
        """
        stepTime = voltageSweep/len(voltageRampRPI)
        print('Generating Voltage Ramp...\n')
        current = np.zeros(len(voltageRampRPI))
        count = 0
        for voltage in voltageRampRPI:
#            DAQC2.setDAC(0, 0, voltage)
            time.sleep(stepTime)
   #         current[count] = DAQC2.getADC(0, 0)
            count += 1
        # Set amplifier output to ~0V when not running experiment.
 #       DAQC2.setDAC(0, 0, zeroVoltageRPI)
        current = (current)/shuntResistor
        print('...Done generating Voltage Ramp...\n')
        return current
    
    def Normalize(self, x):
        normalized = x/np.max(x)
        return normalized
 
    def SaveData(self, raw_current, voltage, filt_current, sweep_num, fname):   
        print('Saving CSV file...\n')
        with open('Measurements/' + fname + ".csv", "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Raw_Current[A]', 'Voltage_Bias[V]', 'Filtered_Current[A]','Sweep_Num', fname])
            for i in range(len(voltage)):
                writer.writerow([str(raw_current[i]), str(voltage[i]), str(filt_current[i]), str(sweep_num[i])])
                
    def FilterSignal(self, rawSignal, numberPoints):
        """
        Filters a signal using a butterworth digital filter. 
        
        Inputs:
            rawSignal = an array of raw data captured by the sensor.
            
        Outputs:
            filteredSignal = signal after being processed by a butterworth digital filter.
        """
        
        sos = signal.butter(2, 0.03, output='sos')
        filteredSignal = signal.sosfiltfilt(sos, rawSignal)
        
        return filteredSignal
    
        # b, a = signal.butter(12, 0.03)
        #filteredSignal = signal.sosfiltfilt(sos, rawSignal, padlen=int(numberPoints/4))
        
        return filteredSignal
        
    def LoadPreviousData(self):
        with open('Feliz_A1 MirorSLP120200813T105858.csv', newline='') as csvfile:
            dataReader = csv.reader(csvfile, delimiter=',', quotechar='|')
            current = []
            voltageSLP = []
            for row in dataReader:
                try:
                    current = np.append(current, float(row[0]))
                    voltageSLP = np.append(voltageSLP, float(row[1]))
                except:
                    None    
            
            return current, voltageSLP
        
            #return current[100:325], voltageSLP[100:325]
            #current = (current-biasVoltageShuntResistor)/shuntResistor
    def Derivative(self, y, x):
        """
        Finds the numerical differentitation of a function and outputs the function derivative. 
        
        Inputs:
            x, y = Funtions to differentiate.
            
        Outputs:
            dy_dx = np.array of the derivative.
        """
        dy_dx = np.zeros(y.shape, float)
        dy_dx[0:-1] = np.diff(y)/np.diff(x)
        
        return dy_dx
    
    def CalculateParameters(self, plasmaParameters, current, voltage, dI_dV, area, B, Zi):
          
        IN, dN, plasmaParameters['vP'], plasmaParameters['vF'], plasmaParameters['I_vP'], index_di_max, errorFlag = self.CalculatePlasmaRegions(current, dI_dV, voltage)
        plasmaParameters['KTe'], plasmaParameters['KTe_eV'] = self.CalculateTemperature(plasmaParameters, current, voltage)
        plasmaParameters['Density'] = self.CalculateDensity(plasmaParameters['I_vP'], plasmaParameters['KTe_eV'], area)
        plasmaParameters['DebyeLength'] = self.CalculateDebye(plasmaParameters['Density'], plasmaParameters['KTe'])
        plasmaParameters['Mean_Free_Path'] = 3.4e18*((plasmaParameters['KTe_eV']**2)/(Zi*plasmaParameters['Density']))
        plasmaParameters["Larmor_Radius"] = self.CalculateLarmorRadius(plasmaParameters['KTe_eV'], B)
        if errorFlag == True:
            plasmaParameters = {"Density": -1,
                            "KTe_eV": -1,
                            "KTe": -1,
                            "vP": [-1,-1],
                            "vF": [-1,-1],
                            "DebyeLength": -1,
                            "Larmor_Radius": -1,
                            "Mean_Free_Path": -1                        
                            }    
        
        return plasmaParameters
    
    def CalculateTemperature(self, plasmaParameters, current, voltage):
        e = -1.60217657e-19
        
        indexMin = plasmaParameters['vF'][1]
        #print('Min: ', str(indexMin))
        
        indexMax = plasmaParameters['vP'][1]
        #print('Max: ', str(indexMax))
        
        middle = int(np.ceil(indexMin + (indexMax - indexMin)/2))
        #print('Middle: ', str(middle))
        V_MVf = voltage[middle]
        #print('V_MVf: ', float(V_MVf))
        
        I_lnMVf = np.log(current[middle])
        #print('I_lnMVf: ', str(I_lnMVf))
        I_lnVs = np.log(current[indexMax])
        #print('I_lnVs: ', str(I_lnVs))
        slope =((I_lnVs - I_lnMVf)/(plasmaParameters['vP'][0] - V_MVf));
        #print('Slope: ', float(slope))
        KTe = -e/slope
        #print('KTe: ', str(KTe))
        KTe_eV = 1/slope
        #print('KTe eV: ', str(KTe_eV))
        
        
        return KTe, KTe_eV
    
    def CalculateDensity(self, I_vP, KTe_eV, area):
        e = -1.60217657e-19
        me = 9.10938291e-31
        density = -I_vP/(e*area*np.sqrt(KTe_eV*abs(e)/(2*np.pi*me)))
        return density
        
    def CalculateDebye(self, density, KTe):
        eo = 8.85418782e-12
        e = - 1.60217657e-19
        debyeLength =(np.sqrt(eo*KTe/(density*e**2)))
        return debyeLength
    
    def CalculateLarmorRadius(self, KTe_eV, B):
        B = B/10000;
    
        if B == 0:
            larmor_Radius = -1
        else:
            larmor_Radius = 3.37e-4*(np.sqrt(KTe_eV))/B;
        return larmor_Radius
    
    def CalculatePlasmaRegions(self, current, dI_dV, voltageSLP):
        errorFlag = False
        IN = self.Normalize(current)
        dN = self.Normalize(dI_dV)
        
        # Calculated using Plasma Potential using the maximum of the derivative.
        try:
            index_di_max = np.argwhere(dN == np.max(dN)).astype(int)[0][0]
            vP = [voltageSLP[index_di_max], index_di_max]
        except:
            errorFlag = True
        
        try:
            vFIndex = np.argwhere(current < 0)[-1].astype(int)[0]
            vF = [voltageSLP[vFIndex], vFIndex]
            #print('Vf =',str(np.around(vF[0], decimals=2))+'V')
        except:
            vF = [-1, -1]
            print('*****ERROR*****\n Plasma Floating Point not found. Error in measurement.\n')
            errorFlag = True
        I_vP = current[index_di_max]
        
        return IN, dN, vP, vF, I_vP, index_di_max, errorFlag
    
    def RunProgramSLP(self, userSettings):
        opAmpGain = [150.85, -296]          # Amplifier gain gain equation y = mx + b; opAmpGain[0] = m, opAmpGain[1] = b.
        probeConfig = "SLP"                 # Probe configuration. Single Langmuir Probe or Double Langmuir Probe.
        shuntResistor = 200                 # Value of the current sensing resistor.
    
        if self.userSettings['gas'] == 'Air':
            Zi = 18
        else:
            Zi = 0
            
        if self.userSettings['voltageRange'][0] < opAmpGain[1]:
            self.userSettings['voltageRange'][0] = opAmpGain[1]
            
        B = 0
        area = 30.3858e-06
    
        now = datetime.datetime.now()
        fname = self.userSettings['magneticField']+probeConfig+now.strftime("_%Y_%m_%d-%H_%M_%S-")+str(abs(self.userSettings['voltageRange'][0]))+'Vto'+str(abs(self.userSettings['voltageRange'][1]))+'V'
        
        self.plasmaParameters = {"Density": 0,
                            "KTe_eV": 0,
                            "KTe": 0,
                            "vP": [0,0],
                            "vF": [0,0],
                            "DebyeLength": 0,
                            "Larmor_Radius": 0,
                            "Mean_Free_Path": 0                        
                            }
        testing = True
        if testing == True:
            
            self.current, self.voltageSLP = self.LoadPreviousData()
            
            self.currentFiltered = self.FilterSignal(self.current, self.userSettings['numberMeasurements'])
            self.dI_dVFiltered = self.Derivative(self.currentFiltered, self.voltageSLP)

            self.plasmaParameters = self.CalculateParameters(self.plasmaParameters, self.currentFiltered, self.voltageSLP, 
                                                            self.dI_dVFiltered, area, B, Zi)
            #self.plasmaParameters['Density'] = random()
            self.w.retranslateUi(self.w.ParametersWindow, self.plasmaParameters)

        else:
            self.zeroVoltageRPI, self.voltageRangeRPI = self.VoltageConversion(self.userSettings['voltageRange'], opAmpGain)
            self.voltageRampRPI, self.voltageSLP = self.DefineVoltageRampRPI(self.userSettings['numberMeasurements'], self.voltageRangeRPI, opAmpGain)
            self.current = self.GenerateVoltageRampRPI(self.voltageRampRPI, self.zeroVoltageRPI, shuntResistor, self.userSettings['sweepTime'])
            #self.SaveData(self.current, self.voltageSLP, fname)
        
            self.currentFiltered = self.FilterSignal(self.current, self.userSettings['numberMeasurements'])
            self.dI_dVFiltered = self.Derivative(self.currentFiltered, self.voltageSLP)
            self.plasmaParameters = self.CalculateParameters(self.plasmaParameters, self.currentFiltered, self.voltageSLP, 
                                                            self.dI_dVFiltered, area, B, Zi)
            self.w.retranslateUi(self.w.ParametersWindow, self.plasmaParameters)
        # V2 addition, returns values to aggregate into a single file
        # for sweeps, and a second file for parameters
        return self.plasmaParameters, self.voltageSLP, self.current, self.currentFiltered

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())