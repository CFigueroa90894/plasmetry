def process_data(self, unformatted_data):
        
        """"""
        sweep_data = []
        calculated_parameters = []
        
        for experiment_run in unformatted_data:
            if not self.is_tlp():
               self.sweep_data.append({'Bias' : experiment_run['Bias 1'], \
                                       'Raw Signal' : experiment_run['Raw voltage 1'],\
                                       'Filtered current': experiment_run['Filtered current']})
               del experiment_run['Bias 1']
               del experiment_run['Raw voltage 1']
               del experiment_run['Filtered current']
            calculated_parameters.append(experiment_run)
        return sweep_data, calculated_parameters
    
def is_tlp(self, unformatted_data):
    
    """"""
    
    if 'Bias 2' in unformatted_data:
        return True
    else:
        return None
        