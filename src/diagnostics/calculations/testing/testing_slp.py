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

print ('floating potential (V):', floating_potential[1])

print ('plasma potential (V):', plasma_potential[1])

electron_temperature_ev, electron_temperature_joules = slp.get_electron_temperature(floating_potential, plasma_potential, filtered_current, bias)

print ('electron temperature (eV): ', electron_temperature_ev)
print('electron temperature (J): ', electron_temperature_joules)

electron_saturation_current = slp.get_electron_saturation_current(filtered_current, plasma_potential[0])

probe_area = 30.3858e-06

electron_density= slp.get_electron_density(electron_saturation_current, electron_temperature_joules, probe_area)

print('Electron Density: ', electron_density)

debye_length = slp.get_debye_length(electron_temperature_joules, electron_density)


print('Debye length (m): ', debye_length)

number_of_charged_particles = slp.get_number_of_electrons(debye_length, electron_density)

print('Number of charged particles in the Debye sphere (integer): ', number_of_charged_particles)
