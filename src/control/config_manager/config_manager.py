""" G3 - Plasma Devs
Layer 2 - Control - Config Manager
    This module provides a class to interface with Plasmetry's configuration file.

author: <----------------------
status: <?>

Classes:
    ConfigManager

"""
# built-in imports
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

# local imports
from protected_dictionary import ProtectedDictionary 

class ConfigManager:
    """The ConfigManager class has been defined for configuration file interfacing.
    
    Attributes:
        + file_name
        + say
        + list_of_biases
        + list_of_positive_floats
        + sys_ref
        + config_ref

    Methods:
        + __init__()
        + load_config_file()
        + save_config_file()
        + config_references_loaded()
        + validate_all()
        + validate_json_path()
        + get_config()
        + set_config()
        + validate_entry()
        + validate_integers
        + validate_positive_floats()
        + validate_voltage()
        + validate_sweep()
        + validate_amp()
        + validate_non_probe_keys()
        + validate_area()
    """
    
    def __init__(self, text_out, status_flags, command_flags, path_name):
        
        "ConfigManager Constructor."
        
        # Storing the file path in file_name attribute for access to the file.
        self.file_name = path_name
        # Log file writer
        self.say = text_out
        # Storing the final word of the keys for validation identification.
        self.list_of_biases = ['min', 'max', 'bias']
        self.list_of_positive_floats = ['rate','gain', '1', '2','area', 'shunt' ]
    def load_config_file(self):
        
        """load_config_file extracts configuration file contents."""
        # Verifying if valid json file.
        if self.validate_json_path(self.file_name):
            
            # Writing to log.
            self.say("loading config...")
            complete_file = {}
            # Opening the file path in order to extract contents.
            with open(f'{self.file_name}', 'r') as config:
                
                # Storing json key-value pairs.
                complete_file = json.load(config)
       
                
           
            # Storing sys_ref key value pair as a class attribute.
            self.sys_ref=ProtectedDictionary(complete_file['sys_ref'])

            # Storing config_ref key value pair as a class attribute.
            self.config_ref=ProtectedDictionary(complete_file['config_ref'])
                
            
            # Validate_all function call to verify config file entries.
            self.validate_all()
            
            # Writing to log.
            self.say('config loaded!')
 
    def save_config_file(self):
        """save_config_file rewrites onfig file contents."""
        
        # Validation of json file set.
        if self.validate_json_path(self.file_name):
            if self.config_references_loaded():
                # Validating all entries before writing on file.
                self.validate_all()
                
                complete_file={'sys_ref':{}, 'config_ref':{}}
                # The  dictionary contents are re-written.
                for key in self.sys_ref.keys():
                    complete_file['sys_ref'][key] = self.sys_ref[key]
                    
                for key in self.config_ref.keys():
                    complete_file['config_ref'][key] = self.config_ref[key]
                
                # Writing to log.
                self.say('\nsaving in memory...')
                
                # Writing on the file at path
                with open(f'{self.file_name}', 'w') as config_file:
                    json.dump(complete_file, config_file, indent=4)
                    
                # Writing to log.
                self.say('Successfully saved!\n')
    def config_references_loaded(self):
        
        
        """config_references_loaded verifies that sys_ref and config_ref have been defined."""
        
        try:
            return self.sys_ref and self.config_ref
        
        except AttributeError:
             self.say('Must load config file before using mutator functions!')

             return False
    def validate_all(self):
        
        """validate_all validates entries on config file, 
        
        except for paths (since paths are validated multiple times by other components)."""
        
        # Storing the probe ids (slp,dlp,tlv,tlv,hea,iea)
        probe_ids = list(self.sys_ref.keys())
        
        # Going through each probe id
        for probe_id in probe_ids:
            
            # Going through sys_ref and config_ref values for validiation by calling validate_entry
            for key in self.sys_ref[probe_id].keys():
                self.validate_entry(self.sys_ref, probe_id, key, self.sys_ref[probe_id][key])
                
            for key in self.config_ref[probe_id].keys():
                self.validate_entry(self.config_ref, probe_id, key, self.config_ref[probe_id][key])
     
            
    def validate_json_path(self, file_name):
        
        """Returns True if file_name is a json file. 
        
        Used for config load and save, as well as credentials file verification."""

        # Check if the path exists
        if  os.path.exists(file_name):
            
            # Check if json file
            if  file_name[-5:] == '.json':
                return True
            else:
                self.say('The file path is invalid, as it is not a JSON file!')
                return False
        else:
             self.say(f'The file path {file_name} is invalid! Check that the name is set correctly.')
             return False
        
    def get_config(self, probe_id, key):
         """get_config function used for retreiving config values."""
         if self.config_references_loaded():
             
             # IF the key is a dictionary, retreiving probe area for display /units 
             if isinstance(key, dict):
                 return self.config_ref[probe_id][list(key.keys())[0]][list(key.values())[0]]
             
             # If no probe_id has been set, retreiving non-probe specific values
             elif key in self.config_ref.keys() and probe_id == '':
                 return self.config_ref[key]
             
             # If config_ref value, retreiving the value for probe specified
             elif key in self.config_ref[probe_id].keys():
                 return self.config_ref[probe_id][key]  
             
             # If sys_ref value, retreving the value for probe specified
             elif key in self.sys_ref[probe_id].keys():
                 return self.sys_ref[probe_id][key]
                 
             # Else no key foucnd in the config file keys, avoids key error
             else:
                 self.say('wrong key!')
    
    def set_config(self, probe_id, key, value):
        
        """Function for setting a config file value on config_ref. May be used for sys_ref.
        
        Before setting any value, validations must always occur. """
        
        # Verifying that sys_ref and config_ref have been defined
        if self.config_references_loaded():
          
            # IF the key is a dictionary, invoking validation for probe area. 
            if isinstance(key, dict):
                self.validate_area(probe_id, key, value)
            
            # If no probe_id has been set, invoking validation for non-probe_id keys
            elif key in self.config_ref.keys() and probe_id == '':
                self.validate_entry(ref=self.config_ref,probe_id='', key=key, value=value)

            
            # config_ref probe-specific key-valye pairs validation invoked
            elif key in self.config_ref[probe_id].keys():
                self.validate_entry(ref=self.config_ref,probe_id=probe_id, key=key, value=value)
            
            # sys_ref probe-specific key-valye pairs validation invoked
            elif key in self.sys_ref[probe_id].keys():
                self.validate_entry(ref=self.sys_ref,probe_id=probe_id, key=key, value=value)
                
            # else no key foucnd in the dictionary, avoids key error
            else:
                self.say(f'Key {key} passed as argument does not exist!')
    def validate_entry(self, ref, probe_id, key, value):
        
        "validate_entry validates new values requested for in-memory config file set."
        
        # Spliting as tokens, used for validation of bias and non-zero float key-values
        tokens = key.split('_')
        
        # If no probe id, validation for non probe specific key-value invoked
        if not probe_id:
            self.validate_non_probe_keys(ref, key, value)
        
        # If the last word in key describes a bias, validation for bias related key-value pairs invoked
        elif tokens[-1] in self.list_of_biases:
            self.validate_voltage(ref, probe_id, key, value, tokens)
        
        # If the last word in key describes a non-negative 
        elif tokens[-1] in self.list_of_positive_floats or 'area' in key:
            self.validate_positive_floats(ref, probe_id, key, value)
            
        # Validating integer-only config values
        else:
            self.validate_integers(ref, probe_id, key, value)
    
   
    def validate_integers(self, ref, probe_id, key, value):
        """validate_integers validates integer related key-value pairs for the probe specified."""
        #Other wise, validating sys_ref values
        if not isinstance(value,(int,float)):
            return
        if value % 1 != 0:
            return
    
        # Number of samples cannot be less than 10 in order to use scipy's butterworth signal filtering 
        # Otherwise (For Triple Langmuir), number of samples cannot be less than 2.
        if 'samples' in key:
            # If the value set for num samples is less than 10, verifying value set.
            if value < 10:
                # If not Triple Langmuir, setting 10 for num samples.
                if 'tl' not in probe_id:
                    value = 10
                    
                # If Triple Langmuir, setting value as 2
                elif value<2:
                    value =2
        # Setting the value
        ref[probe_id][key]= int(value)
        
            
    def validate_positive_floats(self, ref, probe_id, key, value):
        
        """validate_positive_floats validates float related key-value pairs for the probe specified."""
        
        # Verifying that the value is a number
        if isinstance(value,(int, float)):
            
            # Verifing that the value is not 0
            if value > 0:
                if not 'area' in key:
                    value = round(value, 2)
                # If validations are true, setting the value to in-memory config ref
                ref[probe_id][key]= value 
                
                
                
    def validate_voltage(self, ref, probe_id, key, value, tokens):
        
        """validate_voltage validates biases and their respective maximum and minimums,
        
        ensuring all voltage values are within expected ranges."""
        
        # If the value is not a number, invalid, thus not set.
        if not isinstance(value,(int, float)):
           return
       
        # If the value is related to sweeps, invoking sweep related validations
        if tokens[0] == 'sweep':
            
            # If applied min or max of sweep, 
            #invoking method for preliminary validation of applied biases on sweep
            if 'amp' != tokens[1]:
                if self.validate_sweep(ref, probe_id, key, value, tokens):
                    return
            # Otherwise, invoking method for preliminary validation of amplifier values
            else: 
                self.validate_amp(ref, probe_id, key, value, tokens)
        
        
        # If the key is a minimum, verifying that it is less than maximum
        if tokens[-1] == 'min':
            
            # Identifying key of maximum
            tokens[-1] = 'max'
            max_key = '_'.join(tokens)
           
            # If less than maximum, setting the value
            if ref[probe_id][max_key] > value:
                ref[probe_id][key]= round(value, 2)  
        
        # If the key is a maximum, verifying that it is greater than minimum
        elif tokens[-1] == 'max':
            
            # Identifying key of minimum
            tokens[-1] = "min"
            min_key = '_'.join(tokens)
             
            # If greater than minimum, setting the value
            if ref[probe_id][min_key] < value:
                ref[probe_id][key] = round(value, 2)  
        
                
        # If the key-value pair relates to an applied bias 
        else:
            
            # If not collector, poping the token 'bias'
            if not 'collector' in tokens:
                tokens.pop()
            
            # Creating copies of the tokens in key and generating max and min keys
            max_token = tokens.copy()
            min_token = tokens.copy()
            max_token.append("max")
            min_token.append("min")
            max_key = '_'.join(max_token)
            min_key = '_'.join(min_token)
            
            # If the value is within the expected range, storing it in memory.
            if ref[probe_id][min_key] <= value <= ref[probe_id][max_key]:
               ref[probe_id][key]= round(value, 2)  
                
    def validate_sweep(self, ref, probe_id, key, value, tokens):
        
        """validate_sweep performs a preliminary validation of minimim and maximum applied on sweep"""
        
        # index for sweep min and max 
        amp_max_key = "sweep_amp_max"
        amp_min_key = "sweep_amp_min"
        
        # If the value is within accepted range, continuing validations in validate_voltage method
        if ref[probe_id][amp_min_key] <= value <= ref[probe_id][amp_max_key]:
             return False
        else:
            #If applied bia is minimum of sweep
            if tokens[1] == 'min':
                # If the amp minimum voltage is greater than the applied voltage, invalid assignment
                if ref[probe_id][amp_min_key] >= value:
                    
                # Assigning the minimum of amp to the minimum of sweep
                   ref[probe_id][key]= ref[probe_id][amp_min_key]
                   
                   # validate_voltage shall end validations
                   return True
               
            #If applied bias is maximum of sweep 
            elif tokens[1] == 'max': 
                
                # If the amp maximum voltage is less than the applied voltage, invalid assignment.
               if ref[probe_id][amp_max_key] <= value:
                   
                   # Assigning the minimum of amp to the minimum of sweep
                   ref[probe_id][key] = ref[probe_id][amp_max_key]
                   
                   # validate_voltage shall end validations
                   return True
        # Returning false to continue validations
        return False
    
    def validate_amp(self, ref, probe_id, key, value, tokens):
        """validate_amp  performs a preliminary validation of the amplifiers for sweeps 
        and the respective applied bias"""
        

        # If validating maximum of amplifier
        if tokens[-1] == 'max':
            
            # If the max amplifier value is less than max applied bias, storing the amp value as the applied bias
            if value < ref[probe_id]['sweep_max']:
                ref[probe_id]['sweep_max'] = round(value, 2)  
                
            # If the max amplifier value is less than the min applied bias, changing the min applied to min amp value
            if value <= ref[probe_id]['sweep_min']:
                ref[probe_id]['sweep_min'] = ref[probe_id]['sweep_amp_min']
            
        # If validating minimum of amplifier
        elif tokens[-1] == 'min':
            
            # If the minimum amplifier value is greater than min applied bias,
            # Storing the amp value as the applied bias
            if value > ref[probe_id]['sweep_min']:
                ref[probe_id]['sweep_min'] = round(value, 2)  
            
            # If the minimum amplifier value is greater than the max applied bias, 
            # Changing the max applied to max amp value.
            if value >= ref[probe_id]['sweep_max']:
                ref[probe_id]['sweep_max'] = ref[probe_id]['sweep_amp_max']
              
                
    def validate_non_probe_keys(self, ref, key, value):
        """validate_non_probe_keys validates keys that are not probe specific"""
        
        # If key is credentials_path, invoking json validation method
        if key=='credentials_path':
            
            # If the file is valid, storing the path for offsite upload
            if self.validate_json_path(value):
                ref[key] = value
        # If key is local_path, verifying that the path points to a directory
        elif key=='local_path':
            
            # If directory exists, storing the path for local storage
            if os.path.isdir(value):
                ref[key] = value
                
        # If key is selected_gas, storing the value of the gas into the probe_id dictionaries
        elif key == 'selected_gas':
            for probe_id in self.sys_ref:
                ref[probe_id][key] = value
        else:
            # Other values do not require validation.
            ref[key] = value
            
    def validate_area(self, probe_id, key, value):
        """validate_area validates units and area for probe areas in each probe_id dictionary,\
        as well as converts the area to meters for calculations."""
        
        # Storing dictionary with key-value pairs for units of meter
        units = {'km': 1e+3,
                 'hm': 1e+2,
                 'dam': 1e+1,
                 'm': 1,
                 'dm':1e-1,
                 'cm':1e-2,
                 'mm':1e-3,
                 'dmm':1e-4,
                 'cmm':1e-5,
                 'µm':1e-6,
                 'nm':1e-9
            }
        
        # Extracting key info from dictionary stored in the key variable
        config_key = list(key.keys())[0]
        dictionary_key = list(key.values())[0]
        
        # Validating value for display, ensuring it is above 0.01
        if not isinstance(self.config_ref[probe_id][config_key][dictionary_key], str):
            if value<0.01:
                value = self.config_ref[probe_id][config_key]['display_value']
        
        # Storing the value in config
        self.config_ref[probe_id][config_key][dictionary_key] = value
        
        # Converting the display value and units into meters and storing it for calculations
        self.config_ref[probe_id]['Probe area'] = units[self.config_ref[probe_id][config_key]['unit']]\
            * self.config_ref[probe_id][config_key]['display_value']


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

   