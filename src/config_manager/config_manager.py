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
    def load_config_file(self):
        
        self.say( os.path.dirname(os.path.realpath(__file__)))

        if self.validate_path():
            
            self.say("loading config...")
            
            with open(f'{self.file_name}', 'r') as config:
                
                self.complete_file = (json.load(config))
                
                self.sys_ref = self.complete_file['sys_ref']
                self.config_ref= self.complete_file['config_ref']
            self.say('config loaded!')
 
    def save_config_file(self):
        
        if self.validate_path():
            
            self.complete_file['sys_ref'] = self.sys_ref
            self.complete_file['config_ref'] = self.config_ref
            
            self.say('\nsaving in memory...')

            with open(f'{self.file_name}', 'w') as config_file:
                json.dump(self.complete_file, config_file, indent=4)
            self.say('Successfully saved!\n')
            
    def validate_path(self):
        
        """Returns boolean value validating the received path."""

        # Check if the directory exists 
        if  os.path.exists(self.file_name):
            
            if self.file_name[-5:] == '.json':
                return True
            else:
                self.say('The config file path is invalid, as the config file is not a JSON file!')
        else:
             self.say(f'The config file path {self.file_name} is invalid! Check that the name is set correctly.')
        
    def set_config(self, probe_id, key, value):
        
        if self.config_references_loaded():
           
            if key in self.config_ref.keys() and probe_id == '':
                self.config_ref[key] = value
                
            elif key in self.config_ref[probe_id].keys():
                self.config_ref[probe_id][key] = value

            elif key in self.sys_ref[probe_id].keys():
                self.sys_ref[probe_id][key]= value 
                
           
            else:
                self.say('Wrong key {key} passed as argument!')
        
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

   