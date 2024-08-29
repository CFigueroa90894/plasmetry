# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 15:26:51 2024

@author: ajco2
"""

import numpy as np 
import csv
#storing the charge of the electron particle, since it shall be used for calculation
electron_charge = 1.60217657e-19


number_of_iterations = 20
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
    #initial guess is 1/x
    estimated_guess =np.log(2)/ (parameters['Bias']-i)
    #the raphson-newton approximation iterations occur in this while loop
    while abs(estimated_guess - previous_guess)>1e-6 and counter <number_of_iterations:
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
def ParametersToCsv(parameters_dict, fname):
    lists = {key: value for key, value in parameters_dict.items() if isinstance(value, list)}

    with open(fname, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        writer.writerow(lists.keys())
        
        max_length = max(len(lst) for lst in lists.values())
        
        for i in range(max_length):
            row = []  
            for lst in lists.values():
                row.append(lst[i] if i < len(lst) else "")
            writer.writerow(row)
            
def consolidated_parameters(listOfParameters, fname):
   keys = listOfParameters[0].keys()
   

   with open( fname, "w", newline='') as csv_file:
       dict_writer= csv.DictWriter(csv_file, keys)
       dict_writer.writeheader()
       dict_writer.writerows(listOfParameters)
       
max_voltages = list(range(10, 300, 5))

results = []

for max_voltage in max_voltages:
    parameters = {}
    if max_voltage==10:
        minumum_measured = max_voltage - 6
    
    else: 
        minumum_measured = max_voltage-14
    parameters['Potential difference'] = list(range(minumum_measured, max_voltage))
    parameters['Bias'] = max_voltage
    get_electron_temperature(parameters)
    parameters['bias - potential difference'] = [parameters['Bias']- a  for a in parameters['Potential difference']]
    
    ParametersToCsv(parameters, str(max_voltage)+'_bias_testing_tlp_.csv')
    results.append(parameters)


consolidated_parameters(results, 'consolidated bias tested.csv') 
    
    
    
