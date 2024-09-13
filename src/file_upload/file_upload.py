
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

from data_formating import process_data
from datetime import datetime
from google_drive import GoogleDrive

class FileUpload:
    
    def __init__(self, local_path,  credentials_path='', unformatted_data=''):
        
        """FileUpload construtor"""
        self.current_datetime = datetime.now()
        if unformatted_data:
            self.sweep_csv, self.parameters_csv = process_data(unformatted_data)
            
        self.offsite_wrapper = GoogleDrive(credentials_path)
        self.local_path = f'{local_path}{self.current_datetime.date()}'

                
    def new_upload(self, parameters):
        
        """"""
        self.sweep_csv, self.parameters_csv = process_data(parameters)
        
    def offsite_upload(self):
        
        """"""

        self.offsite_wrapper.put_request(self.sweep_csv, f'{self.current_datetime.date()} sweeps data.csv')
        self.offsite_wrapper.put_request(self.parameters_csv, f'{self.current_datetime.date()} parameters.csv')
        
    def upload_data(self):
        """"""
        self.local_upload()
        self.offsite_upload()
    
            
    def local_upload(self):
        
        """"""
        self.write_local(self.parameters_csv, self.local_path + ' parameters.csv' )
        if  self.sweep_csv: 
            self.write_local(self.sweep_csv, self.local_path + ' sweeps data.csv')
        
    def write_local(self,csv_obj, path_name):
        
        """"""
        with open(path_name, 'w', newline='', encoding='utf-8') as f:
            f.write(csv_obj)
                
    


            