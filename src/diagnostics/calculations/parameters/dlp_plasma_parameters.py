import os
import sys

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 3        # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
   # print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #

import numpy as np 
from global_parameters import (
    filter_current,
    get_debye_length,
    get_number_of_electrons
)


def get_ion_saturation_current(parameters):
    
    """**TODO: find a better way to obtain ion saturation current.**
    
    The ion saturation current is yielded from this function.
    
    NOTE: This is a simple and crude way to obtain the value.
    """
    if len(parameters['Filtered current (Amperes)']) != 0:
    # Storing the ion saturation current.
        parameters['Ion saturation current (Amperes)'] = np.min(parameters['Filtered current (Amperes)'] )
        return
    parameters['Ion saturation current (Amperes)'] = np.nan
   
    
def get_electron_temperature( parameters):
    
    """This function calculates the electron temperature in both Joules and electron volts.
    
    The value of  the derivative in the I-V curve where the voltage applied is 0 is used 
    
    to calculate electron temperature, yet it is possible that the voltage applied is never 0, 
    
    thus the value closet to 0 shall be used. 
    """
    if np.isnan(parameters['Ion saturation current (Amperes)']):
        parameters['Electron temperature (eV)'] = np.nan
        parameters['Electron temperature (Joules)'] = np.nan
        return
        
    # Storing the charge of the electron particle, since it shall be used for calculation
    ELECTRON_CHARGE = 1.60217657e-19
    
    # Storing parameters used for calculations
    filtered_current_list = parameters['Filtered current (Amperes)'] 
    voltage_list =  parameters['Bias 1'] 
    ion_saturation_current = parameters['Ion saturation current (Amperes)'] 
    if len(voltage_list) > 0:
    # Storing the index where the voltage is closest to 0.
        voltage_at_zero_index = np.argmin([abs(i) for i in voltage_list])
    else:
        parameters['Electron temperature (eV)'] = np.nan
        parameters['Electron temperature (Joules)'] = np.nan
        return
    
    # Storing the derivative of the I-V values.
    I_V_derivative = np.gradient(filtered_current_list, voltage_list )
    
    denominator_of_equation = 2 * I_V_derivative[voltage_at_zero_index]
    # Calculating electron temperature in electron volts. 
    parameters['Electron temperature (eV)'] = abs(ion_saturation_current / denominator_of_equation)
    
    # Calculating electron temperature in Joules.
    parameters['Electron temperature (Joules)'] = parameters['Electron temperature (eV)'] * ELECTRON_CHARGE


def get_electron_density(parameters):
    
    """This function yields the electron density in Kilograms per cubic meter. """ 
    if np.isnan(parameters['Electron temperature (Joules)']):
        parameters['Electron density (m-3)'] = np.nan
        return
        
    # Storing the charge of the electron particle, since it shall be used for calculation
    ELECTRON_CHARGE = 1.60217657e-19
    
    # Configuration object stored, in order to get 'Probe Area' and 'Ion mass'
    config_object = parameters['config_ref']
    probe_area = config_object['Probe area']
    ion_mass = config_object['Particle mass']
    
    # Acquiring electron density 
    square_root_term =  np.sqrt(ion_mass / parameters['Electron temperature (Joules)'])
    parameters['Electron density (m-3)'] = abs(parameters['Ion saturation current (Amperes)'] / \
                                        (ELECTRON_CHARGE *  probe_area) * \
                                        (square_root_term * np.exp(0.5)))


def get_display_parameters(parameters):
    
    """This function returns a ProtectedDictionary object containing the parameters used for display.
    
    Intended for all probe parameters."""
    display_parameters = []
    display_parameters.append(parameters['Ion saturation current (Amperes)'])
    display_parameters.append(parameters['Electron temperature (eV)'])
    display_parameters.append(parameters['Electron temperature (Joules)'])
    display_parameters.append(parameters['Electron density (m-3)'])
    display_parameters.append(parameters['Debye length (Meters)'])
    display_parameters.append(parameters['Number of electrons'])

    return display_parameters

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
    list_of_references.append(get_display_parameters)
    return list_of_references


""" Sample usage of the equations. Requires protected_dictionary to be loaded in memory."""    
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
    parameters['config_ref'] = {'Probe area' : 30.3858e-06, 'Particle mass': 6.629e-26, 'sweeper_shunt': 1}
    
    
    # Running each equation
    list_of_equations = get_equations()
    
    for i in list_of_equations[:len(list_of_equations)-1]:
        i(parameters)
    
    # Requires protected_dictionary to be loaded in memory
    parameters_to_display = list_of_equations[-1](parameters)
    
   
    
    for i in parameters_to_display: 
        print(i)
        