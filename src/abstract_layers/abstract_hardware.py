"""G3 - Plasma Devs
Layer 4 - Hardware Interface
    Defines the required public functionality for concrete implementations of the Hardware
    Interface Layer.

    Unlike other layers, the Hardware Interface Layer does not perform diagnostic operations
    directly. Instead, it provides hardware objects to the upper layers that model the behavior of
    electronic components. It is upper layers' responsibility to operate and control the hardware
    components through the objects provided by this layer.

author: figueroa_90894@students.pupr.edu
status: WIP
    - confirm and agree with team on interface specifications
"""

# built-in imports
import sys
import os

from abc import abstractmethod

# ----- PATH HAMMER v2.7 ----- resolve absolute imports ----- #
def path_hammer(num_dir:int, root_target:list[str], exclude:list[str], suffix:str="") -> None:  # execute snippet if current script was run directly 
    """Resolve absolute imports by recusring into subdirectories and appending them to python path."""
    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..' + suffix)
    assert src_abs.split('\\')[-1*len(root_target):] == root_target   # validate correct top folder
    
    dirs = [sub[0] for sub in os.walk(src_abs) if sub[0].split('\\')[-1] not in exclude] # get subdirs, exclude unwanted
    for dir in dirs: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: {src_abs}")

if __name__ == "__main__":  # execute path hammer if this script is run directly
    path_hammer(2, ['plasmetry', 'src'], ['__pycache__'], suffix='/src')  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

# local imports
from abstract_base_layer import AbstractBaseLayer

class AbstractHardware(AbstractBaseLayer):
    """This class defines all public methods that 'Layer 4 - Hardware Interface' implementations
    must expose to upper layers.
    
    The two public methods offered are getters to the factories that generate configured 
    hardware objects. This layer's primary responsibility is to abstract the details of instanting,
    mapping, and low-level control between the software and hardware components.

    Public Methods:
        get_component_factory() - returns factory for complex hardware control objects
        get_channel_factory() - returns factory for basic hardware control objects 
    """

    @abstractmethod
    def __init__(self):
        """Called by upper layers to instantiate this layer.
        
        Default or custom subcomponents will be instantiated and assembled as a whole. This layer
        should instantiate all hardware component/channel objects, and return them as requested by
        the upper layers through the corresponding factories.
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")
    
    @abstractmethod
    def get_component_factory(self):
        """Return the instantiated factory that produces hardware component objects."""
        raise NotImplementedError("This function was not overloaded in the subclass!")
    
    @abstractmethod
    def get_channel_factory(self):
        """Return the instantiated factory that produces hardware channel objects."""
        raise NotImplementedError("This function was not overloaded in the subclass!")


    @abstractmethod
    def reset_components(self):
        """Called by upper layers to disable all relays, digital outputs, and reset the HV amp
        outputs to zero.
        
        All hardware objects are tracked independently of probe selection in order to reset the
        system as a whole when changing operating modes. Though each probe will disable the
        hardware it used in its own cleanup script, this function should be called before beginning
        a new operating mode as a failsafe.
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")