"""G3 - Plasma Devs
Layer 1 - Hardware Interface - Concrete Implementation
    Implements the interface specified by AbstractHardware class. Instantiates hardware factories
    for use by upper layers, as well as providing a failsafe to reset all hardware I/O channels.

author: figueroa_90894@students.pupr.edu
status: DONE

Classes:
    HardwareLayer
"""

# built-in imports
import sys
import os

import time

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
    path_hammer(1, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #


# local imports
from abstract_hardware import AbstractHardware

# local config
RELAY_PAUSE = 3


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
        + reset_components() - disables all digital outputs and sets all analog outputs to zero
        # _load_all_subcomponents() - returns dictionary of all subcomponent classes
        ^# _load_mod() - imports and returns a module, specified by name
        # _info() - returns a tuple containing info about the layer's instantiated subcomponents
    """

    # Default subcomponent module names
    hardware_wrapper_mod = 'daqc2plate_wrapper'
    channel_factory_mod = 'channel_factory'
    component_factory_mod = 'component_factory'

    def __init__(self, name:str="HWINT", *args, **kwargs):
        """The constructor for HardwareLayer class. Takes no arguments. Loads subcomponents then
        assembles the layer by instantiating them.
        """
        super().__init__(*args, name=name, **kwargs)    # call parent constructor

        # load subcomponents
        sub = self._load_all_subcomponents()
        hardware_wrapper_cls = sub["hardware_wrapper"]
        channel_factory_cls = sub["channel_factory"]
        component_factory_cls = sub["component_factory"]

        # assemble layer's subcomponents
        self._wrapper = hardware_wrapper_cls()
        self._channel = channel_factory_cls(hardware_wrapper=self._wrapper)
        self._component = component_factory_cls(channel_factory=self._channel)

        # Try to pass the wrapper a SayWriter object
        self._wrapper._say_obj = self._say_obj

        self.say("hardware layer initialized...")

    def get_component_factory(self):
        """Return the instantiated ComponentFactory."""
        return self._component
    
    def get_channel_factory(self):
        """Return the instantiated ChannelFactory."""
        return self._channel
    
    def reset_components(self):
        """This function attempts clear all output channels of the ADC/DAC associated with this
        layer's hardware wrapper. For DAC and DOUT channels, this function iterates over channel
        addresses in separate loops until the wrapped library raises an error for an out bounds
        address.
        """
        # reset digital outputs
        self.say("clearing DOUTs...")
        try:  
            counter = 0
            while 1:    # loop until an exception is raised
                self._wrapper.write_digital(counter, False)
                counter += 1
        except Exception:
            self.say("DOUTs cleared")

        # pause to allow relays to disengage
        time.sleep(RELAY_PAUSE)

        # reset analog outputs
        self.say("clearing DACs...")
        try:  
            counter = 0
            while 1:    # loop until an exception is raised
                self._wrapper.write_analog(counter, 0)
                counter += 1
        except Exception:
            self.say("DACs cleared")

    def _load_all_subcomponents(self):
        """Returns a dictionary with all the subcomponent classes corresponding to this layer."""
        classes = {
            "hardware_wrapper": self._load_mod(self.hardware_wrapper_mod).wrapper,
            "channel_factory": self._load_mod(self.channel_factory_mod).ChannelFactory,
            "component_factory": self._load_mod(self.component_factory_mod).ComponentFactory
        }
        return classes
    
    def layer_shutdown(self):
        """Terminates the layer. Resets all output channels and destroys object references."""
        self.say("shutting down hardware layer...")
        self.reset_components() # reset all components

        # delete subcomponent references
        del self._component
        del self._channel
        del self._wrapper

        self.say("hardware layer terminated")

    def _info(self):
        """Return info about the instantiated layer's subcomponents.
        
        Used for debugging system integration.
        """
        sub = [('Hardware Interface', 'Hardware Wrapper', str(self._wrapper)),
               ('Hardware Interface', 'Channel Factory', str(self._channel)),
               ('Hardware Interface', 'Component Factory', str(self._component))]
        return sub
    
