"""G3 - Plasma Devs
Layer 4 - Hardware Interface - Concrete Implementation
    Implements the interface specified by AbstractHardware class.
    <...>

author: figueroa_90894@students.pupr.edu
status: WIP
  - add docstrings to module header
  - implement reset_components() method
  - validate with team
"""

# built-in imports
import sys
import os

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:
    """Resolve absolute imports by recursing into subdirs and appending them to python path."""
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
    # get subdirs, exclude unwanted
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude]
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: {src_abs}")

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(1, ['plasmetry', 'src'], ['__pycache__'])
# ----- END PATH HAMMER ----- #


# local imports
from abstract_hardware import AbstractHardware


# TO DO
class HardwareLayer(AbstractHardware):
    """This class implements the Hardware Interface Layer's specified interface, providing
    public access to its required functionality. As a simple implementation, its main concern
    is instantiating the factories that upper layer's will call to generate software objects
    associated with the ADC/DAC I/O channels.

    Class Attributes:
        + hardware_wrapper_mod - the module to be loaded, wraps the ADC/DAC's library
        + channel_factory_mod - module to be loaded, generates ADC/DAC channel objects
        + component_factory_mod - module to be loaded, generates hardware representations

    Instance Attributes:
        # _wrapper - instantiated wrapper object
        # _channel - instantiated channel factory
        # _component - instantiated hardware component factory

    Methods:
        + __init__() - initialize the HardwareLayer object
        + get_component_factory() - returns the instantiated component factory
        + get_channel_factory() - returns the instantiated channel factory
        + reset_components() - TO BE IMPLEMENTED - should disable all relays and zero all amps
        # _load_all_subcomponents() - returns dictionary of all subcomponent classes
        ^# _load_mod() - imports and returns a module, specified by name
        # _info() - returns a tuple containing info about the layer's instantiated subcomponents
    """

    # Default subcomponent module names
    hardware_wrapper_mod = 'daqc2plate_wrapper'
    channel_factory_mod = 'channel_factory'
    component_factory_mod = 'component_factory'

    def __init__(self):
        """The constructor for HardwareLayer class. Takes no arguments. Loads subcomponents then
        assembles the layer by instantiating them.
        """
        # load subcomponents
        sub = self._load_all_subcomponents()
        hardware_wrapper_cls = sub["hardware_wrapper"]
        channel_factory_cls = sub["channel_factory"]
        component_factory_cls = sub["component_factory"]

        # assemble layer's subcomponents
        self._wrapper = hardware_wrapper_cls()
        self._channel = channel_factory_cls(hardware_wrapper=self._wrapper)
        self._component = component_factory_cls(channel_factory=self._channel)

    def get_component_factory(self):
        """Return the instantiated ComponentFactory."""
        return self._component
    
    def get_channel_factory(self):
        """Return the instantiated ChannelFactory."""
        return self._channel
    
    # TO DO
    def reset_components(self):
        """<...>"""
        raise NotImplementedError
    
    def _load_all_subcomponents(self):
        """Returns a dictionary with all the classes corresponding to this layer."""
        classes = {
            "hardware_wrapper": self._load_mod(self.hardware_wrapper_mod).wrapper,
            "channel_factory": self._load_mod(self.channel_factory_mod).ChannelFactory,
            "component_factory": self._load_mod(self.component_factory_mod).ComponentFactory
        }
        return classes
    
    def _info(self):
        """Return info about the instantiated layer's subcomponents.
        
        Used for debugging system integration.
        """
        sub = [('Hardware Interface', 'Hardware Wrapper', str(self._wrapper)),
               ('Hardware Interface', 'Channel Factory', str(self._channel)),
               ('Hardware Interface', 'Component Factory', str(self._component))]
        return sub


a = HardwareLayer
a.hardware_wrapper_mod = "counter_wrapper"
a = a()
for info in a._info():
    print(info)