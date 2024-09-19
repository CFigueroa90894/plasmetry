import os 

class LocalUpload:
        
    def __init__(self, local_path=''):
        
        """LocalUpload construtor"""
        
        # Validating the local path
        if not self.validate_path(local_path):
            print('Local path not valid.')
            
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
