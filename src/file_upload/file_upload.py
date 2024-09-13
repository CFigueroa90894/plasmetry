
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


# Datetime import for current time verification
from datetime import datetime

# Contains method for data processing
from data_formating import process_data

# Offsite wrapper import
from google_drive import GoogleDrive

from pathlib import Path

class FileUpload:
    
    def __init__(self, local_path,  credentials_path='', unformatted_data=[]):
        
        """FileUpload construtor"""
        
        # Validating the local path
        self.validate_path(local_path)
        

        # Verifying if unformatted data has been received, if true will commence to process the data
        if unformatted_data:
            
            #Setting the csv contents objects containing sweep and parameters data
            # If no sweep data, the object will remain empty.
            self.parameters_csv, self.sweep_csv = process_data(unformatted_data)
            
        
        # Storing wrapper for offsite data uploading
        self.offsite_wrapper = GoogleDrive(credentials_path)
        
    def validate_path(self, local_path):
        
        """Validates if the received path is valid."""
        # Create a Path object for the directory
        dir_path = Path(local_path)

        # Check if the directory exists 
        if  dir_path.exists():

            self.path_is_set = True
            self.storage_path = local_path
            # Setting the local path name with the current time
            self.set_path()
            
            
        else:
            self.path_is_set = False
            print('Local path set to a directory that does not exist!')
            
                
    def new_data(self, parameters):
        
        """Receives new unformatted data to create new csv content objects."""
        
        #Setting the csv content objects containing sweep and parameters data
        # If no sweep data, the object will remain empty.
        self.parameters_csv, self.sweep_csv = process_data(parameters)
        
        # Setting the local path name with the current time
        self.set_path(self)
       
    def set_path(self):
        
        """This method sets the current date(time*) to the local path."""
        
        # Datetime object with date and time of execution
        self.current_datetime = datetime.now()
        
        # Setting the local path
        self.local_path = f'{self.storage_path}{self.current_datetime.date()}'
        
    def local_upload(self):
        
        """Local storage data uploading."""
        
        # Creating the csv containing parameters data
        self.write_file(self.parameters_csv, self.local_path + ' parameters.csv' )
        
        # Verifying if there is sweep data
        if  self.sweep_csv: 
            # Creating the csv containing the sweep data
            self.write_file(self.sweep_csv, self.local_path + ' sweeps data.csv')
    def upload_data(self):
        
        """Upload data locally and offsite when invoked."""
        
        if self.path_is_set:
            
            self.local_upload()
            
            # Verifying if the credentials path is set
            if self.offsite_wrapper.credentials_path:
                
                # If set, commencing offsite upload
                self.offsite_upload()
                
            # Printing that credentials path must be set
            else:
                print('No credentials path set!')
            
    def offsite_upload(self):
        
        """Offsite storage data uploading."""
        
        # Verifying if there is a connection with the offsite storage to commence upload requests
        if self.offsite_wrapper.valid_internet_connection():
                    
            # Storing the parameters csv object
            self.offsite_wrapper.put_request(self.parameters_csv, \
                                             f'{self.current_datetime.date()} parameters.csv')
                
            # Verifying if there is sweep data
            if  self.sweep_csv:
                
                # Storing the sweep csv object
                self.offsite_wrapper.put_request(self.sweep_csv, \
                                                 f'{self.current_datetime.date()} sweeps data.csv')
            
        
    def write_file(self, csv_obj, file_name):
        
        """Local storage file creation."""
        
        # Creating csv
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            # Writing csv ocntents
            file.write(csv_obj)
            