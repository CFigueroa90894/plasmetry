"""G3 - Plasma Devs
Layer 4 - Hardware Interface - Component Factory
    Defines the ComponentFactory class, used to generate component objects.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    COMP - enumerator of component type identifiers
    ComponentFactory - reuses channel factory when creating hardware component objects
"""

# built-in imports
import sys
import os
from enum import Enum, unique

from typing import Tuple

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
    """The ComponentFactory generates hardware component objects to control their associated
    physical counterparts.
    
    Class Attributes:
        + ID: Enum - component types supported by this factory
        - __CHN: Enum - channel types used by this factory

    Instance Attributes:
        - __channel: ChannelFactory - generates channel objects that make up component objects

    Methods:
        + __init__() - initialize the component factory
        + make() - return generated hardware component object
        # _make_hv_amp() - instantiate a HighVoltAmp object
        # _make_volt_sweeper() - instantiate a VoltagerSweeper object
        # _make_volt_sensor() - instantiate a VoltageSensor object
        # _make_relay() - instantiate a RelaySet object
        - __make_analog_out() - instantiate an analog output channel
        - __make_analog_in() - instantiate an analog input channel
        - __make_digital_out() - instantiate a digital output channel
    """
    ID:COMP = COMP  # package component factory's valid IDs as class attributes
    __CHN = None    # placeholder for channel factory's supported objects

    def __init__(self, channel_factory):
        """Instantiates a ComponentFactory object with the given ChannelFactory object.
        
        Arguments:
            channel_factory - an instantiated ChannelFactory object
        """
        self.__channel = channel_factory
        self.__CHN = channel_factory.ID

    def make(self, type: COMP, *args, **kwargs):
        """<...>"""
        # Select component to instantiate
        match type:
            case COMP.HVAMP:  # HighVoltAmp
                return self._make_hv_amp(*args, **kwargs)
            
            case COMP.SWEEP:  # VoltageSweeper
                return self._make_volt_sweeper(*args, **kwargs)
            
            case COMP.VSENS:  # VoltageSensor
                return self._make_volt_sensor(*args, **kwargs)
            
            case COMP.RLSET:  # RelaySet
                return self._make_relay(*args, **kwargs)


    # ----- Component Instantiators ----- #
    def _make_hv_amp(self, address:int, *args, **kwargs):
        """Return an instatiated HighVoltAmp object by making an analog output channel and
        forwarding other given arguments.
        """
        output_channel = self.__make_analog_out(address)
        return HighVoltAmp(analog_out=output_channel, *args, **kwargs)


    def _make_volt_sweeper(self, address:int, *args, **kwargs):
        """Return an instatiated VoltagerSweeper object by making an analog output channel and
        forwarding other given arguments.
        """
        output_channel = self.__make_analog_out(address)
        return VoltageSweeper(analog_out=output_channel, *args, **kwargs)


    def _make_volt_sensor(self, address:int, *args, **kwargs):
        """Return an instatiated VoltageSensor object by making an analog input channel and
        forwarding other given arguments.
        """
        input_channel = self.__make_analog_in(address)
        return VoltageSensor(analog_in=input_channel, *args, **kwargs)


    def _make_relay(self, address:Tuple[int], *args, **kwargs):
        """Return an instatiated RelaySet by iteratively generating digital output channels."""
        output_channels = []    # aggregate all digital output channels
        
        # instantiate individual digital output channels
        for relay_address in address:   
            output_channels.append(self.__make_digital_out(relay_address))
        
        output_channels = tuple(output_channels)    # cast list to tuple
        return RelaySet(digital_outputs=output_channels, *args, **kwargs)


    # ----- Channel Instantiators ----- #
    def __make_analog_out(self, address:int):
        """Return an analog output channel created by the channel factory."""
        return self.__channel.make(address, self.__CHN.AO)
    

    def __make_analog_in(self, address:int):
        """Return an analog input channel created by the channel factory."""
        return self.__channel.make(address, self.__CHN.AI)


    def __make_digital_out(self, address:int):
        """Return a digital output channel created by the channel factory."""
        return self.__channel.make(address, self.__CHN.DO)

