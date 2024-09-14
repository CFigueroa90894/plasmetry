
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

from local_upload import LocalUpload

class FileUpload():
    
    def __init__(self, local_path = '',  credentials_path='', unformatted_data=[], *args, **kwargs):
        
        
        """FileUpload construtor"""
        
        # Datetime object with date and time of execution
        self.current_datetime = datetime.now()
        
        # Verifying if unformatted data has been received, if true will commence to process the data
        if unformatted_data:
            
            # Setting the csv contents objects containing sweep and parameters data
            # If no sweep data, the object will remain empty.
            self.parameters_csv, self.sweep_csv = process_data(unformatted_data)
            
        # Storing wrapper for offsite data uploading
        self.offsite_wrapper = GoogleDrive(credentials_path)
        
        # Storing local upload object
        self.local_uploader = LocalUpload(local_path) 
                    
    def new_data(self, parameters):
        
        """Receives new unformatted data to create new csv content objects."""
        
        #Setting the csv content objects containing sweep and parameters data
        # If no sweep data, the object will remain empty.
        self.parameters_csv, self.sweep_csv = process_data(parameters)

        # Datetime object with date and time of execution
        self.current_datetime = datetime.now()
        
    def folder_change(self, folder_name, wrapper):
        
        """Args: string, upload object
        
        Changes to folder for upload."""
        
        if not wrapper.folder_exists(folder_name):
            
            wrapper.create_folder(folder_name)
            
    def upload_data(self):
        
        """Uploads data locally and offsite when invoked."""
        
        
        # Store locally
        self.local_upload()
        
        # Store offsite
        self.offsite_upload()
        
        
    def local_upload(self):
        
        """Local storage data uploading."""
        # Valdating the path for storage
        if self.local_uploader.validate_path(self.local_uploader.storage_path):
            # Switching to folder with current date for uploading
            self.folder_change(f'{self.local_uploader.storage_path}/{self.current_datetime.date()}', self.local_uploader)

            # Creating the csv containing parameters date
            self.local_uploader.write_file(self.parameters_csv, f'{self.local_uploader.storage_path}/ parameters.csv' )
            
            # Verifying if there is sweep data
            if  self.sweep_csv: 
                # Creating the csv containing the sweep data
                self.local_uploader.write_file(self.sweep_csv, f'{self.local_uploader.storage_path}/ sweeps data.csv')
        else:
            print('Local path set to a directory that does not exist!')
    def offsite_upload(self):
        
        """Offsite storage data uploading."""
        # Verifying if the credentials path is set
        if self.offsite_wrapper.credentials_path:
             
            # Verifying if there is a connection with the offsite storage to commence upload requests
            if self.offsite_wrapper.validate_connection():
                
                # Switching to folder with current date for uploading
                self.folder_change(f'{self.current_datetime.date()}', self.offsite_wrapper)
                
                # Storing the parameters csv object
                self.offsite_wrapper.put_request(self.parameters_csv, \
                                                 f'{self.current_datetime.date()} parameters.csv')
                    
                # Verifying if there is sweep data
                if  self.sweep_csv:
                    
                    # Storing the sweep csv object
                    self.offsite_wrapper.put_request(self.sweep_csv, \
                                                     f'{self.current_datetime.date()} sweeps data.csv')
        else: print('No credentials path set!')