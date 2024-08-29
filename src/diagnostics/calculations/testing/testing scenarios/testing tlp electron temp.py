# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 15:26:51 2024

@author: ajco2
"""

import numpy as np 
import matplotlib.pyplot as plt
#storing the charge of the electron particle, since it shall be used for calculation
electron_charge = 1.60217657e-19
 

number_of_iterations = 100
def iteration(potential_difference, bias, estimated_guess):
    #declaring limit to avoid overflow
    LIMIT = 500  
    
    #first exponential term, shall be used for function and derivative calculation
    first_exp_term = 2 *np.exp(np.clip(potential_difference*estimated_guess, None, LIMIT))
    
    #second exponential term,  shall be used for function and derivative calculation
    second_exp_term = np.exp(np.clip(bias*estimated_guess, None, LIMIT))
    
    #storing the function, to be used for the next estimated guess calculation
    function_output =  first_exp_term - second_exp_term - 1     
    
    #storing the prime value, to be used for the next estimated guess calculation
    derivative_output = potential_difference * first_exp_term - bias *  second_exp_term    
    
    #if result after the prime calculation is 0, returning 0 to trigger TypeError
    #since the value will be used as a denominator
    if derivative_output ==0:
        return 0
    return function_output, derivative_output

def get_electron_temperature(parameters):
   global estimated_guess 
   parameters['Electron temperature (eV)'] = []
   parameters['Iterations'] = []
   for i in parameters['Potential difference']:
    bias =  parameters['Bias']
    '''
    This function deploys the Raphson-Newton method to calculate electron temperature in electron volts for the Triple Langmuir Probe in electron volts.
    
    The Raphson-Newton method has been deployed as a function of 1/electron temperature in electron volts.
    
    The loop runs 1,000,000 iterations unless a value has been estimated, with an accuracy of 10^-5
    '''
    #storing the counter, shall be used to know the number of iterations
    counter = 0
    #variable storing the previous guess at the beginning of each iteration
    previous_guess = 0
    
    #storing initial guess for raphson-newton approximation iterations implemented for electron temperature calculation
    estimated_guess = 1/(parameters['Bias']-i)/np.log(2)
    #the raphson-newton approximation iterations occur in this while loop
    while abs(estimated_guess - previous_guess)>1e-4 and counter <number_of_iterations:
        #storing previous guess, to compare with the final value of each iteration
        previous_guess =estimated_guess
        
        #try/except clause to verify if the derivative is not 0.
        #if derivative == 0, exiting function
        try:
            function_output, derivative_output = iteration(i, bias, estimated_guess)
        except ValueError:
            return 'No Solution Found.'
        
        #Storing the next estimated value
        estimated_guess = (estimated_guess - function_output/derivative_output)
        
        counter +=1
      
    if counter ==number_of_iterations:
        
        return f'After {counter} iterations, no accurate value has been yielded.'
    
    #storing the electron temperature in eV
    parameters['Electron temperature (eV)'].append( 1/estimated_guess)
    parameters['Iterations'].append(counter)
    #storing the electron temperature in Joules
    #parameters['Electron temperature (Joules)'] = electron_charge *  parameters['Electron temperature (eV)']
parameters = {}
#applied bias, fixed
max_voltage = 50

#generating different measured voltages, to show how temperature calculations and number of iterations changes for each case.
#each generated voltage shall be  an integer between 1 to n-1, where n is the applied voltage
parameters['Potential difference'] = list(range(1, max_voltage))

#setting applied bias as parameter for calculations
parameters['Bias'] = max_voltage

#calculating electron temperature for each generated voltage
get_electron_temperature(parameters)

#bias - generated voltages, used to demonstrate that the difference between the applied bias and  potential difference influences in the electron temperature calculated for each instance
#regardless of the applied bias, as long as the bias and potential difference are much greater than the temperature that is being measured. This will be discussed in the SDD
parameters['bias - potential difference'] = [parameters['Bias']- a  for a in parameters['Potential difference']]

#printing the difference, acquired temperature and number of iterations to acquire the temperature
for i, j, k in zip( parameters['bias - potential difference'], parameters['Electron temperature (eV)'], parameters['Iterations']):
    print(f"difference {i} : temperature {j}, iterations = {k}")

#plotting the results of measured voltage vs acquired temperature for all instances
plt.figure(figsize=(10, 5)) 


plt.plot(parameters['Potential difference'], parameters['Electron temperature (eV)'], marker='o', linestyle='-', color='b')

plt.title('Differential Voltage vs. Electron Temperature')

plt.xlabel('Measured Voltage (V)')

plt.ylabel('Electron Temperature (eV)')

plt.grid()

plt.show()


