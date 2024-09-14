import io
import csv

def is_tlp(unformatted_data):
    
    """Returns a boolean value. True if the probe implemented is Triple Langmuir, False if other wise."""
    
    # Since both TLP implementations contain the key 'Raw voltage 2',verifying if it exists
    if 'Raw voltage 2' in unformatted_data:
        # Return True if TLP
        return True
    else:
        # Return False if not TLP
        return False
    
    
def process_sweep(sweep_data, experiment_run):
    
    """Prepares the sweep data for csv upload."""
    
    for i in range(len(experiment_run['Bias 1'])):
        
        # Appending the sweep data
        sweep_data.append({'Bias' : experiment_run['Bias 1'][i], \
                           'Raw Signal' : experiment_run['Raw voltage 1'][i],\
                           'Filtered current': experiment_run['Filtered current'][i]})
            
    # Deleting the appended sweep data
    del experiment_run['Bias 1']
    del experiment_run['Raw voltage 1']
    del experiment_run['Filtered current']
    
    
def create_csv_object(data):
    
    """Returns a string containing the data used to create a csv file."""
    # Storing the io string writer function, used as the writer function for csv.writer
    output = io.StringIO()
    
    # Initializing the io object
    writer = csv.writer(output)
    
    # Storing the keys of the dictionaries in the list
    header = data[0].keys() 
    
    # Writing the header information in memory, extracted from the keys
    writer.writerow(header)
    
    # For each dictionary in the list of data, writing the values in memory
    for experiment_run in data:
        writer.writerow(experiment_run.values())
        
    # Going to the start of the io object to read all the written contents when returning
    output.seek(0)
    
    # Returning the contents of the csv
    return output.getvalue()

    
def process_data(unformatted_data):
        
    """Returns the csv objects used for uploading"""
    
    # Initializing the lists used for storing the parameters and sweep data
    sweep_data = []
    calculated_parameters = []
    
    # Going through each dictionary in the list of data
    for experiment_run in unformatted_data:
        
        # Verifying if there is sweep data 
        if not is_tlp(unformatted_data):
            # Processing the sweep data and storing it in sweep_data list
            process_sweep(sweep_data, experiment_run)
        # Storing the parameters data.
        calculated_parameters.append(experiment_run)
    
    # Verifying if sweep data exists to create object with csv contents
    if sweep_data:
        
        # Storing csv contents for parameters and sweeps
        sweep_csv = create_csv_object(sweep_data)
        
    else: 
        
        # Storing an empty list
        sweep_csv = sweep_data
     
    # Storing parameter csv contents
    parameters_csv = create_csv_object(calculated_parameters)
    
    # Returning csv contents objects
    return parameters_csv, sweep_csv