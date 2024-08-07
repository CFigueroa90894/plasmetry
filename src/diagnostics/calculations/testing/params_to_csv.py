# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 13:23:17 2024

@author: ajco2
"""
import calculate_parameters as slp
import csv
#from sweep_parser import SweepParser as parser
# Save a separate CSV for plasma parameters
def ParametersToCsv(listOfParameters, fname):
   keys = list(listOfParameters[0].keys())
   

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
    list_of_sweeps = []
    bias, current = LoadPreviousData()
    sweep_list.append(current)
    sweep_list.append(bias)
    list_of_sweeps.append(sweep_list)
    
    print(sweep_list)
    parameter_list = slp.get_sweeps_parameters(list_of_sweeps)
    filename = 'slp parameters from test.csv'
    ParametersToCsv(parameter_list, filename)
    print(parameter_list)
    
    
main()




