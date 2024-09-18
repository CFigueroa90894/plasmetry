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
   # print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #

import json
from protected_dictionary import ProtectedDictionary 

class ConfigManager:
    
    def __init__(self, file_name = ''):
        self.file_name = file_name
        self.complete_file = {}
        
    def load_config_file(self):
        
        
        if self.file_name:
            
            print("loading config...")
            with open(f'{self.file_name}', 'r') as config:
                
                self.complete_file = (json.load(config))
                
                self.sys_ref = self.complete_file['sys_ref']
                self.config_ref= self.complete_file['config_ref']
        else:
            print('Must set config path!')
    
    def save_config_file(self):
        
        if self.file_name:
            
            self.complete_file['sys_ref'] = self.sys_ref
            self.complete_file['config_ref'] = self.config_ref
            print('\nsaving in memory...')

            with open(f'{self.file_name}', 'w') as config_file:
                json.dump(self.complete_file, config_file, indent=4)
            print('Successfully saved!\n')
                
        else:
            print('Must set config path!')
   
    def set_config(self, probe_id, key, value):
        
        if self.config_references_loaded():

            
            if key in self.sys_ref[probe_id].keys():
                self.sys_ref[probe_id][key]= value 
                
            elif key in self.config_ref[probe_id].keys():
                self.config_ref[probe_id][key] = value
                
            else:
                print('Wrong key {key} passed as argument!')
        else:
            print('Must load config file first!')
                
    def get_config(self, probe_id, key):
        
         if self.config_references_loaded():
 
             if key in self.sys_ref[probe_id].keys():
                 return self.sys_ref[probe_id][key]
                 
             elif key in self.config_ref[probe_id].keys():
                 return self.config_ref[probe_id][key]
             else:
                 print('wrong key!')
         else: 
             print('Must load config file first!')
             
    def config_references_loaded(self):
        
        try:
            return self.sys_ref and self.config_ref
        
        except AttributeError:
             return False

if __name__ == "__main__":
    
   sample_address = 39
   probe = 'hea'
   
   config_manager = ConfigManager("")
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

   