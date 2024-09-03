import numpy as np 
from global_parameters import get_particle_density

# Storing the charge of the electron particle, since it shall be used for calculation
ELECTRON_CHARGE = 1.60217657e-19

# Declaring limit to avoid overflow when running np.exp
LIMIT = 500  

# Max number of iterations to be run when executing the Newton-Raphson algorithm
NUMBER_OF_ITERATIONS = 100

# Storing the tolerance for the Newton-Raphson approximation
TOLERANCE = 1e-5

# Storing initial guess for Newton-Raphson iterations
estimated_guess = 0.1


def filter_current(parameters):
    return 0


def iteration(parameters, estimated_guess):
    
    # First exponential term, shall be used for function and derivative calculation
    first_exp_term =  (parameters['Probe 1 filtered current'] - \
                       parameters['Probe 3 filtered current']) * \
                       np.exp(np.clip(parameters['Bias 1'] * estimated_guess, None, LIMIT))
     
    # Second exponential term,  shall be used for function and derivative calculation
    second_exp_term =(parameters['Probe 1 filtered current'] - \
                      parameters['Probe 2 filtered current']) * \
                      np.exp(np.clip(parameters['Bias 2'] * estimated_guess, None, LIMIT))
    
    
    # Storing the function, to be used for the next estimated guess calculation
    function_output =  first_exp_term - second_exp_term - \
                       parameters['Probe 2 filtered current'] + \
                       parameters['Probe 3 filtered current']
    
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
     
    The loop runs 100 iterations unless a value has been approximated, with a tolerance of 1e-5.
    """
    # Initial guess
    global estimated_guess 
    
    # Storing the counter, shall be used to know the number of iterations
    counter = 0
    
    # Variable storing the previous guess at the beginning of each iteration
    previous_guess = 0
   
    
    # The Newton-Raphson approximation iterations occur in this loop
    while abs(estimated_guess - previous_guess) > TOLERANCE and counter < NUMBER_OF_ITERATIONS:
        
        # Storing previous guess, to compare with the final value of each iteration
        previous_guess = estimated_guess
        
        # Try/except clause to verify if the derivative is not 0.
        # If derivative output is 0, exiting function
        try:
            function_output, derivative_output = iteration(parameters, estimated_guess)
            
        except TypeError:
            return 'No Solution Found.'
        
        # Storing the next estimated value
        estimated_guess = (estimated_guess - function_output/derivative_output)
        
        counter +=1
        
    if counter ==NUMBER_OF_ITERATIONS:
        
        return f'After {counter} iterations, no accurate value has been yielded.'
    
    # Storing the electron temperature in eV
    parameters['Electron temperature (eV)'] = 1 / estimated_guess
    
    # Storing the electron temperature in Joules
    parameters['Electron temperature (Joules)'] = ELECTRON_CHARGE * parameters['Electron temperature (eV)']


def get_electron_density(parameters):
    
    # Storing ion saturation current
    parameters['Particle saturation current'] = parameters['Probe 3 filtered current']
    
    # Calling global electron density function, which is deployed by SLP, HEA, and IEA
    get_particle_density(parameters)


def get_probe_current(parameters):
    parameters['Probe 1 filtered current'] = -1 * (parameters['Probe 3 filtered current'] + \
                                                 
                                                   parameters['Probe 2 filtered current'])
def get_equations(): 
    
    """ This function returns a list containing a reference to the equations."""
    
    list_of_references = []
    list_of_references.append(filter_current)
    list_of_references.append(get_probe_current)
    list_of_references.append(get_electron_temperature)
    list_of_references.append(get_electron_density)
    return list_of_references


