""" G3 - Plasma Devs
Layer 2 - Control - Local Upload
    This module provides a class to store experiment results in the local file system.

author: <----------------------
status: <?>

Classes:
    LocalUpload

"""
# built-in imports
import os 

class LocalUpload:
    """LocalUpload is defined to act as an interface for local storage.
    
    Attributes:
        + say
        + parent_folder

    Methods:
        + __init__()
        + validate_path()
        + write_file()
        + create_folder()
        + folder_exists()
    
    """
    def __init__(self, text_out, local_path=''):
        
        """LocalUpload construtor"""
        self.say = text_out
        # Validating the local path
        if not self.validate_path(local_path):
            self.say('Local path not valid.')
            
    def validate_path(self, local_path):
        
        """Returns boolean value validating the received path."""

        # Check if the directory exists 
        if  os.path.exists(local_path):
            
            # Set the path for local storage
            self.parent_folder = local_path
            return True
        else:
            return False
            
    def write_file(self, csv_obj, file_name):
        
        """Local storage file creation."""
        
        # Creating csv
        with open(file_name, 'w', newline='', encoding='utf-8') as file:
            
            # Writing csv ocntents
            file.write(csv_obj)
            
    def create_folder(self, folder_name):
        
        """Create new folder where local data will be uploaded"""
        
        # Making the new directory
        os.mkdir(folder_name)
        
        # Setting new directory as folder path
        self.parent_folder = folder_name
        
    def folder_exists(self, folder_name):
        
        """Validating that the directory argument exists locally."""
        
        return self.validate_path(folder_name)
