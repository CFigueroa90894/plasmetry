# author: figueroa_90894@students.pupt.edu
# status: WIP
#   - add docstrings

# built-in imports
from enum import Enum, unique

# local imports
from abstract_wrapper import AbstractWrapper as interface
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
