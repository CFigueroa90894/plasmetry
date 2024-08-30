import numpy as np
from scipy import signal

# Storing the charge of the electron particle, since it shall be used for calculation
ELECTRON_CHARGE = 1.60217657e-19

# Storing the permittivity of free space constant in F/m, since it shall be used for calculation
EPSILON_NAUGHT= 8.854e-12

"""TODO: verify particle saturation current calculations with Dr. Gonzalez"""


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
    
    
def get_debye_length(parameters):
    
    """DLP and SLP Debye length is calculated from this function in meters."""
    
    # Acquiring Debye length
    parameters['Debye length'] = np.sqrt(2 * EPSILON_NAUGHT *  \
                                         parameters['Electron temperature (Joules)'] /  \
                                        (parameters['Electron density'] * ELECTRON_CHARGE ** 2))
    

def get_number_of_electrons(parameters):
    
    """DLP and SLP number of particles in the debye sphere is yielded from this function."""
    
    # Obtaining the number of electrons in the debye sphere 
    parameters['Number of electrons'] = 4/3 * np.pi * parameters['Debye length'] * \
                                                      parameters['Electron density']


def get_particle_density(parameters):
    
    """This function yields the density for SLP, HEA, and IEA, in Kilograms per cubic meter.
    
    If SLP or HEA for electron parameters is used, must receive electron mass as particle mass.
    
    Otherwise, the particle mass should be the estimated mass of the ions in the plasma
    """
    
    if  'Electron saturation current' in parameters:
        parameters['Particle saturation current'] = parameters['Electron saturation current']
        parameters['Particle temperature (Joules)'] = parameters['Electron temperature (Joules)'] 

    # Acquiring electron density
    parameters['Particle density'] =  abs(parameters['Particle saturation current'] / \
                                         (ELECTRON_CHARGE * parameters['Probe area'] * \
                                          np.sqrt(abs(parameters['Particle temperature (Joules)'] / \
                                         (np.pi * parameters['Particle mass'] * 2)))))
   
    if  'Electron saturation current' in parameters:
       parameters['Electron density'] = parameters['Particle density']
       del parameters['Particle density']
       del parameters['Particle temperature (Joules)']
       
       
def get_particle_saturation_current(parameters):
    
    """This function yields the saturation current for HEA and IEA."""
    
    # Storing parameters used for calculations
    filtered_current = parameters['Filtered current']
    bias = parameters['Bias']
    
    # Storing the charged particle saturation current
    parameters['Particle saturation current'] = np.min(abs(np.gradient(filtered_current, bias)))
    
       
def get_plasma_potential(parameters):
    
    """HEA and IEA plasma potential is yielded by the applied bias where dI/dV = 0"""
    
    # Storing I-V values
    filtered_current_list = parameters['Filtered current'] 
    voltage_list =  parameters['Bias']
    
    # Storing dI/dV
    derivative = np.gradient(filtered_current_list, voltage_list)
    
    # Value closest to 0 is taken to yield the index, since the derivative may not be 0
    parameters['Plasma potential index'] = np.argmin(abs(derivative))
    
    # Storing the plasma potential
    parameters['Plasma potential'] = voltage_list[parameters['Plasma potential index']]

    
def get_particle_temperature(parameters):
    
    """HEA and IEA particle temperature for electron volts and  Joules is yielded by this function.
    
    Particle temperature in electron volts may be yielded from the value of
    
    1/ (d(ln(I))/dV) where the plasma potential occurs.
    """
    # Storing parameters used to calculate temperature
    plasma_potential_index = parameters['Plasma potential index']
    filtered_current_list = parameters['Filtered current'] 
    voltage_list =  parameters['Bias']
    
    # Storing the derivative of the ln(I)-V values
    log_I_V_derivative=  np.gradient(np.log(abs(filtered_current_list)), voltage_list )
    
    # Storing the particle temperature in electron volts
    parameters['Particle temperature (eV)'] = 1 / log_I_V_derivative[plasma_potential_index]
    
    # Storing the particle temperature in Joules
    parameters['Particle temperature (Joules)'] = parameters['Particle temperature (eV)'] * ELECTRON_CHARGE
    

def get_equations():
    
    """This function returns a list of references for the equations used by 
    
    the HEA and IEA implementations.
    """
    
    list_of_references = []
    list_of_references.append(filter_current)
    list_of_references.append(get_particle_saturation_current)
    list_of_references.append(get_plasma_potential)
    list_of_references.append(get_particle_temperature)
    list_of_references.append(get_particle_density)
    return list_of_references


""" Sample usage of the equations. 

Must note, since HEA nor IEA expect a sigmoid, calculation results will not make sense, 

yet they still highlight that the algorithms are running."""    

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
    
    # Electron mass in Kilograms
    parameters ['Particle mass'] = 9.10938356e-31
   
    # Running each equation
    list_of_equations = get_equations()
    for i in list_of_equations:
        i(parameters)
        
    # Printing the parameters
    for key, value in parameters.items():
        if 'Raw current'!= key and 'Filtered current' != key and 'Bias' != key:
            print(key, ': ' ,value)