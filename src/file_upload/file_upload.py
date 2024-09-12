import csv
from data_formating import process_data

class FileUpload:
    
    def __init__(self, local_path, unformatted_data=None, credentials_path=None):
        
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
        
        time_stamp = 10
        self.local_path = self.local_path + str(time_stamp)
        self.local_file_write(self.calculated_parameters)
        
        if  self.sweep_data: 
            self.local_file_write(self.sweep_data)
            
    def local_file_write(self, data):
        
        """"""

        keys = list(data[0].keys())
        with open(self.local_path, "w", newline='') as csv_file:
            dict_writer= csv.DictWriter(csv_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
            
    
        
    
            
    


 
        
        
        
        
        