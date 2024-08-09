import numpy as np 

def iteration(potential_difference, bias, estimated_guess):
    
    
    #first exponential term, shall be used for function and derivative calculation
    first_exp_term = 2 *np.exp(potential_difference*estimated_guess)
    
    #second exponential term,  shall be used for function and derivative calculation
    second_exp_term = np.exp(bias *estimated_guess)
    
    #storing the function, to be used for the next estimated guess calculation
    function_output =  first_exp_term - second_exp_term - 1     
    
    #storing the prime value, to be used for the next estimated guess calculation
    derivative_output = potential_difference * first_exp_term - bias *  second_exp_term    
    
    #if result after the prime calculation is 0, returning 0 to trigger TypeError
    #since the value will be used as a denominator
    if derivative_output ==0:
        return 0
    return function_output, derivative_output

def electron_temperature(potential_difference, bias):
    '''
    This function deploys the Raphson-Newton method to calculate electron temperature in electron volts for the Triple Langmuir Probe in electron volts.
    
    The Raphson-Newton method has been deployed as a function of 1/electron temperature in electron volts
    '''

    #storing the charge of the electron particle, since it shall be used for calculation
    electron_charge = 1.60217657e-19
    #storing initial guess
    estimated_guess = 1
    #storing the counter, shall be used to know the number of iterations
    counter = 0
    #variable storing the previous guess at the beginning of each iteration
    previous_guess = 0

    while abs(estimated_guess - previous_guess)>1e-5 and counter <1000000:
        #storing previous guess, to compare with the final value of each iteration
        previous_guess =estimated_guess
        
        #try/except clause to verify if the derivative is not 0.
        #if derivative = 0, exiting function
        try:
            function_output, derivative_output = iteration(potential_difference, bias, estimated_guess)
        except TypeError:
            return 'No Solution Found.'
        
        #Storing the next estimated value
        estimated_guess = (estimated_guess - function_output/derivative_output)
        
        counter +=1
        
    #storing the electron temperature in eV
    electron_temperature_ev = 1/estimated_guess
    
    #storing the electron temperature in Joules
    electron_temperature_joules = electron_charge * electron_temperature_ev

    return  electron_temperature_ev, electron_temperature_joules

def electron_density(acquired_probe_current , potential_difference, electron_temperature_joules,  probe_area , ion_mass):
    electron_charge = 1.60217657e-19
    exponential_term=  np.exp(abs(electron_charge*potential_difference/electron_temperature_joules))
    numerator_of_equation= abs(acquired_probe_current * exponential_term)
    denominator_of_equation = abs(0.61 * probe_area *electron_charge * np.sqrt(electron_temperature_joules/ion_mass) * (1-exponential_term))
    electron_density = numerator_of_equation/denominator_of_equation
    return(electron_density)



#dummy bias
bias = 30
#dummy potential_difference
potential_difference = 23.7

electron_temperature_ev, electron_temperature_joules = electron_temperature(potential_difference,bias)

print (f'Electron temperature (eV):{electron_temperature_ev}')
print (f'Electron temperature (Joules):{electron_temperature_joules}')
#slp probe area in Felix's implementation
probe_area = 30.3858e-06
#hydrogen ion mass
ion_mass = 1.67e-27
#dummy acquired current
acquired_current = 0.1

print( 'electrons per cubic meter: ',electron_density(.01 , potential_difference, electron_temperature_joules, probe_area , ion_mass))
