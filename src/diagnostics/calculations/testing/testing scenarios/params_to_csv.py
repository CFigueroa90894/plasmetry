# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 13:23:17 2024

@author: ajco2
"""
import calculate_parameters as slp
import csv
from sweep_parser_v2 import SweepParser as parser
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
    
    filepath = 'Feliz_A1 MirorSLP120200813T105858.csv'
    list_of_sweeps = parser.parse_sweeps(filepath)
    parameter_list = slp.get_sweeps_parameters(list_of_sweeps)
    filename = 'slp parameters from test.csv'
    ParametersToCsv(parameter_list, filename)
   
    
    
main()




