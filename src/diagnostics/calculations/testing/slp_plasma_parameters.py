
import numpy as np

'''TODO: a better way to yield floating potential is available. will potentially implement it from PlasmaPy. must study more the documentation'''

def get_floating_and_plasma_potential(filtered_current_list, voltage_list):
    
    '''This function returns two lists that contains the floating potential and plasma potential 
    and their respective index within the filtered_current_list. '''
    
    #initializing the lists
    floating_potential =[]
    plasma_potential= []
    
    
    '''The floating potential is defined as the voltage at which the current captured is 0.
       Since currents acquired may not reach 0, the current value closest to 0 shall be taken.'''
    
    #acquiring the index where the current is closest to 0
    floating_potential_index = np.argmin(abs(filtered_current_list))
    
    #storing the floating potential index in a list since it shall be used to calculate electron temperature
    floating_potential.append(floating_potential_index)
    
    #acquiring the floating potential and storing in the list
    floating_potential.append(voltage_list[floating_potential_index])
    
   
    
    '''The plasma potential may be yielded from the value of the voltage where the maximum value of the derivate occurs'''
    
    #storing the index of the maximum value of the derivative
    plasma_potential_index = np.argmax(np.gradient(filtered_current_list, voltage_list))
    
    #storing the index in a lis since it shall be used to calculate electron temperature 
    plasma_potential.append(plasma_potential_index)
     
    #acquiring plasma potential and storing in the list
    plasma_potential.append( voltage_list[plasma_potential_index])
    
    return floating_potential, plasma_potential

'''TODO: get best way to yield ion saturation current'''
def get_electron_saturation_current(filtered_current_list, plasma_potential_index):
    
    
    '''The electron saturation current is returned from this function.
    
    The electron saturation region commences at the plasma potential, thus the current acquired at this point yields the value of the electron saturation current.'''
     
    #storing the current acquired at the plasma potential 
    electron_saturation_current = filtered_current_list[plasma_potential_index]
    
    return electron_saturation_current
    

    

def get_electron_temperature(floating_potential, plasma_potential, filtered_current_list, voltage_list):
    '''
    Single Langmuir Probe electron temperature in both electron volts and  Joules is returned by the slp_electron_temperature function.
    
    Electron temperature may be yielded from the inverse value of the slope of the ln(I)-V values between the floating and plasma potential.
    '''
    
    #storing the charge of the electron particle, since it shall be used for calculation
    electron_charge = 1.60217657e-19
    
    #since the  floating potential is not yieded in the best way, we'll be using an estimation for the value of the initial point in the slope.
    #where the value is located between the currently estimated floating potential and the plasma potential, 
    #thus the point should be in the line that is generated from the ln(I)-V graph
    middle_index = int(np.ceil((plasma_potential[0] + floating_potential[0] )/2))
    
    
    #to calculate the slope of the ln(I)-V values between the floating and plasma potential, the numerator and denominator shall be acquired 
    numerator_of_slope = np.log(filtered_current_list[plasma_potential[0]]) - np.log(abs(filtered_current_list[middle_index]))
    denominator_of_slope  = plasma_potential[1] - voltage_list[middle_index]
    
    #Denominator/numerator is being performed since the inverse value of the slope yields the electron temperature in electron volts 
    electron_temperature_ev = denominator_of_slope/numerator_of_slope
    
    #multiplying the electron particle mass times the electron temperature in electron volts yields the electron temperature in Joules
    electron_temperature_joules = electron_temperature_ev * electron_charge
    
    #could return the temperature in a list containing both ev and Joules values of electron temperature, need to review with team
    return electron_temperature_ev, electron_temperature_joules


    
   


    
    
    