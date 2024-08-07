
import numpy as np

def get_ion_saturation_current(filtered_current_list):
    '''
    **TODO: find a better way to obtain ion saturation current.**
    
    The ion saturation current is returned from this function.
    
    NOTE: This is a simple and crude way to obtain the value. Refer to SDD to understand logic behind this method. 
    
    '''
    #storing the ion saturation current 
    ion_saturation_current = np.min(filtered_current_list)
    
    return ion_saturation_current
    
    
def get_electron_temperature(filtered_current_list, voltage_list, ion_saturation_current):
    '''
    This function returns the electron temperature in both Joules and electron volts.
    
    The value of  the derivative of the I-V values where the voltage applied is 0 is used to calculate electron temperature, yet it is possible
    that the voltage applied is never 0, thus the value closet to 0 shall be used. 
    '''
    #storing the charge of the electron particle, since it shall be used for calculation
    electron_charge = 1.60217657e-19
    
    #storing the index where the voltage is closest to 0
    voltage_at_zero_index = np.argmin(abs(voltage_list))
    
    #storing the derivative of the I-V values
    
    I_V_derivative = np.gradient(filtered_current_list, voltage_list )
    
    
    #calculating electron temperature in electron volts 
    electron_temperature_ev = abs(ion_saturation_current / (2 * (I_V_derivative[voltage_at_zero_index])))
    
    #calculating electron temperature in Joules
    electron_temperature_joules = electron_temperature_ev * electron_charge
 
    return electron_temperature_ev, electron_temperature_joules

def get_electron_density(electron_temperature_joules, probe_area, ion_saturation_current, ion_mass):
    
    '''
    this function returns the electron density in Kilograms per cubic meter. 
    '''
    #storing the charge of the electron particle, since it shall be used for calculation
    electron_charge = -1.60217657e-19
    
    #acquiring electron density 
    electron_density = ion_saturation_current/(electron_charge *  probe_area) * np.sqrt(ion_mass/electron_temperature_joules) * np.exp(0.5)
    
    return electron_density

    
    
    
    
    