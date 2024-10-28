import os
import sys

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 3           # how many parent folders to reach /plasmetry/src

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
    display_parameters.append(parameters['Plasma potential (Volts)'])
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
    parameters['Debye length (Meters)'] = np.sqrt((2 * EPSILON_NAUGHT *  \
                                         parameters['Electron temperature (Joules)'] )/  \
                                        (parameters['Electron density (m-3)'] * ELECTRON_CHARGE ** 2))

 
def get_number_of_electrons(parameters):
    
    """DLP and SLP number of particles in the debye sphere is yielded from this function."""
    
    if np.isnan(parameters['Debye length (Meters)']) or np.isnan(parameters['Electron density (m-3)']): 
        parameters['Number of electrons'] =  np.nan
        return None
    # Obtaining the number of electrons in the debye sphere 
    parameters['Number of electrons'] = int(4/3 * np.pi * parameters['Debye length (Meters)'] ** 3 * \
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
    
    # Storing the charged particle saturation current
    parameters['Plasma potential index'] = np.argmax(abs(filtered_current))
    
    parameters['Particle saturation current (Amperes)'] = filtered_current[ parameters['Plasma potential index']]
    
    
def get_plasma_potential(parameters):
    
    """HEA and IEA plasma potential is yielded by the applied bias where dI/dV = 0"""
    
    # Storing I-V values
    filtered_current_list = parameters['Filtered current (Amperes)'] 
    voltage_list =  parameters['Bias 1']
 
    
    # Storing the index of the plasma potential and its value

    parameters['Plasma potential (Volts)'] = voltage_list[parameters['Plasma potential index']]
    
    # Storing the index of the floating potential and its value
    parameters['Minimum value index'] = np.argmin(abs(filtered_current_list)) 
    parameters['Minimum value (Volts)'] = voltage_list[parameters['Minimum value index']]
    
def get_particle_temperature(parameters):

    """Single Langmuir Probe electron temperature in both electron volts 
    
    and  Joules is calculated by the slp_electron_temperature function.
    """
    
    """Electron temperature is to be yielded from the inverse value of the slope of the ln(I)-V values 
    
    between the floating and plasma potential. Since the plasma potential and floating potential are yielded 
    
    as approximations, the starting and final point used to calculate the slope of the ln(I)-V graph were chosen
    
    between the plasma and floating potential since these points shall be in the line that is formed in the ln(I)-V graph.
    
    This decision was made to ensure the calculations are based on the expected slope.
    """
    try:
        # Storing the charge of the electron particle, since it shall be used for calculation
        ELECTRON_CHARGE = 1.60217657e-19

        # Storing the number of points between the plasma potential and floating potential.
        points_number = parameters['Plasma potential index'] -  parameters['Minimum value index']
        
        # The starting point used calculate the slope is the point with an index 1/4 of the way
        # between the floating potential and plasma potential.
        starting_index = parameters['Plasma potential index']
        
        # The final point used to calculate the slope is the point with an index 3/4 of the distance 
        # between the floating potential and plasma potential. 
        final_index= int(np.ceil(points_number * 0.75 )) + parameters['Minimum value index']
       
        # To calculate the slope, the numerator and denominator shall be acquired.
        numerator_of_slope = np.log(abs(parameters['Filtered current (Amperes)'][final_index])) - \
        np.log(abs(parameters['Filtered current (Amperes)'] [starting_index]))
        denominator_of_slope = abs(parameters['Bias 1'][final_index]) - parameters['Bias 1'][starting_index]
        # Denominator / numerator is being performed 
        parameters['Particle temperature (eV)'] =abs( denominator_of_slope / numerator_of_slope)
        # Multiplying the electron particle mass times the electron temperature in electron volts
        # yields the electron temperature in Joules
        parameters['Particle temperature (Joules)'] = parameters['Particle temperature (eV)'] * ELECTRON_CHARGE
        
    except Exception as e: 
        
        # storing np.nan since there is an error raise
        parameters['Particle temperature (eV)'] = np.nan
        
        # storing np.nan since there is an error raise
        parameters['Particle temperature (Joules)'] = np.nan
        print (f'{e}')
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
    import matplotlib.pyplot as plt
    
    def LoadPreviousData():
        
        """Function to load data from previous implementation. Code developed by Felix Cuadrado"""
        
        import csv as csv_library
        with open('Leal_IonEnergyAnalyzer.csv', newline='') as csv:
            dataReader = csv_library.reader(csv, delimiter=',', quotechar='|')
            next(dataReader)  # Skip the header row
            current = []
            voltageSLP = []
            for row in dataReader:
                try:
                    current = np.append(current, float(row[1]))
                    voltageSLP = np.append(voltageSLP, float(row[0]))
                except:
                    None    
            
            return voltageSLP, current 
    
    
    # Parameter dictionary, stores parameters
    parameters= {}
    
    # Storing bias and raw current lists from previous implementation
    parameters['Bias 1'], parameters['Filtered current (Amperes)'] =  LoadPreviousData()
   # parameters['Filtered current (Amperes)'] = np.sort(parameters['Filtered current (Amperes)'])
    # Storing Probe area of a previous implementation, and ion mass in kg of argon, 
    # simulating config values
    parameters['config_ref'] = {'Probe area' : 30.3858e-06, 'Particle mass': 6.629e-26, 'sweeper_shunt': 1}
    
    # Running each equation
    list_of_equations = get_equations()

    for i in list_of_equations[1:]:
        i(parameters)
    
    
    
    print(f"Plasma Potential (Volts): {parameters['Plasma potential (Volts)']}")
    plt.plot( parameters['Bias 1'], parameters['Filtered current (Amperes)'], marker='o', linestyle='-')
    plt.xlabel('Bias')
    plt.ylabel('Raw Signal')
    plt.title('Plot of Raw Signal vs Bias')
    plt.grid(True)
    plt.axvline(x= parameters['Plasma potential (Volts)'], color='r')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.show()
    
    print(parameters)