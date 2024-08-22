
import numpy as np
from global_parameters import get_debye_length, get_number_of_electrons, get_particle_density

#storing the charge of the electron particle, since it shall be used for calculation
electron_charge = 1.60217657e-19
   
def get_floating_and_plasma_potential(parameters):
    filtered_current_list = parameters['Filtered current'] 
    voltage_list =  parameters['Bias']
    '''
    ** TODO: a better way to yield floating potential is available. will potentially implement it from PlasmaPy. must study more the documentation
    
    This function returns two lists that contains the floating potential and plasma potential and their respective index within the filtered_current_list. 
    '''
    
    '''
    The floating potential is defined as the voltage at which the current captured is 0.
    
    Since currents acquired may not reach 0, the current value closest to 0 shall be taken.
    
    '''
    
    #acquiring the index where the current is closest to 0
    parameters['Floating potential index'] = np.argmin(abs(filtered_current_list))
    
    parameters['Floating potential'] = voltage_list[parameters['Floating potential index']]
    
    '''
    The plasma potential may be yielded from the value of the voltage where the maximum value of the derivate occurs
    '''
    
    #storing the index of the maximum value of the derivative
    parameters['Plasma potential index']  = np.argmax(np.gradient(filtered_current_list, voltage_list))
    
    #acquiring plasma potential and storing in the list
    parameters['Plasma potential'] =voltage_list[parameters['Plasma potential index'] ]
    

'''TODO: get best way to yield ion saturation current'''
def get_electron_saturation_current(parameters):
    filtered_current_list = parameters['Filtered current']     
    '''
    The electron saturation current is returned from this function.
    
    The electron saturation region commences at the plasma potential, thus the current acquired at this point yields the value of the electron saturation current.
    '''
     
    #storing the current acquired at the plasma potential 
    parameters['Electron Saturation current'] = filtered_current_list[parameters['Plasma potential index']]
    
    
    

    

def get_electron_temperature(parameters):
    '''
    Single Langmuir Probe electron temperature in both electron volts and  Joules is returned by the slp_electron_temperature function.
    
    Electron temperature may be yielded from the inverse value of the slope of the ln(I)-V values between the floating and plasma potential.
    '''
    
    floating_potential=  parameters['Floating potential']
    plasma_potential = parameters['Plasma potential']
    filtered_current_list = parameters['Filtered current'] 
    voltage_list =  parameters['Bias']
    
    
    #since the  floating potential is not yieded in the best way, we'll be using an estimation for the value of the initial point in the slope.
    #where the value is located between the currently estimated floating potential and the plasma potential, 
    #thus the point should be in the line that is generated from the ln(I)-V graph
    middle_index = int(np.ceil((plasma_potential[0] + floating_potential[0] )/2))
    
    #to calculate the slope of the ln(I)-V values between the floating and plasma potential, the numerator and denominator shall be acquired 
    numerator_of_slope = np.log(filtered_current_list[plasma_potential[0]]) - np.log(abs(filtered_current_list[middle_index]))
    
    denominator_of_slope  = plasma_potential[1] - voltage_list[middle_index]
    
    #Denominator/numerator is being performed since the inverse value of the slope yields the electron temperature in electron volts 
    parameters['Electron temperature (eV)'] = denominator_of_slope/numerator_of_slope
    
    #multiplying the electron particle mass times the electron temperature in electron volts yields the electron temperature in Joules
    parameters['Electron temperature (Joules)'] = parameters['Electron temperature (eV)'] * electron_charge
    


def get_equations():
    '''
    This function returns a reference to the equations 
    '''
    list_of_references = []
    list_of_references.append(get_floating_and_plasma_potential)
    list_of_references.append(get_electron_saturation_current)
    list_of_references.append(get_electron_temperature)
    list_of_references.append(get_particle_density)
    list_of_references.append(get_debye_length)
    list_of_references.append(get_number_of_electrons)
    return list_of_references
    
    
   


    
    
    