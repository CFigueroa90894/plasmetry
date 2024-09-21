import os
import sys

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 1         # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
   # self.say(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #

import json
from protected_dictionary import ProtectedDictionary 

class ConfigManager:
    
    def __init__(self, text_out, status_flags, command_flags, path_name = ''):
        self.file_name = path_name
        self.complete_file = {}
        self.say = text_out
        self.list_of_biases = [
            "dac_min", "dac_max", 
            "sweep_min", "sweep_max", "sweep_amp_min", "sweep_amp_max", 
            "rejector_bias", "rejector_min", "rejector_max",
            "collector_bias", "collector_bias_min", "collector_bias_max",
            "up_amp_bias", "up_amp_min", "up_amp_max",
            "down_amp_bias", "down_amp_max", "down_amp_min"
            ]
    def load_config_file(self):
        

        if self.validate_json_path(self.file_name):
            
            self.say("loading config...")
            
            with open(f'{self.file_name}', 'r') as config:
                
                self.complete_file = (json.load(config))
                
                self.sys_ref = self.complete_file['sys_ref']
                self.config_ref= self.complete_file['config_ref']
            self.say('config loaded!')
 
    def save_config_file(self):
        
        if self.validate_json_path(self.file_name):
            
            self.complete_file['sys_ref'] = self.sys_ref
            self.complete_file['config_ref'] = self.config_ref
            
            self.say('\nsaving in memory...')

            with open(f'{self.file_name}', 'w') as config_file:
                json.dump(self.complete_file, config_file, indent=4)
            self.say('Successfully saved!\n')
            
    def validate_json_path(self, file_name):
        
        """Returns boolean value validating the received path."""

        # Check if the directory exists 
        if  os.path.exists(file_name):
    
            if  file_name[-5:] == '.json':
                return True
            else:
                self.say('The file path is invalid, as it is not a JSON file!')
        else:
             self.say(f'The file path {file_name} is invalid! Check that the name is set correctly.')
        
    def set_config(self, probe_id, key, value):
        
        if self.config_references_loaded():
           
            if key in self.config_ref.keys() and probe_id == '':
                self.validate_entry(ref=self.config_ref,probe_id='', key=key, value=value)
            
                
            elif key in self.config_ref[probe_id].keys():
                self.validate_entry(ref=self.config_ref,probe_id=probe_id, key=key, value=value)
            
                

            elif key in self.sys_ref[probe_id].keys():
                self.validate_entry(ref=self.sys_ref,probe_id=probe_id, key=key, value=value)
                
           
            else:
                self.say(f'Wrong key {key} passed as argument!')
        
    def get_config(self, probe_id, key):
        
         if self.config_references_loaded():
             
             if key in self.config_ref.keys() and probe_id == '':
                 return self.config_ref[key]
             elif key in self.sys_ref[probe_id].keys():
                 return self.sys_ref[probe_id][key]
                 
             elif key in self.config_ref[probe_id].keys():
                 return self.config_ref[probe_id][key]  
                 
             else:
                 self.say('wrong key!')
      
    def validate_entry(self, ref, probe_id, key, value):
        
        if not probe_id:
            self.validate_paths(ref, key, value)
            
        elif key in self.list_of_biases:
            self.validate_voltage(ref, probe_id, key, value)
        else: 
            ref[probe_id][key]= value
    
    def validate_voltage(self, ref, probe_id, key, value):
        
        tokens = key.split('_')
        if tokens[-1] == 'min':
           tokens[-1] = 'max'
           max_key = '_'.join(tokens)
           self.say(max_key)
           if ref[probe_id][max_key] > value:
               ref[probe_id][key]= value
        
        elif key[-3:] == 'max':
             min_key = key[:-3] + "min"
             if ref[probe_id][min_key] < value:
                 ref[probe_id][key] = value
        else:
            
             if not 'collector' in tokens:
                 tokens.pop()
                 
             max_token = tokens.copy()
             min_token = tokens.copy()
             
             
             max_token.append("max")
             min_token.append("min")
             
             max_key = '_'.join(max_token)
             min_key = '_'.join(min_token)
             print(f'min key : {min_key}')
             print(f'max key : {max_key}')
             if ref[probe_id][min_key] <= value <= ref[probe_id][max_key]:
                ref[probe_id][key]= value    
                
            
    def validate_paths(self, ref, key, value):
        
        if key=='credentials_path':
            if self.validate_json_path(value):
               self.set_value(ref, key, value)
        else:
            if os.path.isdir(value):
                self.set_value(ref, key, value)
            
    
    def set_value(self, ref, key, value):
        ref[key] = value
        
    def config_references_loaded(self):
        
        try:
            return self.sys_ref and self.config_ref
        
        except AttributeError:
             self.say('Must load config file before using mutator functions!')

             return False

if __name__ == "__main__":
    
   sample_address = 39
   probe = 'hea'
   
   config_manager = ConfigManager("configuration_file.json")
   config_manager.load_config_file()
   
   original = config_manager.get_config(probe, 'sweeper_address')
   print('\noriginal sweeper address:',  original)
   
   
   config_manager.set_config(probe, 'sweeper_address', sample_address)
   
   print('\nsweeper address after changing address:', config_manager.get_config(probe, 'sweeper_address'))

   config_manager.save_config_file()
   config_manager.load_config_file()
   print('\nsweeper address after reloading: ',  config_manager.get_config(probe, 'sweeper_address'))
   
   print(f'\nresetting address to {original}...')
   config_manager.set_config(probe, 'sweeper_address', original)
   
   config_manager.save_config_file()
   config_manager.load_config_file()
   print('\nsweeper address after resetting, saving, and loading: ', config_manager.get_config(probe, 'sweeper_address'))

   