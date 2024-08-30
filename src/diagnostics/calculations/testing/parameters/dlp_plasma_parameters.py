import numpy as np 
from scipy import signal

from global_parameters import (
    get_debye_length,
    get_number_of_electrons
)

# Storing the charge of the electron particle, since it shall be used for calculation
ELECTRON_CHARGE = 1.60217657e-19


def filter_current(parameters):
    
    # Extracted from Felix Cuadrado's code
    """Filters a signal using a butterworth digital filter. 
    
    Inputs:
        rawSignal = an array of raw data captured by the sensor.
        
    Outputs:
        filteredSignal = signal after being processed by a butterworth digital filter.
    """
    
    sos = signal.butter(2, 0.03, output='sos')
    filteredSignal = signal.sosfiltfilt(sos, parameters['Raw current'])
    
    parameters['Filtered current'] = filteredSignal
    
    
def get_ion_saturation_current(parameters):
    
    
    """**TODO: find a better way to obtain ion saturation current.**
    
    The ion saturation current is yielded from this function.
    
    NOTE: This is a simple and crude way to obtain the value.
    """
    
    # Storing the ion saturation current.
    parameters['Ion saturation current'] = np.min(parameters['Filtered current'] )
   
    
    
def get_electron_temperature( parameters):
    
    
    """This function calculates the electron temperature in both Joules and electron volts.
    
    The value of  the derivative of the I-V values where the voltage applied is 0 is used 
    
    to calculate electron temperature, yet it is possible that the voltage applied is never 0, 
    
    thus the value closet to 0 shall be used. 
    """
    
    # Storing parameters used for calculations
    filtered_current_list = parameters['Filtered current'] 
    voltage_list =  parameters['Bias'] 
    ion_saturation_current = parameters['Ion saturation current'] 
    
    # Storing the index where the voltage is closest to 0.
    voltage_at_zero_index = np.argmin(abs(voltage_list))
    
    # Storing the derivative of the I-V values.
    I_V_derivative = np.gradient(filtered_current_list, voltage_list )
    
    denominator_of_equation = 2 * I_V_derivative[voltage_at_zero_index]
    # Calculating electron temperature in electron volts. 
    parameters['Electron temperature (eV)'] = abs(ion_saturation_current / denominator_of_equation)
    
    # Calculating electron temperature in Joules.
    parameters['Electron temperature (Joules)'] = parameters['Electron temperature (eV)'] * ELECTRON_CHARGE


def get_electron_density(parameters):
    
    """This function yields the electron density in Kilograms per cubic meter. """ 
    
    # Acquiring electron density 
    square_root_term =  np.sqrt(parameters['Ion mass'] / parameters['Electron temperature (Joules)'])
    parameters['Electron density'] = abs(parameters['Ion saturation current'] / \
                                        (ELECTRON_CHARGE *  parameters['Probe area']) * \
                                        (square_root_term * np.exp(0.5)))


def get_equations():
    
    """This function returns a reference to the equations """
    
    # List containing the references
    list_of_references = []
    
    # Local parameters
    list_of_references.append(filter_current)
    list_of_references.append(get_ion_saturation_current)
    list_of_references.append(get_electron_temperature)
    list_of_references.append(get_electron_density)
    
    # Global parameters
    list_of_references.append(get_debye_length)
    list_of_references.append(get_number_of_electrons)
    return list_of_references


""" sample usage of the equations"""    
if __name__ == "__main__": 

    
    def LoadPreviousData():
        
        """Function to load data from previous implementation. Code developed by Felix Cuadrado"""
        
        import csv as csv_library
        
        with open('../testing scenarios/Feliz_A1 MirorSLP120200813T105858.csv', newline='') as csv:
            dataReader = csv_library.reader(csv, delimiter=',', quotechar='|')
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
    
    # Parameter dictionary, stores parameters
    parameters= {}
    
    # Storing bias and raw current lists from previous implementation
    parameters['Bias'], parameters['Raw current'] =  LoadPreviousData()
    
    # Probe area of a previous implementation, simulating config values
    parameters['Probe area'] =  30.3858e-06
    
    # Argon atomic mass mass in Kilograms
    parameters['Ion mass'] = 6.629e-26
   
    # Running each equation
    list_of_equations = get_equations()
    for i in list_of_equations:
        i(parameters)
        
    # Printing the parameters
    for i in parameters.keys():
        if 'current' not in i and 'Bias' != i:
            print( i + ': ', parameters[i])
        
    
    