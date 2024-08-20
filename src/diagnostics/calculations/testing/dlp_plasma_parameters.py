
import numpy as np
from global_parameters import get_debye_length, get_number_of_electrons

#storing the charge of the electron particle, since it shall be used for calculation
electron_charge = 1.60217657e-19
   
def get_ion_saturation_current(parameters):
    filtered_current_list = parameters['Filtered current list'] 
    '''
    **TODO: find a better way to obtain ion saturation current.**
    
    The ion saturation current is returned from this function.
    
    NOTE: This is a simple and crude way to obtain the value. Refer to SDD to understand logic behind this method. 
    '''
    #storing the ion saturation current 
    parameters['Ion saturation current'] = np.min(filtered_current_list)
   
    
    
def get_electron_temperature( parameters):
    filtered_current_list = parameters['Filtered current list'] 
    voltage_list =  parameters['Voltage list'] 
    ion_saturation_current = parameters['Ion saturation current'] 
    '''
    This function returns the electron temperature in both Joules and electron volts.
    
    The value of  the derivative of the I-V values where the voltage applied is 0 is used to calculate electron temperature, yet it is possible
    that the voltage applied is never 0, thus the value closet to 0 shall be used. 
    '''
 
    #storing the index where the voltage is closest to 0
    voltage_at_zero_index = np.argmin(abs(voltage_list))
    
    #storing the derivative of the I-V values
    I_V_derivative = np.gradient(filtered_current_list, voltage_list )
    
    #calculating electron temperature in electron volts 
    parameters['Electron temperature (eV)'] = abs(ion_saturation_current / (2 * (I_V_derivative[voltage_at_zero_index])))
    
    #calculating electron temperature in Joules
    parameters['Electron temperature (Joules)'] = parameters['Electron temperature (eV)'] * electron_charge


def get_electron_density(parameters):
    '''
    this function returns the electron density in Kilograms per cubic meter. 
    ''' 
    #acquiring electron density 
    parameters['Electron density'] = parameters['Ion saturation current']/(electron_charge *  parameters['Probe area']) * np.sqrt(parameters['Ion mass']/parameters['Electron temperature (Joules)']) * np.exp(0.5)
    

def get_equations():
    '''
    This function returns a reference to the equations 
    '''
    list_of_references = []
    list_of_references.append(get_ion_saturation_current)
    list_of_references.append(get_electron_temperature)
    list_of_references.append(get_electron_density)
    list_of_references.append(get_debye_length)
    list_of_references.append(get_number_of_electrons)
    return list_of_references
    
    
    