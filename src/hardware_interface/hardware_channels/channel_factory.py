# author: figueroa_90894@students.pupt.edu
# status: WIP
#   - add docstrings

# built-in imports
import sys
import os
from enum import Enum, unique

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 2             # how many parent folders to reach /plasmetry/src

    # absolute path to plasmetry/src
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..')
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    # get subdirs, exclude __pycache__
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__']
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
# ----- END PATH HAMMER ----- #

# local imports
from abstract_wrapper import AbstractWrapper as interface
from channel_objects import AnalogIn, AnalogOut, DigitalIn, DigitalOut

# CHANNEL TYPES
@unique
class CHN(Enum):
    """Enumerator to identify channel types; argument to the factory's make() method."""
    DO = 0
    AO = 1
    DI = 2
    AI = 3


class ChannelFactory:
    """The ChannelFactory generates channel objects associated with analog and digital I/O ports.
    
    The ChannelFactory class abstracts away need to directly import and instantiate the various
    channel classes supported by the Hardware Interface Layer. It must be instantiated by passing
    a hardware wrapper object.
    """
    IDs:CHN = CHN   # package factory's valid IDs as class attribute

    def __init__(self, hardware_wrapper:interface):
        """Instantiates a ChannelFactory object with the given hardware wrapper.
        
        Arguments:
            hardware_wrapper: subclass of AbstractWrapper - passed to channel objects
        """
        # Validate given argument subclasses the AbstractWrapper class
        if not issubclass(type(hardware_wrapper), interface):
            err_msg = f"hardware_wrapper must subclass AbstractWrapper!"
            err_msg += f" Given {type(hardware_wrapper)}"
            raise TypeError(err_msg)
        
        # Save arguments
        self._wrapper = hardware_wrapper

    def make(self, address:int, type:CHN):
        """Generates a channel for the given type with given address.
        
        Arguments:
            address: int - associated address for the required channel object
            type: Enum - type of the channel to be created

        Returns:
            channel object - subclassed from BaseChannel
        """
        # Pack channel object's arguments
        channel_args = {"address": address,
                         "hardware_wrapper": self._wrapper}

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
        return Channel_Class(**channel_args)
