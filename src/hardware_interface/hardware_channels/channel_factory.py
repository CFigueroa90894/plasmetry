"""G3 - Plasma Devs
Layer 1 - Hardware Interface - Channel Factory
    Defines the ChannelFactory class, used to generate channel objects.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    CHN - enumarator of channel type identifiers
    ChannelFactory - reuses hardware wrapper when creating channel objects
"""

# built-in imports
import sys
import os
from enum import Enum, unique

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
    path_hammer(2, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
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

    Class Attributes:
        + ID - enumerator class of supported channel types

    Instance Attributes:
        # _wrapper - instantiated hardware wrapper

    Methods:
        + __init__() - factory constructor
        + make() - returns an instantiated channel object
    """
    ID:CHN = CHN   # package factory's valid IDs as class attribute

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
        """Generates a channel for the given type with the given address.
        
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
