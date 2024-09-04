import unittest
import sys 
import os
sys.path.insert(0, os.path.abspath('Probe test cases'))
from SLPTestCases import SLPTestCases
    

def run_test_suite(probe_test_cases):
    
    suite = unittest.TestSuite()
    
    test_loader = unittest.TestLoader()
    
    suite.addTests(test_loader.loadTestsFromTestCase(probe_test_cases))
        
    runner = unittest.TextTestRunner(verbosity=2)
    
    runner.run(suite)


if __name__ == '__main__':
    
    """SLP sample run"""
    
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
    SLPTestCases.set_parameters(raw_current, bias)
    run_test_suite(SLPTestCases)
