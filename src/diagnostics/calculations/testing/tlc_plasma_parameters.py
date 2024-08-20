import numpy as np 
#storing the charge of the electron particle, since it shall be used for calculation
electron_charge = 1.60217657e-19
#storing initial guess for raphson-newton approximation iterations implemented for electron temperature calculation
estimated_guess = 0.1
 
number_of_iterations = 10000
def iteration(parameters, estimated_guess):
    #declaring limit to avoid overflow
    LIMIT = 500  
    
    #first exponential term, shall be used for function and derivative calculation
    first_exp_term =  (parameters['Probe 1 current'] -parameters['Probe 3 current'])* np.exp(np.clip(parameters['Bias 1']*estimated_guess, None, LIMIT))
    
    #second exponential term,  shall be used for function and derivative calculation
    second_exp_term =(parameters['Probe 1 current'] -parameters['Probe 2 current'])* np.exp(np.clip(parameters['Bias 2']*estimated_guess, None, LIMIT))
    
    
    #storing the function, to be used for the next estimated guess calculation
    function_output =  first_exp_term - second_exp_term -   parameters['Probe 2 current'] + parameters['Probe 3 current']  
    
    #storing the prime value, to be used for the next estimated guess calculation
    derivative_output = parameters['Bias 1'] * first_exp_term - parameters['Bias 2'] *  second_exp_term    
    
    #if result after the prime calculation is 0, returning 0 to trigger TypeError
    #since the value will be used as a denominator
    if derivative_output ==0:
        return 0
    return function_output, derivative_output

def get_electron_temperature(parameters):
    global estimated_guess 

    '''
    This function deploys the Raphson-Newton method to calculate electron temperature in electron volts for the Triple Langmuir Probe in electron volts.
    
    The Raphson-Newton method has been deployed as a function of 1/electron temperature in electron volts.
    
    The loop runs 1,000,000 iterations unless a value has been estimated, with an accuracy of 10^-5
    '''
    #storing the counter, shall be used to know the number of iterations
    counter = 0
    #variable storing the previous guess at the beginning of each iteration
    previous_guess = 0
   
    
    #the raphson-newton approximation iterations occur in this while loop
    while abs(estimated_guess - previous_guess)>1e-13 and counter <number_of_iterations:
        #storing previous guess, to compare with the final value of each iteration
        previous_guess =estimated_guess
        
        #try/except clause to verify if the derivative is not 0.
        #if derivative == 0, exiting function
        try:
            function_output, derivative_output = iteration(parameters, estimated_guess)
        except TypeError:
            return 'No Solution Found.'
        
        #Storing the next estimated value
        estimated_guess = (estimated_guess - function_output/derivative_output)
        
        counter +=1
        print(estimated_guess)
    if counter ==number_of_iterations:
        
        return f'After {counter} iterations, no accurate value has been yielded.'
    
    #storing the electron temperature in eV
    parameters['Electron temperature (eV)'] = 1/estimated_guess
    
    #storing the electron temperature in Joules
    parameters['Electron temperature (Joules)'] = electron_charge *  parameters['Electron temperature (eV)']


def get_electron_density(parameters):
 return 0
def get_equations():
    '''
    This function returns a reference to the equations
    '''
    list_of_references = []
    list_of_references.append(get_electron_temperature)
    list_of_references.append(get_electron_density)
    return list_of_references

