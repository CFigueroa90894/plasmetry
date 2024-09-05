import unittest
import sys 
import os
sys.path.insert(0, os.path.abspath('Probe test cases'))
from GlobalTestCases import GlobalTestCases


def generate_suite(equations, probe_test_cases):
    """This function returns am instantiated TestSuite object. 
    
    The suite contains the tests to be extracted from the GlobalTestCases class"""
    
    # Instantiating TestSuite object
    suite = unittest.TestSuite()
    
    # Instantiating loader
    test_loader = unittest.TestLoader()
    
    # Loading every test case from GlobalTestCases
    all_test_cases = test_loader.loadTestsFromTestCase(probe_test_cases)
    
    # Nested for loops, going through each test case and method reference
    # If the methdod name characters are in test case method name, aggregating
    # the equation to the suite
    for test_case in all_test_cases:
        for eq in equations:  
          if eq.__name__ in test_case._testMethodName:
              suite.addTest(probe_test_cases(test_case._testMethodName))
              break

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
    
    # Simply change from where the equations are imported, the config values, and raw data to test other probe equations
    sys.path.insert(0, os.path.abspath('parameters'))
    from dlp_plasma_parameters import get_equations
    
    # Storing bias and raw current lists from previous implementation
    # For slp, dlp, or EA testing, may use this data, only must change particle mass
    bias, raw_current =  LoadPreviousData()
    
    parameters = {'Bias': bias, 'Raw current': raw_current}
    parameters['config_ref'] = {'Probe area' : 30.3858e-06, 'Particle mass':  9.10938356e-31}

    # Setting the GlobalTestCases paramaters atribute 
    GlobalTestCases.set_parameters(parameters)
    
    # Generating test suite with test cases
    suite = generate_suite(get_equations(), GlobalTestCases)
    
    # Running the test suite
    run_test_suite(suite)
