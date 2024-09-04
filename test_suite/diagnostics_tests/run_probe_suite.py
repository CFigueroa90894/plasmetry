# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 12:44:30 2024

@author: ajco2
"""
import unittest
import numpy as np

import sys 
import os
sys.path.insert(0, os.path.abspath('Probe test cases'))
from SLPTestCases import SLPTestCases

class OrderedTestLoader(unittest.TestLoader):
    
    def getTestCaseNames(self, testCaseClass):
        # Overriding to return tests in the order they appear in the probe testcases script
        test_names = super().getTestCaseNames(testCaseClass)
        return test_names

def LoadPreviousData():
    
    """Function to load data from previous implementation. Code developed by Felix Cuadrado"""
    
    import csv as csv_library
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




def run_test_suite(probe_test_cases):
    
    loader = OrderedTestLoader()
    
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(probe_test_cases))
        
    runner = unittest.TextTestRunner(verbosity=2)
    
    runner.run(suite)


if __name__ == '__main__':
    
    # Storing bias and raw current lists from previous implementation
    bias, raw_current =  LoadPreviousData()
    SLPTestCases.set_parameters(raw_current, bias)
    run_test_suite(SLPTestCases)
