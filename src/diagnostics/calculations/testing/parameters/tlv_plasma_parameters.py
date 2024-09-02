import numpy as np 
# Storing the charge of the electron particle, since it shall be used for calculation
electron_charge = 1.60217657e-19

 
NUMBER_OF_ITERATIONS = 100

TOLERANCE = 1e-5


def iteration(potential_difference, bias, estimated_guess):
    
    """This function performs the function and derivative calculation process in each iteration.
    
       Returns the output of the expressions."""
    
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
    
    global estimated_guess 
    
    potential_difference = parameters['Potential difference']
    
    bias =  parameters['Bias']
    
    # Storing the counter, shall be used to know the number of iterations
    counter = 0
    
    # Variable storing the previous guess at the beginning of each iteration
    previous_guess = 0
   
    # Storing initial guess for Newton-Raphson approximation iterations
    estimated_guess = np.log(2) / (bias - potential_difference)
    
    # The Newton-Raphson approximation iterations occur in this while loop
    while abs(estimated_guess - previous_guess) > TOLERANCE and counter < NUMBER_OF_ITERATIONS:
        
        # Storing previous guess, to compare with the final value of each iteration
        previous_guess = estimated_guess
        
        # Try/except clause to verify if the derivative is not 0.
        # If derivative == 0, exiting function
        try:
            
            function_output, derivative_output = iteration(potential_difference, 
                                                           bias,
                                                           estimated_guess)
        except TypeError:
            return 'No Solution Found.'
        
        # Storing the next estimated value
        estimated_guess = (estimated_guess - function_output / derivative_output)
        
        counter +=1
        
    if counter ==NUMBER_OF_ITERATIONS:
        
        return f'After {counter} iterations, no accurate value has been yielded.'
    
    # Storing the electron temperature in eV
    parameters['Electron temperature (eV)'] = 1/estimated_guess
    
    # Storing the electron temperature in Joules
    parameters['Electron temperature (Joules)'] = electron_charge *  parameters['Electron temperature (eV)']


def get_electron_density(parameters):
    
    """This equation yields electron density in particles per cubic meter."""
    
    # Storing the electron temperature in Joules, to be used in calculations
    electron_temperature =  parameters['Electron temperature (Joules)']
    
    # Exponential term found in equation
    exponential_term=  np.exp(abs(electron_charge *  parameters['Potential difference'] / \
                                  electron_temperature))
                                 
    # Since the density formula is composed of a division, yielding the numerator and denominator
    numerator_of_equation= abs( parameters['Filtered current']  * exponential_term)
    
    denominator_of_equation = abs(0.61 * parameters['Probe area'] * electron_charge * \
                                  np.sqrt(electron_temperature / parameters['Ion mass']) * \
                                 (1 - exponential_term))
    
    # Storing electron density
    parameters['Electron density'] = numerator_of_equation / denominator_of_equation

def get_equations():
    
    """This function returns a reference to the equations"""
    list_of_references = []
    list_of_references.append(get_electron_temperature)
    list_of_references.append(get_electron_density)
    return list_of_references


""" sample usage of the equations"""    
if __name__ == "__main__": 

    
    # Parameter dictionary, stores parameters
    parameters= {}
    
    # Storing bias, measured current, and measured voltage to test the implementation.
    parameters['Bias'], parameters['Potential difference'] =  40, 32
    parameters['Filtered current'] =  0.005176711239483604
    
    # Probe area of a previous implementation
    parameters['Probe area'] =  30.3858e-06
    
    # Argon atomic mass mass in Kilograms
    parameters['Ion mass'] = 6.629e-26
    
    # Running each equation
    list_of_equations = get_equations()
    for i in list_of_equations:
        i(parameters)
        
    # Printing the parameters
    for key, value in parameters.items():
            print(key, ': ' ,value)
