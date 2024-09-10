# author: figueroa_90894@students.pupt.edu
# status: WIP
#   - add docstrings

# built-in imports
import sys
import os
from enum import Enum, unique

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 1             # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #

# local imports
from abstract_wrapper import AbstractWrapper as interface
from daqc2plate_wrapper import DAQC2plateWrapper
from hardware_objects import AnalogIn, AnalogOut, DigitalIn, DigitalOut

# CHANNEL TYPES
@unique
class CHN(Enum):
    """<...>"""
    DO = 0
    AO = 1
    DI = 2
    AI = 3


class HardwareFactory:
    """<...>"""
    IDs:CHN = CHN   # package factory's valid IDs as class attribute

    def __init__(self, wrapper_cls:interface=DAQC2plateWrapper):
        """<...>
        <hardware must be class, not obj>"""
        self.hardware_wrapper = wrapper_cls()

    def make(self, address:int, type:CHN):
        """<...>"""
        
        # Pack hardware object's arguments
        hardware_args = {"address": address,
                         "hardware_wrapper": self.hardware_wrapper}

        # Select class to instantiate channel
        match type:
            # Outputs
            case CHN.DO:
                Channel_Class = DigitalOut
            case CHN.AO:
                Channel_Class = AnalogOut
            
            # Inputs
            case CHN.DI:
                Channel_Class = DigitalIn
            case CHN.AI:
                Channel_Class = AnalogIn
            
            # Edge case
            case _:
                raise ValueError(f"Unknown channel type: {type}")

        # Initialize and return Channel Object using packed arguments.
        return Channel_Class(**hardware_args)
