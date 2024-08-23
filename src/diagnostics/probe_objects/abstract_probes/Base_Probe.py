# author: figueroa_90894@students.pupr.edu
# status: WIP
#   - decide what to do with redundant elements
#   - add relay object once implemented

# built-in imports
from threading import Event             # thread-safe signaling mechanisms
from queue import Queue                 # thread-safe data buffer
from abc import ABC, abstractmethod     # enforce abstraction

# local imports
from ProbeEnum import PRB               # enumator for supported probe types

class BaseProbe(ABC):
    """The top-level, abstract class for all probe implementations.
    Includes initialization for flags, data buffer, equations, config, and data buffer.
    Defines abstract methods run(), _graceful_exit(), and _emergency_exit()."""
    def __init__(self, 
                 shutdown:Event,
                 diagnose:Event,
                 emergency:Event,
                 operating:Event,
                 equations:list,
                 config:dict,
                 data_buff:Queue,
                 sampling_rate:int
                 ):
        
        # SIGNAL FLAGS - Set externally, indicates an action this object must perform.
        self.shutdown = shutdown        # graceful system-wide shutdown, begin exit script
        self.diagnose = diagnose        # diagnostics must be performed
        self.emergency = emergency      # emergency system-wide shutdown, terminate immediately
        
        # STATUS FLAGS - Set internally, notifies other subcomponents of this objects state.
        # !!! HIGH VOLTAGE INDICATOR !!!
        # Set this BEFORE enabling the relay
        # Clear AFTER confirming the relay is disabled
        self.operating = operating      # indicate that diagnostics are being performed
        
        # PROBE INFO
        self.probe_type = PRB.ABS   # specifies the probe's type, in this case abstract
        self.config = config        # dictionary containing relevant configuration data
        self.equations = equations  # list of callables to calculate plasma parameters
        self.data_buff = data_buff  # thread-safe queue, pass data samples to probe operation
        self.sampling_rate = sampling_rate      # samples to obtain per second, Hertz (Hz)
        
        # TO DO - Redundant? Is this needed if run() creates a new one every time it pushes to data_buff?
        self.params:dict = None     # used to store data samples and calculated parameters

        # TO DO - PROBE SUBCOMPONENTS
        self._relay = None      # <relay object from hardware interface>
    
    @abstractmethod
    def run(self) -> None:
        """Executes the data acquisition process. Children must override it."""
        raise NotImplementedError
    
    @abstractmethod
    def _graceful_exit(self):
        """Complete all pending actions, then exit gracefully."""
        raise NotImplementedError
    
    @abstractmethod
    def _emergency_exit(self):
        """Force termination, perform critical actions and terminate immediately."""
        raise NotImplementedError

