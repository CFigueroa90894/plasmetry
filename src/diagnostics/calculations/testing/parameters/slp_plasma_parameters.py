import numpy as np
from global_parameters import get_debye_length, get_number_of_electrons, get_particle_density
from scipy import signal

"""TODO: get best way to yield ion saturation current"""

# Storing the charge of the electron particle, since it shall be used for calculation
electron_charge = 1.60217657e-19


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
    

def get_floating_and_plasma_potential(parameters):
    
    
    """This function yields two lists that contains the floating potential and plasma potential and their respective index within the filtered_current_list. 
    
    The floating potential is defined as the voltage at which the current captured is 0.
    
    Since currents acquired may not reach 0, the current value closest to 0 shall be taken.
    """
    
    # Storing filtered current and applied bias 
    filtered_current_list = parameters['Filtered current'] 
    voltage_list = parameters['Bias']

    # Storing the index of the floating potential and it's value
    parameters['Floating potential index'] = np.argmin(abs(filtered_current_list)) 
    parameters['Floating potential'] = voltage_list[parameters['Floating potential index']]
    
    
    """The plasma potential may be yielded from the value of the voltage where the 

    minimum value of the second order derivate occurs
    """
    
    # Acquiring second order derivative
    first_derivative = np.gradient(filtered_current_list, voltage_list)
    second_derivative = np.gradient(first_derivative, voltage_list)
    # Storing the index of the plasma potential and it's value
    parameters['Plasma potential index'] = np.argmin(second_derivative)
    parameters['Plasma potential'] = voltage_list[parameters['Plasma potential index']]
    
    if parameters['Plasma potential']<= 0: 
        return 'currents measured in this sweep are not valid, as they do not produce a sigmoid.'


def get_electron_saturation_current(parameters):    
    
    """The electron saturation current yields from this function.
    
    The electron saturation region commences at the plasma potential,
    thus the current acquired at this point yields the value of the electron saturation current.
    """
    
    filtered_current_list = parameters['Filtered current']
    
    # Storing the current acquired at the plasma potential 
    parameters['Electron saturation current'] = filtered_current_list[parameters['Plasma potential index']]


def get_electron_temperature(parameters):

    """Single Langmuir Probe electron temperature in both electron volts 
    
    and  Joules is returned by the slp_electron_temperature function.
    
    Electron temperature may be yielded from the inverse value of the slope of the ln(I)-V values
    
    between the floating and plasma potential.
    
    Since the plasma potential and floating potential are yielded as approximations,
    
    The starting and final point used to calculate the slope of the ln(I)-V graph were chosen between 
    
    the previously acquired plasma and floating potential.
    
    Since these points should be within the line between the floating potential and plasma potential of the ln(i)-v 
    """
   
    # The final point is the point with an index 3/4 of the distance between the floating potential and plasma potential. 
    final_index= int(np.ceil((parameters['Plasma potential index']  -  parameters['Floating potential index']) *0.75 ))+ parameters['Floating potential index']
    # The starting point is the point with an index 1/4 of the way between the floating potential and plasma potential. 
    starting_index = int(np.ceil((parameters['Plasma potential index']  -  parameters['Floating potential index'] )*0.25) )+ parameters['Floating potential index']
   
    # To calculate the slope of the ln(I)-V values between the floating and plasma potential, the numerator and denominator shall be acquired 
    numerator_of_slope = np.log(parameters['Filtered current'][final_index]) - \
    np.log(abs(parameters['Filtered current'] [starting_index]))
    denominator_of_slope = parameters['Bias'][final_index] - parameters['Bias'][starting_index]
    
    # Denominator/numerator is being performed since the inverse value of the slope yields the electron temperature in electron volts 
    parameters['Electron temperature (eV)'] = denominator_of_slope/numerator_of_slope
    
    # Multiplying the electron particle mass times the electron temperature in electron volts yields the electron temperature in Joules
    parameters['Electron temperature (Joules)'] = parameters['Electron temperature (eV)'] * electron_charge


def get_equations():

    """This function returns a reference to the equations defined in this script"""

    # List containing the references
    list_of_references = []

    # Local parameters
    list_of_references.append(filter_current)

    list_of_references.append(get_floating_and_plasma_potential)
    list_of_references.append(get_electron_saturation_current)
    list_of_references.append(get_electron_temperature)

    # Global parameters
    list_of_references.append(get_particle_density) 
    list_of_references.append(get_debye_length)
    list_of_references.append(get_number_of_electrons)

    return list_of_references


if __name__ == "__main__": 
    ''' sample usage of the equations'''    
    def LoadPreviousData():
        import csv 

        """Function to load data from previous implementation. Code developed by Felix Cuadrado"""
        with open('../testing scenarios/Feliz_A1 MirorSLP120200813T105858.csv', newline='') as csvfile:
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
    
    #parameter dictionary, stores parameters
    parameters= {}
    
    #storing bias and raw current from previous implementation
    parameters['Bias'], parameters['Raw current'] =  LoadPreviousData()
    
    #probe area of a previous implementation, simulating config values
    parameters['Probe area'] =  30.3858e-06
    
    #electron mass in Kilograms
    parameters ['Particle mass'] = 9.10938356e-31
   
    #running each equation
    list_of_equations = get_equations()
    for i in list_of_equations:
        i(parameters)
        
    #printing the parameters
    for i in parameters.keys():
        if 'current' not in i and 'Bias' != i:
            print( i + ': ', parameters[i])
    
    
    