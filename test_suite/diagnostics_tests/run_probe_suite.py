import sys 
import os

# ----- PATH HAMMER 2 v1.0 ----- resolve absolute imports for test_suite ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 1    # how many parent folders to reach /plasmetry/test_suite

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
   # print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'test_suite'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    #print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #

import unittest
from slp_plasma_parameters import get_equations
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
    
    # Nested loops, going through each test case and method reference
    # If the methdod name characters are in test case method name, aggregating
    # the test case method to the suite
    for test_case in all_test_cases:
        for eq in equations:  
          if eq.__name__ in test_case._testMethodName:
              suite.addTest(probe_test_cases(test_case._testMethodName))
              break

    return suite

    
def run_test_suite(suite):
    
    """THis function runs the test cases in the test suite."""
    
    # Instantiating TextTestRunner object with enough verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Running the test cases in the suite
    runner.run(suite)


if __name__ == '__main__':
    
    """SLP test cases sample run."""
    
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
    # For slp, dlp, or EA testing, may use this data to test the parameter methods.
    # Only must change particle mass and the imported equations reference
    bias, raw_current =  LoadPreviousData()
    
    parameters = {'Bias': bias, 'Raw current': raw_current}
    parameters['config_ref'] = {'Probe area' : 30.3858e-06, 'Particle mass':  9.10938356e-31}

    # Setting the GlobalTestCases paramaters atribute 
    GlobalTestCases.set_probe_type(get_equations(), parameters)
    
    # Generating test suite with test cases
    suite = generate_suite(get_equations(), GlobalTestCases)
    
    # Invoking run_test_suite with the test cases as an argument
    run_test_suite(suite)
