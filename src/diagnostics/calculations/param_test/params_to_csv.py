# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 13:23:17 2024

@author: ajco2
"""
import calculate_parameters as slp
import csv
import sweep_parser as parser
# Save a separate CSV for plasma parameters
def ParametersToCsv(listOfParameters, fname):
   
   keys = list(listOfParameters[0].keys())
   
   for row in listOfParameters:
       row['vP'] = row['vP'][0]
       row['vF'] = row['vF'][0]
   with open( fname, "w", newline='') as csv_file:
       dict_writer= csv.DictWriter(csv_file, keys)
       dict_writer.writeheader()
       dict_writer.writerows(listOfParameters)

def LoadPreviousData():
    with open('Feliz_A1 MirorSLP120200813T105858.csv', newline='') as csvfile:
        dataReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(dataReader)  # Skip the header row
        current = []
        voltageSLP = []
        for row in dataReader:
            try:
                current.append(float(row[0]))
                voltageSLP.append(float(row[1]))
            except:
                None    
        
        return voltageSLP, current

def main():
    sweep_list = []
    bias, current = LoadPreviousData()
    sweep_list.append(current)
    sweep_list.append(bias)
    
    parameter_list = slp.get_sweeps_parameters(sweep_list)
    filename = 'slp parameters from test.csv'
    #slp.ParametersToCsv(parameter_list, filename)
    print(parameter_list)
    
    
main()




