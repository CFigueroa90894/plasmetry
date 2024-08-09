import numpy as np 

def electron_temperature(potential_difference, bias):
    #storing the charge of the electron particle, since it shall be used for calculation
    electron_charge = 1.60217657e-19
    #storing initial guess
    estimated_guess = 0.1
    #storing the counter, shall be used to know the number of iterations
    counter = 0
    #variable storing the previous guess at the beginning of each iteration
    previous_guess = 0

    while abs(estimated_guess - previous_guess)>1e-6 and counter <1000000:
        #storing previous guess, to compare with the final value of each iteration
        previous_guess =estimated_guess
        
        #first exponential term, shall be used for function and derivative calculation
        first_exp_term = 2 *np.exp(potential_difference*estimated_guess)
        
        #second exponential term,  shall be used for function and derivative calculation
        second_exp_term = np.exp(bias *estimated_guess)
        
        #storing the function, to be used for the next estimated guess calculation
        function_output =  first_exp_term - second_exp_term - 1     
        
        #storing the prime value, to be used for the next estimated guess calculation
        derivative_output = potential_difference * first_exp_term - bias *  second_exp_term    
        
        #if result after the prime calculation is 0, exiting the function, since the value will be used as a denominator
        if derivative_output ==0:
            return 'No solution found.'
        
        #estimating the next guess
        estimated_guess = (estimated_guess - function_output/derivative_output)
        
        #counting the iteration number
        counter +=1
        
    #storing the electron temperature in eV 
    electron_temperature_ev = 1/estimated_guess
    
    #storing the electron temperature in Joules 
    electron_temperature_joules = electron_charge * electron_temperature_ev
    
    print(f'Coverged after {counter} iterations. The estimated temperature is:\n\
{electron_temperature_ev} eV\n{electron_temperature_joules} Joules')    

    return  electron_temperature_ev, electron_temperature_joules

#def electron_density(electron_saturation_current, electron_temperature_joules, probe_area, particle_mass):
    

electron_temperature(23,30)
