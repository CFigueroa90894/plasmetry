import os
import sys

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 4            # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
   # print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #

import numpy as np
from scipy import signal
from protected_dictionary import ProtectedDictionary

# Normalized cutoff frequency for the butterworth filter
CUTOFF_FREQUENCY = 0.03

# Order of the butterworth filter
FILTER_ORDER = 2


def filter_current(parameters):
    
    # Extracted from Felix Cuadrado's code
    """Filters a signal using a butterworth digital filter. 
    
    Inputs:
        rawSignal = an array of raw data captured by the sensor.
        
    Outputs:
        filteredSignal = signal after being processed by a butterworth digital filter.
    """

    try:
        sos = signal.butter(FILTER_ORDER, CUTOFF_FREQUENCY, output='sos')
        
        filteredSignal = np.array(signal.sosfiltfilt(sos, parameters['Raw voltage 1']))
       
        parameters['Filtered current (Amperes)'] = filteredSignal / parameters['config_ref']['sweeper_shunt']
        
    except Exception as e: 
        print(f'{e}')
        parameters['Particle density (m-3)'] = np.nan
        
    
def get_display_parameters(parameters):
    
    """This function returns a ProtectedDictionary object containing the parameters used for display.
    
    Intended for all probe parameters."""
    
    display_parameters = []

    display_parameters.append(parameters['Particle saturation current (Amperes)'])
    display_parameters.append(parameters['Particle temperature (eV)'])
    display_parameters.append(parameters['Particle temperature (Joules)'])
    display_parameters.append(parameters['Particle density (m-3)'])
    
    return display_parameters

def get_debye_length(parameters):
    
    """DLP and SLP Debye length is calculated from this function in meters."""
    if np.isnan(parameters['Electron temperature (Joules)']):
        parameters['Debye length (Meters)'] = np.nan
    # Storing the charge of the electron particle in Coulumb
    ELECTRON_CHARGE = 1.60217657e-19
    
    # Storing the permittivity of free space constant in F/m
    EPSILON_NAUGHT= 8.854e-12
    
    # Acquiring Debye length
    parameters['Debye length (Meters)'] = np.sqrt(2 * EPSILON_NAUGHT *  \
                                         parameters['Electron temperature (Joules)'] /  \
                                        (parameters['Electron density (m-3)'] * ELECTRON_CHARGE ** 2))

 
def get_number_of_electrons(parameters):
    
    """DLP and SLP number of particles in the debye sphere is yielded from this function."""
    
    if np.isnan(parameters['Debye length (Meters)']) or np.isnan(parameters['Electron density (m-3)']): 
        parameters['Number of electrons'] =  np.nan
        return None
    # Obtaining the number of electrons in the debye sphere 
    parameters['Number of electrons'] = int(4/3 * np.pi * parameters['Debye length (Meters)'] * \
                                            parameters['Electron density (m-3)'])
        
        
def get_particle_density(parameters):
    
    """This function yields the density for SLP, HEA, and IEA, in particles per cubic meter.
    
    If SLP or HEA for electron parameters is used, must receive electron mass as particle mass.
    
    Otherwise, the particle mass should be the estimated mass of the ions in the plasma
    """
    try:
        # Storing the charge of the electron particle in Coulumb
        ELECTRON_CHARGE = 1.60217657e-19
        
        # Configuration object stored, in order to get 'Probe Area'
        config_object = parameters['config_ref']
        probe_area = config_object['Probe area']
        particle_mass =  config_object['Particle mass']
        
        # Verifying the argument keys in order to store variables
        if  'Electron saturation current (Amperes)' in parameters:
            particle_saturation_current = parameters['Electron saturation current (Amperes)']
            particle_temperature = parameters['Electron temperature (Joules)'] 
            
        elif 'Ion saturation current (Amperes)' in parameters:
            particle_saturation_current = parameters['Ion saturation current (Amperes)']
            particle_temperature = parameters['Electron temperature (Joules)'] 

        else:
            particle_temperature = parameters['Particle temperature (Joules)']
            particle_saturation_current = parameters['Particle saturation current (Amperes)']
        # Acquiring electron density
        parameters['Particle density (m-3)'] =  abs(particle_saturation_current / \
                                             (ELECTRON_CHARGE * probe_area * \
                                              np.sqrt(abs(particle_temperature / \
                                             (np.pi * particle_mass * 2)))))

        # Deleting the temporary key created for SLP
        if ('Electron saturation current (Amperes)' in parameters) or ('Ion saturation current (Amperes)' in parameters):       
            parameters['Electron density (m-3)'] = parameters['Particle density (m-3)']
            del parameters['Particle density (m-3)']
    except Exception as e:
        print('f{e}')
        parameters['Particle density (m-3)'] = np.nan
        parameters['Electron density (m-3)'] = np.nan
       
       
       
def get_particle_saturation_current(parameters):
    
    """This function yields the saturation current for HEA and IEA."""
    
    # Storing parameters used for calculations
    filtered_current = parameters['Filtered current (Amperes)']
    bias = parameters['Bias 1']
    
    # Storing the charged particle saturation current
    saturation_index = np.argmin(abs(np.gradient(filtered_current, bias)))
    parameters['Particle saturation current (Amperes)'] = filtered_current[saturation_index]
       
    
def get_plasma_potential(parameters):
    
    """HEA and IEA plasma potential is yielded by the applied bias where dI/dV = 0"""
    
    # Storing I-V values
    filtered_current_list = parameters['Filtered current (Amperes)'] 
    voltage_list =  parameters['Bias 1']
    
    # Storing dI/dV
    derivative = np.gradient(filtered_current_list, voltage_list)
    
    # Value closest to 0 is taken to yield the index, since the derivative may not be 0
    parameters['Plasma potential index'] = np.argmin(abs(derivative))
    
    # Storing the plasma potential
    parameters['Plasma potential (Volts)'] = voltage_list[parameters['Plasma potential index']]

    
def get_particle_temperature(parameters):
    
    """HEA and IEA particle temperature for electron volts and  Joules is yielded by this function.
    
    Particle temperature in electron volts may be yielded from the value of
    
    1/ (d(ln(I))/dV) where the plasma potential occurs.
    """
    
    # Storing the charge of the electron particle in in Coulumb
    ELECTRON_CHARGE = 1.60217657e-19
    
    # Storing parameters used to calculate temperature
    plasma_potential_index = parameters['Plasma potential index']
    filtered_current_list = parameters['Filtered current (Amperes)'] 
    voltage_list =  parameters['Bias 1']
    
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
    list_of_references.append(get_display_parameters)

    return list_of_references


""" Sample usage of the equations. 

Must note, since  the EAs do not expect a sigmoid, calculation results will not make sense, 

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
    parameters['Bias 1'], parameters['Raw voltage 1'] =  LoadPreviousData()
    
    # Storing Probe area of a previous implementation, and ion mass in kg of argon, 
    # simulating config values
    parameters['config_ref'] = {'Probe area' : 30.3858e-06, 'Particle mass': 6.629e-26, 'Shunt 1': 1}
    
    # Running each equation
    list_of_equations = get_equations()
    for i in list_of_equations[:len(list_of_equations)-1]:
        i(parameters)
    
    parameters_to_display = list_of_equations[-1](parameters)
    
    keys = parameters_to_display.keys()
    
    for i in keys: 
        print(i, ':', parameters_to_display[i])