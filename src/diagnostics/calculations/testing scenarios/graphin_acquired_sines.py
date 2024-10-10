

import numpy as np
from scipy import signal
import csv
import matplotlib.pyplot as plt
import os

def LoadPreviousData(file_name):
    
    # Extracted from Felix Cuadrado's Code
    with open(file_name, newline='') as csvfile:
        dataReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(dataReader)  # Skip the header row
        current = []
        bias = []
        for row in dataReader:
            try:
                if 'parameters' in file_name:
                    current = np.append(current, float(row[0]))
                    bias = np.append(bias, float(row[1]))
                else:
                    current = np.append(current, float(row[1]))
                    bias = np.append(bias, float(row[0]))
            except:
                None    
        
        return bias, current
    
def filter_current(parameters):
    
    """Filters a signal using a butterworth digital filter. 
    
    Inputs:
        rawSignal = an array of raw data captured by the sensor.
        
    Outputs:
        filteredSignal = signal after being processed by a butterworth digital filter.
    """

    
    sos = signal.butter(2, 0.03, output='sos')
    ba = signal.butter(2, 0.03, output='ba')
    ba_freq= signal.freqz(ba[0],ba[1])
    parameters['ba_freq'] = ba_freq
    filteredSignal = np.array(signal.sosfiltfilt(sos, parameters['Raw voltage 1']))
   
    parameters['Filtered current (Amperes)'] = filteredSignal / parameters['config_ref']['sweeper_shunt']

folder = 'Data Acquisition validations/'
data_acquired = [f for f in os.listdir(folder)]

for csv_filename in data_acquired:
    
    bias, current = LoadPreviousData(f'{folder}/{csv_filename}')

    parameters ={'Raw voltage 1':current, 'Bias 1': bias, 'config_ref': {'sweeper_shunt': 1}}
    filter_current(parameters)

    #plotting bias vs raw current 
    print('\nraw current vs bias:\n')
    plt.plot(bias, current, marker='o', linestyle='-')
    plt.xlabel('Bias')
    plt.ylabel('Raw Signal')
    plt.title('Plot of Raw Signal vs Bias')
    plt.grid(True)
    plt.savefig(f'{folder}/plots/{csv_filename[:-4]} raw_signal.png')  

    plt.show()


    print('filtered current vs bias:\n')
    plt.plot(parameters['Bias 1'], parameters['Filtered current (Amperes)'], marker='o', linestyle='-')
    plt.xlabel('Bias')
    plt.ylabel('Raw Signal')
    plt.title('Plot of Raw Signal vs Bias')
    plt.grid(True)
    plt.savefig(f'{folder}/plots/{csv_filename} filtered_signal.png')  
    plt.show()
        
    frequency = 1

    f, t, Sxx = signal.spectrogram(parameters['Filtered current (Amperes)'], frequency)
    plt.pcolormesh(t, f, Sxx, shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()

    x, y = parameters['ba_freq']

    y = abs(np.array(y))
    
print('Magnitude Frequency Response of Butterworth Filter:\n')
plt.plot(np.array(x), y, marker='o', linestyle='-')
plt.xlabel('Rad/sample')
plt.ylabel('Attenuation')
plt.title('Magnitude Frequency Response of Butterworth Filter')
plt.grid(True)
plt.show()



