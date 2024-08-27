# author: figueroa_90894@students.pupt.edu
# status: WIP
#   - add docstrings

# built-in imports
import sys
import os
from enum import Enum, unique

# ----- PATH HAMMER ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 2             # how many parent folders to reach /plasmetry/src
    
    # Locate absolute path to /plasmetry/src
    parent = os.path.dirname(__file__)  # traverse directory upwards
    for _ in range(num_dir): parent = os.path.dirname(parent)
    print(f"Path Hammer: {parent}")     # expect absolute path to /plasmetry/src

    # Append all target folders to python path
    for dir in os.listdir(parent): sys.path.append(f"{parent}/{dir}")
    print(f"Path Hammer: folders appended")
# ----- END PATH HAMMER ----- #

# local imports
from hardware_interface.abstract_wrapper import AbstractWrapper as interface
from hardware_interface.hardware_objects import AnalogIn, AnalogOut, DigitalIn, DigitalOut

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

    def __init__(self, wrapper_cls:interface):
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
