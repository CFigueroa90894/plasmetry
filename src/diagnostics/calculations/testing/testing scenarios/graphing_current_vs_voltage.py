
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import csv

def LoadPreviousData():
    with open('Feliz_A1 MirorSLP120200813T105858.csv', newline='') as csvfile:
        dataReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(dataReader)  # Skip the header row
        current = []
        voltageSLP = []
        for row in dataReader:
            try:
                current = np.append(current, float(row[0]))
                voltageSLP = np.append(voltageSLP, float(row[1]))
            except:
                None    
        
        return voltageSLP, current
    

def FilterSignal(rawSignal):
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

#loading bias and current 
bias, current = LoadPreviousData();

#filtered current list
filtered_current = FilterSignal(current)

#calculating first derivative to yield second
derivative = np.gradient(filtered_current, bias)

#second derivative
second_deriv = np.gradient(derivative, bias)

#cutting the lists to have a 'zoom' of the graph
cut_bias = [a for a in bias if 0 < a < 80]
cut_filtered_current = filtered_current[401-99:len(filtered_current)-len(cut_bias)]
cut_second_derivative = second_deriv[401-99:len(second_deriv)-len(cut_bias)]

#plotting bias vs raw current 
print('\nraw current vs bias:\n')
plt.plot(bias, current, marker='o', linestyle='-')
plt.xlabel('bias')
plt.ylabel('current')
plt.title('Plot of Y vs X')
plt.grid(True)
plt.show()

#plotting bias vs filtered current 
print('\nfiltered current vs bias:\n')

plt.plot(bias, filtered_current, marker='o', linestyle='-')
plt.xlabel('bias')
plt.ylabel('filtered current')
plt.title('Plot of Y vs X')
plt.grid(True)
plt.show()

plt.plot(cut_bias, cut_filtered_current, marker='o', linestyle='-')
plt.xlabel('bias')
plt.ylabel('filtered current')
plt.title('Plot of Y vs X')
plt.grid(True)
plt.show()

print('\nsecond order derivative of the current vs bias:\n')

#plotting bias vs second order derivative of the filtered current
plt.plot(bias, second_deriv, marker='o', linestyle='-')
plt.ylabel('bias')
plt.xlabel('second order derivative')
plt.title('Plot of Y vs X')
plt.grid(True)
plt.show()


plt.plot(cut_bias, cut_second_derivative, marker='o', linestyle='-')
plt.ylabel('bias')
plt.xlabel('second order derivative')
plt.title('Plot of Y vs X')
plt.grid(True)
plt.show()
