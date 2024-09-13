import os
import sys

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 1           # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
   # print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #


import numpy as np
from slp_plasma_parameters import get_equations
from file_upload import FileUpload

def LoadPreviousData():
    
    """Function to load data from previous implementation. Code developed by Felix Cuadrado"""
    
    import csv as csv_library
    with open('Feliz_A1 MirorSLP120200813T105858.csv', newline='') as csv:
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
    
def set_params():
    # Parameter dictionary, stores parameters
    parameters= {}
    
    # Storing bias and raw current lists from previous implementation
    parameters['Bias 1'], parameters['Raw voltage 1'] =  LoadPreviousData()
    
    # Storing Probe area of a previous implementation, and ion mass in kg of argon, 
    # simulating config values
    parameters['config_ref'] = {'Probe area' : 30.3858e-06, 'Particle mass': 6.629e-26, 'Shunt 1': 1}
    return parameters


def calc_params(parameters):
    # Running each equation
    list_of_equations = get_equations()
    
    for i in list_of_equations[:len(list_of_equations)-1]:
        i(parameters)
        
    return parameters

""" Sample usage of the equations and file upload. """    
if __name__ == "__main__": 
    
    
    LOCAL_PATH = 'testing path/testing '
    CREDENTIALS = 'credentials/plasma-software-data-upload-d6f40f4fefdc.json'
    NUMBER_OF_SWEEPS = 3
    
    list_of_parameters = []
    
    for i in range(NUMBER_OF_SWEEPS):
    
        parameters = set_params()
    
        list_of_parameters.append(calc_params(parameters))

    
    
    upload_object = FileUpload(LOCAL_PATH, CREDENTIALS , list_of_parameters)
    
    upload_object.upload_data()
    
    print('data uploaded locally and in google drive')
    
