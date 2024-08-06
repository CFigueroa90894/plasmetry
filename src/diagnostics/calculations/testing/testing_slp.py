import slp_plasma_parameters as slp
import numpy as np
from scipy import signal
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


bias, current = LoadPreviousData();

filtered_current = FilterSignal(current)

floating_potential, plasma_potential = slp.get_floating_and_plasma_potential(filtered_current, bias)
print (plasma_potential)

ev, joules = slp.get_electron_temperature(floating_potential, plasma_potential, filtered_current, bias)

print (ev, joules)

