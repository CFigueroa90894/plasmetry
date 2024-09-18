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


   parameters['Electron temperature (eV)'] = []
   
   parameters['Iterations'] = []
   
   
   for i in parameters['Potential difference']:
    bias =  parameters['Bias']
    #storing the counter, shall be used to know the number of iterations
    counter = 0
    #variable storing the previous guess at the beginning of each iteration
    previous_guess = 0
    
    #storing initial guess for raphson-newton approximation iterations implemented for electron temperature calculation
    #initial guess is 1/x
    estimated_guess =np.log(2)/ (parameters['Bias']-i)
    #the raphson-newton approximation iterations occur in this while loop
    while abs(estimated_guess - previous_guess)>1e-5 and counter <number_of_iterations:
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

# Storing biases with a value of 10V to 2000V, in a factor of 2. 
max_voltages = list(range(10, 2000, 2))

# List for parameter dictionaries
results = []

# Number of cases tested
number_of_cases= 0

#for every generated bias: 
for max_voltage in max_voltages:
    
    
    # Storing parameters in a dictionary
    parameters = {}
    
    # Verifying bias value to see how to set potential difference, done since at case with 10 applied bias, 
    # The measured voltage is impossible to be below 4 
    if max_voltage==10:
        minumum_measured = max_voltage - 6
    else: 
        # For the rest of the cases, keeping the measured voltage at 1 to showcase how it behaves
        minumum_measured = 1
    
    # Storing measured voltages in parameters dictioanry, from 1 to n-1, n being the applied bias
    parameters['Potential difference'] = list(range(minumum_measured, max_voltage))
    
    number_of_cases+=len(parameters['Potential difference'])
    
    # Storing value for applied bias in parameters dictionary
    parameters['Bias'] = max_voltage
   
    # Calculating electron temperature for each potential difference 
    get_electron_temperature(parameters)
    
    # Storing info about the results
    parameters['bias - potential difference'] = [parameters['Bias'] - a  for a in parameters['Potential difference']]
    parameters['Average number of iterations'] = round(np.sum(parameters['Iterations'])/len(parameters['Iterations']))
    parameters['number of missing measurements'] = len(parameters['Potential difference']) - len(parameters['Electron temperature (eV)'])
    
    # Storing the info in a parameter csv, this is done for each applied bias, since we are still in the loop. 
    ParametersToCsv(parameters, 'different test cases results per applied bias/' + str(max_voltage)+'_bias_testing_tlp_.csv')
    results.append(parameters)


print(f'number of cases tested: {number_of_cases}') 

consolidated_parameters(results, str(number_of_cases) + '_cases_consolidated test.csv') 

missing = 0    
unique_biases = 0
list_of_biases = []

for i in results:
    #if any electron temperature outputs are missing in the results, storing info of applied bias. 
    missing += i['number of missing measurements']
    if missing!= 0:
        list_of_biases.append((i['Bias'], i['number of missing measurements']))
        unique_biases +=1
        

print(f'Number of missing temperatures: {missing} \n\nNumber of unique biases with missing temperatures: {unique_biases}, \n\nBias applied and number of missing temperatures: {list_of_biases}')