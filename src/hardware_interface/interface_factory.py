# author: figueroa_90894@students.pupt.edu
# status: WIP
#   - add docstrings

# built-in imports
from enum import Enum, unique

# local imports
from abstract_interface import AbstractWrapper as interface
from interface_objects import AnalogIn, AnalogOut, DigitalIn, DigitalOut

# ----- CHANNEL TYPES ----- #
@unique
class CHN(Enum):
    """<...>"""
    DO = 0
    AO = 1
    DI = 2
    AI = 3

# ----- FACTORY ----- #
class InterfaceFactory:
    def __init__(self, hardware_cls:interface):
        """<...>
        <hardware must be class, not obj>"""
        self.hardware = hardware_cls()

    def Channel(self, address:int, type:CHN):
        """<...>"""
        match type:
            # Outputs
            case CHN.DO:
                return DigitalOut(address=address, hardware_obj=self.hardware)
            case CHN.AO:
                return AnalogOut(address=address, hardware_obj=self.hardware)
            
            # Inputs
            case CHN.DI:
                return DigitalIn(address=address, hardware_obj=self.hardware)
            case CHN.AI:
                return AnalogIn(address=address, hardware_obj=self.hardware)
            
            # Edge case
            case _:
                raise ValueError(f"Unknown channel type: {type}")
                  
                  
