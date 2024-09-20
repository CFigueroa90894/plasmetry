"""G3 - Plasma Devs
Layer 2 - Control Interface
    Defines the required public functionality for concrete implementations of the Control Layer.

author: figueroa_90894@students.pupr.edu
status: DONE

    The Control Layer is responsible for coordinating top level functionality between all the
    architecture's layer, and serves as the entry point through which the UI layer (front end)
    interacts with the rest of the software.

Classes:
    AbstractControl
"""

# built-in imports
import sys
import os

from abc import abstractmethod
from threading import Event
from typing import Tuple

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
    path_hammer(2, ['plasmetry', 'src'], ['__pycache__'], suffix='/src')
# ----- END PATH HAMMER ----- #

# local imports
from abstract_base_layer import AbstractBaseLayer

class AbstractControl(AbstractBaseLayer):
    """This class defines all public methods that 'Layer 2 - Control' implementations must
    expose to the upper layers.
    
    Public methods include setters/getters for config values, config file operations, 
    start/stop/setup functions for experiments, getters for control objects, and a 
    system-wide shutdown method.

    The Control Layer MUST be instantiable without arguments. Concrete implementations may
    implement optional arguments for customizable behavior.
    

    Attributes:
        ^+ name: str - name identifying the layer for printing purposes
        ^# _say_obj: SayWriter - text output object

    Layer Setup:
        ^+ __init__() - instantiates an object of the class

    Config Methods:
        + set_config() - save a config value to memory
        + get_config() - read a config value from memory
        + save_config_file() - write config values in memory to a config file
        + load_config_file() - load config values into memory from a config file
    
    System Actions:
        + setup_experiment() - begin initializations for plasma diagnostics
        + start_experiment() - perform plasma diagnostics
        + stop_experiment() - halt plasma diagnostics
        + layer_shutdown() - initiate system-wide shutdown

    Control Object Getters:
        + get_real_time_container() - returns object concurrently updated with new data
        + get_status_flags() - returns state indicators
        + get_command_flags() - returns action triggers

    Layer Utils:
        ^+ say() - print messages to configured output
        ^# _info() - returns information about a layer's subcomponents
        ^# _load_all_subcomponents() - returns uninstantiated classes of subcomponents
        ^# _load_mod() - returns a module for a subcomponent
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """Called by upper layers to instantiate this layer.
        
        Default or custom subcomponents will be instantiated and assembled as a whole, as well as
        initializing the lower layers.
        """
        super().__init__(*args, **kwargs)   # call parent constructor

    @abstractmethod
    def set_config(self, probe_id, key:str, value: any) -> bool:
        """Modifies a config value (or object) in memory specified by the given key. Returns True if
        the value was successfully committed to memory.

        Arguments:
            probe_id - specifies the probe to which the config value corresponds
            key: str - identifier for the value to be modified
            value: any - new object or value to be committed to memory

        Return: bool
            True: change was successful
            False: value is invalid and the change was rejected
            
            * NOTE: If the frontend devs find it useful, backend devs could modify this method to
            return a tuple containing the offending value, or a perhaps an explanation for why it
            was rejected. For example: (True | False, bad_value, reason)

        Exceptions:
            KeyError: key is not used in memory
            TypeError: key's type is not supported
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")
    

    @abstractmethod
    def get_config(self, probe_id, key:str) -> any:
        """Returns a config value or object in memory, specified by the given key.
        
        Arguments:
            probe_id - specifies the probe to which the config value corresponds
            key:str - the identifier for the value that is being requested

        Exceptions:
            KeyError: key is not used in memory
            TypeError: key's type is not supported
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")
    

    @abstractmethod
    def save_config_file(self, filename:str) -> bool:
        """Attempts to save the config values in memory to a config file with the given file name.
        Existing files will be overwritten. Returns True if the file was successfully saved.

        Arguments:
            filename: str - Name of the new or existing file to write.

        Return: bool
            True: file successfully created or overwritten
            False: file could not be created or overwritten
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")
    

    @abstractmethod
    def load_config_file(self, filename:str=None) -> None:
        """Attempts to read a config file into memory, specified by the given file name.
        
        * NOTE: If no filename is specified, the system will load default config values into memory.

        Arguments:
            filename: str - the name of an existing file to load into memory
                default: None - load default values

        Exceptions:
            FileNotFoundError: the specified file does not exist
            ValueError: config values in requested file are invalid
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")


    @abstractmethod
    def get_real_time_container(self) -> Tuple[dict, Event]:
        """Returns a tuple consisting of a thread-safe dictionary and an Event object from the
        built-in threading module.
        
        The dictionary will be updated in-place with the most recent plasma parameters that must
        be displayed to the user. The Event flag will be set when new data is available.

        * NOTE: The upper layers are responsible for clearing the Event flag once the new data is
        read, to prevent re-reading stale data. The paramater container will be overwritten by the
        lower layers as new data is available, without buffering un-read data, and regardless of
        the Event flag's state.
        
        Return: tuple(dict, Event)
            dict: real-time parameter container, updated concurrently by lower layers
            Event: built-in signaling mechanism, set when new data is available
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")


    @abstractmethod
    def setup_experiment(self, probe_id) -> None:
        """Called by upper layers to prepare the system for plasma diagnostic operations.

        Notifies lower layers to begin plasma diagnostic initializations. When ready, lower levels
        will wait until this interface's `start_experiment()` method is called before beginning
        plasma diagnostics.

        Arguments:
            probe_id - identifier for the selected probe, used to select which config set will
                be passed to the lower layers
        Exceptions:
            RuntimeError: `setup_experiment()` was called while:
                - plasma diagnostics are being performed, or
                - system shutdown is underway
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")


    @abstractmethod
    def start_experiment(self) -> None:
        """Called by upper layers to trigger plasma diagnostic operations in lower layers.

        Exceptions:
            RuntimeError: `start_experiment()` was called:
                - without first calling `setup_experiment()`, or
                - while system shutdown is underway
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")


    @abstractmethod
    def stop_experiment(self) -> None:
        """Called by upper layers to halt plasma diagnostic operations in lower layers.
        
        This layer will attempt to complete all pending operations. It will signal lower layers
        that they must halt diagnsotics, then await the results of the experiment returned by the
        diagnostic layer. These results will be formatted and stored by this layer, before
        returning to its idle state.

        Exceptions:
            RuntimeError: `stop_experiment()` was called while:
                - system was not performing plasma diagnostics, or
                - system shutdown was underway
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")


    @abstractmethod
    def layer_shutdown(self) -> None:
        """Called by upper layers to initiate a system-wide shutdown.
        
        Lower layers will attempt to complete pending operations, then terminate their processes.
        * NOTE: this call blocks until lower layers have terminated to prevent corruption.
        This layer should await until all buffered results are saved to files before terminating
        its subcomponents.
        """
        raise NotImplementedError("This function was not overloaded in the subclass!")


    @abstractmethod
    def get_status_flags(self) -> object:
        """Returns the system's StatusFlag control object."""
        raise NotImplementedError("This function was not overloaded in the subclass!")


    @abstractmethod
    def get_command_flags(self) -> object:
        """Returns the system's CommandFlags control object."""
        raise NotImplementedError("This function was not overloaded in the subclass!")