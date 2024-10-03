
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import csv

# Normalized cutoff frequency for the butterworth filter
CUTOFF_FREQUENCY = 0.03

# Order of the butterworth filter
FILTER_ORDER = 2

def LoadPreviousData():
    
    # Extracted from Felix Cuadrado's Code
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
    


def filter_current(parameters):
    
    """Filters a signal using a butterworth digital filter. 
    
    Inputs:
        rawSignal = an array of raw data captured by the sensor.
        
    Outputs:
        filteredSignal = signal after being processed by a butterworth digital filter.
    """

    
    sos = signal.butter(FILTER_ORDER, CUTOFF_FREQUENCY, output='sos')
    
    filteredSignal = np.array(signal.sosfiltfilt(sos, parameters['Raw voltage 1']))
   
    parameters['Filtered current (Amperes)'] = filteredSignal / parameters['config_ref']['sweeper_shunt']
    
parameters = {}
#loading bias and current 
bias, parameters['Raw voltage 1'] = LoadPreviousData();

parameters['config_ref'] = {'sweeper_shunt': 1}

#filtered current list
filter_current(parameters)
filtered_current = parameters['Filtered current (Amperes)'] 

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
plt.plot(bias, parameters['Raw voltage 1'], marker='o', linestyle='-')
plt.xlabel('Bias')
plt.ylabel('Raw Signal')
plt.title('Plot of Raw Signal vs Bias')
plt.grid(True)
plt.show()

#plotting bias vs filtered current 
print('\nfiltered current vs bias:\n')

plt.plot(bias, filtered_current, marker='o', linestyle='-')
plt.xlabel('Bias')
plt.ylabel('Filtered Signal')
plt.title('Plot of Filtered Signal vs Bias')
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
plt.xlabel('bias')
plt.ylabel('second order derivative')
plt.title('Plot of Y vs X')
plt.grid(True)
plt.show()


plt.plot(cut_bias, cut_second_derivative, marker='o', linestyle='-')
plt.xlabel('bias')
plt.ylabel('second order derivative')
plt.title('Plot of Y vs X')
plt.grid(True)
plt.show()
