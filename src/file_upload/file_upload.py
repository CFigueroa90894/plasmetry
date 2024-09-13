
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
from datetime import datetime

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
        
    def upload_data(self):
        
        """"""
        current_datetime = datetime.now()
        self.local_upload(current_datetime)
            
    def local_upload(self, current_datetime):
        
        self.local_path = f'{self.local_path}{current_datetime.date()}'
        self.write_local(self.calculated_parameters, self.local_path + ' parameters.csv' )
        if  self.sweep_data: 
            self.write_local(self.sweep_data, self.local_path + ' sweeps data.csv')
        
        
    def write_local(self, data, path_name):
        
        """"""

        keys = list(data[0].keys())
        with open(path_name, "w", newline='') as csv_file:
            dict_writer= csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        