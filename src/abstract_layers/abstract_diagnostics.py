"""G3 - Plasma Devs
Layer 3 - Diagnostics Interface
    Defines the required public functionality for concrete implementations of the Diagnostics Layer.

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

class AbstractDiagnostics(AbstractBaseLayer):
    """This class defines all public methods that 'Layer 3 - Diagnostics' implementations must
    must exppose to the upper layers.

    Public methods include start/stop/setup functions for diagnostics, a system-wide shutdown.
    
    The Diagnostics Layer CANNOT be instantiable without arguments. Concrete implementations may
    specify optional arguments for customizable behavior.

    Layer Setup:
        __init__() - initializes this layer, its subcomponents, and the lower layer

    System Actions:
        setup_diagnostics() - begin initializations for plasma diagnostics
        start_diagnostics() - perform plasma diagnostics
        stop_diagnostics() - halt plasma diagnostics
        diagnostic_shutdown() - initiate diagnostic layer shutdown
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """Called by upper layers to instantiate this layer.
        
        Default or custom subcomponents will be instantiated and assembled as a whole, as well as
        initializing the lower layers. Custom subcomponents and lower layers should be specified
        through class methods before instantiating this layer.

        Arguments:
            status_flags: StatusFlags - control object to indicate system states
            command_flags: CommandFlags - control object to trigger system behavior
            results_buff: Queue - thread-safe buffer to pass results to upper layers
                default: Queue - if no queue given, creates a new one, accesible as an attribute
            keysets: dict - all sets of keys and enumerators used to access structured data
        """
        super().__init__(*args, **kwargs)   # call parent constructor

    @abstractmethod
    def setup_diagnostics(self):
        """Called by upper layers to prepare the diagnostic layer for plasma diagnostic operations.
        
        Instantiates and primes all required plasma diagnostic objects, then awaits until this
        interface's `start_diagnostics()` method is called to proceed.

        Exceptions:
            RuntimeError: `setup_diagnostics()` was called while:
                - plasma diagnostics are being performed, or
                - system shutdown is underway
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")
    
    @abstractmethod
    def start_diagnostics(self):
        """Called by upper layers to trigger plasma diagnostics operations in this layer.

        Exceptions:
            RutimeError: `start_experiment()` was called:
                - without first calling `setup_diagnostics()`, or
                - while system shutdown was underway 
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")
    
    @abstractmethod
    def stop_diagnostics(self):
        """Called by upper layers halt plasma diagnostics operations in this layer.
        
        This layer will attempt to complete all pending operations, including data sampling, 
        parameter calculations, and aggregating results, and passing them to the upper layer before
        it returns to its idle state.
        
        Exceptions:
            RuntimeError: `stop_diagnostics()` was called while:
                - system was not performing plasma diagnostics, or
                - system shutdown was underway
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")
        
    @abstractmethod
    def diagnostics_shutdown(self):
        """Called by upper layers to initiates this layer's shutdown process.
        
        This Diagnostic Layer will attempt to complete all pending operations before finally
        terminating all its subcomponents.

        * NOTE: this call blocks until the diagnostic layer has terminated to prevent corruption.
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")