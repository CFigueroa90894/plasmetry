import unittest
import sys 
import os
sys.path.insert(0, os.path.abspath('Probe test cases'))
from GlobalTestCases import GlobalTestCases
sys.path.insert(0, os.path.abspath('parameters'))
from global_parameters import get_equations



def generate_suite(equations, probe_test_cases):

    suite = unittest.TestSuite()

    test_loader = unittest.TestLoader()

    all_test_cases = test_loader.loadTestsFromTestCase(probe_test_cases)

    equation_names = {eq.__name__ for eq in equations}

    for test_case in all_test_cases:
        for eq in equation_names:  
          if eq in test_case._testMethodName:
           suite.addTest(probe_test_cases(test_case._testMethodName))

    return suite


    
def run_test_suite(suite):
    
        
    runner = unittest.TextTestRunner(verbosity=2)
    
    runner.run(suite)


if __name__ == '__main__':
    
    """SLP test cases sample run"""
    
    def LoadPreviousData():
        
        """Function to load data from previous implementation. Code developed by Felix Cuadrado"""
        
        import csv as csv_library
        import numpy as np
        
        with open('initial data for test cases/Feliz_A1 MirorSLP120200813T105858.csv', newline='') as csv:
            dataReader = csv_library.reader(csv, delimiter=',', quotechar='|')
            next(dataReader)  # Skip the header row
            current = []
            voltageSLP = []
            for row in dataReader:
                try:
                    current = np.append(current, float(row[0]))
                    voltageSLP = np.append(voltageSLP, float(row[1]))
                except:
                    None    
            
            return voltageSLP, current

    
    # Storing bias and raw current lists from previous implementation
    bias, raw_current =  LoadPreviousData()
    GlobalTestCases.set_parameters(raw_current, bias)
    suite=  generate_suite(get_equations(), GlobalTestCases)
    run_test_suite(suite)
