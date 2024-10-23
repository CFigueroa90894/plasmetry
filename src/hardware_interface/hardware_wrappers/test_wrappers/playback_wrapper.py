"""G3 - Plasma Devs
Layer 1 - Hardware Interface - Playback <...>
    Implements the hardware interfacing methods specified by the AbstractWrapper class using
    <...>

author: figueroa_90894@students.pupr.edu
status: WIP

Classes:
    <...> - exported as 'wrapper'
"""
# built-in imports
import sys
import os
import csv
from itertools import cycle

# ----- PATH HAMMER v3.0 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recursing into subdirs and appending them to python path."""
    # os delimeters
    win_delimeter, rpi_delimeter = "\\", "/"

    # locate project root
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    print(f"Path Hammer: {src_abs}")

    # select path delimeter
    if win_delimeter in src_abs: delimeter = win_delimeter
    elif rpi_delimeter in src_abs: delimeter = rpi_delimeter
    else: raise RuntimeError("Path Hammer could not determine path delimeter!")

    # validate correct top folder
    assert src_abs.split(delimeter)[-1*len(root_target):] == root_target
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split(delimeter)[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(3, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #


# local imports
from abstract_wrapper import AbstractWrapper
from type_enforcer import enforce_type


class PlaybackWrapper(AbstractWrapper):
    """<...>
    Implements the methods specified by AbstractWrapper, providing calls to the 
    library without the caller having to be aware of the used interface.

    Attributes:

    Methods:
        + __init__() - object constructor
        + write_analog() - sets 
        + read_analog() - reads 
        + write_digital() - sets 
        + read_digital() - reads 
    """
    def __init__(self, csv_path=''):
        """
        <...>
        Constructor for the wrapper object.
        
        Arguments:
            
        """
        channel_dict = self._load_csv_columns_to_dict(filepath=csv_path)
        channels = self._parse_channel_dict_to_lists(channel_dict)

        self.ain = channels['AIN']   # list of channels, each channel is a list of values

        # cast each channel list to a cycle iterable (circular list)
        for i in range(len(self.ain)):
            self.ain[i] = cycle(self.ain[i])

    
    # ----- CSV Utils ----- #
    def _parse_channel_dict_to_lists(channel_dict):
        """Returns dictionaries with two lists, one for AIN channels, and one for AOUT channels."""
        ain_keys = []   # tracks keys for simulated analog inputs
        aout_keys = []  # tracks keys for simulated analog outputs
        
        # parse keys by channel type
        for key in channel_dict.keys():
            if 'AIN' in key:
                ain_keys.append(key)
            elif 'AOUT' in key:
                aout_keys.append(key)
            else:
                raise ValueError('Not a valid channel key!')
            
        # sort both key lists to identify largest channel address in each
        ain_keys.sort()
        aout_keys.sort()

        # -- MAKE AIN LIST -- # 
        # generate empty list of empty input channels
        big_ain = ain_keys[-1].split('_')[-1]  # get the largest ain address
        num_ain = int(big_ain) + 1             # cast and add 1 to be zero-inclusive
        ain = [[]]*num_ain                     # list with empty element for each analog in

        # populate ain with channel values
        for key in ain_keys:
            index = int(key.split('_')[-1])    # use address as index
            ain[index] = channel_dict[key]

        # -- MAKE AOUT LIST -- #
        # generate empty list of empty output channels
        big_aout = aout_keys[-1].split('_')[-1]  # get the largest aout address
        num_aout = int(big_aout) + 1             # cast to int and add 1 to be zero-inclusive
        
        aout = [[]]*num_aout                     # list with empty element for each analog out

        # populate aout with channel values
        for key in aout_keys:
            index = int(key.split('_')[-1])    # use address as index
            aout[index] = channel_dict[key]

        # return both analog I/O lists in a dicitonary
        return {"AOUT": aout, "AIN": ain}


    def _load_csv_columns_to_dict(self,
                filepath:str=None,
                newline_char:str='',
                delimiter_char:str=',',
                quote_char:str='|'):
        """Accepts a file path to a CSV and returns a list of its unparsed rows."""
       
        # Parse CSV columns into lists for simulated analog I/O
        with open(filepath, newline=newline_char) as csvfile:
            # Get all rows
            dataReader = csv.DictReader(csvfile, delimiter=delimiter_char, quotechar=quote_char)
            
            column_keys = dataReader[0].keys()     # get all keys for columns in CSV
            raw_dicts = {}                  # generate empty dictionary for parsed CSV columns

            # Populate column dictionary with empty lists for each column
            for key in column_keys:
                # Check keys represent an analog channel
                if 'AIN' in key or 'AOUT' in key:   # exclude unknown keys
                    
                    # add valid keys to dictionary
                    try:
                        int(key.split('_')[-1]) # check address is int, raise exception otherwise
                        raw_dicts[key] = []     # map each valid key to an empty list
                    
                    # catch exceptions if address isnt int
                    except ValueError:
                        pass
            
            # Populate each column list with their values
            valid_keys = raw_dicts.keys()           # get valid channel keys
            for row in dataReader:                  # iterate over every row
                for key in valid_keys:              # get each value for the row by key
                    raw_dicts[key].append(row[key]) # append the column value to its list
            
            return raw_dicts

    # ----- ANALOG I/0 ----- #
    @enforce_type
    def write_analog(self, address:int, value:float|int) -> None:
        """Sets the output voltage of the DAC channel at the given address.
        
        Arguments:
            address: int - the address of the channel being written
            value: float|int - the voltage value to output from the channel (Volts)
        """
        pass
        
    
    @enforce_type
    def read_analog(self, address:int) -> float:
        """Returns the voltage value measured at the given ADC channel."""
        return self.ain[address].next()
    
    # ----- DIGITAL I/O ----- #
    @enforce_type
    def write_digital(self, address:int, level:bool) -> None:
        """Sets the output voltage level of the DOUT channel at the given address.
        
        Arguments:
            address: int - the address of the channel being written
            level: bool - voltage level to output
                True: High
                False: Low
        """
        if level:   # set on True
            pass
        else:       # clear on False
            pass
    
    @enforce_type
    def read_digital(self, address:int) -> bool:
        """Returns the voltage level measured at the given DIN channel.
        
        Returns:
            True: High
            False: Low
        """
        return None

    
# WRAPPER EXPORT
wrapper = PlaybackWrapper

# if __name__ == "__main__":
    # keys = ['AIN_1', 'bad', 'AIN_1.0', 'apple', 'AIN_2', 'butter', 'AOUT_aB', 'AOUT_1', 'AOUT_2', "cake"]
    # channels = []

    # for k in keys:
    #     if 'AIN' in k or 'AOUT' in k:
    #         split = k.split("_")
    #         try:
    #             channels.append([k, int(split[-1])])
    #         except ValueError:
    #             pass


    # for c in channels:
    #     print(c)


# if __name__ == "__main__":
#     a = {'AOUT_1': [1, 2, 3, 4],
#          'AOUT_4': [5, 6, 7, 8],
#          'AIN_3': [-1, -2, -3, -4],
#          'AIN_5': [-5, -6, -7, -8]}
    
#     b = PlaybackWrapper._parse_channel_dict_to_lists(a)

#     aout = b['AOUT']
#     ain = b['AIN']

#     print('\nAIN')
#     for i in range(len(ain)):
#         print(i, ain[i])

#     print('\nAOUT')
#     for i in range(len(aout)):
#         print(i, aout[i])