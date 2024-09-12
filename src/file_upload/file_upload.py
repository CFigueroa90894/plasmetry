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

import csv
from data_formating import process_data

class FileUpload:
      
    def __init__(self, local_path, unformatted_data='', credentials_path=''):
        
        """FileUpload construtor"""
        
        if unformatted_data:
            # Storing unformatted parameters dictionary
            self.sweep_data, self.calculated_parameters = process_data(unformatted_data)
            
        self.local_path = local_path
        self.offsite_credentials = credentials_path
                
    def new_upload(self, parameters):
        
        """"""
        
        # Storing unformatted parameters dictionary
        self.sweep_data, self.calculated_parameters = process_data(parameters)
    
    def local_upload(self):
        
        """"""
        
        time_stamp = 2
        self.local_path = self.local_path + ' testing ' + str(time_stamp)
        self.local_file_write(self.calculated_parameters, self.local_path + ' parameters.csv' )
        if  self.sweep_data: 
            self.local_file_write(self.sweep_data, self.local_path + ' sweeps data.csv')
        
    def local_file_write(self, data, path_name):
        
        """"""

        keys = list(data[0].keys())
        with open(path_name, "w", newline='') as csv_file:
            dict_writer= csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    
""" Sample usage of the equations and local file upload. """    
if __name__ == "__main__": 
    
    import numpy as np
    from slp_plasma_parameters import get_equations
    
    
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
    
    
    list_of_parameters = []
        
    parameters = set_params()
    
    list_of_parameters.append(calc_params(parameters))
    
    parameters = set_params()
    
    list_of_parameters.append(calc_params(parameters))
        
    upload_object = FileUpload('testing path/', list_of_parameters)
    upload_object.local_upload()
    
 
        
        
        
        
        