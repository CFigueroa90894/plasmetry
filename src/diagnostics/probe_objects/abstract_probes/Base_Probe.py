# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - 

# built-in imports
import sys
import os

from threading import Event             # thread-safe signaling mechanisms
from queue import Queue                 # thread-safe data buffer
from abc import ABCMeta, abstractmethod     # enforce abstraction

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
    path_hammer(3, ['plasmetry', 'src'], ['__pycache__'])  # hammer subdirs in plasmetry/src
# ----- END PATH HAMMER ----- #

# local imports
from base_thread import BaseThread

class BaseProbe(BaseThread, metaclass=ABCMeta):
    """The top-level, abstract class for all probe implementations.
    Includes initialization for flags, data buffer, equations, config, and data buffer.
    Defines abstract methods run(), and _graceful_exit().
    
    Attributes:
        + probe_id - identifier for the probe's type
        + sys_ref: dict - reference to system settings
        + config_ref: dict - reference to user settings
        + status_flags - state indicators
        + command_flags - action triggers
        + data_buff: Queue - buffer to return data samples
        + sampling_rate: int - samples to obtain per second (Hz)
        + relay_set: RelaySet - collection of relays

    Methods:
        + __init__() - initialize the object, called by subclasses
        + run() - perform data acquistion, override in subclasses
        # _graceful_exit() - complete pending actions and temrinate, override in subclasses
    """
    def __init__(self,
                 probe_id,
                 sys_ref:dict,
                 config_ref:dict,
                 status_flags,
                 command_flags,
                 equations:list,
                 data_buff:Queue,
                 sampling_rate:int,
                 num_samples:int,
                 relay_set:int,
                 sample_trig:Event=None,
                 *args, **kwargs
                 ):
        """<...>"""
        super().__init__(*args, **kwargs)   # call parent constructor

        # PROBE INFO
        self.id = probe_id                  # identifier for testing and validation
        self.sys_ref = sys_ref              # dictionary with system settings
        self.config_ref = config_ref        # dictionary with user settings
        self.num_samples = num_samples      # samples per sweep (LP/EA) or averaging window (TLP)

        # SYSTEM FLAGS
        self.status_flags = status_flags    # system state indicators
        self.command_flags = command_flags  # action triggers
        self.diagnose = self.status_flags.diagnose  # the most checked flag in a probe thread loop
        
        # PROBE OPERATION
        self.equations = equations  # list of callables to calculate plasma parameters
        self.data_buff = data_buff  # thread-safe queue, pass data samples to probe operation
        self.sampling_rate = sampling_rate      # samples to obtain per second, Hertz (Hz)
        self.sample_trig = sample_trig          # indicates when the next sample should be obtained

        # PROBE SUBCOMPONENTS
        self.relay_set = relay_set          # collection of relays that select probe operating mode
    
    @abstractmethod
    def run(self) -> None:
        """Executes the data acquisition process. Children must override it."""
        super().run()   # call parent run method
    
    @abstractmethod
    def preprocess_samples(self, samples:dict):
        """<...>"""
        raise NotImplementedError("This method was not overloaded in the subclass!")

    def say(self, msg):
        """<...>"""
        super().say(msg)

