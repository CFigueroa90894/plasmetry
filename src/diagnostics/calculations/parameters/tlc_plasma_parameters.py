import numpy as np 


# Storing the charge of the electron particle, since it shall be used for calculation
ELECTRON_CHARGE = 1.60217657e-19

# Declaring limit to avoid overflow when running np.exp
LIMIT = 500  

# Max number of iterations to be run when executing the Newton-Raphson algorithm
NUMBER_OF_ITERATIONS = 100

# Storing the tolerance for the Newton-Raphson approximation
TOLERANCE = 1e-5



def filter_current(parameters):
    
    parameters['Probe 2 filtered current (Amperes)'] = (np.sum(parameters['Raw voltage 1']) / len(parameters['Raw voltage 1']))/ parameters['config_ref']['up_shunt']
    parameters['Probe 3 filtered current (Amperes)'] = (np.sum(parameters['Raw voltage 2']) / len(parameters['Raw voltage 2']))/ parameters['config_ref']['down_shunt']
    parameters['Raw voltage 1'] = parameters['Raw voltage 1'][-1]
    parameters['Raw voltage 2'] = parameters['Raw voltage 2'][-1]

def iteration(parameters, estimated_guess):
    
    # First exponential term, shall be used for function and derivative calculation
    first_exp_term =  (parameters['Probe 1 filtered current (Amperes)'] - \
                       parameters['Probe 3 filtered current (Amperes)']) * \
                       np.exp(np.clip(  parameters['Bias 1'] *estimated_guess, None, LIMIT))
    # Second exponential term,  shall be used for function and derivative calculation
    second_exp_term =(parameters['Probe 1 filtered current (Amperes)'] - \
                      parameters['Probe 2 filtered current (Amperes)']) * \
                      np.exp(np.clip(  parameters['Bias 2'] *estimated_guess, None, LIMIT))
    
   
    

    # Storing the function, to be used for the next estimated guess calculation
    function_output =  first_exp_term - second_exp_term - \
                       parameters['Probe 2 filtered current (Amperes)'] + \
                       parameters['Probe 3 filtered current (Amperes)']
    
    # Storing the prime value, to be used for the next estimated guess calculation
    derivative_output = parameters['Bias 1'] * first_exp_term - \
                        parameters['Bias 2'] * second_exp_term    
    # If result after the prime calculation is 0, returning 0 to trigger TypeError
    # Since the value will be used as a denominator
    if derivative_output ==0:
        return 0
    return function_output, derivative_output


def get_electron_temperature(parameters):
    
    """This function calculates electron temperature in electron volts and Joules.
     
    The Newton-Raphson method has been deployed to calculte the inverse value of the temperature.
     
    The loop runs 100 iterations unless a value has been approximated, with a base tolerance of 1e-5.
    """
    
    # Initial guess
    
    # Storing the counter, shall be used to know the number of iterations
    counter = 0
    
    # Variable storing the previous guess at the beginning of each iteration
    previous_guess = 0
    
    # Initial guess
    estimated_guess =0.1
    
    # The Newton-Raphson approximation iterations occur in this loop
    while abs(estimated_guess - previous_guess) > TOLERANCE and counter < NUMBER_OF_ITERATIONS:
        
        # Storing previous guess, to compare with the final value of each iteration
        previous_guess = estimated_guess
        
        # Try/except clause to verify if the derivative is not 0.
        # If derivative output is 0, exiting function
        try:
            function_output, derivative_output = iteration(parameters, estimated_guess)
            
        except TypeError:
            # Storing the electron temperature in eV  as np.nan
            parameters['Electron temperature (eV)'] = np.nan
            
            # Storing the electron temperature in Joules  as np.nan
            parameters['Electron temperature (Joules)'] = np.nan
            print( 'No Solution Found.')
            # Exiting function
            return
        
        # Storing the next estimated value
        estimated_guess = (estimated_guess - function_output/derivative_output)
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
    parameters['Electron temperature (eV)'] = 1 / estimated_guess
    
    # Storing the electron temperature in Joules
    parameters['Electron temperature (Joules)'] = ELECTRON_CHARGE * parameters['Electron temperature (eV)']

def get_electron_density(parameters):
    
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
 



def get_probe_current(parameters):
    "This function returns "
    parameters['Probe 1 filtered current (Amperes)'] = -1 * (parameters['Probe 3 filtered current (Amperes)'] + \
                                                 
                                                   parameters['Probe 2 filtered current (Amperes)'])
    parameters['Ion saturation current (Amperes)']=  parameters['Probe 2 filtered current (Amperes)']
def get_display_parameters(parameters):
    
    """This function returns a list object containing the parameters used for display.
    
    Intended for all probe parameters."""
    display_parameters = []
    display_parameters.append(parameters['Ion saturation current (Amperes)'])
    display_parameters.append(parameters['Electron temperature (eV)'])
    display_parameters.append(parameters['Electron temperature (Joules)'])
    display_parameters.append(parameters['Electron density (m-3)'])

    return display_parameters

def get_equations(): 
    
    """ This function returns a list containing a reference to the equations."""
    
    list_of_references = []
    list_of_references.append(filter_current)
    list_of_references.append(get_probe_current)
    list_of_references.append(get_electron_temperature)
    list_of_references.append(get_electron_density)
    list_of_references.append(get_display_parameters)

    return list_of_references


if __name__ == "__main__": 

    
    # Parameter dictionary, stores parameters
    parameters= {}
    
    # Storing bias, measured current, and measured voltage to test the implementation.
    parameters['Bias 1'], parameters['Bias 2'] =  1, 1
    parameters['Probe 3 filtered current (Amperes)'] = 0
    parameters['Probe 2 filtered current (Amperes)'] = -1
    parameters['Bias 1']= 60
    parameters['Bias 2'] = 50
    
    # Storing Probe area of a previous implementation, and ion mass of Argon in kg, simulating config values
    parameters['config_ref'] = {'Probe area' : 30.3858e-06, 'Particle mass':  6.629e-26, 'up_shunt': 1, 'down_shunt':1}
    
    
    # Running each equation
    list_of_equations = get_equations()
   
    for i in list_of_equations[1:len(list_of_equations)-1]:
        i(parameters)
    print(parameters)
    # Requires protected_dictionary to be loaded in memory
    parameters_to_display = list_of_equations[-1](parameters)
    print(f'Ion Saturation Current (Amperes): {parameters_to_display[0]}')
 