import os
import sys

import traceback


# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 1           # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
   # self.say(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #


# Datetime import for current time verification
from datetime import datetime

# Contains method for data processing
from data_formating import process_data

# Offsite wrapper import
from google_drive import GoogleDrive

# Local storage interface
from local_upload import LocalUpload

class FileUpload:
    """FileUpload is defined to act as an interface for data storage operations."""
    
    def __init__(self, 
                 text_out, 
                 status_flags, 
                 command_flags,
                 probe_type="",
                 local_path = '',
                 unformatted_data=[],
                 credentials_path='',
                 experiment_name='',
                 folder_id='',
                 name="UPLDR"):
        """FileUpload construtor"""

        # Save control objects
        self._say_obj = text_out    # store SayWriter
        self.name = name            # name used to label text output
        self.status_flags = status_flags    # state indicators
        self.command_flags = command_flags  # action triggers
        
        # Datetime object with date and time of execution
        self.current_datetime = datetime.now()
        
      
        # Storing wrapper for offsite data uploading
        self.offsite_wrapper = GoogleDrive(text_out, credentials_path, folder_id)
        
        # Storing local upload object
        self.local_uploader = LocalUpload(text_out, local_path) 
        
        self.experiment_name = experiment_name
        
        self.get_probe_folder(probe_type)
        # Verifying if unformatted data has been received, if true will commence to process the data
        if unformatted_data:
            # Setting the csv contents objects containing sweep and parameters data
            # If no sweep data, the object will remain empty.
            self.experiment_metadata, self.parameters_csv, self.sweep_csv = process_data(unformatted_data)

        self.say("initialized...")
            
    def say(self, msg):
        """Output text to the Saywriter object labeled with name attribute."""
        self._say_obj(f"{self.name}: {msg}")        
                    
    def new_data(self, parameters):
        
        """new_data receives unformatted data to create new csv content objects and commence upload."""
        
        self.say("processing results...")
        self.status_flags.formatting.set()

        #Setting the csv content objects containing sweep and parameters data
        # If no sweep data, the object will remain empty.
        self.experiment_metadata, self.parameters_csv, self.sweep_csv = process_data(parameters)
        self.say("processing complete.")
        self.status_flags.formatting.clear()

        
        # Datetime object with date and time of execution
        self.current_datetime = datetime.now()
        self.upload_data()
            
    def upload_data(self):
        
        """upload_data uploads data locally and offsite when invoked."""
        
        # Store locally
        self.local_upload()
        
        # Store offsite
        self.offsite_upload()
        
    def local_upload(self):
        """local_upload performs local storage data uploading."""
        
        self.say("storing results locally...")
        
        # Validating the path for storage
        if self.local_uploader.validate_path(self.local_uploader.parent_folder):
            # Switching to folder with current date for uploading
            self.folder_change(self.local_uploader, f'{self.local_uploader.parent_folder}/{self.current_datetime.date()}')
            
            self.folder_change(self.local_uploader, f'{self.local_uploader.parent_folder}/{self.probe_folder}')
            
            current_hour = int(self.current_datetime.hour) % 12
            if current_hour == 0:
                current_hour = 12
                
            self.local_uploader.write_file(self.experiment_metadata, f"{self.local_uploader.parent_folder}/{current_hour}_{self.current_datetime.minute}_{self.current_datetime.strftime('%p')} experiment metadata.csv")
            
            # Creating the csv containing parameters date
            self.local_uploader.write_file(self.parameters_csv, f"{self.local_uploader.parent_folder}/{current_hour}_{self.current_datetime.minute}_{self.current_datetime.strftime('%p')} parameters.csv" )
            
            # Verifying if there is sweep data
            if  self.sweep_csv: 
                # Creating the csv containing the sweep data
                self.local_uploader.write_file(self.sweep_csv, f"{self.local_uploader.parent_folder}/{current_hour}_{self.current_datetime.minute}_{self.current_datetime.strftime('%p')} sweeps data.csv")
            self.say("local storage successful.")
        else:
            self.say('Local path set to a directory that does not exist! Cannot store locally!')
            
    def offsite_upload(self):
        """offsite_upload performs offsite storage data uploading."""
        
        self.say("uploading results to remote storage...")

        # Verifying if the credentials path is set
        if self.offsite_wrapper.validate_path(self.offsite_wrapper.credentials_path):
            try:
                # Verifying if there is a connection with the offsite storage to commence upload requests
                if self.offsite_wrapper.validate_connection():
                    
                    self.status_flags.transmitting.set()    # indicate transmission is ocurring

                    # Switching to folder with current date for uploading
                    self.folder_change(self.offsite_wrapper, f'{self.experiment_name}')
                        
                    # Switching to folder with current date for uploading
                    self.folder_change(self.offsite_wrapper, f'{self.current_datetime.date()}')

                    self.folder_change(self.offsite_wrapper, f'{self.probe_folder}')
                    
                    # Format hour style
                    current_hour = int(self.current_datetime.hour) % 12
                    if current_hour == 0:
                        current_hour = 12
                    
                    # Storing the parameters csv object
                    self.offsite_wrapper.put_request(self.experiment_metadata,f"{current_hour}_{self.current_datetime.minute}_{self.current_datetime.strftime('%p')} experiment metadata.csv")
                    
                    # Storing the parameters csv object
                    self.offsite_wrapper.put_request(self.parameters_csv, f"{current_hour}_{self.current_datetime.minute}_{self.current_datetime.strftime('%p')} parameters.csv")
                    
                    # Verifying if there is sweep data
                    if  self.sweep_csv:
                        
                        # Storing the sweep csv object
                        self.offsite_wrapper.put_request(self.sweep_csv, f"{current_hour}_{self.current_datetime.minute}_{self.current_datetime.strftime('%p')} sweeps data.csv")
                    
                    self.say("upload successful.")
                    
            # Catch error and print with SayWriter.
            except Exception as err:
                self.say("Error during upload!")
                self.say(err)
                self.say(traceback.format_exc())


            # Disable transmitting flag no matter what
            finally:
                self.status_flags.transmitting.clear()

        else: self.say('No credentials path set! Cannot upload results!')
    
    def folder_change(self, wrapper, folder_name):
        
        """folder_change changes to folder for upload."""
        
        if not wrapper.folder_exists(folder_name) and folder_name:
            
            wrapper.create_folder(folder_name)
            
    def get_probe_folder(self, probe_type):
        
        match probe_type:
            
            # Single Langmuir Probe
            case 'slp':
                self.probe_folder = "Single Langmuir Probe"
            # Double Langmuir Probe
            case 'dlp':
                self.probe_folder= 'Double Langmuir Probe'
            
            # Hyperbolic Energy Analyzer
            case 'hea':
                self.probe_folder= 'Hyperbolic Energy Analyzer'
            
            # Ion Energy Analyzer
            case 'iea':
                self.probe_folder= 'Ion Energy Analyzer'
            
            # Triple Langmuir Probe - Voltage Mode
            case 'tlv':
                self.probe_folder= 'Triple Langmuir Probe - Voltage Mode'
            
            # Triple Langmuir Probe - Current Mode
            case 'tlc':
                self.probe_folder= 'Triple Langmuir Probe - Current Mode'
            
            # Unknown Probe
            case _:
                raise ValueError(f"Unknown probe type: {self.probe_type}")