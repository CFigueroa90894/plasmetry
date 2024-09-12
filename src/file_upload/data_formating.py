

def is_tlp(unformatted_data):
    
    """"""
    
    if 'Bias 2' in unformatted_data:
        return True
    else:
        return None
    
def process_sweep(sweep_data, experiment_run):
    
    for i in range(len(experiment_run['Bias 1'])):
        sweep_data.append({'Bias' : experiment_run['Bias 1'][i], \
                           'Raw Signal' : experiment_run['Raw voltage 1'][i],\
                           'Filtered current': experiment_run['Filtered current'][i]})
    del experiment_run['Bias 1']
    del experiment_run['Raw voltage 1']
    del experiment_run['Filtered current']
    
def process_data(unformatted_data):
        
    """"""
    sweep_data = []
    calculated_parameters = []
    for experiment_run in unformatted_data:
        if not is_tlp(unformatted_data):
            process_sweep(sweep_data, experiment_run)
        calculated_parameters.append(experiment_run)
    return sweep_data, calculated_parameters
    