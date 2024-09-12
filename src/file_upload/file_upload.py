import csv

class FileUpload:
    
    def __init__(self, local_path, unformatted_data=None, credentials_path=None):
        
        """FileUpload construtor"""
        
        if unformatted_data:
            # Storing unformatted parameters dictionary
            self.process_data(unformatted_data)
            
        self.local_path = local_path
        self.offsite_credentials = credentials_path
                
    def new_upload(self, parameters):
        
        """"""
        # Storing unformatted parameters dictionary
        self.process_data(parameters)
    
    def is_tlp(self, unformatted_data):
        
        """"""
        
        if 'Bias 2' in unformatted_data:
            return True
        else:
            return None
            
    def process_data(self, unformatted_data):
        
        """"""
        self.sweep_data = []
        self.calculated_parameters = []
        
        for experiment_run in unformatted_data:
            if not self.is_tlp():
               self.sweep_data.append({'Bias' : experiment_run['Bias 1'], \
                                       'Raw Signal' : experiment_run['Raw voltage 1'],\
                                       'Filtered current': experiment_run['Filtered current']})
               del experiment_run['Bias 1']
               del experiment_run['Raw voltage 1']
               del experiment_run['Filtered current']
            self.calculated_parameters.append(experiment_run)
            
    def local_upload(self, local_path_name):
        
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
            
    


 
        
        
        
        
        