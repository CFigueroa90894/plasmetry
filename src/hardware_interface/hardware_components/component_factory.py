"""G3 - Plasma Devs
Layer 4 - Hardware Interface - Component Factory
    Defines the ComponentFactory class, used to generate component objects.

author: figueroa_90894@students.pupt.edu
status: WIP
  - add docstrings
  - validate with team
"""

# built-in imports
import sys
import os
from enum import Enum, unique

from typing import Tuple

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
from component_objects import HighVoltAmp, VoltageSweeper, VoltageSensor, RelaySet


# COMPONENT TYPES
@unique
class COMP(Enum):
    """Enumerator to identify component types; arguments to the factory's make() method."""
    HVAMP = 0   # HighVoltAmp
    SWEEP = 1   # VoltageSweeper
    VSENS = 2   # VoltageSensor
    RLSET = 3   # RelaySet


class ComponentFactory:
    """<...>
    
    Class Attributes:
        + ID: Enum - component types supported by this factory
        - CHN: Enum - channel types used by this factory

    Instance Attributes:
        - __channel: ChannelFactory - generates channel objects that make up component objects
    """
    ID:COMP = COMP  # package component factory's valid IDs as class attributes
    __CHN = None    # placeholder for channel factory's supported objects

    def __init__(self, channel_factory):
        """<...>
        
        Arguments:
            channel_factory - an instantiated ChannelFactory object
        """
        self.__channel = channel_factory
        self.__CHN = channel_factory.ID

    def make(self, type: COMP, *args, **kwargs):
        """<...>"""
        # Select component to instantiate
        match type:
            case COMP.HVAMP:
                return self._make_hv_amp(*args, **kwargs)
            
            case COMP.SWEEP:
                return self._make_volt_sweeper(*args, **kwargs)
            
            case COMP.VSENS:
                return self._make_volt_sensor(*args, **kwargs)
            
            case COMP.RLSET:
                return self._make_relay(*args, **kwargs)


    # ----- Component Instantiators ----- #
    def _make_hv_amp(self, address:int, *args, **kwargs):
        """<...>"""
        output_channel = self.__make_analog_out(address)
        return HighVoltAmp(analog_out=output_channel, *args, **kwargs)


    def _make_volt_sweeper(self, address:int, *args, **kwargs):
        """<...>"""
        output_channel = self.__make_analog_out(address)
        return VoltageSweeper(analog_out=output_channel, *args, **kwargs)


    def _make_volt_sensor(self, address:int, *args, **kwargs):
        """<...>"""
        input_channel = self.__make_analog_in(address)
        return VoltageSensor(analog_in=input_channel, *args, **kwargs)


    def _make_relay(self, address:Tuple[int], *args, **kwargs):
        """<...>"""
        output_channels = []    # aggregate all digital output channels
        
        # instantiate individual digital output channels
        for relay_address in address:   
            output_channels.append(self.__make_digital_out(relay_address))
        
        output_channels = tuple(output_channels)    # cast list to tuple
        return RelaySet(digital_outputs=output_channels, *args, **kwargs)


    # ----- Channel Instantiators ----- #
    def __make_analog_out(self, address:int):
        """<...>"""
        return self.__channel.make(address, self.__CHN.AO)
    

    def __make_analog_in(self, address:int):
        """<...>"""
        return self.__channel.make(address, self.__CHN.AI)


    def __make_digital_out(self, address:int):
        """<...>"""
        return self.__channel.make(address, self.__CHN.DO)

