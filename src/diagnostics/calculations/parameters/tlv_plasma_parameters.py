import numpy as np 
from global_parameters import get_display_parameters



# Storing the charge of the electron particle, since it shall be used for calculation
ELECTRON_CHARGE = 1.60217657e-19
 
NUMBER_OF_ITERATIONS = 100

TOLERANCE = 1e-5


def filter_current(parameters):
    
    parameters['Potential difference'] = np.sum(parameters['Raw voltage 2']) / len(parameters['Raw voltage 2'])
    del parameters['Raw voltage 2']
    parameters['Raw voltage 1'] = np.sum(parameters['Raw voltage 1']) / len(parameters['Raw voltage 1'])
    parameters['Filtered current (Amperes)'] = parameters['Raw voltage 1'] / parameters['config_ref']['up_shunt']
    
def iteration(potential_difference, bias, estimated_guess):
    
    """This function performs the function and derivative calculation process in each iteration.
    
       Returns the value expressions."""
    
    # Declaring limit to avoid overflow
    LIMIT = 500  
    
    # First exponential term, shall be used for function and derivative calculation
    first_exp_term = 2 * np.exp(np.clip(potential_difference * estimated_guess, None, LIMIT))
    # Second exponential term,  shall be used for function and derivative calculation
    second_exp_term = np.exp(np.clip(bias * estimated_guess, None, LIMIT))
    
    # Storing the function, to be used for the next estimated guess calculation
    function_output =  first_exp_term - second_exp_term - 1     
    # Storing the prime value, to be used for the next estimated guess calculation
    derivative_output = potential_difference * first_exp_term - bias *  second_exp_term    
    
    # If the derivative calculation output is 0, returning 0 to trigger TypeError,
    # since the output will be used as a denominator.
    if derivative_output == 0:
        return 0
    
    return function_output, derivative_output


def get_electron_temperature(parameters):

    
    """This function calculates electron temperature in electron volts and Joules.
    
    The Newton-Raphson method has been deployed to calculte the inverse value of the temperature.
    
    The loop runs 100 iterations unless a value has been approximated, with a tolerance of 1e-5.
    """
    
    potential_difference = parameters['Potential difference']
    
    bias =  parameters['Bias 1']
    if bias and potential_difference:
        
        # Storing the counter, shall be used to know the number of iterations
        counter = 0
        
        # Variable storing the previous guess at the beginning of each iteration
        previous_guess = 0
       
        # Storing initial guess for Newton-Raphson approximation iterations
        estimated_guess = np.log(2) / (bias - potential_difference)
        
        # The Newton-Raphson approximation iterations occur in this while loop
        while abs(estimated_guess - previous_guess) > TOLERANCE:
            
            # Storing previous guess, to compare with the final value of each iteration
            previous_guess = estimated_guess
            
            # Try/except clause to verify if the derivative is not 0.
            # If derivative == 0, exiting function
            try:
                
                function_output, derivative_output = iteration(potential_difference, 
                                                               bias,
                                                               estimated_guess)
            except TypeError:
                # Storing the electron temperature in eV  as np.nan
                parameters['Electron temperature (eV)'] = np.nan
                
                # Storing the electron temperature in Joules  as np.nan
                parameters['Electron temperature (Joules)'] = np.nan
                print( 'No Solution Found.')
                # Exiting function
                return
            
            # Storing the next estimated value
            estimated_guess = (estimated_guess - function_output / derivative_output)
            
            counter +=1
            
        if counter ==NUMBER_OF_ITERATIONS:
            
            # Storing the electron temperature as np.nan
            parameters['Electron temperature (eV)'] = np.nan
            
            # Storing the electron temperature in Joules as np.nan
            parameters['Electron temperature (Joules)'] = np.nan
            
            print( f'After {counter} iterations, no accurate value has been yielded.')
            
            # Exiting function
            return
        
        # Storing the electron temperature in eV
        parameters['Electron temperature (eV)'] = 1/estimated_guess
        
        # Storing the electron temperature in Joules
        parameters['Electron temperature (Joules)'] = ELECTRON_CHARGE *  parameters['Electron temperature (eV)']


def get_electron_density(parameters):
    
    """This method yields electron density in particles per cubic meter."""
    if np.isnan(parameters['Electron temperature (Joules)']):
        parameters['Electron density (m-3)'] = np.nan
        return
    # Configuration object stored, in order to get 'Probe Area'
    config_object = parameters['config_ref']
    probe_area = config_object['Probe area']
    ion_mass =  config_object['Particle mass']
    
    # Storing the electron temperature in Joules, to be used in calculations
    electron_temperature =  parameters['Electron temperature (Joules)']
    
    # Exponential term found in equation
    exponential_term=  np.exp(abs(ELECTRON_CHARGE *  parameters['Potential difference'] / \
                                  electron_temperature))
                                 
    # Since the density formula is composed of a division, yielding the numerator and denominator
    numerator_of_equation= abs( parameters['Filtered current (Amperes)']  * exponential_term)
    
    denominator_of_equation = abs(0.61 * probe_area * ELECTRON_CHARGE * \
                                  np.sqrt(electron_temperature / ion_mass) * \
                                 (1 - exponential_term))
    
    # Storing electron density
    parameters['Electron density (m-3)'] = numerator_of_equation / denominator_of_equation
    
def get_display_parameters(parameters):
    
    """This function returns a ProtectedDictionary object containing the parameters used for display.
    
    Intended for all probe parameters."""
    display_parameters = []
    display_parameters.append(parameters['Electron temperature (eV)'])
    display_parameters.append(parameters['Electron temperature (Joules)'])
    display_parameters.append(parameters['Electron density (m-3)'])

    return display_parameters

def get_equations():
    
    """This function returns a reference to the equations"""
    
    list_of_references = []
    list_of_references.append(filter_current)
    list_of_references.append(get_electron_temperature)
    list_of_references.append(get_electron_density)
    list_of_references.append(get_display_parameters)

    return list_of_references


""" sample usage of the equations"""    
if __name__ == "__main__": 

    
    # Parameter dictionary, stores parameters
    parameters= {}
    
    # Storing bias, measured current, and measured voltage to test the implementation.
    parameters['Bias 1'], parameters['Potential difference'] =  40, 32
    get_electron_temperature(parameters)
    print(parameters)
    parameters['Raw voltage 1']= [34.4 for i in range(1,10)]
    parameters['Raw voltage 2'] =  [0.005176711239483604 for i in range(1,10)]
    # Storing Probe area of a previous implementation, and ion mass of Argon in kg, simulating config values
    parameters['config_ref'] = {'Probe area' : 30.3858e-06, 'Particle mass':  6.629e-26, 'up_shunt': 1}
    
    
    # Running each equation
    list_of_equations = get_equations()
   
    for i in list_of_equations[:len(list_of_equations)-1]:
        i(parameters)
    
    # Requires protected_dictionary to be loaded in memory
    parameters_to_display = list_of_equations[-1](parameters)
    
    for i in parameters_to_display: 
        print(i)
