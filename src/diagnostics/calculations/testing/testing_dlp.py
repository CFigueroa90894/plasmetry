import dlp_plasma_parameters as dlp
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

#storing bias and raw current in lists
bias, current = LoadPreviousData()

#filtering raw current, storing the output in a list
filtered_current = FilterSignal(current)


ion_saturation_current = dlp.get_ion_saturation_current(filtered_current)

electron_temperature_ev, electron_temperature_joules = dlp.get_electron_temperature(filtered_current, bias, ion_saturation_current)
print ('electron temperature (eV): ', electron_temperature_ev)
print('electron temperature (J): ', electron_temperature_joules)


probe_area = 30.3858e-06

#hydrogen ion mass
ion_mass = 1.67e-27

electron_density = dlp.get_electron_density(electron_temperature_joules, probe_area, ion_saturation_current, ion_mass)

print('Electron Density: ', electron_density)

debye_length = dlp.get_debye_length(electron_temperature_joules, electron_density)


print('Debye length (m): ', debye_length)

number_of_charged_particles = dlp.get_number_of_electrons(debye_length, electron_density)

print('Number of charged particles in the Debye sphere (integer): ', number_of_charged_particles)
