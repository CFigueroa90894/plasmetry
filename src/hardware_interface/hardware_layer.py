"""G3 - Plasma Devs
Layer 4 - Hardware Interface - Concrete Implementation
    Implements the interface specified by AbstractHardware class.
    <...>

author: figueroa_90894@students.pupt.edu
status: WIP
  - add docstrings
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


# class HardwareLayer(AbstractHardware):
class HardwareLayer(AbstractHardware):
    """<...>"""
    hardware_wrapper_modname = 'daqc2plate_wrapper'
    channel_factory_modname = 'channel_factory'
    component_factory_modname = 'component_factory'

    def __init__(self):
        """<...>"""
        # load layer subcomponents
        hardware_wrapper_cls = __import__(self.hardware_wrapper_modname).wrapper
        channel_factory_cls = __import__(self.hardware_wrapper_modname).ChannelFactory
        component_factory_cls = __import__(self.component_factory_modname).ComponentFactory

        # assemble subcomponents
        self.__wrapper = hardware_wrapper_cls()
        self.__channel = channel_factory_cls(hardware_wrapper=self.__wrapper)
        self.__component = component_factory_cls(channel_factory=self.__channel)

    def get_component_factory(self):
        """<...>"""
        return self.__component
    
    def get_channel_factory(self):
        """<...>"""
        return self.__channel
    
    def reset_components(self):
        """<...>"""
        raise NotImplementedError

