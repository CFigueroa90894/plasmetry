# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - 

# built-in imports
import sys
import os

from threading import Event             # thread-safe signaling mechanisms
from queue import Queue                 # thread-safe data buffer
from abc import ABCMeta, abstractmethod     # enforce abstraction

# ----- PATH HAMMER v2.4 ----- resolve absolute imports ----- #
if __name__ == "__main__":  # execute snippet if current script was run directly 
    num_dir = 3             # how many parent folders to reach /plasmetry/src

    src_abs = os.path.abspath(os.path.dirname(__file__) + num_dir*'/..') # absolute path to plasmetry/src
    print(f"Path Hammer: {src_abs}")
    split = src_abs.split('\\')     # separate path into folders for validation
    assert split[-2] == 'plasmetry' and split[-1] == 'src'  # validate correct top folder
    
    targets = [x[0] for x in os.walk(src_abs) if x[0].split('\\')[-1]!='__pycache__'] # get subdirs, exclude __pycache__
    for dir in targets: sys.path.append(dir)    # add all subdirectories to python path
    print(f"Path Hammer: subdirectories appended to python path")
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
                 relay_set:int,
                 sample_trig:Event=None,
                 ):
        """<...>"""
        # PROBE INFO
        self.id = probe_id                  # identifier for testing and validation
        self.sys_ref = sys_ref              # dictionary with system settings
        self.config_ref = config_ref        # dictionary with user settings

        # SYSTEM FLAGS
        self.status_flags = status_flags    # system state indicators
        self.command_flags = command_flags  # action triggers
        
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
        raise NotImplementedError

